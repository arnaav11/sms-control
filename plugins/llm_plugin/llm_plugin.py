from plugins.plugin import Plugin
from plugins.llm_plugin.llm_connector import LLMConnector

class LLMPlugin(Plugin):
    def __init__(
            self,
            base_url: str,
            available_reasoning: list[str],
            available_tools: dict[str, str],
            
            model: str = None,
            use_tools: bool = True,
            max_tokens: int = 4096,
            reasoning: str = 'none',
            save_folder: str = './chats',
            system_message: str = 'You are a helpful AI Assistant, reply to the user accordingly'
        ):
        super().__init__()

        self.connector = LLMConnector(
            base_url=base_url,
            model=model,
            reasoning=reasoning,
            max_tokens=max_tokens,
            system_message=system_message
        )

        self.available_reasoning = available_reasoning
        self.save_folder = save_folder
        self.tool_calling = use_tools
        self.system_message = system_message

        self.tools = available_tools
        self.setup_tool_message()

        self.callback_method = 'chat'

        self.tools = {
            'chat': {
                'method': self.get_chat_response,
                'description': 'send a message to the LLM and get a response. Takes the prompt as the argument'
            },
            'reasoning': {
                'method': self.reasoning,
                'description': 'If no arg is provided, returns current reasoning value. changes reasoning value to arg if possible'
            },
            'models': {
                'method': self.get_models,
                'description': 'Returns a list of the models available by the provider.'
            },
            'model': {
                'method': self.model,
                'description': 'Tries to set the model to arg'
            },
            'reset_chat': {
                'method': self.reset_chat,
                'description': 'Resets chat and saves it in JSON'
            },
            'respond': {
                'method': lambda x: '',
                'description': 'Respond to the user, Only for the LLM for agentic tasks'
            }
        }
    
    def get_models(self, command: str = '') -> str:
        return f"Available models: {', '.join(self.connector.get_models())}"
    
    def get_response_tool(self) -> dict[str, str]:
        return self.response_tool
    
    def get_chat_response(self, prompt: str) -> str:
        return self.cleanup_reasoning(self.connector.get_chat_response(prompt).content or 'No Response')

    
    def set_available_tools(self, tools: dict[str, str]) -> None:
        self.tools = tools
        self.setup_tool_message()


    def reasoning(self, command: str) -> str:
        if command == '':
            return f'Reasoning is currently "{self.connector.get_reasoning()}"'
        
        elif command in self.available_reasoning:
            reason = self.connector.set_reasoning(command)
            return f'Reasoning set to "{reason}"'

        else:
            return f'Reasoning not available Choose from {self.available_reasoning}'
        
    
    def model(self, command: str) -> str:
        if command == '':
            return f'Model in use: {self.connector.get_model()}'

        else:
            set_model = self.connector.set_model(command)
            if set_model:
                return f'Model set to {set_model}'
            else:
                return 'Model not available'
            

    def setup_tool_message(self) -> None:
        tool_message = ''
        n = 1
        for tool in self.tools:
            tool_message += f'{n}. {tool}: {self.tools[tool]}\n'
            n += 1

        self.cur_msg = self.system_message
        self.connector.set_system_message(f'{self.cur_msg}\n{tool_message}')

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