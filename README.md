# HormoziGPT

HormoziGPT is a chatbot application that simulates a conversation with Alex Hormozi. The chatbot provides valuable business advice and coaching to users, drawing from Alex's experience in customer acquisition, monetization, and scaling businesses. It also has access to transcripts of Alex's podcasts, which are used to provide context and support for the chatbot's responses.

## Features

- Engage in a conversation with a chatbot that emulates Alex Hormozi's communication style.
- Receive focused, practical, and direct business advice.
- Access relevant snippets from transcripts of Alex's podcasts to support the chatbot's responses.
- Utilize semantic search to find relevant content from the transcripts.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- OpenAI API key
- Pinecone API key and environment details

### Installation

1. Clone the repository:
```
git clone https://github.com/your-repo-url/HormoziGPT.git
```
2. Change to the project directory:
```
cd HormoziGPT
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Set up the environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Your Pinecone environment details
- `PINECONE_ENDPOINT`: Your Pinecone endpoint

### Usage

1. Run the Streamlit app:
```
streamlit run app.py
```
2. Open the app in your web browser and enter your prompt to start the conversation with the chatbot.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to the project.

## Acknowledgments

- Alex Hormozi for his valuable insights and business advice! (don't sue me)
- OpenAI for their language models and embeddings.
- Pinecone for their semantic search capabilities.
