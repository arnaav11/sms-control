import os

from queue import Queue
from dotenv import load_dotenv

from plugins.plugin import Plugin
from plugins.llm_plugin.llm_plugin import LLMPlugin
from plugins.shell_plugin.shell_plugin import ShellPlugin
from plugins.search_plugin.search_plugin import SearchPlugin
from listeners.sms_listener.sms_listener import SMSListener
from parsers.default_parser.default_parser import DefaultParser
from tooling.default_tooling.default_tooling import DefaultTooling

os.chdir(os.path.dirname(os.path.realpath(__file__)))
load_dotenv()



allowed_shell_commands = [
    'ls',
    'yay',
    'cd',
    'llama-server',
    'ollama',
    'koboldcpp',
    'fastfetch',
    'inxi',
    'free',
    'df'
]

shell_plugin = ShellPlugin(
    allowed_commands=allowed_shell_commands
)

searxng_url = 'http://localhost:8888/search'
search_plugin = SearchPlugin(
    search_url=searxng_url,
)


base_url = 'https://integrate.api.nvidia.com/v1'
model = 'z-ai/glm-5.3'

reasoning = 'high'
chat_save_folder = './chats'
with open('./system_messages/test_msg.txt') as f:
    system_message = f.read()
max_tokens = 4096

available_reasoning = ['none', 'low', 'medium', 'high']

# tool_messages = [
#     'Here are tools:',
#     'use them in json with {"tool_name": {"args": "tool_args", "callback": bool}, "tool_name"....} reply only in json. The callback is for whether you want the output of the tool call to be returned back to you. You can use as many tools as you want.'
# ]

llm_plugin = LLMPlugin(
    base_url=base_url,
    model=model,
    reasoning=reasoning,
    available_reasoning=available_reasoning,
    max_tokens=max_tokens,
    save_folder=chat_save_folder,
    system_message=system_message,
    available_tools = {}
)


plugins: list[Plugin] = [llm_plugin, shell_plugin, search_plugin]

max_depth = 5
tooling = DefaultTooling(plugins, max_depth)

parser = DefaultParser(plugins=plugins, tooling=tooling)

tools = {}
for plugin in plugins:
    tools.update(plugin.get_tools())
llm_plugin.set_available_tools(tools)


sms_queue = Queue()
listener = SMSListener(data_queue=sms_queue)
