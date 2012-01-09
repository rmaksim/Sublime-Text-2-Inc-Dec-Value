'''
Inc-Dec-Value v0.1.1

Increase / Decrease of
    - numbers (integer and fractional),
    - dates in ISO format `YYYY-MM-DD` (months from 1 to 12, days from 1 to 31),
    - hex color values (#fff or #ffffff),
    - opposite relations or cycled enumerations (`true`->`false`, `Jan`->`Feb`->`Mar`...),
    on the configured value
    and a bonus
    - string actions (UPPER, lower, Capitalize)

https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value

Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>

Minor contrib by
    Denis Ryzhkov <denis@ryzhkov.org>
    Vitaly Pikulik <v.pikulik@gmail.com>

MIT License, see http://opensource.org/licenses/MIT
'''

import sublime, sublime_plugin, re, string

class IncDecValueCommand(sublime_plugin.TextCommand):

    def run(self, edit, action):

        self.edit = edit
        self.action = action

        self.load_settings()
        self.delta = self.settings.get("action_" + action)

        for region in self.view.sel():

            self.region = region
            self.word_reg = self.view.word(region)

            if not self.word_reg.empty():
                (
                    self.apply_date()               or
                    self.apply_hex_color()          or
                    self.apply_floating_point()     or
                    self.apply_integer()            or
                    self.apply_enums()              or
                    self.apply_string()
                )


    def load_settings(self):
        """Load settings from file or set defaults

        default settings - see below `defaults`
        package settings - ${packages}/Inc-Dec-Value/inc_dec_value.sublime-settings
        user    settings - ${packages}/User/inc_dec_value.sublime-settings

        if the file `inc_dec_value.sublime-settings` does not exist
        - accept the default settings.
        """

        defaults = {
            "action_inc_min":    1,
            "action_dec_min":   -1,
            "action_inc_max":   10,
            "action_dec_max":  -10,
            "action_inc_all":  100,
            "action_dec_all": -100,
            "enums": [],
            "force_use_upper_case_for_hex_color": False
        }
        self.settings = {}
        settings = sublime.load_settings(__name__ + '.sublime-settings')

        for setting in defaults:
            self.settings[setting] = settings.get(setting, defaults.get(setting))


    def apply_date(self):
        """any date in ISO 8603 format, "YYYY-MM-DD", ex: 2011-12-31"""

        word = self.get_word()

        re_date = re.compile('([\d]{4}-[\d]{2}-[\d]{2})$')

        if re.match('([\d]{4})$', word): # check year
            date = self.get_word(self.word_reg.begin(), self.word_reg.begin() + 10)

            if re_date.match(date): # date is valid -> year
                # process with apply_integer
                return False

        elif re.match('([\d]{2})$', word): # check month or day:
            date = self.get_word(self.word_reg.begin() - 5, self.word_reg.begin() + 5)

            if re_date.match(date): # date is valid -> month
                self.replace(self.cycle(word, 12, self.delta))

                return True

            else: # check day
                date = self.get_word(self.word_reg.begin() - 8, self.word_reg.begin() + 2)

                if re_date.match(date): # date is valid -> day
                    self.replace(self.cycle(word, 31, self.delta))

                    return True


    def cycle(self, word, max, delta):
        """cycle `word` between 1 and `max` value when adding `delta`"""

        return '%02d' % ((int(word) + max - 1 + delta) % max + 1)


    def apply_hex_color(self):
        """any hex color, ex: #ee77ee; #f12; #f0e"""

        word = self.get_word()

        re_hex_color = re.compile('([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$')
        match = re_hex_color.match(word)

        prev = self.prev()

        if match and prev['sym'] == "#":

            tmp_reg = self.word_reg

            # applies for one of hex numbers
            if self.action in ["inc_min", "dec_min"]:
                # take the symbol to the left
                # if the cursor between '#' and the number - move it to the right
                if tmp_reg.begin() == self.region.begin():
                    tmp_reg = sublime.Region(tmp_reg.begin(), self.region.end() + 1)
                else:
                    tmp_reg = sublime.Region(self.region.begin() - 1, self.region.end())

                re_hex = re.compile('([0-9a-fA-F])')

            else: # self.action in ["inc_max", "dec_max"]
                re_hex = re_hex_color

            word = self.get_word(tmp_reg)
            match = re_hex.match(word)

            if match:
                delta = 1 if self.delta > 0 else -1
                new_word = ""
                for char in word:
                    char = hex(int(char, 16) + delta & 0xf)[2:]
                    new_word += char

                if self.settings.get("force_use_upper_case_for_hex_color"):
                    new_word = new_word.upper()

                self.replace(new_word, tmp_reg)

                return True


    def apply_floating_point(self):
        """any number of floating point, ex: 2.3mm or -0.27m"""

        prev = self.prev()

        # floating-point numbers
        if prev['sym'] == ".":
            while True:
                prev = self.prev(prev['pos'] - 1)
                if not re.match('(\d)', prev['sym']):
                    break

            if prev['sym'] != "-":
                prev = self.prev(prev['pos'] + 1)

            tmp_reg = sublime.Region(prev['pos'], self.word_reg.end())
            word = self.get_word(tmp_reg)
            match = re.match('(-*\d+\.(\d+))([a-zA-Z%]+)?$', word)

            if match:
                float_len = len(match.group(2))
                result = float(match.group(1)) + float(self.delta) / (10 ** float_len)
                match3 = match.group(3) if match.group(3) else ""
                self.replace(('%%0.%sf' % float_len) % result + match3, tmp_reg)

                return True


    def apply_integer(self):
        """any integer, ex: -12 123px; 123% 1em;"""

        prev = self.prev()

        tmp_reg = self.word_reg
        if prev['sym'] == "-":
            tmp_reg = sublime.Region(prev['pos'], self.word_reg.end())

        word = self.get_word(tmp_reg)
        match = re.match('(-*[0-9]+)([a-zA-Z%]+)?$', word)

        if match:
            result = int(match.group(1)) + self.delta
            match2 = match.group(2) or ""
            self.replace(str(result) + match2, tmp_reg)

            return True


    def apply_enums(self):
        """any value from the list `enums`"""

        if self.action not in ["inc_all", "dec_all"]:
            return

        word = self.get_word()

        fn = string.lower
        if re.match('^([A-Z1-9_]+)$', word):
            fn = string.upper
        if re.match('^([A-Z]{1}[a-z1-9_]+)$', word):
            fn = string.capitalize

        word = string.lower(word)

        enums = self.settings.get("enums")

        for enum in enums:
            if word in enum:
                delta = 1 if self.delta > 0 else -1
                new_value = enum[(enum.index(word) + delta) % len(enum)]
                self.replace(fn(new_value))
                return True


    def apply_string(self):
        """any string"""

        if self.action in ["inc_all", "dec_all"]:
            return

        word = self.get_word()
        match = re.match('([a-zA-Z1-9_]+)', word)

        if match:
            fn = {
                "inc_min": lambda s: s[0].capitalize() + s[1:],
                "dec_min": string.lower,
                "inc_max": string.upper,
                "dec_max": string.lower,
            }.get(self.action, None)

            fn and self.replace(fn(word))

            return True


    def prev(self, pos = None):
        """@return {string} Previous symbol"""

        pos = pos or self.word_reg.begin() - 1
        sym = self.view.substr(pos) # = self.get_word(pos, pos + 1)

        return {'pos': pos, 'sym': sym}


    def replace(self, text, region = None):
        """replace text in an editor on the `text`"""

        if not region:
            region = self.word_reg

        self.view.replace(self.edit, region, text)


    def get_word(self, reg_begin = None, reg_end = None):
        """get the text from the editor in the region

        - from `reg_begin` to `reg_end` if they are integers
        - from `reg_begin` = sublime.Region() if `reg_end` is None
        - from `self.word_reg` if `reg_end` and `reg_begin` is None
        """

        if not reg_begin:
            return self.view.substr(self.word_reg)

        if not reg_end:
            return self.view.substr(reg_begin)

        return self.view.substr(sublime.Region(reg_begin, reg_end))
