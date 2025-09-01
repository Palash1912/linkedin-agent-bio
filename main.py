import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup
from schema.models import LinkedinData, DateObject, Experience, Education
from langchain_ollama import ChatOllama
from linkedin_api import Linkedin
from mockup import mockup_data
from output_parsers import summary_parser

load_dotenv()


def fetch_linkedin_data(linkedin_profile_url: str, mockup: bool = False):
    linkedin_user_name = os.getenv("LINKEDIN_USER_NAME")
    linkedin_user_password = os.getenv("LINKEDIN_USER_PASSWORD")

    if not mockup:
        api = Linkedin(linkedin_user_name, linkedin_user_password)
        profile = api.get_profile(linkedin_profile_url)
        linkedin_data = LinkedinData(**profile)
    else:
        linkedin_data = LinkedinData(**mockup_data)

    return linkedin_data


def generate_summary(linkedin_data: LinkedinData):

    linkedin_template = """
    You are a professional content writer. Analyze the following LinkedIn information and create a structured response.

    LinkedIn Information: {information}

    Your task:
    1. Write a short professional summary (2-3 sentences)
    2. Identify exactly 2 interesting facts about this person

    IMPORTANT: You must respond with valid JSON only. Do not include any explanations, code, or additional text.

    {format_instructions}
    """

    linkedin_summary_template = PromptTemplate(
        input_variables=["information"], template=linkedin_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )

    # Use temperature=0 for consistent JSON output
    llm = ChatOllama(model="llama3.2", temperature=0)
    chain = linkedin_summary_template | llm | summary_parser
    res = chain.invoke({"information": linkedin_data})  
    return res



def generate_linkedin_summary(name: str):

    linkedin_profile_url = lookup(name,mockup=True)
    print("Fetched LinkedIn profile URL: ", linkedin_profile_url)

    print("\nFetched LinkedIn data...")
    linkedin_data = fetch_linkedin_data(linkedin_profile_url, mockup=True)

    print("\nGenerating summary...")
    genai_summary = generate_summary(linkedin_data)

    return genai_summary


summary = generate_linkedin_summary("Palash . Amdocs, Pune")
print(summary)