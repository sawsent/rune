from .process import main
import os

if __name__ == "__main__":
    host = os.environ.get("HOST")
    port_str = os.environ.get("PORT")
    if not (host and port_str):
        print("HOST and PORT environment variables are not set. Not spawning daemon.")
        exit(2)
    try:
        port = int(port_str)
    except:
        print("Bad port. Not spawning daemon.")
        exit(2)

    main(host, port)
