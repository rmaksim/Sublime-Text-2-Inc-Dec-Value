#Inc-Dec-Value

**v0.1.21** - [#40](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/40) enums: fixed for values with few "-" and with "(" ")"

**v0.1.20** - [#41](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/41) Insert cutting preceding characters

**v0.1.19** - [#30](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/30) cursor duplicates...

**v0.1.18** - [#33](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/33) added settings for RGB instead RGBA

**v0.1.17** - [#34](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/34) space after comma in rgba

**v0.1.16** - [#32](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/32) convert from rgba() to short notation if its possible

**v0.1.15** - convert from rgba(x,x,x,1): remove /* alpha: 1 */ if alpha == 1

**v0.1.14** - [#37](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/pull/37) New Feature & Bug Fixes

**v0.1.13** - [#35](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/35) Cycle through enum with Java capitalization

**v0.1.12** - [#27](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/27) Ability to autosave after incrementing

**v0.1.11** - [#31](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/31) ST3: Getting TypeError in console when using the number inc/dec functions

**v0.1.10** - [#31](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/31) ST3: Getting TypeError in console when using the number inc/dec functions

**v0.1.9** - Fixed apply_integer (x -> -x when cursor before x)

**v0.1.8** - [#29](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/pull/29) Fix apply_hex_color exception

**v0.1.7** - [#19](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/19) Swapping the color notation in CSS

**v0.1.6** - [#20](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/20) (upper, lower, capitalize) works on non-ascii strings

**v0.1.5** - [#15](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/issues/15) Don't place action in undo history when nothing happens

**v0.1.4** - [#14](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/pull/14) Saving the position of the cursors/selections on the change

**v0.1.3** - added support for the mouse wheel

---
## increase / decrease of numbers (integer and fractional), dates, hex color values, opposite relations or cycled enumerations on the configured value and a bonus - string actions (upper, lower, capitalize)

Instead of the arrows can use your mouse wheel.

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

    Pressing the key `super+up/down`(Linux) or `super+alt+up/down`(Windows & OSX)
    increases/decreases
    the total value of the hex color on +111/-111 or +111111/-111111
    (regardless of the settings)

    Pressing the key `super+alt+up/down`(Linux) or `super+ctrl+up/down`(Windows) or `super+alt+ctrl+up/down`(OSX)
    swapping the color notation in CSS:

    from:

        color: rgba(0, 17, 34, 0.4);

    to:

        color: #012; /* alpha: 0.4 */

    again:

        color: rgba(0, 17, 34, 0.4);


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

    Pressing the key `super+alt+up/down`(Linux) or `super+ctrl+up/down`(Windows) or `super+alt+ctrl+up/down`(OSX)
    changes the value under the cursor ("true" or "false") to the opposite

    Version 0.1.0 adds the ability to cycle more than two values:

    => "Jan" > "Feb" > "Mar" > ... > "Dec" > "Jan"

    Version 0.1.13 adds the ability to cycle through enum with Java capitalization

    => "centerX" > "centerY", "screenLeft" > "screenRight"

    Version 0.1.21 fixed for values with few "-" and with "(" ")"

    => "last-child" > "last-of-type" > "nth-child()"

    Example of settings see in
    <a href="https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value/blob/master/inc_dec_value.sublime-settings">inc\_dec\_value.sublime-settings</a>


  * **any string**

    => string String STRING

    Pressing the key `alt+up` makes the first letter in the word in Uppercase (Capitalize) without affecting the remaining characters.

    Pressing the key `super+up`(Linux) or `super+alt+up`(Windows & OSX) makes the word in UPPERCASE.

    Pressing the key `alt+down` or `super+down`(Linux) or `super+alt+down`(Windows & OSX) makes the word in lowercase.

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
        ,   ["block", "none", "inline", "inline-block"]
        ,   ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        ]

    ,   "force_use_upper_case_for_hex_color": false
    ,   "autosave": false
    ,   "space_after_comma_in_rgba": true
    ,   "RGB_instead_RGBA": false
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
