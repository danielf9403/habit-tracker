from datetime import date
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
# from kivymd.uix.picker import MDDatePickerDialog
from kivymd.app import MDApp
import psycopg2
from kivymd.uix.pickers import MDTimePicker


KV = '''
MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

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
                        on_release: app.show_date_picker()

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


class HabitApp(MDApp):
    habits = []  # List to store the habits

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def show_date_picker(self):
        date_dialog = MDTimePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
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

            # Save the habit in the list with the selected date
            habit = {
                'name': habit_text,
                'start_date': value.strftime("%Y-%m-%d"),
            }
            self.habits.append(habit)

            # Insert the habit into the database
            insert_habit(habit_text, value)

            Snackbar(text=f"Habit '{habit_text}' added with start date: {value}").show()

    def save_habits(self):
        # Save the habits to a file or database
        with open("habits.txt", "w") as file:
            for habit in self.habits:
                file.write(f"{habit['name']},{habit['start_date']}\n")


def insert_habit(habit_name, start_date):
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="habit tracker",
        user="postgres",
        password="postgres"
    )
    cursor = connection.cursor()

    # Check if the 'habits' table exists
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'habits')")
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # Create the table if it doesn't exist
        create_table_sql = """
        CREATE TABLE habits (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            start_date DATE
        )
        """
        cursor.execute(create_table_sql)
        connection.commit()

    sql = "INSERT INTO habits (name, start_date) VALUES (%s, %s)"
    values = (habit_name, start_date)
    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    HabitApp().run()
