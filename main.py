"""
    Application made by Gabro all rights reserved
"""

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem, OneLineIconListItem, MDList
from kivy.lang import Builder
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.taptargetview import MDTapTargetView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import PIL
import numpy as np
import pandas as pd
from kivy import platform
import kivymd.uix.card
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import webbrowser

LabelBase.register(name='Colossalis Regular', fn_regular="Colossalis Regular.otf")

can_edit = False
episode_to_edit = {}

new_description = ""


class ListaMatch(TwoLineListItem):

    def __init__(self, **kwargs):
        super(ListaMatch, self).__init__(**kwargs)

        self.text_color = "white"
        self.secondary_text_color = "white"
        self.secondary_theme_text_color = "Custom"
        self.theme_text_color = "Custom"


class ListaPreferiti(MDCardSwipe):
    text = StringProperty()
    _python_access = ObjectProperty(None)


class LoadingPopup(Popup):
    _python_access = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadingPopup, self).__init__(**kwargs)
        self.title = "In cerca della verità..."
        self.content = Loadingimage()
        self.size_hint = (None, None)
        self.size = (700, 700)
        self.font_name = "Colossalis Regular"


class Loadingimage(Image):
    source = StringProperty()
    _python_access = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Loadingimage, self).__init__(**kwargs)
        self.source = 'loading.png'
        self.allow_stretch = True
        self.nocache = True


class Lefticon(OneLineIconListItem):
    id = StringProperty()
    text = StringProperty()
    icon = StringProperty()
    _python_access = ObjectProperty(None)


# Action do do if left icons are clicked
class SelectItemonList(kivymd.uix.card.ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        for item in self.children:
            instance_item.text_color = self.theme_cls.primary_color
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                if item.text == "[font=Colossalis Regular]Instagram":
                    webbrowser.open('https://www.instagram.com/ga8ro/')
                elif item.text == "[font=Colossalis Regular]Email":
                    webbrowser.open('https://mail.google.com/mail/u/0/?fs=1&to=gabriaquila729@gmail.com&tf=cm')
                elif item.text == "[font=Colossalis Regular]YouTube":
                    webbrowser.open("https://www.youtube.com/channel/UCkGvbGqYzDi3lfgtbQ_pngg")
                elif item.text == "[font=Colossalis Regular]Info":
                    a = InfoPopup()
                    a.open()
                break


class InfoPopup(Popup):

    def __init__(self, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title = "Gabro_29 ©"
        self.content = MDLabel(text="Gabriele Lo Cascio è uno studente iscritto al corso di laurea in Scienze"
                                   " Fisiche presso l'Università degli studi di Palermo. La passione "
                                   "per l'infromatica maturata negli ultimi anni lo ha spinto verso la "
                                   "Data Science e l'analisi dati. Questo progetto dedicato "
                                   "al Detective in miniatura vede la luce dopo un mese di lavoro. "
                                   "Un ringraziamento speciale a mia sorella per essersi offerta "
                                   "come beta tester.", font_size=30, font_name="Colossalis Regular",
                               theme_text_color="Custom", text_color="white", padding_x=25, line_height=1.5)
        self.size_hint = (None, None)
        self.size = (1000, 1200)
        self.font_name = "Colossalis Regular"


class InfoBox(GridLayout):

    def __init__(self, **kwargs):
        super(InfoBox, self).__init__(**kwargs)
        self.cols = 1
        self.adaptive_height = True
        self.text = ["Gabriele Lo Cascio è uno studente", "iscritto al corso di laurea in Scienze",
                     "Fisiche presso l'Università degli studi di Palermo",
                     "La passione  per l'infromatica maturata", "negli ultimi anni lo ha spinto verso la"
                                                                "Data Science e l'analisi dati.",
                     "Questo progetto dedicato al",
                     "Detective in miniatura vede la", "luce dopo un mese di lavoro.",
                     "Un ringraziamento speciale a", "mia sorella per essersi offerta "
                                                     "come beta tester."]
        for i in self.text:
            self.add_widget(InfoLabel(text=i))
        self.padding = 25


class InfoLabel(OneLineIconListItem):

    def __init__(self, **kwargs):
        super(InfoLabel, self).__init__(**kwargs)
        self.font_size = 50
        self.font_name = "Colossalis Regular"
        self.theme_text_color = "Custom"
        self.text_color = "white"


class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, ListaMatch):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view"""
        self.selected = is_selected
        if is_selected:
            global can_edit
            global episode_to_edit
            can_edit = True
            episode_to_edit = rv.data[index]


class PencilPopup(Popup):

    def __init__(self, **kwargs):
        super(PencilPopup, self).__init__(**kwargs)
        self.title = "Ehy! Non ho abbastanza indizi"
        self.content = PencilLabel()
        self.size_hint = (None, None)
        self.size = (700, 700)
        self.font_name = "Colossalis Regular"


class PencilLabel(MDLabel):

    def __init__(self, **kwargs):
        super(PencilLabel, self).__init__(**kwargs)
        self.text = "Questo bottone serve a modificare o ad aggiungere " \
                    "una descrizione agli episodi. Ma per farlo devi prima " \
                    "selezionarne uno dalla schermata 'Ricerca'."

        self.font_name = "Colossalis Regular"
        self.font_size = 55
        self.color = "white"
        self.padding_x = 25
        self.line_height = 1.5


class EditPopup(Popup):

    def __init__(self, row, old_description, file, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.title = "Non compromettere le prove :)"
        self.content = EditBox(row, old_description, file)
        self.size_hint = (None, None)
        self.size = (700, 700)
        self.font_name = "Colossalis Regular"


class EditBox(GridLayout):

    def __init__(self, row, old_description, file, **kwargs):
        super(EditBox, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 1
        self.add_widget(EditText(row, old_description, file))
        self.add_widget(MYBoxLayout())
        self.padding = 25
        self.adaptive_height = True


class MYBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MYBoxLayout, self).__init__(**kwargs)
        self.add_widget(SaveButton())


class SaveButton(MDRaisedButton):

    def __init__(self, **kwargs):
        super(SaveButton, self).__init__(**kwargs)
        self.text = "Salva"
        self.font_name = "Colossalis Regular"
        self.size_hint_x = 1

    def on_release(self):
        EditText(row=0, old_description="None", file="").get_text()


class EditText(TextInput):

    def __init__(self, row, old_description, file, **kwargs):
        super(EditText, self).__init__(**kwargs)
        self.hint_text = old_description
        self.multiline = True
        self.foreground_color = (1, 1, 1, 1)
        self.font_name = "Colossalis Regular"
        self.font_size = 55
        self.background_color = (0, 0, 0, 0)
        self.padding_y = 50
        self.size_hint_x = 1
        self.id = "edit"
        self.my_row = row
        self.my_file = file

    def get_text(self):
        self.on_text_validate()

    def _on_textinput_focused(self, instance, value, *largs):
        ConanApp().edit_csv(self.my_row, instance.text, self.my_file)


KV = """
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.4, 0.1, 0.1, .3) if self.selected else (.3, .3, .3, .6)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: True
        
