from algorithm_module import interp_4_dote, interp_6_dote
from numpy import interp

"""
def interp_4_dote(
        point_limits: list[int],  # [-4, 4]
        prcnt_limits: list[float],  # [-3, 5]
        dote_prcnt: float,  # x -- 0.7
        prcnt_start_limit: float,  # 0.2
        is_abs_limit=True
):
def interp_6_dote(
        point_limits: list[int],  # [-6, 6]
        prcnt_limits: list[float],  # [-2, -1, 1, 2]
        dote_prcnt: float,  # x -- 0.7
        prcnt_start_limit: float,  # 0.2
        is_abs_limit=True
):
"""

cur_prcnt = -3.1

"""
print(interp(
    cur_prcnt,
    fp=[-4, 0],
    xp=[-4, 0]
))
print(interp_4_dote(
    point_limits=[-4, 4],
    prcnt_limits=[-3, 5],
    dote_prcnt=cur_prcnt,
    prcnt_start_limit=0.2
))
print(interp_6_dote(
    point_limits=[-6, 6],
    prcnt_limits=[-6, -3, 3, 6],
    dote_prcnt=cur_prcnt,
    prcnt_start_limit=0
))
"""
