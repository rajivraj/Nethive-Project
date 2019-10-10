import parsers
import sniffers
import threading
from activators import activate


if __name__ == "__main__":
    # --- Dependency and installation management
    activate.all()

    # --- Thread initialization for every modules
    http = threading.Thread(target=sniffers.http.run, args=("*", "ens33"))
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=())
    bash_parser = threading.Thread(target=parsers.bash_parser.run, args=())

    # --- Begin running modules and sensors
    # http.start()
    # slog_parser.start()
    bash_parser.start()


