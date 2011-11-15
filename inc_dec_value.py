import sublime, sublime_plugin, re, string, datetime

class IncDecValueCommand(sublime_plugin.TextCommand):

    def run(self, edit, delta):

        self.edit = edit
        self.delta = int(delta)

        for region in self.view.sel():

            self.region = region
            self.word_reg = self.view.word(region)

            if not self.word_reg.empty():

                self.apply_date()               or \
                self.apply_hex_color()          or \
                self.apply_floating_point()     or \
                self.apply_integer()            or \
                self.apply_opposite()           or \
                self.apply_string()


    #
    # any date in ISO 8601 format, "YYYY-MM-DD", ex: 2011-11-14
    #
    def apply_date(self):

        word_reg = self.word_reg
        word = self.view.substr(word_reg)

        re_date = '([\d]{4}-[\d]{2}-[\d]{2})$'

        if re.compile('([\d]{4})$').match(word): # check year

            tmp_reg = sublime.Region(word_reg.begin(), word_reg.begin() + 10)
            word = self.view.substr(tmp_reg)

            if re.compile(re_date).match(word): # date is valid -> year
                # process with apply_integer
                return False

        elif re.compile('([\d]{2})$').match(word): # check month or day:

            date_reg = sublime.Region(word_reg.begin() - 5, word_reg.begin() + 5)
            date = self.view.substr(date_reg)

            if re.compile(re_date).match(date): # date is valid -> month
                self.view.replace(self.edit, word_reg, self.cycle(word, 12, self.delta))

                return True

            else: # check day
                date_reg = sublime.Region(word_reg.begin() - 8, word_reg.begin() + 2)
                date = self.view.substr(date_reg)

                if re.compile(re_date).match(date): # date is valid -> day
                    self.view.replace(self.edit, word_reg, self.cycle(word, 31, self.delta))

                    return True


    #
    # cycle `word` between 1 and `max` value when adding `delta`
    #
    def cycle(self, word, max, delta):
        return '%02d' % (((int(word) + max - 1 + delta) % max) + 1)


    #
    # any hex color, ex: #ee77ee; #f12; #f0e
    #
    def apply_hex_color(self):

        word_reg = self.word_reg
        word = self.view.substr(word_reg)

        re_hex_color = '([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$'
        match = re.compile(re_hex_color).match(word)

        prev = self.prev()

        if match and prev['sym'] == "#":

            delta = self.delta

            # applies for one of hex numbers
            if delta in [1, -1]:
                # take the symbol to the left
                # if the cursor between '#' and the number - move it to the right
                if word_reg.begin() == self.region.begin():
                    word_reg = sublime.Region(word_reg.begin(), self.region.end() + 1)
                else:
                    word_reg = sublime.Region(self.region.begin() - 1, self.region.end())

                word = self.view.substr(word_reg)
                match = re.compile('([0-9a-fA-F])').match(word)

            else:
                delta /= 10
                word = self.view.substr(word_reg)
                match = re.compile(re_hex_color).match(word)

            if match:
                new_word = ""
                for char in word:
                    char = hex(int(char, 16) + delta & 0xf)[2:]
                    new_word += char
                self.view.replace(self.edit, word_reg, new_word)

                return True


    #
    # any number of floating point, ex: 2.3mm or -0.27m
    #
    def apply_floating_point(self):

        prev = self.prev()

        # floating-point numbers
        if prev['sym'] == ".":
            while True:
                prev = self.prev(prev['pos'] - 1)
                if not re.compile('(\d)').match(prev['sym']):
                    break

            if prev['sym'] != "-":
                prev = self.prev(prev['pos'] + 1)

            word_reg = sublime.Region(prev['pos'], self.word_reg.end())
            word = self.view.substr(word_reg)
            match = re.compile('(-*\d+\.(\d+))([a-zA-Z%]+)?$').match(word)

            if match:
                float_len = len(match.group(2))
                result = float(match.group(1)) + float(self.delta) / (10 ** float_len)
                match3 = match.group(3) if match.group(3) else ""
                self.view.replace(self.edit, word_reg, ('%%0.%sf' % float_len) % result + match3)

                return True


    #
    # any integer, ex: 12 123px; 123% 1em;
    #
    def apply_integer(self):

        word_reg = self.word_reg
        prev = self.prev()

        if prev['sym'] == "-":
            word_reg = sublime.Region(prev['pos'], word_reg.end())

        word = self.view.substr(word_reg)
        match = re.compile('(-*[0-9]+)([a-zA-Z%]+)?$').match(word)

        if match:
            result = int(match.group(1)) + self.delta
            match2 = match.group(2) if match.group(2) else ""
            self.view.replace(self.edit, word_reg, str(result) + match2)

            return True


    #
    # any value from the list `opp_values`
    #
    def apply_opposite(self):

        word = self.view.substr(self.word_reg)

        opp_values = [
            ("true", "false"),
            ("True", "False"),
            ("TRUE", "FALSE"),
            ("left", "right"),
        ]
        new_value = ''
        for k, v in opp_values:
            if k == word:
                new_value = v
            if v == word:
                new_value = k

        if new_value:
            self.view.replace(self.edit, self.word_reg, new_value)

            return True


    #
    # any string
    #
    def apply_string(self):

        word = self.view.substr(self.word_reg)
        match = re.compile('([a-zA-Z]+)').match(word)

        if match:
            if   self.delta == 1:
                fn = string.capitalize #capwords
            elif self.delta == -1:
                fn = string.lower
            elif self.delta == 10:
                fn = string.upper
            elif self.delta == -10:
                fn = string.lower

            fn and self.view.replace(self.edit, self.word_reg, fn(word))

            return True


    #
    # @return {String} Previous symbol
    #
    def prev(self, pos = None):

        pos = pos or self.word_reg.begin() - 1
        reg = sublime.Region(pos, pos + 1)
        sym = self.view.substr(reg)

        return {
            'pos': pos,
            'reg': reg,
            'sym': sym
        }
