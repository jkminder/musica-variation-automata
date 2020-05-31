import copy

class Value:
    lines = ["      ", "      ", "      ", "      ", "––––––", "      ", "––––––", "      ", "––––––", "      ",
             "––––––", "      ", "––––––", "      "]
    lines = [list(line) for line in lines]

class Note:
    convertion_table = {
        "d1": 13, "e1": 12, "f1": 11, "g1": 10, "a1": 9, "b1":8, "c2": 7, "d2": 6, "e2": 5, "f2": 4, "g2": 3
    }
    midi_convertion_table = {
        "d1": 62, "e1": 64, "f1": 65, "g1": 67, "a1": 69, "b1":71, "c2": 72, "d2": 74, "e2": 76, "f2": 77, "g2": 79
    }
    def __init__(self, pitch, length):
        assert(length == 0.25 or length == 0.125) # Only 1/2 and 1/4 supported
        assert(pitch in Note.convertion_table.keys()) # Pitch not supported
        self.pitch = pitch
        self.length = length

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.length == other.length and self.pitch == other.pitch

    def dump(self):
        lines = copy.deepcopy(Value.lines)
        pitch_idx = Note.convertion_table[self.pitch]
        lines[pitch_idx - 3][3] = "|"
        if self.length == 0.125:
            lines[pitch_idx - 3][4] = "\\"
        lines[pitch_idx - 2][3] = "|"
        lines[pitch_idx - 1][3] = "|"
        lines[Note.convertion_table[self.pitch]][2] = "O"
        lines[Note.convertion_table[self.pitch]][3] = "'"

        return lines

class Pause:
    def __init__(self, length):
        assert(length == 0.25 or length == 0.125) # Only 1/2 and 1/4 supported
        self.length = length

    def __eq__(self, other):
        if isinstance(other, Pause):
            return self.length == other.length

    def dump(self):
        lines = copy.deepcopy(Value.lines)
        if self.length == 0.125:
            lines[7][2] = "<"
            lines[7][3] = ">"
            lines[7][4] = "-"
            lines[7][5] = "/"
            lines[8][4] = "/"
        else:
            lines[6][3] = "\\"
            lines[7][3] = "/"
            lines[8][3] = "\\"
            lines[9][3] = "C"

        return lines


class VariationFunction:
    length_converter = {0.125: "1/8", 0.25: "1/4"}
    def __init__(self, theme, variation):
        self.theme = theme
        self.variation = variation

    def dump(self):
        p_string = ""
        for val in self.theme:
            if isinstance(val, Pause):
                p_string += "p_" + VariationFunction.length_converter[val.length] + "  "
            else:
                p_string += val.pitch + "_" + VariationFunction.length_converter[val.length] + "  "
        p_string += "  ---->  "
        if self.variation == "halt":
            p_string += "HALT"
        else:
            for val in self.variation:
                if isinstance(val, Pause):
                    p_string += "p_" + VariationFunction.length_converter[val.length] + "  "
                else:
                    p_string += val.pitch + "_" + VariationFunction.length_converter[val.length] + "  "
        print(p_string)

class Automata:
    def __init__(self, name):
        self.name = name
        self._score = []
        self._header_position = -1
        self._variation_functions = []
        self._halting_position = -1

    def add_theme(self, theme):
        self._score = theme
        self._header_position = 0

    def add_variation_function(self, function):
        self._variation_functions.append(function)

    def run(self, verbose_mode = False, max_iterations = 1000):
        assert(self._header_position >= 0) # a theme/input musst be given
        if verbose_mode:
            self.dump()

        iterations = 0
        while True:
            if (verbose_mode):
                input("\nPress enter for next iteration:")
            iterations += 1
            if iterations > max_iterations:
                print("Automata reached maximum number of iterations " + str(max_iterations))
                break
            halt = True
            for func in self._variation_functions:
                equal = True
                for i in range(len(func.theme)):
                    if len(self._score) <= self._header_position + i:
                        func.dump()
                        break
                    if self._score[self._header_position + i] != func.theme[i]:
                        equal = False
                        break
                if equal:
                    if verbose_mode:
                        func.dump()
                    if func.variation != "halt":
                        self._score.extend(copy.deepcopy(func.variation))
                        halt = False
                        self._header_position += len(func.theme)
                        break
            if halt:
                print(f"\n\n\n######## Musical Variation Automata HALTED after {iterations} iterations#######")
                self._halting_position = self._header_position
                self._header_position += 1
                self.dump()
                break
            if verbose_mode:

                self.dump()

    def dump(self):
        lines = []
        for value in self._score:
            val_lines = value.dump()
            if len(lines) == 0:
                lines = val_lines
            else:
                for line_idx in range(len(lines)):
                    lines[line_idx].extend(val_lines[line_idx])
        for line in lines:
            print("".join(line))
        if self._halting_position >= 0:
            print((self._halting_position * 6) * " " + " HALT ")
        print((self._header_position * 6) * " " + "/HEAD\\")

    def describe(self):
        print("Musical Variation Automata: ", self.name)
        print("\nVariation Functions:")
        for func in self._variation_functions:
            func.dump()

        print("\nTheme:")
        self.dump()


    def save_score_to_midi(self, filename):
        from midiutil.MidiFile import MIDIFile
        track = 0
        channel = 0
        time = 0
        midi = MIDIFile(1)
        time = 0
        midi.addTempo(track, time, 100)
        for val in self._score:
            if isinstance(val, Pause):
                time += val.length*4
            else:
                midi.addNote(track, channel, Note.midi_convertion_table[val.pitch], time, val.length*4, 100)
                time += val.length*4

        with open(filename + ".mid", "wb") as output_file:
            midi.writeFile(output_file)