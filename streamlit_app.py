import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup
from schema.models import LinkedinData, DateObject, Experience, Education
from langchain_ollama import ChatOllama
from linkedin_api import Linkedin
from mockup import mockup_data
from output_parsers import summary_parser

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="LinkedIn Profile Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def fetch_linkedin_data(linkedin_profile_url: str, mockup: bool = False):
    """Fetch LinkedIn data from profile URL"""
    linkedin_user_name = os.getenv("LINKEDIN_USER_NAME")
    linkedin_user_password = os.getenv("LINKEDIN_USER_PASSWORD")

    if mockup:
        api = Linkedin(linkedin_user_name, linkedin_user_password)
        profile = api.get_profile(linkedin_profile_url)
        linkedin_data = LinkedinData(**profile)
    else:
        linkedin_data = LinkedinData(**mockup_data)

    return linkedin_data

def generate_summary(linkedin_data: LinkedinData):
    """Generate AI summary from LinkedIn data"""
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

def generate_linkedin_summary(name: str, use_mockup: bool = True):
    """Main function to generate LinkedIn summary"""
    try:
        # Step 1: Lookup LinkedIn profile URL
        with st.spinner("Looking up LinkedIn profile..."):
            linkedin_profile_url = lookup(name, mockup=use_mockup)
            st.success(f"Found LinkedIn profile: {linkedin_profile_url}")

        # Step 2: Fetch LinkedIn data
        with st.spinner("Fetching LinkedIn data..."):
            linkedin_data = fetch_linkedin_data(linkedin_profile_url, mockup=False)
            st.success("LinkedIn data retrieved successfully")

        # Step 3: Generate AI summary
        with st.spinner("Generating AI summary..."):
            genai_summary = generate_summary(linkedin_data)
            st.success("Summary generated successfully")

        return genai_summary, linkedin_profile_url, linkedin_data

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None, None

# Main Streamlit App
def main():
    st.title("LinkedIn Profile Analyzer")
    st.markdown("---")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    use_mockup = st.sidebar.checkbox("Use Mockup Mode", value=True, help="When enabled, uses hardcoded LinkedIn URL for testing")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This app analyzes LinkedIn profiles and generates:
    - Professional summary
    - Interesting facts about the person
    
    **Features:**
    - AI-powered content generation
    - Real-time LinkedIn lookup
    - Professional formatting
    """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Enter Person Details")
        
        # Input form
        with st.form("linkedin_search_form"):
            name_input = st.text_input(
                "Enter full name (include company/location for better results)",
                placeholder="e.g., John Doe Software Engineer Google",
                help="Include workplace, location, or other identifying details for better search results"
            )
            
            submitted = st.form_submit_button("Generate Summary", type="primary")
            
        if submitted and name_input.strip():
            # Process the request
            st.markdown("---")
            st.header("Analysis Results")
            
            summary, profile_url, linkedin_data = generate_linkedin_summary(name_input, use_mockup)
            
            if summary:
                # Display results in organized layout
                col_summary, col_facts = st.columns(2)
                
                with col_summary:
                    st.subheader("📝 Professional Summary")
                    st.write(summary.summary)
                
                with col_facts:
                    st.subheader("🎯 Interesting Facts")
                    for i, fact in enumerate(summary.facts, 1):
                        st.write(f"{i}. {fact}")
                
                # Additional information
                st.markdown("---")
                with st.expander("🔗 Profile Information", expanded=False):
                    st.write(f"**LinkedIn URL:** {profile_url}")
                    if linkedin_data:
                        st.write(f"**Full Name:** {linkedin_data.full_name}")
                        st.write(f"**Headline:** {linkedin_data.headline or 'N/A'}")
                        st.write(f"**Location:** {linkedin_data.city or 'N/A'}, {linkedin_data.country_full_name or 'N/A'}")
                
                # Download option
                st.markdown("---")
                summary_text = f"""
LinkedIn Profile Analysis

Name: {linkedin_data.full_name if linkedin_data else name_input}
Profile URL: {profile_url}

Professional Summary:
{summary.summary}

Interesting Facts:
1. {summary.facts[0] if len(summary.facts) > 0 else 'N/A'}
2. {summary.facts[1] if len(summary.facts) > 1 else 'N/A'}

Generated by LinkedIn Profile Analyzer
                """
                
                st.download_button(
                    label="Download Summary",
                    data=summary_text,
                    file_name=f"linkedin_summary_{name_input.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        
        elif submitted and not name_input.strip():
            st.warning("Please enter a name to search for.")
    
    with col2:

        st.header("Tips")
        st.markdown("""
        **For better results:**
        - Include company name
        - Add location details
        - Use professional titles
        - Be specific with names
        
        **Example searches:**
        - "John Smith Microsoft Seattle"
        - "Sarah Johnson Data Scientist Netflix"
        - "Mike Chen Product Manager Apple"
        """)

if __name__ == "__main__":
    main()
