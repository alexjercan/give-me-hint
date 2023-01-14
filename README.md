# GiveMeHint

GiveMeHint is a CLI tool that can be used to query the Codex API to provide a
hint for a source code file.

## QuickStart

Install the dependencies from `requirements.txt`. You will need the openai
library.

```console
pip install -r requirements.txt
```

The to be ablen to use the tool you will need to have an openai account
and create an API key. Then you have to export an evnrionment variable with the name
`OPENAI_API_KEY` with the value of the key.

```console
export OPENAI_API_KEY=...
```

And finally you can run the script.

```console
python main.py --input path.ext --language language --line number
```

The input argument is used to point to the given file containing source code.
The language argument is used to specify the programming language used.
The line argument is a number that specifies the line number of where the bug
is and it starts from 1.
