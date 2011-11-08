import sublime, sublime_plugin, re

class IncDecNumberCommand(sublime_plugin.TextCommand):

    def run(self, edit, delta):
        for region in self.view.sel():

            word_reg = self.view.word(region)
            if not word_reg.empty():

                inc_dec = int(delta)

                # expand region for test the previous symbol is "#" or ...
                prev_sym_pos = word_reg.begin() - 1
                prev_sym_reg = sublime.Region(prev_sym_pos, prev_sym_pos + 1)

                # hex string
                if self.view.substr(prev_sym_reg) == "#":

                    # applies for one of hex numbers
                    if delta in [1, -1]:
                        # take the symbol to the left
                        # if the cursor between '#' and the number - move it to the right
                        if word_reg.begin() == region.begin():
                            word_reg = sublime.Region(word_reg.begin(), region.end() + 1)
                        else:
                            word_reg = sublime.Region(region.begin() - 1, region.end())

                        word = self.view.substr(word_reg)
                        match = re.compile('([0-9a-fA-F])').match(word)

                    else:
                        inc_dec /= 10
                        word = self.view.substr(word_reg)
                        match = re.compile('([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$').match(word)

                    if match:
                        new_word = ""
                        for char in word:
                            char = hex(int(char, 16) + inc_dec & 0xf)[2:]
                            new_word += char
                        self.view.replace(edit, word_reg, new_word)

                # simple the positive & negative numbers (integers & floating-point numbers)
                else:
                    # floating-point numbers
                    if self.view.substr(prev_sym_reg) == ".":
                        while True:
                            prev_sym_pos -= 1
                            prev_sym_reg = sublime.Region(prev_sym_pos, prev_sym_pos + 1)
                            prev_sym = self.view.substr(prev_sym_reg)
                            if not re.compile('(\d)').match(prev_sym):
                                break

                        if self.view.substr(prev_sym_reg) != "-":
                            prev_sym_pos += 1

                        prev_sym_reg = sublime.Region(prev_sym_pos, prev_sym_pos + 1)

                        word_reg = sublime.Region(prev_sym_pos, word_reg.end())
                        word = self.view.substr(word_reg)
                        match = re.compile('(-*\d+\.(\d+))([a-zA-Z%]+)?').match(word)

                        if match:
                            float_len = len(match.group(2))
                            result = float(match.group(1)) + float(inc_dec) / (10 ** float_len)
                            match3 = match.group(3) if match.group(3) else ""
                            self.view.replace(edit, word_reg, ('%%0.%sf' % float_len) % result + match3)

                    # integers
                    else:

                        if self.view.substr(prev_sym_reg) == "-":
                            word_reg = sublime.Region(prev_sym_pos, word_reg.end())

                        word = self.view.substr(word_reg)
                        match = re.compile('(-*[0-9]+)([a-zA-Z%]+)?').match(word)

                        if match:
                            result = int(match.group(1)) + inc_dec
                            match2 = match.group(2) if match.group(2) else ""
                            self.view.replace(edit, word_reg, str(result) + match2)

                        # opposite values
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
                            self.view.replace(edit, word_reg, new_value)
