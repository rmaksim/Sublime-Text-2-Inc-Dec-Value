'''
Inc-Dec-Value v0.1.7

Increase / Decrease of
    - numbers (integer and fractional),
    - dates in ISO format `YYYY-MM-DD` (months from 1 to 12, days from 1 to 31),
    - hex color values (#fff or #ffffff),
    - opposite relations or cycled enumerations (`true`->`false`, `Jan`->`Feb`->`Mar`...),
    on the configured value
    and a bonus
    - string actions (UPPER, lower, Capitalize)

Instead of the arrows can use your mouse wheel.

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

        for index, region in enumerate(self.view.sel()):

            self.region = region
            self.region_index = index # save the index of the current region to reuse it later on replace
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

        if self.action in ["inc_all", "dec_all"]:

            # color: rgba(255,0,128,0.4);
            # color: rgba(0,255,3,0.4);
            pos_rgba_beg = self.find_left("r")
            pos_rgba_end = self.find_right(")")

            if pos_rgba_beg and pos_rgba_end:
                pos_rgba_end = pos_rgba_end + 1

                if self.view.substr(pos_rgba_end) == ";":
                    pos_rgba_end = pos_rgba_end + 1

                rgba_str = self.get_word(pos_rgba_beg, pos_rgba_end)

                re_rgba = re.compile('rgba\((.*),(.*),(.*),(.*)\)(;?)$')
                match = re_rgba.match(rgba_str)

                if match:
                    hex_str = "#" \
                            + self.int_to_hex(match.group(1)) \
                            + self.int_to_hex(match.group(2)) \
                            + self.int_to_hex(match.group(3)) \
                            + "; /* alpha: " + match.group(4) +" */"

                    self.view.sel().subtract(sublime.Region(self.region.begin(), self.region.end()))
                    self.view.replace(self.edit, sublime.Region(pos_rgba_beg, pos_rgba_end), hex_str)
                    self.view.sel().add(sublime.Region(pos_rgba_beg, pos_rgba_beg))

                    return True

            # color: #ff1080; /* alpha: 1 */
            # color: #0f1080;
            # color: #012; /* alpha: 0.4 */
            # color: #f12; /* alpha: .1 */
            # color: #f12; /* alpha: 0 */
            # color: #f12; /* alpha: 1 */
            pos_hex_beg = self.word_reg.begin()
            pos_hex_end = self.word_reg.end()
            word = self.get_word()

            # curson on #
            if word[-1] == "#":
                word2_reg = self.view.word(self.word_reg.end() + 1)
                pos_hex_beg = self.word_reg.end() - 1
                pos_hex_end = word2_reg.end()
            else:
                prev = self.prev()
                if prev['sym'] == "#":
                    pos_hex_beg = self.word_reg.begin() - 1
                    pos_hex_end = self.word_reg.end()

            alpha = ""
            pos_alpha1 = self.find_right("/", pos_hex_end)
            if pos_alpha1:
                pos_alpha2 = self.find_right("/", pos_alpha1 + 1)
                alpha_str = self.get_word(pos_alpha1, pos_alpha2 + 1)

                re_alpha = re.compile('^\/\* alpha: (.*) \*\/$')
                match_alpha = re_alpha.match(alpha_str)
                if match_alpha:
                    alpha = match_alpha.group(1)

            word = self.get_word(pos_hex_beg, pos_hex_end)

            re_hex_color = re.compile('(?:#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2}))|(?:#([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1}))$')
            match = re_hex_color.match(word)
            if match:
                r = str(int(match.group(1) or match.group(4) + match.group(4), 16))
                g = str(int(match.group(2) or match.group(5) + match.group(5), 16))
                b = str(int(match.group(3) or match.group(6) + match.group(6), 16))
                rgba_alpha = "1" if alpha == "" else alpha
                semi = ";" if alpha != "" else ""
                rgba_str = "rgba("+r+","+g+","+b+","+rgba_alpha+")"+semi

                self.view.sel().subtract(sublime.Region(self.region.begin(), self.region.end()))
                self.view.replace(self.edit, sublime.Region(pos_hex_beg, pos_hex_end if alpha == "" else pos_alpha2 + 1), rgba_str)
                self.view.sel().add(sublime.Region(pos_hex_beg, pos_hex_beg))

                return True

        # "inc_min", "dec_min", "inc_max", "dec_max"
        else:
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
                    if tmp_reg.end() == self.region.end():
                        tmp_reg = sublime.Region(self.region.begin() - 1, self.region.begin())
                    else:
                        tmp_reg = sublime.Region(self.region.begin(), self.region.begin() + 1)

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

        prev = self.prev()
        if prev['sym'] == "-":
            prev = self.prev(prev['pos'] - 1)
            while re.match('([A-Za-z])', prev['sym']):
                prev = self.prev(prev['pos'] - 1)

            prev = self.prev(prev['pos'] + 1)
            self.word_reg = sublime.Region(prev['pos'], self.word_reg.end())
            word = self.get_word()

        last = self.prev(self.word_reg.end())
        if last['sym'] == "-":
            last = self.prev(last['pos'] + 1)
            while re.match('([A-Za-z])', last['sym']):
                last = self.prev(last['pos'] + 1)

            self.word_reg = sublime.Region(self.word_reg.begin(), last['pos'])
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
        # match = re.match('([a-zA-Z1-9_]+)', word)

        # if match:
        fn = {
            "inc_min": lambda s: s.capitalize() if s[0].islower() else s.upper(),
            "dec_min": lambda s: s.capitalize() if s.isupper() else s.lower(),
            "inc_max": string.upper,
            "dec_max": string.lower,
        }.get(self.action, None)

        if fn:
            new_word = fn(word)
            if word != new_word:
                self.replace(new_word)

        return True


    def prev(self, pos = None):
        """@return {string} Previous symbol"""

        pos = pos or self.word_reg.begin() - 1
        sym = self.view.substr(pos) # = self.get_word(pos, pos + 1)

        return {'pos': pos, 'sym': sym}


    def next(self, pos = None):
        """@return {string} Next symbol"""

        pos = pos or self.word_reg.begin() + 1
        sym = self.view.substr(pos)

        return {'pos': pos, 'sym': sym}


    def replace(self, text, region = None):
        """replace text in an editor on the `text`"""

        old_pos = self.view.sel()[self.region_index]

        if not region:
            region = self.word_reg

        self.view.replace(self.edit, region, text)


        # restore the initial position of the cursor
        offset = len(text) - len(self.view.substr(region))

        self.view.sel().subtract(sublime.Region(region.end() + offset, region.end() + offset))

        offset_start = old_pos.begin() + offset
        offset_end = old_pos.end() + offset

        if old_pos.begin() == region.begin(): # don't use offset if we're at the start of the initial value
            offset_start = old_pos.begin()

            if old_pos.begin() == old_pos.end(): # don't use offset for ending point if we're not at selection
                offset_end = old_pos.end()

        self.view.sel().add(sublime.Region(offset_start, offset_end))


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


    def find_right(self, sym, pos = None):
        pos = pos or self.region.begin()
        line = self.view.line(pos)
        end_pos = line.end()

        while pos < end_pos:
            pos_sym = self.view.substr(pos)
            if pos_sym == sym:
                return pos
            pos = pos + 1


    def find_left(self, sym, pos = None):
        pos = pos or self.region.begin()
        line = self.view.line(pos)
        pos_beg = line.begin()

        while pos > pos_beg:
            pos_sym = self.view.substr(pos)
            if pos_sym == sym:
                return pos
            pos = pos - 1


    def int_to_hex(self, int_str, digits = 2):
        hex_str = hex(int(int_str))[2:]
        if len(hex_str) < digits:
            hex_str = "0" + hex_str

        return hex_str
