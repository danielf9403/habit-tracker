from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from datetime import date
import sqlite3


class CalendarApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Habit Tracker'
        self.conn = sqlite3.connect('habits.db')
        self.create_table()
        self.habit_list = []

    def build(self):
        layout = BoxLayout(orientation='horizontal', spacing=10)
        layout.padding = 10
        self.calendar_layout = GridLayout(cols=7, spacing=10, size_hint=(0.7, 1))
        self.habit_list_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.3, 1))
        layout.add_widget(self.calendar_layout)
        layout.add_widget(self.habit_list_layout)

        # Set the background color
        with layout.canvas.before:
            Window.size = (400, 400)  # Set the initial window size
            layout.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
            layout.bg_color = get_color_from_hex('#FFFFFF')

        layout.bind(pos=self.update_background_rect, size=self.update_background_rect)
        self.update_calendar()
        self.load_habits()

        return layout

    def update_background_rect(self, instance, value):
        instance.bg_rect.size = instance.size
        instance.bg_rect.pos = instance.pos

    def get_month_year(self):
        today = date.today()
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        return month_names[today.month - 1] + ' ' + str(today.year)

    def update_calendar(self):
        today = date.today()
        first_day = date(today.year, today.month, 1)
        days_in_month = 31

        # Clear the previous calendar layout
        self.calendar_layout.clear_widgets()

        # Create buttons for each day of the month
        for i in range(days_in_month):
            day_button = Button(text=str(i + 1), on_press=self.on_day_select)

            # Highlight the current day
            if i + 1 == today.day:
                day_button.background_color = (0.5, 0.5, 1, 1)

            self.calendar_layout.add_widget(day_button)

    def on_day_select(self, instance):
        selected_day = int(instance.text)
        print("Selected day:", selected_day)
        instance.background_color = (1, 0.5, 0.5, 1)  # Change background color on selection

        # Save the date and habit to the database
        habit_date = date.today().replace(day=selected_day)
        habit_input = TextInput(text="New Habit", multiline=False)

        # Create a layout for the habit input popup
        habit_input_layout = BoxLayout(orientation='vertical')
        habit_input_layout.add_widget(Label(text="Habit Name"))
        habit_input_layout.add_widget(habit_input)

        # Create a popup to enter the habit name
        popup = Popup(title='Add Habit', content=habit_input_layout, size_hint=(0.6, 0.4))
        popup.open()

        def save_habit(instance):
            habit = habit_input.text
            self.save_habit(habit_date, habit)
            print("Added habit:", habit)
            popup.dismiss()

        save_button = Button(text="Save", size_hint=(1, None), height=40)
        save_button.bind(on_press=save_habit)
        habit_input_layout.add_widget(save_button)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_date DATE,
                habit TEXT
            );
        """)
        self.conn.commit()
        cursor.close()

    def save_habit(self, habit_date, habit):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO habits (habit_date, habit)
            VALUES (?, ?);
        """, (habit_date, habit))
        self.conn.commit()
        cursor.close()

        # Reload the habit list
        self.load_habits()

    def load_habits(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM habits")
        self.habit_list = cursor.fetchall()
        cursor.close()

        # Clear the habit list layout
        self.habit_list_layout.clear_widgets()

        # Display the habit list in the sidebar
        for habit in self.habit_list:
            habit_text = f"{habit[1]}: {habit[2]}"
            self.habit_list_layout.add_widget(Label(text=habit_text))

    def on_stop(self):
        self.conn.close()


if __name__ == '__main__':
    CalendarApp().run()
