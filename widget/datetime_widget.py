from tkinter import ttk
from datetime import datetime
import tkinter as tk


class DatetimeVar(tk.Variable):
    """Value holder for datetime variables."""
    _default = None

    def __init__(self, master=None, value=None, name=None):
        """
        Initialize the DatetimeVar.

        Args:
            master (tk.Widget): The parent widget.
            value (datetime, optional): The initial value.
            name (str, optional): The name of the variable.
        """
        tk.Variable.__init__(self, master, value, name)

    def set(self, value):
        """
        Set the variable to VALUE.

        Args:
            value (datetime or str): The value to set. If a datetime object is provided, it will be converted to an ISO format string.
        """
        if isinstance(value, datetime):
            value = value.isoformat()
        return self._tk.globalsetvar(self._name, value)

    initialize = set

    def get(self):
        """
        Return the value of the variable as a datetime.

        Returns:
            datetime: The value of the variable as a datetime object.
        """
        value = self._tk.globalgetvar(self._name)
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("invalid literal for datetime")


class DatetimeEntry(ttk.Frame):
    """
    DatetimeEntry is a custom widget that allows users to input and manipulate date and time values using individual entry fields for year, month, day, hour, minute, and second.
    Attributes:
        textvariable (tk.Variable): The variable to store the datetime value.
        default_values (dict): Default values for year, month, day, hour, minute, and second.
        entries (dict): Entry widgets for year, month, day, hour, minute, and second.
    Methods:
        __init__(self, master=None, textvariable=None, style=None, **kwargs):
        set_datetime(self, year, month, day, hour=0, minute=0, second=0):
        get_datetime(self):
    """
    def __init__(self, master=None, textvariable=None, style=None, **kwargs):
        """
        Initialize the DatetimeEntry widget.

        Args:
            master (tk.Widget, optional): The parent widget.
            textvariable (tk.Variable, optional): The variable to store the datetime value.
            style (str, optional): The style to apply to the widget.
            **kwargs: Additional keyword arguments for the ttk.Frame.
        """
        super().__init__(master, style=style, **kwargs)
        self.textvariable = textvariable

        # Get today's date and time
        now = datetime.now()
        self.default_values = {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': '00',
            'second': '00'
        }

        # Validation command to ensure only digits are entered and within valid ranges
        vcmd = (self.register(self.validate_digit), '%P', '%W')

        # Creating Entry widgets for year, month, day, hour, minute, and second
        self.entries = {
            'year': ttk.Entry(
                self, width=5, validate='key', validatecommand=vcmd,
                style=style),
            'month': ttk.Entry(
                self, width=3, validate='key', validatecommand=vcmd,
                style=style),
            'day': ttk.Entry(
                self, width=3, validate='key', validatecommand=vcmd,
                style=style),
            'hour': ttk.Entry(
                self, width=3, validate='key', validatecommand=vcmd,
                style=style),
            'minute': ttk.Entry(
                self, width=3, validate='key', validatecommand=vcmd,
                style=style),
            'second': ttk.Entry(
                self, width=3, validate='key', validatecommand=vcmd,
                style=style)
        }

        # Setting default values to current date and time
        self.set_datetime(**self.default_values)

        # Placing the Entry widgets in the window
        self.entries['year'].pack(
            side="left", padx=0, pady=0, anchor='w', fill='y')
        ttk.Label(self, text="-").pack(side="left", anchor='w')
        self.entries['month'].pack(
            side="left", padx=0, pady=0, anchor='w', fill='y')
        ttk.Label(self, text="-").pack(side="left", anchor='w')
        self.entries['day'].pack(
            side="left", padx=0, pady=0, anchor='w', fill='y')
        ttk.Label(self, text=" ").pack(side="left", anchor='w')
        self.entries['hour'].pack(
            side="left", padx=(10, 0), pady=0, anchor='w', fill='y')
        ttk.Label(self, text=":").pack(side="left", anchor='w')
        self.entries['minute'].pack(
            side="left", padx=0, pady=0, anchor='w', fill='y')
        ttk.Label(self, text=":").pack_forget() #.pack(side="left", anchor='w')
        self.entries['second'].pack_forget()
        # self.entries['second'].pack(
        #     side="left", padx=(0, 10), pady=0, anchor='w', fill='y')

        if self.textvariable:
            self.textvariable.trace_add("write", self.update_entries)

        # Add traces to month and year entries to revalidate the day entry
        self.entries['month'].bind("<FocusOut>", self.revalidate_day)
        self.entries['year'].bind("<FocusOut>", self.revalidate_day)

        # Bind arrow keys to increment and decrement functions
        self.bind_arrow_keys()

        # Add traces to entry fields to update textvariable
        for entry in self.entries.values():
            entry.bind("<FocusOut>", self.on_entry_change)
            entry.bind("<Return>", self.on_entry_change)

    def bind_arrow_keys(self):
        """Bind the up and down arrow keys to increment and decrement functions."""
        for key in ['year', 'month', 'day', 'hour', 'minute', 'second']:
            self.entries[key].bind("<Up>", lambda event, k=key: self.increment(k, 1))
            self.entries[key].bind("<Down>", lambda event, k=key: self.increment(k, -1))

    def increment(self, key, step):
        """
        Increment or decrement the value in the entry widget.

        Args:
            key (str): The key of the entry to increment or decrement.
            step (int): The step value to increment or decrement by.
        """
        entry = self.entries[key]
        value = entry.get()
        if value.isdigit():
            value = int(value) + step
            min_value, max_value = self.get_min_max_values(key)
            value = max(min_value, min(value, max_value))
            entry.delete(0, "end")
            entry.insert(0, str(value).zfill(2))

    def get_min_max_values(self, key):
        """
        Get the minimum and maximum values for the given key.

        Args:
            key (str): The key to get the min and max values for.

        Returns:
            tuple: The minimum and maximum values.
        """
        if key == 'hour':
            return 0, 23
        elif key in ['minute', 'second']:
            return 0, 59
        elif key == 'month':
            return 1, 12
        elif key == 'day':
            month = int(self.entries['month'].get() or 1)
            year = int(self.entries['year'].get() or 1)
            return 1, self.days_in_month(month, year)
        return 1, 9999  # Ensure year is at least 1

    def validate_digit(self, P, W):
        """
        Validate that the input contains only digits and is within valid ranges.

        Args:
            P (str): The value to validate.
            W (str): The widget name.

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if P.isdigit() or P == "":
            for key, entry in self.entries.items():
                if W == str(entry):
                    min_value, max_value = self.get_min_max_values(key)
                    return P == "" or min_value <= int(P) <= max_value
        return False

    def days_in_month(self, month, year):
        """
        Return the number of days in the given month and year.

        Args:
            month (int): The month.
            year (int): The year.

        Returns:
            int: The number of days in the month.
        """
        if month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            else:
                return 28
        else:
            return 31

    def revalidate_day(self, event=None):
        """
        Revalidate the day entry based on the current month and year.

        Args:
            event (tk.Event, optional): The event that triggered the revalidation.
        """
        day = self.entries['day'].get()
        if day.isdigit():
            day = int(day)
            month = int(self.entries['month'].get() or 1)
            year = int(self.entries['year'].get() or 1)
            max_day = self.days_in_month(month, year)
            if day > max_day:
                self.entries['day'].delete(0, "end")
                self.entries['day'].insert(0, str(max_day).zfill(2))

    def on_entry_change(self, event=None):
        """
        Update the textvariable when an entry field changes.

        Args:
            event (tk.Event, optional): The event that triggered the change.
        """
        try:
            # Correct invalid values
            for key in ['hour', 'minute', 'second']:
                value = self.entries[key].get()
                if value.isdigit() and int(value) > 59:
                    self.entries[key].delete(0, "end")
                    self.entries[key].insert(0, "59")
                elif value.isdigit() and len(value) > 2:
                    self.entries[key].delete(0, "end")
                    self.entries[key].insert(0, value[-2:].zfill(2))

            date_str = (
                f"{self.entries['year'].get()}-{self.entries['month'].get().zfill(2)}-"
                f"{self.entries['day'].get().zfill(2)} {self.entries['hour'].get().zfill(2)}:"
                f"{self.entries['minute'].get().zfill(2)}:{self.entries['second'].get().zfill(2)}"
            )
            if self.textvariable:
                self.textvariable.set(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            pass  # Handle invalid date format if necessary

    def set_datetime(self, year, month, day, hour=0, minute=0, second=0):
        """
        Set the datetime values in the entry fields.

        Args:
            year (int): The year.
            month (int): The month.
            day (int): The day.
            hour (int, optional): The hour. Defaults to 0.
            minute (int, optional): The minute. Defaults to 0.
            second (int, optional): The second. Defaults to 0.
        """
        for key, value in {
            'year': year, 'month': month, 'day': day, 'hour': hour,
            'minute': minute, 'second': second
        }.items():
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, str(value).zfill(2))

        # Update the textvariable if it exists
        if self.textvariable:
            date_str = (
                f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)} "
                f"{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}"
            )
            self.textvariable.set(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))

    def get_datetime(self):
        """
        Get the datetime values from the entry fields.

        Returns:
            str: The datetime string in the format "YYYY-MM-DD HH:MM:SS".
        """
        return (
            f"{self.entries['year'].get()}-{self.entries['month'].get().zfill(2)}-"
            f"{self.entries['day'].get().zfill(2)} {self.entries['hour'].get().zfill(2)}:"
            f"{self.entries['minute'].get().zfill(2)}:{self.entries['second'].get().zfill(2)}"
        )

    def update_entries(self, *args):
        """
        Update the entry fields based on the textvariable value.

        Args:
            *args: Additional arguments.
        """
        date = self.textvariable.get()
        self.set_datetime(
            date.year, date.month, date.day, date.hour, date.minute,
            date.second
        )


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Datetime Entry Test")

    datetime_var = DatetimeVar()
    datetime_entry = DatetimeEntry(root, textvariable=datetime_var)
    datetime_entry.pack(padx=10, pady=10)

    def show_datetime():
        print("Selected datetime:", datetime_var.get())

    show_button = ttk.Button(root, text="Show Datetime", command=show_datetime)
    show_button.pack(pady=10)

    root.mainloop()