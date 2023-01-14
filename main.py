import argparse
import logging
import os
from dataclasses import dataclass

import openai

LOGGER = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

assert OPENAI_API_KEY is not None, "You have to provide an api key for openai"


@dataclass
class Options:
    path: str
    language: str
    line: int


def get_options() -> Options:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        dest="input",
        required=True,
        help="the path to the input file",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        dest="language",
        required=True,
        help="the language of the source code",
    )
    parser.add_argument(
        "-n",
        "--line",
        type=int,
        dest="line",
        required=True,
        help="the line where the bug is",
    )

    args = parser.parse_args()

    return Options(
        path=args.input,
        language=args.language,
        line=args.line - 1,
    )


def make_codex_prompt(source: str, language: str, line: int) -> str:
    if language == "C++":
        comment = "//"
    elif language == "Python":
        comment = "#"
    else:
        raise NotImplementedError(f"{language} not implemented yet")

    lines = source.splitlines()
    lines[line] = f"{lines[line]} {comment} Fixme"
    lines.append(f"{comment} Q: Propose a hint that can help me fix the bug")
    lines.append(f"{comment} A:")

    return "\n".join(lines)


def main(opt: Options):
    with open(opt.path, "r") as f:
        source = f.read()
    prompt = make_codex_prompt(source, opt.language, opt.line)

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
    )

    print(prompt, end="")
    print(response["choices"][0]["text"])


if __name__ == "__main__":
    main(get_options())
