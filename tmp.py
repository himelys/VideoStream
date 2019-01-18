import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.uix.image import Image as ImageWidget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
import particlesystem as kivyparticle
from colorpicker.cblcolorpicker import CBLColorPicker, CBLColorWheel
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.rst import RstDocument
from kivy.core.window import Window
from kivy.graphics.opengl import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE
from kivy.uix.scrollview import ScrollView
import os
import math
import pygame
from random import randint
from functools import partial
from time import sleep
from xml.dom.minidom import Document
import xml.dom.minidom
from kivy.uix.dropdown import DropDown


class ParticleBuilder(Widget):
    demo_particle = ObjectProperty(kivyparticle.ParticleSystem)
    particle_window = ObjectProperty(None)
    active_filename = StringProperty(None)
    init_count = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ParticleBuilder, self).__init__(**kwargs)


class ParticleParamsLayout(Widget):

    tabs_loaded = BooleanProperty(False)

    def __init__(self,**kwargs):
        super(ParticleParamsLayout, self).__init__(**kwargs)

class ParticleLoadSaveLayout(Widget):
    new_particle = ObjectProperty(None)
    load_dir = 'templates'

    def __init__(self,**kwargs):
        load_particle_popup_content = LoadParticlePopupContents(self)
        self.load_particle_popup = Popup(title="Particle Effects", content=load_particle_popup_content, size_hint = (None,None), size=(512,512), on_open=self._popup_opened, on_dismiss=self._popup_dismissed)

        save_particle_popup_content = SaveParticlePopupContents(self)
        self.save_particle_popup = Popup(title="Particle Effects", content=save_particle_popup_content, size_hint = (None,None), size=(512,512), on_open=self._popup_opened, on_dismiss=self._popup_dismissed)

        super(ParticleLoadSaveLayout,self).__init__(**kwargs)

        # load the default particle (scheduled for the next frame so that it doesn't break)
        Clock.schedule_once(self.load_default_particle)



class GetNewFilenameLayout(Widget):
    fname_input = ObjectProperty(None)


    def __init__(self, load_save_widget, **kwargs):
        self.load_save_widget = load_save_widget
        super(GetNewFilenameLayout,self).__init__(**kwargs)



class LoadParticlePopupContents(Widget):
    blayout = ObjectProperty(None)
    blayout_height = NumericProperty(50)
    menu_height = NumericProperty(50)
    label_height = NumericProperty(50)

    def __init__(self, load_save_widget, **kwargs):
        self.load_save_widget = load_save_widget
        super(LoadParticlePopupContents,self).__init__(**kwargs)

    def button_callback(self,value):
        if value == 'load templates':
            self.load_save_widget.load_templates()
        elif value == 'load user files':
            self.load_save_widget.load_user_files()

class SaveParticlePopupContents(Widget):
    blayout = ObjectProperty(None)
    blayout_height = NumericProperty(50)
    label_height = NumericProperty(50)

    def __init__(self, load_save_widget, **kwargs):
        self.load_save_widget = load_save_widget
        super(SaveParticlePopupContents,self).__init__(**kwargs)


class Default_Particle_Panel(Widget):
    pass

class ImageChooserCell(Widget):
    image_location = StringProperty("None")
    image_chooser = ObjectProperty(None)

    def cell_press(self):
        self.image_chooser.select(self.image_location)


class ImageChooserPopupContent(GridLayout):
    def __init__(self, image_chooser = None, **kwargs):
        super(ImageChooserPopupContent,self).__init__(rows = 6, cols = 6, col_force_default = True, row_force_default = True, row_default_height = 80, col_default_width = 80, **kwargs)
        self.image_chooser = image_chooser
        png_files = self.get_all_images('./media/particles', '.png')
        # atlasses = self.get_all_images('.', '.atlas')
        for i in png_files:
            self.add_widget(ImageChooserCell(image_location=i, image_chooser = self.image_chooser, size=(self.col_default_width, self.row_default_height)))


    def get_all_images(self,dir_name,extension):
        outputList = []
        for root, dirs, files in os.walk(dir_name):
            for fl in files:
                if fl.endswith(extension): outputList.append(os.path.join(root,fl))
        return outputList


class ImageChooser(Widget):
    button_text = StringProperty("Choose a texture...")
    image_location = StringProperty('media/particle.png')

    def __init__(self,**kwargs):
        image_chooser_popup_content = ImageChooserPopupContent(image_chooser = self)
        self.image_chooser_popup = Popup(title="Images", content=image_chooser_popup_content, size_hint = (None,None), size=(512,512))
        super(ImageChooser,self).__init__(**kwargs)

    def button_callback(self,):
        self.image_chooser_popup.open()

    def select(self,image_location):
        self.image_location = image_location
        self.image_chooser_popup.dismiss()


