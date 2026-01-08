from rune.models.session.protocol.command import EndSessionCmd, GetSessionKeyCmd, SessionCmd, StartSessionCmd
from rune.models.session.protocol.response import SessionResp
from rune.session.daemon import process
import socket
import json


def sandbox():
    print("sandbox rune")
    spawn_daemon()
    #try:
    #    set_password()
    #except ConnectionRefusedError as e:
    #    print(e)
    #get_password()
    #stop()

def spawn_daemon():
    print("spawning daemon")
    process.main("localhost", 5000)

def send(request: SessionCmd) -> SessionResp:
    HOST = "localhost"
    PORT = 5000

    with socket.create_connection((HOST, PORT)) as s:
        s.sendall((json.dumps(request.to_dict()) + "\n").encode("utf-8"))

        response = s.recv(4096)
        raw = json.loads(response.decode("utf-8"))
        return SessionResp.from_dict(raw)


def set_password():
    print("setting password")
    resp = send(StartSessionCmd("pass", 10, "user"))
    print(resp.to_dict())

def get_password():
    print("getting password")
    resp = send(GetSessionKeyCmd("user"))
    print(resp.to_dict())

def stop():
    print("stopping session")
    resp = send(EndSessionCmd())
    print(resp.to_dict())