<Lefticon>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    IconLeftWidget:
        id: root.id
        icon: root.icon
        theme_text_color: "Custom"
        
<ListaPreferiti>:
    _python_access: lista
    size_hint_y: None
    height: lista.height
    swipe_distance: 1200
    MDCardSwipeLayerBox:
        padding: "8dp"
        MDIconButton:
            id: cestino
            icon: "trash-can"
            on_release:
                app.remove_item_star(root)
    MDCardSwipeFrontBox:

        OneLineListItem:
            id: lista
            _no_ripple_effect: True
            text: root.text
            
# <ListaMatch>:
#     _no_ripple_effect: True
#     text: root.text
#     font_name: root.font
#     secondary_text: root.secondary_text

<LoadingPopup>:
    _python_access: display_photo
    font_name: "Colossalis Regular"
    Loadingimage:
        id: display_photo


<Loadingimage>:
    source: root.source

MDNavigationLayout:
    ScreenManager:
        Screen:
            BoxLayout:
                orientation: 'vertical'
                MDToolbar:
                    title: "Menu"
                    elevation: 10
                    left_action_items: [['menu', lambda x: nav_drawer.set_state()]]
                    right_action_items: [["refresh", lambda x: app.reload()], ["border-color", lambda x: app.edit_description()]]
                    
                MDBottomNavigation:
                    panel_color: .2, .2, .2, 1
                    MDBottomNavigationItem:
                        name: 'RND'
                        id: prima
                        text: 'Random'
                        font_name: "Colossalis Regular"
                        icon: 'chart-histogram'

                        GridLayout:
                            adaptive_height: True
                            rows: 4
                            spacing: 15
                            canvas.before:
                                Color:
                                    rgba: 0, 0, 0, .7
                                Rectangle:
                                    size: self.size
                                    pos: self.pos
                            AnchorLayout:
                                size_hint_y: None
                                height: 170
                                orientation: "vertical"
                                anchor_x: 'center'
                                anchor_y: 'top'
                                pad_x: 7
                                pad_y: 5
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, .7
                                MDTextField:
                                    id: epsnumero
                                    multiline: False
                                    hint_text: "Cerca qui episodi in base al numero"
                                    helper_text: "Salva l'episodio nei preferiti se vuoi"
                                    font_name: "Colossalis Regular"
                                    helper_text_mode: "on_focus"
                                    mode: "rectangle"
                                    keyboard_suggestions: True
                                    use_bubble: True
                                    use_handles: True
                                    size_hint_y: None
                                    size_hint_x: None
                                    width: 880
                                    icon_right: "border-color"
                            BoxLayout:
                                ScrollView:
                                    MDLabel:
                                        id: rnd_window
                                        padding_x: 10
                                        padding_y: 50
                                        color: (1, 1, 1, 1)
                                        font_size: 50
                                        text: "Premi il bottone per generare un episodio random"
                                        font_name: "Colossalis Regular"
                                        bold: True
                                        size_hint_y: None
                                        height: self.texture_size[1]
                                        text_size: self.width, None
                            GridLayout:
                                size_hint: 1, None
                                height: 150
                                cols: 3
                                rows: 1
                                spacing: 5
                                canvas:
                                    Color:
                                        rgba: .4, .4, .4, 1
                                    Rectangle:
                                        size: self.width, 1
                                        pos: self.x, self.y+self.height-1
                                AnchorLayout:
                                    size_hint_y: None
                                    height: onoff.height + 10
                                    MDIconButton:
                                        id: onoff
                                        icon: "blank"
                                        padding_x: 15
                                        md_bg_color: app.theme_cls.primary_color
                                        pos_hint: {"center_x": 0, "center_y": .5}
                                        pos: 10, 10
                                        on_release: app.fileadd()
                                BoxLayout:
                                AnchorLayout:
                                    size_hint_y: None
                                    height: brack.height + 10
                                    MDIconButton:
                                        id: brack
                                        icon: "blank"
                                        md_bg_color: app.theme_cls.primary_color
                                        pos_hint: {"center_x": 1, "center_y": .5}
                                        on_press:
                                            app.tap_brackets()
                                        on_release:
                                            app.description_brackets()

                            BoxLayout:
                                orientation: "vertical"
                                size_hint_y: None
                                height: 100
                                GridLayout:
                                    adaptive_height: True
                                    cols: 3
                                    spacing: 7
                                    MDRaisedButton:
                                        id: randbu
                                        text: "Episodio Random"
                                        font_name: "Colossalis Regular"
                                        background_normal: ""
                                        background_color: (0, 0.5, 0, 0.5)
                                        background_down: ""
                                        size_hint_y: None
                                        size_hint_x: 1
                                        width: 130
                                        height: 100
                                        on_press:
                                            self.background_color = (1, 0, 0, 1)
                                        on_release:
                                            self.background_color = (0.5, 0.5, 0, 0.5)
                                            app.randomize()
                                    MDRaisedButton:
                                        id: cercanumero
                                        text: "Cerca"
                                        font_name: "Colossalis Regular"
                                        background_normal: ""
                                        background_color: (0, 0.5, 0, 0.5)
                                        background_down: ""
                                        size_hint_y: None
                                        size_hint_x: 1
                                        width: 130
                                        height: 100
                                        on_press:
                                            self.background_color = (1, 0, 0, 1)
                                        on_release:
                                            self.background_color = (0.5, 0.5, 0, 0.5)
                                            app.cercanumber()
                    MDBottomNavigationItem:
                        name: 'search_window'
                        id: seconda
                        text: 'Ricerca'
                        font_name: "Colossalis Regular"
                        icon: 'book-search-outline'
                        GridLayout:
                            rows: 3
                            spacing: 10
                            adaptive_height: True
                            canvas.before:
                                Color:
                                    rgba: 0, 0, 0, .7
                                Rectangle:
                                    size: self.size
                                    pos: self.pos
                            AnchorLayout:
                                size_hint_y: None
                                height: 170
                                orientation: "vertical"
                                anchor_x: 'center'
                                anchor_y: 'top'
                                pad_x: 15
                                pad_y: 5
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, .7

                                MDTextField:
                                    id: keyword
                                    multiline: False
                                    hint_text: "Digita una parola da cercare"
                                    helper_text: 'Parole chiave: "all", "canon", "tips"'
                                    font_name: "Colossalis Regular"
                                    helper_text_mode: "on_focus"
                                    mode: "rectangle"
                                    keyboard_suggestions: True
                                    use_bubble: True
                                    use_handles: True
                                    size_hint_y: None
                                    size_hint_x: None
                                    width: 710
                            RV:
                                id: match

                            GridLayout:
                                cols: 3
                                size_hint_y: None
                                size_hint_x: 1
                                height: 150
                                spacing: 315
                                adaptive_height: True
                                pad_x: 0
                                pad_y: 15
                                canvas.before:
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                MDIconButton:
                                    id: left
                                    icon: "menu-left"
                                    theme_text_color: "ContrastParentBackground"
                                    #text_color: 0.2, 0.6, 1, 0.3
                                    md_bg_color: app.theme_cls.primary_color
                                    #pos_hint: {"left_x": 1, "center_y": 0}
                                    on_press:
                                        self.background_color = (1, 0, 0, 1)
                                        app.show_popup()
                                    on_release:
                                        app.arrow_sex()
                                MDRaisedButton:
                                    id: searchbu
                                    text: "Cerca"
                                    font_name: "Colossalis Regular"
                                    pos_hint: {"center_x": 1, "center_y": 0}
                                    background_normal: ""
                                    background_color: (0, 0.5, 0, 0.5)
                                    background_down: ""
                                    on_press:
                                        self.background_color = (1, 0, 0, 1)
                                        app.show_popup()
                                    on_release:
                                        self.background_color = (0.5, 0.5, 0, 0.5)
                                        app.search()
                                MDIconButton:
                                    id: right
                                    icon: "menu-right"
                                    theme_text_color: "ContrastParentBackground"
                                    #text_color: 0.2, 0.6, 1, 0.3
                                    md_bg_color: app.theme_cls.primary_color
                                    pos_hint: {"center_x": 1, "center_y": 0}
                                    on_press:
                                        self.background_color = (1, 0, 0, 1)
                                        app.show_popup()
                                    on_release:
                                        app.arrow_dex()
                    MDBottomNavigationItem:
                        name: 'star_window'
                        id: preferiti
                        text: 'Preferiti'
                        font_name: "Colossalis Regular"
                        icon: 'star'
                        BoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDToolbar:
                                elevation: 10
                                title: "Episodi preferiti"
                                font_name: "Colossalis Regular"
                                MDIconButton:
                                    icon: "refresh"
                                    md_bg_color: app.theme_cls.primary_color
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    on_release:
                                        app.filerefresh()
                            ScrollView:
                                scroll_timeout : 130
                                MDList:
                                    id: episodistar
                                    padding: 0
    MDNavigationDrawer:
        id: nav_drawer
        BoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"
            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
                height: avatar.height
                Image:
                    id: avatar
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "dc2buona.png"
            MDLabel:
                text: "DC App"
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                text: "Created by Gabro"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]
            ScrollView:
                SelectItemonList:
                    id: left_icon
