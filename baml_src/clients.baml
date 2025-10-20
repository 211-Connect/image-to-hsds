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
