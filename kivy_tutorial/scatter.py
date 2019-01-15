from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scatter import  Scatter
from kivy.uix.floatlayout import FloatLayout

class myKivy(App):
    def build(self):
        f = FloatLayout()
        s = Scatter()
        l = Label(text="Howdy", font_size=150)
        #Can only return one widget, so the other widgets will need to be children
        f.add_widget(s)
        s.add_widget(l)
  #Scatter and label are now children of float
        return f

if __name__ == "__main__":
    myKivy().run()
