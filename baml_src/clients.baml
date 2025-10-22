// Original OpenAI Vision client (for reference)
client<llm> GPT4Vision {
  provider "openai"
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
    temperature 0.1
    allowed_roles ["user", "system"]
    default_role "user"
  }
}

// New Ollama client for gpt-oss-20b
client<llm> OllamaGPTOSS {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "gpt-oss:20b"
    temperature 0.1
    allowed_roles ["user", "system"]
    default_role "user"
  }
}
