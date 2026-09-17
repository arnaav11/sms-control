import openai
import json
import os

from datetime import datetime
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage

class LLMConnector:
    def __init__(self, base_url: str, model: str = None, reasoning: str = 'none', max_tokens: int = 4096, system_message: str = 'You are a helpful AI Assistant, reply to the user accordingly'):
        self.client = OpenAI(
            base_url = base_url
        )
        self.system_message = system_message
        self.reset_chat()

        self.reasoning = reasoning

        self.max_tokens = max_tokens
        self.set_model(model or self.get_models()[0])

        self.set_reasoning(reasoning)


        
    def get_models(self) -> list[str]:
        return [i.id for i in self.client.models.list().data]
    
    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> str:
        if model in self.get_models():
            self.model = model
            self.set_reasoning(self.reasoning)
        else:
            self.model = self.get_models()[0]

        return self.model
    
    def get_max_tokens(self) -> int:
        return self.max_tokens
    
    def set_max_tokens(self, max_tokens: int) -> None:
        self.max_tokens = max_tokens

    def get_reasoning(self) -> str:
        return self.reasoning
    
    def set_reasoning(self, reasoning = str) -> str:
        try:
            self.reasoning = reasoning
            max_tok = self.max_tokens
            self.max_tokens = 1

            print('Testing reasoning validity')
            self.get_direct_response('')
            self.max_tokens = max_tok
        
        except openai.BadRequestError as e:
            print('Reasoning invalid')
            print(e.message)
            self.reasoning = None

        return self.reasoning
    
    def get_system_message(self) -> str:
        return self.system_message
    
    def set_system_message(self, sys_msg: str) -> None:
        self.system_message = sys_msg
        self.chat[0] = {
            'role': 'system',
            'content': sys_msg
        }
    
    def get_chat(self) -> list[dict[str: str]]:
        return self.chat
    
    def set_chat(self, chat = list[dict[str: str]]) -> None:
        self.chat = chat

    def load_chat(self, chat_file: str) -> None:
        with open(chat_file, 'r') as file:
            self.set_chat(json.load(chat_file))

    def reset_chat(self) -> None:
        self.chat = [
            {
                'role': 'system',
                'content': self.system_message
            }
        ]

    def save_conversation(self, save_folder: str) -> str:
        filename = os.path.join(save_folder, f'{datetime.now()}.json')
        with open(filename, 'w') as file:
            json.dump(self.chat, file, indent=4)

    def load_conversation(self, convo_file: str) -> None:
        with open(convo_file, 'r') as file:
            self.chat = json.load(file)


    def get_direct_completion(self, prompt: str) -> openai.types.completion.Completion:
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            n=1,
            best_of=1,
            max_tokens=self.max_tokens,
        )

        return response
    
    def get_direct_response(self, prompt: str) -> ChatCompletionMessage:
        messages_gen = [
            {
                'role': 'system',
                'content': self.system_message
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        response = self.client.chat.completions.create(
            messages=messages_gen,
            model=self.model,
            n=1,
            max_completion_tokens=self.max_tokens,
            reasoning_effort=self.reasoning,
        )

        return response.choices[0].message
    
    def get_chat_response(self, prompt: str) -> ChatCompletionMessage:
        self.chat.append(
            {
                'role': 'user',
                'content': prompt
            }
        )

        print(f'Reasoning: {self.reasoning}')

        response = self.client.chat.completions.create(
            messages=self.chat,
            model=self.model,
            n=1,
            reasoning_effort=self.reasoning,
            max_completion_tokens=self.max_tokens
        )

        reply =  response.choices[0].message
        self.chat.append(
            {
                'role': 'assistant',
                'content': reply.content
            }
        )

        return reply


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    base_url = 'https://api.groq.com/openai/v1'
    # api_key = ''
    # model = 'koboldcpp/Ornith-1.0-9B-Heretic-Uncensored-Q4_K_M'

    tester = LLMConnector(
        base_url=base_url,
        # api_key=api_key,
    )

    print(f"connected to {base_url} \n\nAvailable models: {tester.get_models()}")

    tester.set_model('openai/gpt-oss-120b')

    test_input = input('Enter Prompt: ')

    while test_input != '/quit':
        test_response = tester.get_chat_response(test_input)

        print(f'\n\nResponse: \n{test_response.content}')
        test_input = input('\n\nEnter your prompt: ')

    tester.save_conversation()