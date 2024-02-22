from library.global_variables import RUN_PORT
from moduls.server import run_server
import uvicorn
import sys


def main():
    """External server runner function
    """
    app = run_server()
    uvicorn.run(app, **RUN_PORT)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