class Particle_Property_Slider(Widget):
    slider_bounds_min = NumericProperty(0)
    slider_bounds_max = NumericProperty(100)
    slider_bounds_init_value = NumericProperty(0)
    slider_step = NumericProperty(1.0)
    box_margin = NumericProperty(5)
    prop_slider = ObjectProperty(None)
    increment_slider_by = NumericProperty(1.0)

    def increment_slider(self):
        if self.prop_slider.value + self.increment_slider_by <= self.slider_bounds_max:
            self.prop_slider.value += self.increment_slider_by

    def decrement_slider(self):
        if self.prop_slider.value - self.increment_slider_by >= self.slider_bounds_min:
            self.prop_slider.value -= self.increment_slider_by


class Particle_Color_Sliders(Widget):
    color_r = NumericProperty(1.)
    color_r_min = NumericProperty(0)
    color_r_max = NumericProperty(1.)
    color_g = NumericProperty(1.)
    color_g_min = NumericProperty(0)
    color_g_max = NumericProperty(1.)
    color_b = NumericProperty(1.)
    color_b_min = NumericProperty(0)
    color_b_max = NumericProperty(1.)
    color_a = NumericProperty(1.)
    color_a_min = NumericProperty(0)
    color_a_max = NumericProperty(1.)

    # necessary because of weird slider bug that allows values to go over bounds
    def clip(self, val, vmin, vmax):
        if val < vmin:
            return vmin
        elif val > vmax:
            return vmax
        else:
            return val

