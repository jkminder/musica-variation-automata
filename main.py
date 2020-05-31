from src.examples import *

ADD_mva = BINARY_ADDITION()

ADD_mva.add_theme([c2_4, c2_4, c2_4, c2_4 , e2_4, e2_4, e2_4, e2_4, p_8])
ADD_mva.describe()
ADD_mva.run(verbose_mode=False)
#ADD_mva.save_score_to_midi("test")