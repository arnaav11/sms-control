import json

from typing import Literal

from plugins.plugin import Plugin
from tooling.tooling import Tooling

class DefaultTooling(Tooling):
    def __init__(self, plugins: list[Plugin], max_depth: int = 5):
        super().__init__()

        self.plugins = plugins
        self.max_depth = max_depth
        self.extract_tools()

    def call_tool(self, tool: str, tool_call: dict[Literal['args', 'callback'], str]) -> dict[Literal['output', 'callback_output'], str]:
        if self.cur_depth > self.max_depth:
            return{
                'output': 'Max tool depth reached',
                'callback_output': 'Max tool depth reached' if tool_call['callback'] else ''
            }
        elif tool == 'respond':
            return {
                'output': f'\n{tool_call["args"]}\n',
                'callback_output': ''
            }

        tool_call_output = self.tools[tool]['method'](tool_call['args'])

        return {
            'output': f'Running {tool} tool with the args "{tool_call["args"]} \n"',
            'callback_output': f'\n{tool_call_output}\n' if tool_call['callback'] else ''
        }

    def call_tools_dict(self, tools: dict[str, dict[Literal['args', 'callback'], str]]) -> dict[Literal['output', 'callback_output'], str]:
        result = {
            'output': '',
            'callback_output': ''
        }

        print(f'tool call: {tools}')

        for tool in tools:
            try:
                tool_call_output = self.call_tool(tool, tools[tool])
                result['output'] += tool_call_output['output']
                result['callback_output'] += tool_call_output['callback_output']
            except Exception as e:
                result['output'] += repr(e)

        return result

    def call_tools(self, tools: str, callback_cmd: str) -> str:
        try:
            tools_dict = json.loads(tools)
        except json.decoder.JSONDecodeError:
            print('Not a tool call, or invalid call')
            print(tools[:15])
            return tools
        
        self.cur_depth += 1

        result_dict = self.call_tools_dict(tools_dict)
        result_dict['callback_output'] = result_dict['callback_output'].strip()
        result_dict['output'] = result_dict['output'].strip()

        if result_dict['callback_output']:
            callback_result = self.run_callback(callback_cmd, result_dict['callback_output'])
            result_dict['output'] += f'\n{callback_result}\n'

        self.cur_depth -= 1

        return result_dict['output']


    def run_callback(self, callback_cmd: str, callback_output: str) -> str:
        result = ''

        for idx in range(len(self.plugins)):
                plugin = self.plugins[idx]
                if callback_cmd in plugin.get_tools():
                    method = plugin.get_tools()[callback_cmd]['method']
                    try:
                        command_output = method(callback_output)
                    except Exception as e:
                        return f'An error occurred: {repr(e)} \n'

                    result = self.call_tools(command_output, callback_cmd=callback_cmd)
                    break

        return result        
        

    def extract_tools(self):
        for plugin in self.plugins:
            self.tools.update(plugin.get_tools())


        