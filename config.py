import os

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
model = 'nvidia/nemotron-3-ultra-550b-a55b'

reasoning = 'high'
chat_save_folder = './chats'
system_message = 'You are a helpful AI Agent'
max_tokens = 4096

available_reasoning = ['none', 'low', 'medium', 'high']
response_tool = {'respond': 'Respond to the user. Takes in the response text as the argument'}

tool_messages = [
    "Here are tools:",
    "use them in json with {'tool_name': {'args': 'tool_args', 'callback': bool}, 'tool_name'....} reply only in json. The callback is for whether you want the output of the tool call to be returned back to you"
]

llm_plugin = LLMPlugin(
    base_url=base_url,
    model=model,
    reasoning=reasoning,
    available_reasoning=available_reasoning,
    max_tokens=max_tokens,
    save_folder=chat_save_folder,
    system_message=system_message,
    available_tools = {},
    tool_messages=tool_messages,
    response_tool=response_tool
)


plugins = [llm_plugin, shell_plugin, search_plugin]
parser = DefaultParser(plugins=plugins)

tools = {}
for plugin in plugins:
    tools.update(plugin.get_tools())
llm_plugin.set_available_tools(tools)


sms_queue = Queue()
listener = SMSListener(data_queue=sms_queue)
