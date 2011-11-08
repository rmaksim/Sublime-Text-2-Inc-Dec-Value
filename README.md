inc_dec_number.py
=======================================

## Increase/Decrease number by delta_value

### Support Multiple Selections

![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Solutions/raw/master/inc_dec_number.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Solutions/raw/master/inc_dec_hex_color.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Solutions/raw/master/inc_dec_opposite.gif)
![blame screenshot](https://github.com/rmaksim/Sublime-Text-2-Solutions/raw/master/inc_dec_float.gif)


Example of the correct values:
------------------------------

  * positive and negative integer numbers

    => ... -2, -1, 0, 1, 2, ...

  * positive and negative floating-point numbers

    => ... -1.1, -1.19, 0.119, 1.1119, 2.11119, ...

  * positive and negative (integer and floating-point) numbers and any text after them

    => 12px, -5em, 100%, 42sometext, (24), [12, -13], {77: -88}, 0.1em, 62.5%/1.5

  * hex colors

    => #123 #123456

  * opposite values

    => true/false, True/False, TRUE/FALSE, left/right


Pressing the key `alt+up/down` increases/decreases
the one character to the left

If value is floating-point - increases/decreases applies from last position.
for example 1.19 + `alt+up` = 1.20 and 1.11200 + `alt+down` = 1.11199

If the cursor between the '#' and the hex number in the #123
- the action applies to first character '1'

Pressing the key `super+up/down` increases/decreases
the total value of the hex color on +111/-111 or +111111/-111111

Pressing the key `alt+up/down`
changes the value under the cursor ("true" or "false") to the opposite


Not supported:
--------------

  * numbers in the text and after

    => qwe42asd, text42

  * incorrect hex colors

    => #1 #12 #1234 #12345 #1234567...


Default (Linux).sublime-keymap
--------------------------------------------------------------------------------

    [
        { "keys": ["alt+up"],  "command": "inc_dec_number", "args": { "delta": 1} },
        { "keys": ["alt+down"], "command": "inc_dec_number", "args": { "delta": -1} },
        { "keys": ["super+up"],  "command": "inc_dec_number", "args": { "delta": 10} },
        { "keys": ["super+down"], "command": "inc_dec_number", "args": { "delta": -10} }
    ]
