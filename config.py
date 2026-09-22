import os
from plugins.plugin import Plugin

from queue import Queue
from dotenv import load_dotenv

from plugins.llm_plugin.llm_plugin import LLMPlugin
from plugins.shell_plugin.shell_plugin import ShellPlugin
from plugins.search_plugin.search_plugin import SearchPlugin
from listeners.sms_listener.sms_listener import SMSListener
from parsers.default_parser.default_parser import DefaultParser

os.chdir(os.path.dirname(os.path.realpath(__file__)))
load_dotenv()



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
    exe=shell
)

searxng_url = 'http://localhost:8888/search'
search_plugin = SearchPlugin(
    search_url=searxng_url,
    exe=shell
)

base_url = 'https://integrate.api.nvidia.com/v1'
available_reasoning = ['none', 'low', 'medium', 'high']
reasoning = 'high'
max_token = 4096
chat_save_folder = './chats'
system_message = 'You are a helpful AI Agent'

llm_plugin = LLMPlugin(
    base_url=base_url,
    model='nvidia/nemotron-3-nano-omni-30b-a3b-reasoning',
    reasoning=reasoning,
    available_reasoning=available_reasoning,
    max_tokens=max_token,
    save_folder=chat_save_folder,
    system_message=system_message
)


plugins = [llm_plugin, shell_plugin, search_plugin]
parser = DefaultParser(
    plugins=plugins
)

tools = {}
for plugin in plugins:
    tools.update(plugin.get_tools())


sms_queue = Queue()
listener = SMSListener(data_queue=sms_queue)
