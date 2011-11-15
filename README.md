#Inc-Dec-Value

## increase / decrease of numbers (integer and fractional), dates, hex color values, and logical (or any, predetermined, opposing values) on the configured value and a bonus - string actions (upper, lower, capitalize)

### Support Multiple Selections

![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_number.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_hex_color.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_opposite.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_float.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_dates.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_strings.gif)


Example of the correct values:
------------------------------

  * ### positive and negative integer numbers

    => ... -2, -1, 0, 1, 2, ...


  * ### positive and negative floating-point numbers

    => ... -1.1, -1.19, 0.119, 1.1119, 2.11119, ...

    If value is floating-point - increases/decreases applies from last position.
    for example 1.19 + `alt+up` = 1.20 and 1.11200 + `alt+down` = 1.11199


  * ### positive and negative (integer and floating-point) numbers and any text after them

    => 12px, -5em, 100%, 42sometext, (24), [12, -13], {77: -88}, 0.1em, 62.5%/1.5


  * ### hex colors

    => #123 #123456

    Pressing the key `alt+up/down` increases/decreases
    the one character to the left

    If the cursor between the '#' and the hex number in the #123
    the action applies to first character '1'

    Pressing the key `super+up/down` increases/decreases
    the total value of the hex color on +111/-111 or +111111/-111111


  * ### dates in ISO format `YYYY-MM-DD`

    => 2011-11-15

    The increase in year / month / day is its own, without checking the validity of the resulting date.

    For days, the value of loops between 1 and 31, for months - loops between 1 and 12.


  * ### opposite values

    => true/false, True/False, TRUE/FALSE, left/right

    Pressing the key `alt+up/down`
    changes the value under the cursor ("true" or "false") to the opposite


  * ### any string

    => string String STRING

    Pressing the key `alt+up` makes the first letter in the word in Uppercase (Capitalize).

    Pressing the key `super+up` makes the word in UPPERCASE.

    Pressing the key `alt+down` or `super+down` makes the word in lowercase.

    **Important !**
    There will be no change of words, which were applied different rules.
    For example, the opposite of the values "true" will not be given to upper case, as a rule is applied to modify this value to "false".


Not supported:
--------------

  * #### numbers in the text and after

    => qwe42asd, text42

  * #### incorrect hex colors

    => #1 #12 #1234 #12345 #1234567...


Default (Linux).sublime-keymap
--------------------------------------------------------------------------------

    [
        { "keys": ["alt+up"],  "command": "inc_dec_value", "args": { "delta": 1} },
        { "keys": ["alt+down"], "command": "inc_dec_value", "args": { "delta": -1} },
        { "keys": ["super+up"],  "command": "inc_dec_value", "args": { "delta": 10} },
        { "keys": ["super+down"], "command": "inc_dec_value", "args": { "delta": -10} }
    ]
