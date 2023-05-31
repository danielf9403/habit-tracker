from datetime import datetime
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App
import psycopg2
from tkinter import *
from tkcalendar import Calendar

KV = '''
BoxLayout:
    orientation: "vertical"
    padding: dp(16)

    Label:
        text: "Track Your Habits"
        color: app.theme_cls.secondary_text_color
        halign: "center"
        font_size: "20sp"
        size_hint_y: None
        height: self.texture_size[1]

    TextInput:
        id: habit_input
        hint_text: "Enter a habit"
        size_hint: None, None
        width: dp(200)
        pos_hint: {"center_x": 0.5}
        multiline: False

    Button:
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


class HabitApp(App):
    habits = []  # List to store the habits

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def show_date_picker(self):
        habit_text = self.root.ids.habit_input.text.strip()
        if habit_text:
            # Create a popup with the tkinter calendar
            popup = Popup(title='Select Start Date', size_hint=(None, None), size=(400, 400))
            frame = Frame(popup.content)
            frame.pack()
            cal = Calendar(frame, selectmode='day')
            cal.pack(pady=20)
            button = Button(frame, text='Select Date', on_release=lambda dt: self.on_date_save(popup, cal, habit_text))
            button.pack(pady=20)
            popup.open()

    def on_date_save(self, popup, cal, habit_text):
        date = cal.get_date()
        if date:
            habit_label = Label(
                text=habit_text,
                color=(0, 0, 1, 1),
                size_hint_y=None,
                height=dp(40),
                valign="center",
                font_size="16sp",
            )
            self.root.ids.habit_grid.add_widget(habit_label)
            self.root.ids.habit_input.text = ""

            # Save the habit in the list with the selected date
            habit = {
                'name': habit_text,
                'start_date': date.strftime("%Y-%m-%d"),
            }
            self.habits.append(habit)

            # Insert the habit into the database
            insert_habit(habit_text, date)

        popup.dismiss()

    def save_habits(self):
        # Save the habits to a file or database
        with open("habits.txt", "w") as file:
            for habit in self.habits:
                file.write(f"{habit['name']},{habit['start_date']}\n")


def insert_habit(habit_name, start_date):
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="habit_tracker",
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
