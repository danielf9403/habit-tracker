from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

KV = '''
MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Habit Tracker"
                    elevation: 4
                    pos_hint: {"top": 1}
                    md_bg_color: "#e7e4c0"
                    specific_text_color: "#4a4939"
                    left_action_items:
                        [['menu', lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: "vertical"
                    padding: dp(16)

                    MDLabel:
                        text: "Track Your Habits"
                        theme_text_color: "Secondary"
                        halign: "center"
                        font_style: "H4"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDTextField:
                        id: habit_input
                        hint_text: "Enter a habit"
                        size_hint: None, None
                        width: dp(200)
                        pos_hint: {"center_x": 0.5}
                        multiline: False

                    MDFlatButton:
                        text: "Add Habit"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.add_habit()

                    ScrollView:
                        GridLayout:
                            id: habit_grid
                            cols: 1
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(8)
                            padding: dp(8)
'''




class ContentNavigationDrawer(MDBoxLayout):
    pass


class Example(MDApp):
    habit_counter = 1  # To assign unique IDs to habits

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def add_habit(self):
        habit_text = self.root.ids.habit_input.text.strip()
        if habit_text:
            habit_label = MDLabel(
                text=habit_text,
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(40),
                valign="center",
                font_style="Subtitle1",
            )
            self.root.ids.habit_grid.add_widget(habit_label)
            self.root.ids.habit_input.text = ""
            self.habit_counter += 1


Example().run()

