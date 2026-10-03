import logging

from queue import Queue, Empty

from listeners.listener import Listener
from parsers.parser import Parser
from loggers.logger import Logger
from config import sms_queue, parser, listener, logger


def parse_sms(sms_data: dict, parser: Parser, logger: Logger) -> None:
    logger.info('Message sent to parser')
    return parser.parse_command(sms_data['content'])


def main(sms_queue: Queue, listener: Listener, command_parser: Parser, logger: Logger):
    try:
        logger.info(f'Starting listener')
        listener.start()
    except Exception as e:
        logging.error(repr(e))

    while True:
        try:
            incoming_sms = sms_queue.get(timeout=1)
            logger.info(f'Listener event detected, sending message to parser')

            # TODO Make this post pipeline response action modular and expandable
            print(parse_sms(incoming_sms, command_parser, logger))

            sms_queue.task_done()
            logger.info('Task has been completed, waiting for next event')

        except Empty:
            pass
        except KeyboardInterrupt:
            logger.info('Exiting')
        except Exception as e:
            logger.error(repr(e))


if __name__ == '__main__':
    main(sms_queue, listener, parser, logger)

