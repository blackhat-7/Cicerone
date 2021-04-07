import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.cache import Cache 
from kivy.uix.textinput import TextInput
Cache._categories['kv.image']['limit'] = 0 
Cache._categories['kv.image']['timeout'] = 1 
Cache._categories['kv.texture']['limit'] = 0 
Cache._categories['kv.texture']['timeout'] = 1 
from sign_translate import translate_from_image
from models import Cicerone_Inception
import joblib
import pandas as pd
loaded_model = joblib.load('cicerone_inception.model')

locationDetails = pd.read_csv('LocationDetails.csv')

def getData(name):
    nameView = locationDetails[locationDetails['Location'] == name]
    return nameView['Summary'].values.tolist()[0], nameView['Contact'].values.tolist()[0], nameView['Description'].values.tolist()[0]

class MainMenu(GridLayout):

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.cols=1

        self.sign = Button(text='Open Camera')
        self.sign.bind(on_press=self.switchToCam)
        self.add_widget(self.sign)

    def switchToCam(self, *args):
        main_app.screen_manager.transition = SlideTransition(direction='left')
        main_app.screen_manager.current = 'Cam'

class OptionsMenu(GridLayout):

    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__(**kwargs)
        self.cols=1
        self.image = Image(source = '')
        self.add_widget(self.image)

        self.sign = Button(text='Translate Signboard')
        self.sign.bind(on_press=self.switchToSign)
        self.add_widget(self.sign)

        self.landmark = Button(text='Identify Landmark')
        self.landmark.bind(on_press=self.switchToLandmark)
        self.add_widget(self.landmark)

    def switchToSign(self, *args):
        main_app.sign_menu.label.text = translate_from_image('cur_image.png')
        print(main_app.sign_menu.label.text)
        main_app.screen_manager.transition = SlideTransition(direction='left')
        main_app.screen_manager.current = 'Sign'

    def switchToLandmark(self, *args):
        named = loaded_model.predict_image_path('cur_image.png')
        print(named)
        main_app.landmark_menu.nameData.text = named
        summaryD,contactD,contextD = getData(named)
        print(contextD)
        main_app.landmark_menu.summaryData.text = str(summaryD)
        main_app.landmark_menu.contactData.text = str(contactD)
        main_app.landmark_menu.contextData.text = str(contextD)
        main_app.screen_manager.transition = SlideTransition(direction='left')
        main_app.screen_manager.current = 'Landmark'

class SignMenu(GridLayout):

    def __init__(self, **kwargs):
        super(SignMenu, self).__init__(**kwargs)
        self.cols=1
        self.label = Label(text='')
        self.add_widget(self.label)

        self.back = Button(text='Back')
        self.back.bind(on_press=self.switchBack)
        self.add_widget(self.back)

    def switchBack(self, *args):
        main_app.screen_manager.transition = SlideTransition(direction='right')
        main_app.screen_manager.current = 'Main'

class LandmarkMenu(GridLayout):

    def __init__(self, **kwargs):
        super(LandmarkMenu, self).__init__(**kwargs)
        self.cols=1
        self.name = Label(text = 'Name', font_size = '20sp')
        self.summary = Label(text = 'Summary', font_size = '20sp')
        self.contact = Label(text = 'Contact', font_size = '20sp')
        self.context =  Label(text = 'Context', font_size = '20sp')

        # nameData = Label(text = named)
        # summaryD,contactD,contextD = getData(named)
        # summaryData = Label(text = summaryD)
        # contactData = Label(text = contactD)
        # ContextData = Label(text = contextD)

        self.nameData = Label(text = '')
        self.summaryData = Label(text = '')
        self.contactData = Label(text = '')
        self.contextData = Label(text = '', text_size=(1000, 200))

        self.add_widget(self.name)
        self.add_widget(self.nameData)
        self.add_widget(self.summary)
        self.add_widget(self.summaryData)
        self.add_widget(self.contact)
        self.add_widget(self.contactData)
        self.add_widget(self.context)
        self.add_widget(self.contextData)

        self.back = Button(text='Back')
        self.back.bind(on_press=self.switchBack)
        self.add_widget(self.back)

    def switchBack(self, *args):
        main_app.screen_manager.transition = SlideTransition(direction='right')
        main_app.screen_manager.current = 'Main'

class CamMenu(GridLayout):

    def __init__(self, **kwargs):
        super(CamMenu, self).__init__(**kwargs)
        self.cols=1
        self.cameraObject = Camera(play=True, index=0, resolution=(640,480))

        self.camaraClick = Button(text="Take Photo")
        self.camaraClick.bind(on_press=self.onCameraClick)

        self.back = Button(text='Back')
        self.back.bind(on_press=self.switchBack)

        self.add_widget(self.cameraObject)
        self.add_widget(self.camaraClick)
        self.add_widget(self.back)

    def onCameraClick(self, *args):
        self.cameraObject.export_to_png('cur_image.png')
        main_app.screen_manager.transition = SlideTransition(direction='left')
        main_app.screen_manager.current = 'Options'
        main_app.options_menu.image.source = ''
        main_app.options_menu.image.source = 'cur_image.png'

    def switchBack(self, *args):
        main_app.screen_manager.transition = SlideTransition(direction='right')
        main_app.screen_manager.current = 'Main'

class SwitchBtn(Button):

    pressed = ListProperty([0, 0])

    def __init__(self,text,**kwargs):
        super(SwitchBtn, self).__init__(**kwargs)
        self.text = text
        self.toggle = False

    def on_touch_down(self, touch):
        # super(CustomBtn, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            if main_app.screen_manager.current == 'Main':
                main_app.screen_manager.transition = SlideTransition(direction='left')
                main_app.screen_manager.current = 'Cam'
            else:
                main_app.screen_manager.transition = SlideTransition(direction='right')
                main_app.screen_manager.current = 'Main'
        
        return super(SwitchBtn, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print ('pressed at {pos}'.format(pos=pos))

class TestApp(App):

    def build(self):
        self.screen_manager = ScreenManager()

        # Initial, connection screen (we use passed in name to activate screen)
        # First create a page, then a new screen, add page to screen and screen to screen manager
        self.main_menu = MainMenu()
        screen = Screen(name='Main')
        screen.add_widget(self.main_menu)
        self.screen_manager.add_widget(screen)

        # Info page
        self.cam_menu = CamMenu()
        screen = Screen(name='Cam')
        screen.add_widget(self.cam_menu)
        self.screen_manager.add_widget(screen)

        self.options_menu = OptionsMenu()
        screen = Screen(name='Options')
        screen.add_widget(self.options_menu)
        self.screen_manager.add_widget(screen)

        self.sign_menu = SignMenu()
        screen = Screen(name='Sign')
        screen.add_widget(self.sign_menu)
        self.screen_manager.add_widget(screen)

        self.landmark_menu = LandmarkMenu()
        screen = Screen(name='Landmark')
        screen.add_widget(self.landmark_menu)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    main_app = TestApp()
    main_app.run()