from lynq import app, LynqServer, App

@app(LynqServer(8000, "./")) .\
style .\
    add_attribute("#button") .\
        add_option(background_color="#000000") .\
        add_option(color="#ffffff") .\
        add_option(font_family="consolas") .\
        back() .\
    back() .\
export .standard
def index(self: App) -> None:
    with self.ctrl.function("on_button_click"):
        self.ctrl.line("console.log('Hello, world')")

    with self.button(id="button", onclick="on_button_click()"):
        self.singular("Hello, world!")

index().open()