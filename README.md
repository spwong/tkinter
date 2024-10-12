# DatetimeEntry Widget

The `DatetimeEntry` widget is a custom widget that allows users to input and manipulate date and time values using individual entry fields for year, month, day, hour, minute, and second.

## Usage

To use the `DatetimeEntry` widget, follow these steps:

1. Import the necessary modules:
2. Create an instance of the `DatetimeEntry` widget:
3. Access the selected date and time using the `textvariable`:
## API

### `DatetimeEntry` Class

#### `__init__(self, master=None, textvariable=None, style=None, **kwargs)`

Initialize the `DatetimeEntry` widget.

- `master` (tk.Widget, optional): The parent widget.
- `textvariable` (tk.Variable, optional): The variable to store the datetime value.
- `style` (str, optional): The style to apply to the widget.
- `**kwargs`: Additional keyword arguments for the `ttk.Frame`.

#### `set_datetime(self, year, month, day, hour=0, minute=0, second=0)`

Set the datetime values in the entry fields.

- `year` (int): The year.
- `month` (int): The month.
- `day` (int): The day.
- `hour` (int, optional): The hour. Defaults to 0.
- `minute` (int, optional): The minute. Defaults to 0.
- `second` (int, optional): The second. Defaults to 0.

#### `get_datetime(self)`

Get the datetime values from the entry fields.

Returns:
- `str`: The datetime string in the format "YYYY-MM-DD HH:MM:SS".

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