class ParticlePanel(Widget):
    particle_builder = ObjectProperty(None)
    texture_path = StringProperty("media/particle.png")
    max_num_particles = NumericProperty(200.)
    max_num_particles_min = NumericProperty(1.)
    max_num_particles_max = NumericProperty(500.)
    life_span = NumericProperty(2.)
    life_span_min = NumericProperty(.01)
    life_span_max = NumericProperty(10.)
    life_span_variance = NumericProperty(0.)
    life_span_variance_min = NumericProperty(0.)
    life_span_variance_max = NumericProperty(10.)
    start_size = NumericProperty(8.)
    start_size_min = NumericProperty(0.)
    start_size_max = NumericProperty(256.)
    start_size_variance = NumericProperty(0.)
    start_size_variance_min = NumericProperty(0.)
    start_size_variance_max = NumericProperty(256.)
    end_size = NumericProperty(8.)
    end_size_min = NumericProperty(0.)
    end_size_max = NumericProperty(256.)
    end_size_variance = NumericProperty(0.)
    end_size_variance_min = NumericProperty(0.)
    end_size_variance_max = NumericProperty(256.)
    emit_angle = NumericProperty(0.)
    emit_angle_min = NumericProperty(0.)
    emit_angle_max = NumericProperty(360.)
    emit_angle_variance = NumericProperty(0.)
    emit_angle_variance_min = NumericProperty(0.)
    emit_angle_variance_max = NumericProperty(360.)
    start_rotation = NumericProperty(0.)
    start_rotation_min = NumericProperty(0.)
    start_rotation_max = NumericProperty(360.)
    start_rotation_variance = NumericProperty(0.)
    start_rotation_variance_min = NumericProperty(0.)
    start_rotation_variance_max = NumericProperty(360.)
    end_rotation = NumericProperty(0.)
    end_rotation_min = NumericProperty(0.)
    end_rotation_max = NumericProperty(360.)
    end_rotation_variance = NumericProperty(0.)
    end_rotation_variance_min = NumericProperty(0.)
    end_rotation_variance_max = NumericProperty(360.)

    def __init__(self, pbuilder, **kwargs):
        super(ParticlePanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent

class BehaviorPanel(Widget):
    particle_builder = ObjectProperty(None)
    emitter_type = NumericProperty(0)

    ## Gravity Emitter Params
    emitter_x_variance = NumericProperty(0.)
    emitter_x_variance_min = NumericProperty(0.)
    emitter_x_variance_max = NumericProperty(200.)
    emitter_y_variance = NumericProperty(0.)
    emitter_y_variance_min = NumericProperty(0.)
    emitter_y_variance_max = NumericProperty(200.)
    gravity_x = NumericProperty(0)
    gravity_x_min = NumericProperty(-1500)
    gravity_x_max = NumericProperty(1500)
    gravity_y = NumericProperty(0)
    gravity_y_min = NumericProperty(-1500)
    gravity_y_max = NumericProperty(1500)
    speed = NumericProperty(0.)
    speed_min = NumericProperty(0.)
    speed_max = NumericProperty(300.)
    speed_variance = NumericProperty(0.)
    speed_variance_min = NumericProperty(0.)
    speed_variance_max = NumericProperty(300.)
    radial_acceleration = NumericProperty(0)
    radial_acceleration_min = NumericProperty(-400)
    radial_acceleration_max = NumericProperty(400)
    radial_acceleration_variance = NumericProperty(0.)
    radial_acceleration_variance_min = NumericProperty(0.)
    radial_acceleration_variance_max = NumericProperty(400.)
    tangential_acceleration = NumericProperty(0)
    tangential_acceleration_min = NumericProperty(-500)
    tangential_acceleration_max = NumericProperty(500)
    tangential_acceleration_variance = NumericProperty(0.)
    tangential_acceleration_variance_min = NumericProperty(0.)
    tangential_acceleration_variance_max = NumericProperty(500.)

    ## Radial Emitter Params
    max_radius = NumericProperty(100.)
    max_radius_min = NumericProperty(0.)
    max_radius_max = NumericProperty(250.)
    max_radius_variance = NumericProperty(0.)
    max_radius_variance_min = NumericProperty(0.)
    max_radius_variance_max = NumericProperty(250.)
    min_radius = NumericProperty(0.)
    min_radius_min = NumericProperty(0.)
    min_radius_max = NumericProperty(250.)
    rotate_per_second = NumericProperty(0)
    rotate_per_second_min = NumericProperty(-720)
    rotate_per_second_max = NumericProperty(720)
    rotate_per_second_variance = NumericProperty(0.)
    rotate_per_second_variance_min = NumericProperty(0.)
    rotate_per_second_variance_max = NumericProperty(720.)

    def __init__(self, pbuilder, **kwargs):
        super(BehaviorPanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent



class ColorPanel(Widget):
    particle_builder = ObjectProperty(None)

    start_color = ListProperty([1,1,1,1])
    end_color = ListProperty([1,1,1,1])
    start_color_r_variance = NumericProperty(.1)
    start_color_r_variance_min = NumericProperty(0)
    start_color_r_variance_max = NumericProperty(1.)
    start_color_g_variance = NumericProperty(.1)
    start_color_g_variance_min = NumericProperty(0)
    start_color_g_variance_max = NumericProperty(1.)
    start_color_b_variance = NumericProperty(.1)
    start_color_b_variance_min = NumericProperty(0)
    start_color_b_variance_max = NumericProperty(1.)
    start_color_a_variance = NumericProperty(.1)
    start_color_a_variance_min = NumericProperty(0)
    start_color_a_variance_max = NumericProperty(1.)
    end_color_r_variance = NumericProperty(.1)
    end_color_r_variance_min = NumericProperty(0)
    end_color_r_variance_max = NumericProperty(1.)
    end_color_g_variance = NumericProperty(.1)
    end_color_g_variance_min = NumericProperty(0)
    end_color_g_variance_max = NumericProperty(1.)
    end_color_b_variance = NumericProperty(.1)
    end_color_b_variance_min = NumericProperty(0)
    end_color_b_variance_max = NumericProperty(1.)
    end_color_a_variance = NumericProperty(.1)
    end_color_a_variance_min = NumericProperty(0)
    end_color_a_variance_max = NumericProperty(1.)
    current_blend_src = NumericProperty(0, allownone = True)
    current_blend_dest = NumericProperty(0, allownone = True)

    def __init__(self, pbuilder, **kwargs):
        super(ColorPanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent

class ScrollViewWithBars(ScrollView):
    def _start_decrease_alpha(self, *l):
        pass

class DebugPanel(Widget):
    fps = StringProperty(None)
    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps, .03)

    def update_fps(self,dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .03)

class WorkingFile(Widget):
    filename = StringProperty(None)

class VariableDescriptions(Widget):

    def tab_info(self):


class BlendFuncChoices(Popup):

    def __init__(self, func_chooser, **kwargs):
        super(BlendFuncChoices, self).__init__(**kwargs)
        self.func_chooser = func_chooser
        self.populate_list()


class BlendFuncChooser(BoxLayout):
    func_choices = ObjectProperty(None)
    current_src = NumericProperty(None)
    current_dest = NumericProperty(None)

    def __init__(self, **kwargs):
        super(BlendFuncChooser, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_chooser)


Builder.load_file(os.path.dirname(os.path.realpath(__file__)) + '/colorpicker/cblcolorpicker.kv')

class ParticleBuilderApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    ParticleBuilderApp().run()
