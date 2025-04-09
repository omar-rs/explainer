from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def read_file(directory: str, name: str) -> str:
    with open(Path(__file__).parent / f"{directory}" / f"{name}", "r") as f:
        content = f.read()
        return content


def main():
    content = "quarto-error-1"
    entrypoint = "tech_notes/810_pharmaverse_NOTES.qmd"

    codebase = read_file("codebases", f"{content}.xml")
    logs = read_file("logs", f"{content}.log")

    system_prompt = read_file("prompts", "explain_error.txt")

    user_prompt = f"""
    The code base is in: {codebase}, the output logs are in: {logs}, and the entrypoint file is: {entrypoint}.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
