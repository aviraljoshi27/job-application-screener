from abc import ABC, abstractmethod
import time


class LLMClient(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
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
        pass

    def _time_call(self, func, *args, **kwargs):
        """
        This method tells you how much time does each method takes.

        Args:
            func: method that we are checking the time for.
            *args: Optional parameters
            **kwargs: Optional parameters in for of keyword and value

        Returns:
            Output of the function and time used by that method to give the output.
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        return result, time_taken

    def cost_dollars(self, input_tokens: int, output_tokens: int) -> tuple:
        """
        This method returns the price for input tokens and output tokens.

        Args:
            input_tokens: total tokens used in the input.
            output_tokens: total tokens used in the output.

        Returns:
            A tuple of both input and output price.
        """
        total_input_price = input_tokens * self.input_price_per_token
        total_output_price = output_tokens * self.output_price_per_token
        return total_input_price, total_output_price
