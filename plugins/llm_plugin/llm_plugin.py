from plugins.plugin import Plugin
from plugins.llm_plugin.llm_connector import LLMConnector

class LLMPlugin(Plugin):
    def __init__(
            self,
            base_url: str,
            tool_messages: list[str],
            response_tool: dict[str, str],
            available_reasoning: list[str],
            tools: dict[str, str],
            
            model: str = None,
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
        self.non_command = True
        self.system_message = system_message

        self.usable_tools = tools
        self.tool_messages = tool_messages
        self.response_tool = {}
        self.set_response_tool(response_tool)
        self.setup_tool_message()

        self.commands = {
            'chat': self.get_chat_response,
            'reasoning': self.reasoning,
            'models': self.get_models,
            'model': self.model,
            'reset_chat': self.reset_chat
        }

    def get_tools(self) -> dict[str, str]:
        return self.usable_tools

    def get_tool_messages(self) -> list[str]:
        return self.tool_messages
    
    def get_models(self, command: str = '') -> str:
        return f"Available models: {', '.join(self.connector.get_models())}"
    
    def get_response_tool(self) -> dict[str, str]:
        return self.response_tool
    
    def get_chat_response(self, prompt: str) -> str:
        return self.cleanup_reasoning(self.connector.get_chat_response(prompt).content or 'No Response')

    
    def set_tools(self, tools: dict[str, str]) -> None:
        self.usable_tools = tools
        self.setup_tool_message()

    def set_response_tool(self, response_tool: dict[str]) -> None:
        self.response_tool = response_tool


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
        tool_message = self.tool_messages[0]

        n = 1
        for tool in self.usable_tools:
            tool_message += f'{n}. {tool}: {self.usable_tools[tool]}'
            n += 1

        cur_msg = self.system_message
        self.connector.set_system_message(f'{cur_msg}\n{tool_message}\n{self.tool_messages[1]}')

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