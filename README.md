#Inc-Dec-Value

**v0.1.1**

---
## increase / decrease of numbers (integer and fractional), dates, hex color values, opposite relations or cycled enumerations on the configured value and a bonus - string actions (upper, lower, capitalize)

**Forum Thread**
http://www.sublimetext.com/forum/viewtopic.php?f=5&t=2395

### Support Multiple Selections
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_number.gif)
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_hex_color.gif)
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_opposite.gif)
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_float.gif)
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_dates.gif)
![Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/raw/master/inc_dec_strings.gif)


### Example of the correct values:
  * **positive and negative integer numbers**

    => ... -2, -1, 0, 1, 2, ...


  * **positive and negative floating-point numbers**

    => ... -1.1, -1.19, 0.119, 1.1119, 2.11119, ...

    If value is floating-point - increases/decreases applies from last position.
    for example 1.19 + `alt+up` = 1.20 and 1.11200 + `alt+down` = 1.11199


  * **positive and negative (integer and floating-point) numbers and any text after them**

    => 12px, -5em, 100%, 42sometext, (24), [12, -13], {77: -88}, 0.1em, 62.5%/1.5


  * **hex colors**

    => #f01 #f00456

    Pressing the key `alt+up/down` increases/decreases
    the one character to the left on +1/-1 (regardless of the settings)

    If the cursor between the '#' and the hex number in the #f01
    the action applies to first character 'f'

    Pressing the key `super+up/down` increases/decreases
    the total value of the hex color on +111/-111 or +111111/-111111
    (regardless of the settings)


  * **dates in ISO format `YYYY-MM-DD`**

    => 2011-11-15

    The increase in year / month / day is its own,
    without checking the validity of the resulting date.

    For days, the value of loops between 1 and 31,
    for months - loops between 1 and 12.


  * **opposite relations or cycled enumerations**

    => `true > false, True > False, FALSE > TRUE, left > right`

    also

    => `truE > false, tRUe > false, FaLsE > true, LeFT > right`

    Pressing the key `super+alt+up/down`
    changes the value under the cursor ("true" or "false") to the opposite

    Version 0.1.0 adds the ability to cycle more than two values:

    => "Jan" > "Feb" > "Mar" > ... > "Dec" > "Jan"

    Example of settings see in
    <a href="https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/blob/master/inc_dec_value.sublime-settings">inc\_dec\_value.sublime-settings</a>


  * **any string**

    => string String STRING

    Pressing the key `alt+up` makes the first letter in the word in Uppercase (Capitalize) without affecting the remaining characters.

    Pressing the key `super+up` makes the word in UPPERCASE.

    Pressing the key `alt+down` or `super+down` makes the word in lowercase.

    **Important !**
    There will be no change of words, which were applied different rules.
    For example, the integer "12px"
    will not be given "px" to upper case,
    as a rule is applied to modify this value to "13px".


### Not supported:
  * **numbers in the text and after**

    => qwe42asd, text42

  * **incorrect hex colors**

    => #1 #12 #1234 #12345 #1234567...

  * **and may be something else that would like to see...**

    *let me know if you find an error*

    *or you will have new ideas*


### [inc_dec_value.sublime-settings](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/blob/master/inc_dec_value.sublime-settings)
    {
        "file": "inc_dec_value.sublime-settings"

    ,   "action_inc_min":    1  // default:   1,  key: Alt + Up
    ,   "action_dec_min":   -1  // default:  -1,  key: Alt + Down

    ,   "action_inc_max":   10  // default:  10,  key: Super + Up
    ,   "action_dec_max":  -10  // default: -10,  key: Super + Down

    ,   "action_inc_all":  100  // default:  10,  key: Super + Alt + Up
    ,   "action_dec_all": -100  // default: -10,  key: Super + Alt + Down

    ,   "enums": [ // write values to the list only in lowercase
            ["yes", "no"]
        ,   ["true", "false"]
        ,   ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        ]

    ,   "force_use_upper_case_for_hex_color": false
    }


### Default (Linux).sublime-keymap
    [
        { "keys": ["alt+up"],         "command": "inc_dec_value", "args": { "action": "inc_min" } },
        { "keys": ["alt+down"],       "command": "inc_dec_value", "args": { "action": "dec_min" } },

        { "keys": ["super+up"],       "command": "inc_dec_value", "args": { "action": "inc_max" } },
        { "keys": ["super+down"],     "command": "inc_dec_value", "args": { "action": "dec_max" } },

        { "keys": ["super+alt+up"],   "command": "inc_dec_value", "args": { "action": "inc_all" } },
        { "keys": ["super+alt+down"], "command": "inc_dec_value", "args": { "action": "dec_all" } }
    ]


### Copyright

**Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>**

Minor contrib by

  * Denis Ryzhkov <denis@ryzhkov.org>
  * Vitaly Pikulik <v.pikulik@gmail.com>
  * Alexandra Ignatyeva <e.xelga@gmail.com>

MIT License, see http://opensource.org/licenses/MIT
