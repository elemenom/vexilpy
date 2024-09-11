from lynq import yamlapp, SelfApp

@yamlapp("index.yaml") .\
    export.standard
def index() -> None:
    ...

index().open()