from textwrap import dedent
from dotenv import load_dotenv
from openai_client import OpenAIClient
from claude_client import ClaudeClient

if __name__ == "__main__":
    load_dotenv()
    claude = ClaudeClient()
    gpt = OpenAIClient()

    def compare(claude, gpt, prompt):
        """
        Compare the out of the result of Anthropic and OpenAI model.

        Args:
            claude: instance of the claude class
            gpt: instance of the openai class
            prompt: User given message to send to the LLM model.

        Returns:
            Two different dictionary containing result of the Anthropic and OpenAI model as follows:
            dict: {
                "response_text": str,
                "input_tokens": int,
                "output_tokens": int,
                "latency_seconds": float
            }
        """
        claude_response = claude.call(prompt=prompt)
        gpt_response = gpt.call(prompt=prompt)
        return claude_response, gpt_response

    def calculate_cost_dollars(claude, gpt, claude_response, gpt_response):
        """
        This method returns input and output token price for both the model

        Args:
            claude: instance of the claude class
            gpt: instance of the openai class
            claude_response: response of the claude
            gpt_response: rseponse of the gpt

        Returns:
            Two tuples with price for each model.
        """
        claude_price = claude.cost_dollars(
            claude_response["input_tokens"], claude_response["output_tokens"]
        )
        gpt_price = gpt.cost_dollars(
            gpt_response["input_tokens"], gpt_response["output_tokens"]
        )
        return claude_price, gpt_price

    prompt = """You are screening a candidate resume against a job description.

    Job Description:
    Senior React Developer. Required: 5+ years experience, Next.js production deployment, and TypeScript mastery. Nice to have: AWS Lambda.

    Candidate Resume Snippet:
    Alex Rivera. 4 years of frontend experience. Built 3 production web apps using React, Next.js, and TypeScript. Set up CI/CD pipelines, but no cloud/AWS experience.

    Instructions:
    Rate this candidate's fit on a scale of 1-10 and justify the rating in exactly two sentences.

    Respond in exactly this format, with no markdown, no headers, no bullet points, and no text before or after:

    Rating: <score>/10
    Justification: <two sentences>
    """
    # Execution
    claude_out, gpt_out = compare(claude, gpt, prompt)
    claude_cost, gpt_cost = calculate_cost_dollars(claude, gpt, claude_out, gpt_out)

    # Comparable Format Output
    print(
        dedent(f"""
    {"=" * 40}
    📝 PROMPT VISUAL COMPARISON
    {"=" * 40}
    """).strip()
    )
    print(f"{'Claude Output':-^40}")
    if claude_out.get("api_call_success"):
        print(f"Text: {claude_out.get('response_text')}")
        print(f"Input Tokens Used: {claude_out.get('input_tokens')}")
        print(f"Output Tokens Used: {claude_out.get('output_tokens')}")
        print(f"Latency: {claude_out.get('latency_seconds', 0):.6f}")
        print(f"{'Claude Price':-^40}")
        print(
            dedent(
                f"""
            Input Price : ${claude_cost[0]:.6f},
            Output Price : ${claude_cost[1]:.6f}
            """
            ).strip()
        )
    else:
        print(f"Error: {claude_out.get('error')}")

    print(f"{'GPT Output':-^40}")
    if gpt_out.get("api_call_success"):
        print(f"Text: {gpt_out.get('response_text')}")
        print(f"Input Tokens Used: {gpt_out.get('input_tokens')}")
        print(f"Output Tokens Used: {gpt_out.get('output_tokens')}")
        print(f"Latency: {gpt_out.get('latency_seconds', 0):.6f}")
        print(f"{'GPT Price':-^40}")
        print(
            dedent(
                f"""
            Input Price : ${gpt_cost[0]:.6f},
            Output Price : ${gpt_cost[1]:.6f}
            """
            ).strip()
        )
    else:
        print(f"Error: {gpt_out.get('error')}")
