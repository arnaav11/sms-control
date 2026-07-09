import os

from queue import Queue
from dotenv import load_dotenv

from plugins.llm_plugin.llm_plugin import LLMPlugin
from plugins.shell_plugin.shell_plugin import ShellPlugin
from plugins.search_plugin.search_plugin import SearchPlugin
from sms_listener import SMSListener
from command_parser import CommandParser

os.chdir(os.path.dirname(os.path.realpath(__file__)))
load_dotenv()

base_url = 'https://api.groq.com/openai/v1'
available_reasoning = ['none', 'low', 'medium', 'high']
reasoning = 'high'
max_token = 4096
chat_save_folder = './chats'
system_message = 'You are a helpful AI Agent'

llm_plugin = LLMPlugin(
    base_url=base_url,
    reasoning=reasoning,
    available_reasoning=available_reasoning,
    max_tokens=max_token,
    save_folder=chat_save_folder,
    system_message=system_message
)

llm_plugin.model('openai/gpt-oss-120b')


allowed_shell_commands = [
    'ls',
    'yay',
    'cd',
    'llama-server',
    'ollama',
    'koboldcpp'
]

allow_piping = False
allow_chains = False

shell = '/usr/bin/fish'

shell_plugin = ShellPlugin(
    allowed_commands=allowed_shell_commands,
    allow_piping=allow_piping,
    allow_chains=allow_chains,
    exe=shell
)

searxng_url = 'http://localhost:8888/search'
search_plugin = SearchPlugin(
    search_url=searxng_url,
    exe=shell
)

plugins = [llm_plugin, shell_plugin, search_plugin]
parser = CommandParser(
    plugins=plugins
)


sms_queue = Queue()
listener = SMSListener(data_queue=sms_queue)
