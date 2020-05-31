from src.automata import Automata, Pause, Note, VariationFunction

c2_4 = Note("c2", 1 / 4)
c2_8 = Note("c2", 1 / 8)
e2_4 = Note("e2", 1 / 4)
e2_8 = Note("e2", 1 / 8)
a1_4 = Note("a1", 1 / 4)
a1_8 = Note("a1", 1 / 8)
f1_4 = Note("f1", 1/4)
f1_8 = Note("f1", 1/8)
p_4 = Pause(1 / 4)
p_8 = Pause(1 / 8)

def AND():
    AND_mva = Automata("AND")
    AND_mva.add_variation_function(VariationFunction([c2_8, e2_8], [p_8, a1_8]))
    AND_mva.add_variation_function(VariationFunction([c2_4, e2_8], [p_8, a1_8]))
    AND_mva.add_variation_function(VariationFunction([c2_8, e2_4], [p_8, a1_8]))
    AND_mva.add_variation_function(VariationFunction([c2_8, e2_8], [p_8, a1_8]))
    AND_mva.add_variation_function(VariationFunction([c2_4, e2_4], [p_8, a1_4]))

    AND_mva.add_theme([c2_4, e2_4])

    return AND_mva


def BINARY_ADDITION():

    ADD_mva = Automata("Binary Adder")
    # 1-bit addition
    ADD_mva.add_variation_function(VariationFunction([c2_4, e2_4], [f1_4, a1_8]))
    ADD_mva.add_variation_function(VariationFunction([c2_8, e2_4], [a1_4]))
    ADD_mva.add_variation_function(VariationFunction([c2_4, e2_8], [a1_4]))
    ADD_mva.add_variation_function(VariationFunction([c2_8, e2_8], [a1_8]))

    # concat carries
    ADD_mva.add_variation_function(VariationFunction([p_8, f1_4], [p_4, a1_4]))
    ADD_mva.add_variation_function(VariationFunction([p_8, a1_4, f1_4], [p_4, a1_4, a1_8]))
    ADD_mva.add_variation_function(VariationFunction([p_8, a1_8, f1_4], [p_4, a1_4]))
    ADD_mva.add_variation_function(VariationFunction([a1_4, f1_4], [f1_4, a1_8]))
    ADD_mva.add_variation_function(VariationFunction([a1_8, f1_4], [a1_4]))

    # swapping
    ADD_mva.add_variation_function(VariationFunction([a1_4, e2_4], [e2_4, a1_4]))
    ADD_mva.add_variation_function(VariationFunction([a1_4, e2_8], [e2_8, a1_4]))
    ADD_mva.add_variation_function(VariationFunction([a1_8, e2_4], [e2_4, a1_8]))
    ADD_mva.add_variation_function(VariationFunction([a1_8, e2_8], [e2_8, a1_8]))
    ADD_mva.add_variation_function(VariationFunction([f1_4, e2_4], [e2_4, f1_4]))
    ADD_mva.add_variation_function(VariationFunction([f1_4, e2_8], [e2_8, f1_4]))

    # self reproducing
    for el in [c2_4, c2_8, e2_4, e2_8, a1_4, a1_8, f1_4, p_8]:
        ADD_mva.add_variation_function(VariationFunction([el], [el]))

    return ADD_mva
