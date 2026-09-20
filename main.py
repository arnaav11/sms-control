from queue import Queue, Empty

from listeners.listener import Listener
from parsers.parser import Parser

def parse_sms(sms_data: dict, parser: Parser) -> None:
    return parser.parse_command(sms_data['content'])


def main(sms_queue: Queue, listener: Listener, command_parser: DefaultParser):
    listener.start()
    
    try:
        while True:
            try:
                incoming_sms = sms_queue.get(timeout=1)
                print(f'parsing SMS \nInfo: {incoming_sms} \n')

                print(parse_sms(incoming_sms, command_parser))

                sms_queue.task_done()

            except Empty:
                pass

    except KeyboardInterrupt:
        print("\n[Main Program] Shutting down...")


if __name__ == '__main__':
    from config import *

    main(sms_queue, listener, parser)

