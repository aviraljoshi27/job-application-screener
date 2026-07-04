import openai
from llm_client import LLMClient


class OpenAIClient(LLMClient):
    input_price_per_token = 0.15 / 1_000_000
    output_price_per_token = 0.60 / 1_000_000

    def __init__(self, model_name: str = "gpt-4o-mini"):
        super().__init__(model_name)
        self.client = openai.OpenAI()

    def call(self, prompt: str) -> dict:
        """
        This method takes the user message and returns the response_text, input_tokens, output_tokens, latency_seconds

        Args:
            prompt: User input message that we send to the LLM.

        Returns:
            dict: {
                "response_text": str,
                "input_tokens": int,
                "output_tokens": int,
                "latency_seconds": float
            }
        """
        response, latency = self._time_call(
            self.client.chat.completions.create,
            model=self.model_name,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return {
            "response_text": response_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_seconds": latency,
        }
