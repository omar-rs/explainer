from pathlib import Path

from chatlas import ChatOpenAI, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()


def read_file(directory: str, name: str) -> str:
    with open(Path(__file__).parent / f"{directory}" / f"{name}", "r") as f:
        content = f.read()
        return content


def main():
    content = "streamlit-error-2"
    entrypoint = "app.py"

    print("** Reading source code...\n")
    codebase = read_file("codebases", f"{content}.xml")

    print("** Reading logs...\n")
    logs = read_file("logs", f"{content}.log")

    system_prompt = read_file("prompts", "explain_error.txt")
    print(f"** Using system prompt: {system_prompt}")

    user_prompt = f"""
    The code base is in: {codebase}, the output logs are in: {logs}, and the entrypoint file is: {entrypoint}.
    """

    # chat = ChatOpenAI(model="o1", system_prompt=system_prompt)
    # chat = ChatAnthropic(model="claude-3-7-sonnet-latest", system_prompt=system_prompt)
    chat = ChatOpenAI(model="gpt-4o", system_prompt=system_prompt)
    response = chat.stream(user_prompt)
    for chunk in response:
        print(chunk, end="")


if __name__ == "__main__":
    main()
