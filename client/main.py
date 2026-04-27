import os
import asyncio
import traceback
from dotenv import load_dotenv

from app.core.config import setup_environment
from app.services.chat import run_terminal_chat
from app.ui.formatter import print_shutdown, print_exit_message

setup_environment()
load_dotenv()

if __name__ == "__main__":
    try:
        asyncio.run(run_terminal_chat())
    except* KeyboardInterrupt:
        print_shutdown()
    except* Exception as eg:
        for e in eg.exceptions:
            traceback.print_exception(type(e), e, e.__traceback__)
    finally:
        print_exit_message()
        os._exit(0)