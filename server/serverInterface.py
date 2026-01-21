import socketio
import threading
from vars.globals import server_namespace
from vars.direction import Direction
from game.items.itemFactory import ItemFactory


class ServerInterface:
    def __init__(self):
        self.socket = socketio.Client()
        self.move_issued = Direction.NONE
        self.connected_event = threading.Event()
        self.items_to_use = []
        self.item_factory = ItemFactory()
        self.next_turn = 0
        self.votes = {
            Direction.UP: 0,
            Direction.RIGHT: 0,
            Direction.DOWN: 0,
            Direction.LEFT: 0
        }
        self.leaderboard = []
        self.cheese_count = 0

        @self.socket.event(namespace=server_namespace)
        def move(data):
            self.move_issued = Direction(data)

        @self.socket.event(namespace=server_namespace)
        def use_item(data):
            item = self.item_factory.build(data["item"], data["user"], data["config"])
            self.items_to_use.append(item)

        @self.socket.event(namespace=server_namespace)
        def update(data):
            self.votes = {
                Direction.UP: data["votes"]["up"],
                Direction.RIGHT: data["votes"]["right"],
                Direction.DOWN: data["votes"]["down"],
                Direction.LEFT: data["votes"]["left"]
            }
            self.next_turn = data["next_turn"]
            self.leaderboard = data["leaderboard"]
            self.cheese_count = data["cheese_count"]

    def start_client(self):
        self.socket.connect(
            "http://localhost:5000",
            namespaces=[server_namespace]
        )
        self.connected_event.set()
        self.socket.wait()

    def start_round(self, got_cheese, directions):
        data = {
            "got_cheese": got_cheese,
            "directions": {
                "up": directions[Direction.UP],
                "right": directions[Direction.RIGHT],
                "down": directions[Direction.DOWN],
                "left": directions[Direction.LEFT]
            }
        }
        self.socket.emit("start_round", data, namespace=server_namespace)

    def update_directions(self, directions):
        data = {
            "up": directions[Direction.UP],
            "right": directions[Direction.RIGHT],
            "down": directions[Direction.DOWN],
            "left": directions[Direction.LEFT]
        }
        self.socket.emit("update_directions", data, namespace=server_namespace)
