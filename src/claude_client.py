import anthropic
from llm_client import LLMClient


class ClaudeClient(LLMClient):
    input_price_per_token = 3 / 1_000_000
    output_price_per_token = 15 / 1_000_000

    def __init__(self, model_name: str = "claude-sonnet-4-6"):
        super().__init__(model_name)
        self.client = anthropic.Anthropic()

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
            self.client.messages.create,
            model=self.model_name,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        return {
            "response_text": response_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_seconds": latency,
        }
