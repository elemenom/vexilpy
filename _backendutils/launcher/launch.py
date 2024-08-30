from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects

def launch(server: LynqServerOrRelatedObjects) -> LynqServerOrRelatedObjects:
    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()

        return server