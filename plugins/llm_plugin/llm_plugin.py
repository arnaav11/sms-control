from collections.abc import Callable

from plugins.plugin import Plugin
from plugins.llm_plugin.llm_connector import LLMConnector

class LLMPlugin(Plugin):
    def __init__(
            self,
            base_url: str,
            reasoning: str = 'none',
            available_reasoning: list[str] = ['none', 'high'],
            max_tokens: int = 4096,
            save_folder: str = './chats',
            system_message: str = 'You are a helpful AI Assistant, reply to the user accordingly'
    ):

        self.connector = LLMConnector(
            base_url=base_url,
            reasoning=reasoning,
            max_tokens=max_tokens,
            system_message=system_message
        )

        self.available_reasoning = available_reasoning
        self.save_folder = save_folder

        self.commands = {
            'chat': self.get_chat_response,
            'reasoning': self.reasoning,
            'models': self.get_models,
            'model': self.model,
            'reset_chat': self.reset_chat
        }

    def get_chat_response(self, prompt: str) -> str:
        return self.cleanup_reasoning(self.connector.get_chat_response(prompt).content or 'No Response')
    
    def reasoning(self, command: str) -> str:
        if command == '':
            return f'Reasoning is currently "{self.connector.get_reasoning()}"'
        
        elif command in self.available_reasoning:
            reason = self.connector.set_reasoning(command)
            return f'Reasoning set to "{reason}"'
        
    def get_models(self, command: str = '') -> str:
        return f'Available models: {', '.join(self.connector.get_models())}'
    
    def model(self, command: str) -> str:
        if command == '':
            return f'Model in use: {self.connector.get_model()}'

        else:
            set_model = self.connector.set_model(command)
            if set_model:
                return f'Model set to {set_model}'
            else:
                return f'Model not available'

    def reset_chat(self, command: str) -> str:
        convo_file = self.connector.save_conversation(self.save_folder)
        return f'chat reset and saved to {convo_file}'
    
    def cleanup_reasoning(self, response: str) -> str:
        think_end_tag = '</think>'
        think_end_idx = response.find(think_end_tag)
        if think_end_idx >= 0:
            think_end_idx += len(think_end_tag)
        else: 
            think_end_idx = 0

        return response[think_end_idx:]

            
    def get_commands(self) -> dict[str, Callable[[str], str]]:
        return self.commands