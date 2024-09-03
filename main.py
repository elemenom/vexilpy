from lynq.app import jsonapp

@jsonapp("server.json") .export .direct
def index(self) -> None:
    self.singular("Hello, world!")

index()