import logging

from controller import ApiServer


class Main:

    def runServer(self):
        if __name__ == "__main__":
            ApiServer.run()


app = Main()

try:
    app.runServer()
except Exception:
    logging.error("An error occurred", exc_info=True)
