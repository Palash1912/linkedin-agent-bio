import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from tools.tool import get_profile_url_tavily

def lookup(name: str, mockup: bool = False) -> str:
    """
    LinkedIn profile lookup using ReAct agent with proper formatting.
    """
    
    print(f"Mockup mode: {mockup}")
    
    # If mockup mode is enabled, return hardcoded URL directly
    if mockup:
        return get_profile_url_tavily(name=name, mockup=True)

    # Create a more focused prompt
    template = """Find the LinkedIn profile URL for {person_name}. 
    Use the available tool to search and return ONLY the LinkedIn URL."""

    prompt_template = PromptTemplate(
        input_variables=["person_name"], template=template
    )

    # Tool with cleaner output
    tools_for_agent = [
        Tool(
            name="linkedin_search",
            func=lambda x: get_profile_url_tavily(name=x, mockup=mockup),
            description="Search for a person's LinkedIn profile URL. Input: person's name. Output: LinkedIn URL"
        )
    ]

    # Improved ReAct prompt with clear stopping condition
    react_prompt = PromptTemplate(
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        template="""You are a LinkedIn profile finder. Answer the question by finding the LinkedIn profile URL.

        Available tools:
        {tools}

        IMPORTANT: Once you get a LinkedIn URL from the tool, immediately provide it as your Final Answer. Do not search multiple times.

        Use this exact format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        Thought: I now have the LinkedIn URL, I should provide it as the final answer
        Final Answer: [just the LinkedIn URL, nothing else]

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
    )

    # Configure LLM
    llm = ChatOllama(model="llama3.2", temperature=0)

    # Create agent with better settings
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent, 
        verbose=True, 
        max_iterations=3,  # Should only need 1 iteration for this task
        max_execution_time=20,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
        early_stopping_method="generate"  # Stop as soon as final answer is generated
    )

    # Execute the agent
    try:
        result = agent_executor.invoke(
            input={"input": prompt_template.format_prompt(person_name=name).text}
        )
        
        # If we got a proper output, return it
        if result["output"] and "Agent stopped" not in result["output"]:
            return result["output"]
        
        # If no LinkedIn URL found in steps, fallback to direct tool call
        print("No LinkedIn URL found in agent output, falling back to direct tool call")
        return get_profile_url_tavily(name=name, mockup=False)
        
    except Exception as e:
        print(f"Agent execution error: {e}")
        # Fallback to direct tool call
        return get_profile_url_tavily(name=name, mockup=False)


if __name__ == "__main__":
    linkedin_url = lookup("Jatin, UKG DTU", mockup=False)
    print(linkedin_url)





