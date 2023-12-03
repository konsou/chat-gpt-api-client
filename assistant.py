import json
import os
import time

import dotenv
import tiktoken
from openai import OpenAI

if __name__ == '__main__':
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    model = 'gpt-4-1106-preview'
    assistant = client.beta.assistants.create(
        name="ChatGPT",
        instructions="You are ChatGPT, a helpful assistant.",
        tools=[],
        model="gpt-4-1106-preview",
    )

    thread = client.beta.threads.create()

    while True:
        user_input = input(f"You:\n").strip()

        print(f"Creating message")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        print(f"Message created")

        print(f"Creating run")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        print(f"Run created")

        print(f"Waiting for run to complete")
        time.sleep(1)
        while True:
            print(f"Getting run status")
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Run status is {run.status}")

            if run.status == 'completed':
                break

            if run.status in ('queued', 'in_progress'):
                time.sleep(5)
                continue

            raise NotImplemented(f"Implement status handling for {run.status}")
        print(f"Run completed")

        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        for message in messages.data:
            if message.role == 'assistant':
                print(f"ChatGPT:\n{message.content}")
            else:
                break

