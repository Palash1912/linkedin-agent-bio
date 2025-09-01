# LinkedIn Profile Analyzer - Streamlit App

A modern web application that analyzes LinkedIn profiles and generates AI-powered summaries and insights.

## 🚀 Features

- **Smart Profile Lookup**: Automatically finds LinkedIn profiles based on name and context
- **AI-Powered Analysis**: Uses LLaMA 3.2 (open source) to generate professional summaries
- **Interactive UI**: Clean, modern Streamlit interface
- **Real-time Processing**: Live updates with progress indicators
- **Export Functionality**: Download summaries as text files
- **Mockup Mode**: Test with sample data

## 📍 Result

<img src="images/homepage.PNG" alt="Homepage Image" width="1200" height="600"><br>

<img src="images/input_username.PNG" alt="Input Profile Name Image" width="1200" height="600"><br>

<img src="images/results.PNG" alt="Results Image" width="1200" height="600">

## 🛠️ Installation

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (create `.env` file):

   ```
   LINKEDIN_USER_NAME=your_linkedin_email
   LINKEDIN_USER_PASSWORD=your_linkedin_password
   TAVILY_API_KEY=your_tavily_api_key
   ```

3. **Ensure Ollama is running** with LLaMA 3.2 model:
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

## 🚀 Usage

### Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

### Using the Application

1. **Enter a name** in the search field (include company/location for better results)
2. **Configure settings** in the sidebar:
   - Toggle mockup mode for testing
   - View app information and tips
3. **Click "Generate Summary"** to start the analysis
4. **View results**:
   - Professional summary
   - Interesting facts
   - Profile information
5. **Download** the summary as a text file

### Example Searches

- "John Smith Microsoft Seattle"
- "Sarah Johnson Data Scientist Netflix"
- "Mike Chen Product Manager Apple"

## 📁 Project Structure

```
linkedin-search-agent/
├── streamlit_app.py          # Main Streamlit application
├── main.py                   # Core functionality (CLI version)
├── requirements.txt          # Python dependencies
├── agents/                   # LinkedIn lookup agents
├── schema/                   # Data models
├── tools/                    # Search tools
├── output_parsers.py         # AI output parsing
└── mockup.py                # Sample data for testing
```

## 🔧 Configuration

### Sidebar Options

- **Mockup Mode**: Use sample data instead of real LinkedIn API calls
- **About Section**: Information about app features
- **Tips**: Guidelines for better search results

### Environment Setup

Make sure you have:

- Valid LinkedIn credentials
- Tavily API key for web searching
- Ollama running locally with LLaMA 3.2

## 🎯 Tips for Better Results

- Include company names in search queries
- Add location details when possible
- Use professional titles and specific information
- Enable mockup mode for testing without API calls

## 🚨 Troubleshooting

1. **Streamlit not found**: Install with `pip install streamlit`
2. **LLM errors**: Ensure Ollama is running and LLaMA 3.2 is installed
3. **API errors**: Check your environment variables and credentials
4. **JSON parsing errors**: Try using mockup mode first
