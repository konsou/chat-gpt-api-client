import datetime
import json
import os
from dataclasses import dataclass

PRICING = {
    'gpt-4-1106-preview': {
        'input-1k-tokens': 0.01,
        'output-1k-tokens': 0.03,
    }
}
TOKEN_USAGE_DIR = 'usage-logs'


@dataclass
class Usage:
    tokens_input: int
    tokens_output: int


def filename() -> str:
    return f'{datetime.date.today().strftime("%Y-%m-%d")}.json'


def full_path() -> str:
    return os.path.join(TOKEN_USAGE_DIR, filename())


def get() -> Usage:
    full_path_ = full_path()
    if not os.path.isfile(full_path_):
        print(f"Creating {full_path_}")
        save(Usage(tokens_input=0, tokens_output=0))

    with open(full_path_, encoding='utf-8') as f:
        return Usage(**json.load(f))


def save(usage: Usage):
    full_path_ = full_path()
    with open(full_path_, 'w', encoding='utf-8') as f:
        json.dump(usage.__dict__, f)


def add(tokens_input: int = 0, tokens_output: int = 0):
    if tokens_input == 0 and tokens_output == 0:
        return

    input_str = '' if not tokens_input else f'{tokens_input} input tokens'
    output_str = '' if not tokens_output else f'{tokens_output} output tokens'
    print(f"Usage: {input_str} {output_str}")
    u = get()
    u.tokens_input += tokens_input
    u.tokens_output += tokens_output
    save(u)


def print_summary():
    u = get()
    cost = (
            (u.tokens_input / 1000 * PRICING['gpt-4-1106-preview']['input-1k-tokens']) +
            (u.tokens_output / 1000 * PRICING['gpt-4-1106-preview']['output-1k-tokens'])
    )
    print(f"Usage: cost $ {cost:.2f} ({u.tokens_input} input tokens, {u.tokens_output} output tokens)")


if __name__ == '__main__':
    print(get())
    add(5, 10)
    print(get())
    add()
    print(get())
    add(tokens_output=200)
    print(get())
