# sms-control
Control your linux machine via SMS and a spare android

This project has gone ar beyond in scope as compared to what I had in mind. The architecture is what I have mainly been working on.

## Architecture
- Plugins: This is for all the actual functionality that the app is responsible for. Plugins are what the input goes to and output comes from. This is also where the tools come from. See [plugin.py](plugins/plugin.py) and [llm_plugin.py](plugins/llm_plugin/llm_plugin.py)
- Tooling: This is the helper class that parses and executes tool calls, and tool chains. See [tooling.py](tooling/tooling.py) and [default_tooling.py](tooling/default_tooling/default_tooling.py)

- Listener: This is the input class. Currently the least implemented and untested. This is what listens to events, that alerts the program to run the parser pipeline. See [listener.py](listeners/listener.py) and the WIP [sms_listener.py](listeners/sms_listener.py)
- Parsers: This is the connector between the listener and the plugins and tooling pipeline.


This is basicall what the project boils down to. Nothing has been documented yet, but I am planning to do a lot once it gets to a decent working state
.

Currently whats running is the parser pipeline that you can run with:

```bash
python3 -m parsers.default_parser.default_parser
```

For [config.py](config.py), I plan on moving to some other format like YAML, XML etc. But for now, Just the LLM settings need to be changed (See [config.py](config.py#L42-L67)). Also SearXNG needs to be configured for the search tool to work (see [config.py](config.py#L36-39) and [search_connector.py](plugins/search_plugin/search_connector.py)).