"""


class ConanApp(MDApp):
    overlay_color = get_color_from_hex("#6042e4")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Conan App"

        self.episode_file = pd.read_csv(f"episodi.csv")
        self.Num_Eps = self.episode_file["Numero"]
        self.Episodi = self.episode_file["Titolo"]
        self.Description = self.episode_file["Descrizione"]

        self.episode_mib = pd.read_csv(f"nero.csv")
        self.Num_Eps_mib = self.episode_mib["Numero"]
        self.Episodi_mib = self.episode_mib["Titolo"]
        self.Description_mib = self.episode_mib["Descrizione"]
        self.couple_mib = [couple for couple in self.Num_Eps_mib.items()]

        self.preferiti = list()
        self.list_eps = list()
        self.data_list = list()
        self.tempo = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
                      'Ottobre', 'Novembre', 'Dicembre', 'Lunedì', 'Martedi', 'Mercoledì', 'Giovedì', 'Venerdì',
                      'Sabato', 'Domenica', 'Natale', 'Primavera', 'Estate', 'Inverno', 'San Valentino',
                      'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre',
                      'ottobre', 'novembre', 'dicembre', 'estate', 'lunedì', 'martedì', 'mercoledì', 'giovedì',
                      'venerdì', 'sabato', 'domenica']

        self.K_Word = str()
        self.text_tips = ["La lista di episodi utilizzata è canonica,", "tuttavia le descrizioni di ciascun episodio",
                          "sono del tutto personali e vengono", "anche troncate. Per vederle",
                          "interamente andare nella", "schermata 'Random' e cercare", "da lí tramite il numero.",
                          "Per modificarle invece,", "cliccare sull'episodio e", "premere la matita in alto."]
        self.start = 0
        self.end = 100
        self.search_text = "first"
        self.length = 0
        self.row = int()
        self.new_description = str()
        self.description = True
        self.output_text = str()
        self.prev_episode = str()
        self.my_popup = LoadingPopup()
        self.my_image = Loadingimage()

    def build(self):
        """Build KV file"""
        return Builder.load_string(KV)

    def on_start(self):
        """Do stuffs on start"""

        with open("preferiti.txt", "r") as file:
            for line in file:
                self.preferiti.append(f"[font=Colossalis Regular]{line}")
                self.root.ids.episodistar.add_widget(ListaPreferiti(text=f"[font=Colossalis Regular]{line}"))

        self.root.ids["brack"].icon = "code-parentheses"
        self.root.ids["onoff"].icon = "star-off"

        icons_item = {
            "instagram": "Instagram",
            "youtube": "YouTube",
            "information": "Info"
        }
        for icon_name in icons_item.keys():
            self.root.ids.left_icon.add_widget(
                Lefticon(icon=icon_name, text=f"[font=Colossalis Regular]{icons_item[icon_name]}")
            )

        self.root.ids.match.data = [{"text": text} for text in self.text_tips]

    def randomize(self):
        """Generate a random episode and show it on the screen"""

        self.root.ids["onoff"].icon = "star-off"
        if self.description:
            self.root.ids["brack"].icon = "code-parentheses"
        elif not self.description:
            self.root.ids["brack"].icon = "slash-forward"

        rnd_num = np.random.randint(1, 778)

        if "(" in f'{self.Description[rnd_num]}':
            self.prev_episode = f"{self.Num_Eps[rnd_num]} - {self.Episodi[rnd_num]} {self.Description[rnd_num]}"
            random_Eps = f"{self.Num_Eps[rnd_num]} - {self.Episodi[rnd_num]} {self.Description[rnd_num]}"
        else:
            self.prev_episode = f"{self.Num_Eps[rnd_num]} - {self.Episodi[rnd_num]}"
            random_Eps = f"{self.Num_Eps[rnd_num]} - {self.Episodi[rnd_num]}"

        if self.description:
            self.root.ids["rnd_window"].text = random_Eps
        elif not self.description:
            output_text = random_Eps
            self.root.ids["rnd_window"].text = output_text[:output_text.find(" (")]

        self.root.ids["onoff"].disabled = False

        with open("preferiti.txt", "r") as file:
            if self.root.ids["rnd_window"].text in file:
                self.root.ids["onoff"].icon = "star"

    def description_brackets(self):
        """Hide/Show descriptions of episodes"""

        if self.description:
            self.description = False
            self.output_text = self.root.ids["rnd_window"].text
            self.prev_episode = self.output_text
            if "(" in self.output_text:
                self.root.ids["rnd_window"].text = self.output_text[:self.output_text.find(" (")]
                self.root.ids["brack"].icon = "slash-forward"
            else:
                pass
        elif not self.description:
            self.description = True
            self.root.ids["rnd_window"].text = self.prev_episode
            self.root.ids["brack"].icon = "code-parentheses"

    def arrow_sex(self):
        """Let user move in the window to see more widget"""

        if self.K_Word in ("tips", "tempo"):
            pass
        elif self.K_Word == "all":

            if self.start == 0:
                pass
            elif self.end == len(self.list_eps):

                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - (len(self.list_eps) % 100)):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

                self.start = inizio - 100
                self.end = fine - (len(self.list_eps) % 100)

            else:
                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - 100):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio - self.length
                self.end = fine - self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        elif self.K_Word == "classic" and self.length == 100:

            if self.start == 0:
                pass
            elif self.end == len(self.list_eps):

                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - (len(self.list_eps) % 100)):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

                self.start = inizio - 100
                self.end = fine - (len(self.list_eps) % 100)

            else:
                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - 100):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio - self.length
                self.end = fine - self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        elif self.K_Word == "canon":

            if self.start == 0:
                pass
            elif self.end == len(self.list_eps):

                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - (len(self.list_eps) % 100)):
                    if f'{self.Description_mib[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description_mib[i]}"})

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

                self.start = inizio - 100
                self.end = fine - (len(self.list_eps) % 100)

            else:
                self.data_list.clear()
                inizio = self.start
                fine = self.end

                for i in range(inizio - 100, fine - 100):
                    if f'{self.Description_mib[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description_mib[i]}"})

                self.start = inizio - self.length
                self.end = fine - self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        self.my_popup.dismiss()

    def arrow_dex(self):
        """Let user move in the window to see more widget"""

        if self.K_Word in ("tips", "tempo"):
            pass
        elif self.end == len(self.list_eps):
            pass
        elif self.K_Word == "all":

            if self.end == (len(self.list_eps) - (len(self.list_eps) % self.length)):

                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + 100, fine + (len(self.list_eps) % 100)):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio + 100
                self.end = fine + (len(self.list_eps) % 100)

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

            else:
                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + self.length, fine + self.length):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{i + 1} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio + self.length
                self.end = fine + self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        elif self.K_Word == "classic" and self.length == 100:

            if self.end == (len(self.list_eps) - (len(self.list_eps) % self.length)):

                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + 100, fine + (len(self.list_eps) % 100)):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio + 100
                self.end = fine + (len(self.list_eps) % 100)

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

            else:
                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + self.length, fine + self.length):
                    if f'{self.Description[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description[i]}"})

                self.start = inizio + self.length
                self.end = fine + self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        elif self.K_Word == "canon":

            if self.end == (len(self.list_eps) - (len(self.list_eps) % self.length)):

                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + 100, fine + (len(self.list_eps) % 100)):
                    if f'{self.Description_mib[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description_mib[i]}"})

                self.start = inizio + 100
                self.end = fine + (len(self.list_eps) % 100)

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

            else:
                self.data_list.clear()

                inizio = self.start
                fine = self.end

                for i in range(inizio + self.length, fine + self.length):
                    if f'{self.Description_mib[i]}' == "nan":
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f""})
                    else:
                        self.data_list.append(
                            {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[i]} - {self.list_eps[i]}',
                             "secondary_text": f"[font=Colossalis Regular]{self.Description_mib[i]}"})

                self.start = inizio + self.length
                self.end = fine + self.length

                self.root.ids.match.data.clear()
                self.root.ids.match.data = self.data_list

        self.my_popup.dismiss()

    def clear_listone(self):
        """Remove showed widgets"""

        for eps_in_list in reversed(self.root.ids.match.children):
            self.root.ids.match.remove_widget(eps_in_list)

    def search(self):
        """Search for keyword in dataframe"""

        if self.search_text == self.root.ids["keyword"].text:
            pass
        elif self.root.ids["keyword"].text == "":
            pass
        elif self.root.ids["keyword"].text == "canon":
            self.search_text = self.root.ids["keyword"].text
            self.add_line("canon")

        elif self.root.ids["keyword"].text == "tips":
            self.search_text = self.root.ids["keyword"].text
            self.add_line("tips")

        elif self.root.ids["keyword"].text == "tempo":
            self.search_text = self.root.ids["keyword"].text
            self.add_line("tempo")

        elif self.root.ids["keyword"].text == "all":
            self.search_text = self.root.ids["keyword"].text
            self.add_line("all")

        else:
            self.search_text = self.root.ids["keyword"].text
            self.add_line("classic")

        self.my_popup.dismiss()

    def add_line(self, keyword):
        """Add a new widget on List"""

        self.data_list.clear()
        self.start = 0
        self.end = 100

        if keyword == "canon":
            self.K_Word = keyword
            self.length = 100
            self.list_eps = np.array(self.Episodi_mib.copy())

            for eps in range(self.length):
                if f'{self.Description_mib[eps]}' == "nan":
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[eps]} - {self.list_eps[eps]}',
                         "secondary_text": f""})
                else:
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{self.Num_Eps_mib[eps]} - {self.list_eps[eps]}',
                         "secondary_text": f"[font=Colossalis Regular]{self.Description_mib[eps]}"})

            self.root.ids.match.data = self.data_list

        elif keyword == "tips":

            self.K_Word = keyword
            for text in self.text_tips:
                self.data_list.append({"text": f'[font=Colossalis Regular]{text}', "secondary_text": f""})

            self.root.ids.match.data.clear()
            self.root.ids.match.data = self.data_list

        elif keyword == "tempo":
            self.K_Word = keyword
            self.list_eps = []
            for chrono in self.tempo:
                for eps in range(self.Episodi.size):
                    if chrono in str(f"{self.Episodi[eps]}") or chrono in str(f"{self.Description[eps]}"):
                        if f'{self.Description[eps]}' == "nan":
                            self.list_eps.append(
                                str(f"{self.Num_Eps[eps]} - {self.Episodi[eps]}"))
                        else:
                            self.list_eps.append(
                                str(f"{self.Num_Eps[eps]} - {self.Episodi[eps]} {self.Description[eps]}"))

            self.list_eps = self.sorting(self.list_eps)
            for eps in self.list_eps:
                if f'{self.Description[eps - 1]}' == "nan":
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{eps} - {self.Episodi[eps - 1]}',
                         "secondary_text": f""})
                else:
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{eps} - {self.Episodi[eps - 1]}',
                         "secondary_text": f"[font=Colossalis Regular]{self.Description[eps - 1]}"})

            self.root.ids.match.data.clear()
            self.root.ids.match.data = self.data_list

        elif keyword == "all":
            self.K_Word = keyword
            self.length = 100
            self.list_eps = np.array(self.Episodi.copy())
            for eps in range(self.length):
                if f'{self.Description[eps]}' == "nan":
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{eps + 1} - {self.list_eps[eps]}',
                         "secondary_text": f""})
                else:
                    self.data_list.append(
                        {"text": f'[font=Colossalis Regular]{eps + 1} - {self.Episodi[eps]}',
                         "secondary_text": f"[font=Colossalis Regular]{self.Description[eps]}"})

            self.root.ids.match.data.clear()
            self.root.ids.match.data = self.data_list

        elif keyword == "classic":
            self.K_Word = keyword
            self.list_eps = [
                str(f"{self.Num_Eps[eps]} - {self.Episodi[eps]} {self.Description[eps]}").rsplit(" nan", 1)[0] for eps
                in
                range(self.Episodi.size)
                if
                str(self.search_text) in str(f"{self.Num_Eps[eps]} - {self.Episodi[eps]} {self.Description[eps]}")]

            if len(self.list_eps) >= 100:
                self.length = 100
            else:
                self.length = len(self.list_eps)

            if len(self.list_eps) == 0:
                self.data_list.append(
                    {"text": f"[font=Colossalis Regular]Non ho trovato corrispondenze",
                     "secondary_text": f""})
            else:
                for eps in range(self.length):
                    if len(self.list_eps[eps].rsplit('(')) > 1:
                        self.data_list.append(
                            {"text": f"[font=Colossalis Regular]{self.list_eps[eps].rsplit('(')[0]}",
                             "secondary_text": f"[font=Colossalis Regular]({self.list_eps[eps].rsplit('(')[1]}"})
                    else:
                        self.data_list.append(
                            {"text": f"[font=Colossalis Regular]{self.list_eps[eps].rsplit('(')[0]}",
                             "secondary_text": f""})

            self.root.ids.match.data.clear()
            self.root.ids.match.data = self.data_list

    @staticmethod
    def sorting(shuffle_array):
        """Sort my array"""

        sort_list = []
        shuffle_array_num = []

        for element in shuffle_array:
            shuffle_array_num.append(int(element.rsplit(" -", 1)[0]))

        low = shuffle_array_num[0]
        prev = low

        for num in range(0, len(shuffle_array_num)):

            if shuffle_array_num[num] in sort_list:
                pass
            elif shuffle_array_num[num] == low:
                sort_list.insert(0, shuffle_array_num[num])
            elif shuffle_array_num[num] < low:
                sort_list.insert(0, shuffle_array_num[num])
                low = shuffle_array_num[num]
            elif low < shuffle_array_num[num] < prev:
                count = 0
                for n in range(len(sort_list)):
                    if sort_list[n] < shuffle_array_num[num]:
                        pass
                    elif sort_list[n] > shuffle_array_num[num] and count == 0:
                        sort_list.insert(sort_list.index(sort_list[n]), shuffle_array_num[num])
                        count = 1
                    elif count == 1:
                        pass
            elif shuffle_array_num[num] > prev:
                sort_list.insert(len(sort_list), shuffle_array_num[num])
                prev = shuffle_array_num[num]

        shuffle_array_num.clear()
        shuffle_array.clear()
        return sort_list

    def cercanumber(self):
        """Find episode by number"""

        self.root.ids["onoff"].icon = "star-off"
        self.root.ids["brack"].icon = "code-parentheses"

        try:
            eps_to_find = int(self.root.ids["epsnumero"].text) - 1
        except ValueError:
            self.root.ids["rnd_window"].text = "Inserisci un episodio da cercare"
        else:
            if self.description:
                self.root.ids["brack"].icon = "code-parentheses"
                self.output_text = f"{self.Num_Eps[eps_to_find]} - {self.Episodi[eps_to_find]} {self.Description[eps_to_find]} "
                self.prev_episode = self.output_text
                if "(" in self.output_text:
                    self.root.ids["rnd_window"].text = self.output_text
                else:
                    self.root.ids["rnd_window"].text = self.output_text.split(" nan")[0]

            elif not self.description:
                self.root.ids["brack"].icon = "slash-forward"
                self.output_text = f"{self.Num_Eps[eps_to_find]} - {self.Episodi[eps_to_find]} {self.Description[eps_to_find]} "
                self.prev_episode = self.output_text
                self.root.ids["rnd_window"].text = self.output_text[:self.output_text.find(" (")]

    def show_popup(self):
        """Show Popup while loading"""

        self.my_popup.open()

    def tap_brackets(self):
        """Show info of the button"""

        self.tap_target_brack = MDTapTargetView(
            widget=self.root.ids.brack,
            title_text="[font=Colossalis Regular]Questo bottone rimuove",
            description_text="[font=Colossalis Regular]la descrizione",
            widget_position="right_bottom",
            cancelable=True,
            outer_radius=350,
            title_text_size=50,
            description_text_size=60,
            description_text_bold=True
        )

        if self.tap_target_brack.state == "close":
            self.tap_target_brack.start()
            self.info_star = False
        else:
            self.tap_target_brack.stop()

    def fileadd(self):
        """Save favourite episode in a txt file"""

        if self.root.ids["rnd_window"].text == "Premi il bottone per generare un episodio random":
            pass
        else:
            with open("preferiti.txt", "a+") as file:
                if self.root.ids["rnd_window"].text in file:
                    self.root.ids["onoff"].disabled = True
                elif self.root.ids["rnd_window"].text == "":
                    pass
                else:
                    file.write(f"[font=Colossalis Regular]{self.root.ids['rnd_window'].text}" + "\n")
                    self.root.ids["onoff"].icon = "star"

    def filerefresh(self):
        """Reload the screen to see previous added episode"""

        self.preferiti.clear()

        for episodi_star in reversed(self.root.ids.episodistar.children):
            self.root.ids.episodistar.remove_widget(episodi_star)
        with open("preferiti.txt", "rt") as file:
            for line in file:
                self.preferiti.append(f"{line}")
                self.root.ids.episodistar.add_widget(ListaPreferiti(text=f"{line}"))

    def remove_item_star(self, instance):
        """Remove a widget from MDCardSwipe"""

        self.root.ids.episodistar.remove_widget(instance)
        self.preferiti.remove(str(instance.text))
        with open("preferiti.txt", "w") as file:
            for line in self.preferiti:
                file.write(line)

    def edit_description(self):
        """Make custom description for each episode"""

        global can_edit
        global episode_to_edit

        if can_edit:
            for value in episode_to_edit.values():
                if len(str(value).split("[font=Colossalis Regular]")) > 1:
                    try:
                        self.row = int((value.split("]", 2)[1]).split()[0])
                    except Exception:
                        pass
                    for val in str(value).split("[font=Colossalis Regular]"):
                        if "(" in val:
                            if self.K_Word == "canon":
                                for i in range(len(self.couple_mib)):
                                    if (i, self.row) in self.couple_mib:
                                        self.row = i
                                        break
                                old_description = self.Description_mib.iat[self.row]
                                EditPopup(self.row, old_description, self.episode_mib).open()
                            else:
                                old_description = self.Description.iat[self.row - 1]
                                EditPopup(self.row, old_description, self.episode_file).open()
                else:
                    if self.K_Word == "canon":
                        EditPopup(self.row, "Non è presente nessuna descrizione ma puoi aggiungerla",
                                  self.episode_mib).open()
                    else:
                        EditPopup(self.row, "Non è presente nessuna descrizione ma puoi aggiungerla",
                                  self.episode_file).open()

        elif not can_edit:
            PencilPopup().open()

    def edit_csv(self, row, text, file):
        """Edit csv file"""

        if text == "":
            pass
        elif text == self.new_description:
            pass
        elif text != self.new_description:
            self.new_description = text

            if file.size == self.episode_mib.size:
                file.iat[row, 2] = "(" + self.new_description + ")"
                file.to_csv(f'nero.csv', index=False)
            elif file.size == self.episode_file.size:
                file.iat[row - 1, 2] = "(" + self.new_description + ")"
                file.to_csv(f'episodi.csv', index=False)

    def reload(self):

        global can_edit

        if can_edit:
            if self.root.ids["keyword"].text not in ("canon", "tempo", "all", "tips"):
                self.add_line("classic")
            elif self.root.ids["keyword"].text in ("canon", "tempo", "all", "tips"):
                self.add_line(self.root.ids["keyword"].text)
        elif not can_edit:
            pass


try:
    txt = open("preferiti.txt", "xt")
except FileExistsError:
    pass

ConanApp().run()
