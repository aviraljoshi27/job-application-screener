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
                "api_call_success" :bool,
                "response_text": str,
                "input_tokens": int,
                "output_tokens": int,
                "latency_seconds": float
            }
        """
        try:
            response, latency = self._time_call(
                self.client.messages.create,
                model=self.model_name,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )
            api_call_success = True
            response_text = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            return {
                "api_call_success": api_call_success,
                "response_text": response_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_seconds": latency,
            }
        except anthropic.RateLimitError:
            return {
                "api_call_success": False,
                "error": "Too many attempts please try after some time",
                "response_text": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency_seconds": 0,
            }
        except anthropic.AuthenticationError:
            return {
                "api_call_success": False,
                "error": "api key is not correct please check it",
                "response_text": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency_seconds": 0,
            }
        except anthropic.APIConnectionError:
            return {
                "api_call_success": False,
                "error": "Something wrong with the connection please try after some time",
                "response_text": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency_seconds": 0,
            }
        except anthropic.APIStatusError as e:
            return {
                "api_call_success": False,
                "error": f"API error (status {e.status_code})",
                "response_text": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency_seconds": 0,
            }
        except Exception as e:
            return {
                "api_call_success": False,
                "error": f"Unexpected error: {e}",
                "response_text": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency_seconds": 0,
            }
