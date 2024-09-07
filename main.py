from lynq import jsonapp, App

@jsonapp("index.json") .\
style .\
    add_attribute("#main-button") .\
        add_option(background_color="black") .\
        add_option(color="white") .\
        back() .\
    back() .\
export.standard
def index(self: App) -> None:
    with self.ctrl.function("on_button_click()"):
        self.ctrl.line("console.log('Hello, world!!!!!!!!!!!!!!!!')")

    with self.button(id="main-button", onclick="on_button_click()"):
        self.singular("Press me!")