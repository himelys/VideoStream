from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class Fejkbiljett(App):

    def build(self):
        gen_btn = Button(text='Generera',
                         size_hint=(.90, .10),
                         pos=(5, 5),
                         font_size=21)
        gen_btn.bind(on_press=StockholmTicket.getMessage)
        l = BoxLayout()
        l.add_widget(gen_btn)
        return l


class StockholmTicket(object):

    def getMessage(self):
        print "2. this is called on the method getMessage of StockholmTicket"

if __name__ == "__main__":
    Fejkbiljett().run()
