import enum


class ParametersNames(enum.Enum):
    X = 0
    THETA_X = 1
    Y = 2
    THETA_Y = 3
    PT = 4
    CROSSING_ANGLE = 5
    D_X = 6
    L_X = 7
    V_X = 8
    D_Y = 9
    L_Y = 10
    V_Y = 11
    S = 12
    E = 13
    DELTA_X = 14
    DELTA_THETA_X = 15
    DELTA_Y = 16
    DELTA_THETA_Y = 17
    DELTA_PT = 18
    T = 19
    TURN = 20

    @classmethod
    def get_delta(cls, parameter):
        mapping = {
            ParametersNames.X: ParametersNames.DELTA_X,
            ParametersNames.THETA_X: ParametersNames.DELTA_THETA_X,
            ParametersNames.Y: ParametersNames.DELTA_Y,
            ParametersNames.THETA_Y: ParametersNames.DELTA_THETA_Y,
            ParametersNames.PT: ParametersNames.DELTA_PT
        }
        return mapping[parameter]

    @classmethod
    def get_name_in_xml(cls, parameter):
        mapping = {
            ParametersNames.X: "x",
            ParametersNames.THETA_X: "theta_x",
            ParametersNames.Y: "y",
            ParametersNames.THETA_Y: "theta_y"
        }
        return mapping[parameter]

