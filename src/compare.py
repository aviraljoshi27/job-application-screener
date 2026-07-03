from textwrap import dedent
from dotenv import load_dotenv
from openai_client import OpenAIClient
from claude_client import ClaudeClient

if __name__ == "__main__":
    load_dotenv()
    claude = ClaudeClient()
    gpt = OpenAIClient()

    def compare(prompt):
        """
        Compare the out of the result of Anthropic and OpenAI model.

        Args:
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

    prompt = """
    Job Description:
    Senior React Developer. Required: 5+ years experience, Next.js production deployment, and TypeScript mastery. Nice to have: AWS Lambda.

    Candidate Resume Snippet:
    Alex Rivera. 4 years of frontend experience. Built 3 production web apps using React, Next.js, and TypeScript. Set up CI/CD pipelines but no cloud/AWS experience.

    Instruction:
    Rate this candidate's fit on a scale of 1-10 and provide a 2-sentence justification.
    """
    # Execution
    claude_out, gpt_out = compare(prompt)

    # Comparable Format Output
    print(
        dedent(f"""
    {"=" * 40}
    📝 PROMPT VISUAL COMPARISON
    {"=" * 40}
    """).strip()
    )
    print(f"{'Claude Output':-^40}")
    print(
        dedent(
            f"""
            Text: {claude_out.get("response_text")}
            Input Tokens Used: {claude_out.get("input_tokens")}
            Output Tokens Used: {claude_out.get("output_tokens")}
            Latency: {claude_out.get("latency_seconds"):.2f}
            """
        ).strip()
    )
    print(f"{'GPT Output':-^40}")
    print(
        dedent(
            f"""
            Text: {gpt_out.get("response_text")}
            Input Tokens Used: {gpt_out.get("input_tokens")}
            Output Tokens Used: {gpt_out.get("output_tokens")}
            Latency: {gpt_out.get("latency_seconds"):.2f}
            """
        ).strip()
    )
