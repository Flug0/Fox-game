
class Converter():
    """
    Class with map from all the outputs to the corresponding move
    Output will be long list of floats, highest one will be the one choosen
    First index should represent moving from the first position to the first of its neighbors
    Keep going for all neighbors and all "double jump neighbors". Then continue with the second position and so on

            00  01  02
            03  04  05
    06  07  08  09  10  11  12
    13  14  15  16  17  18  19
    20  21  22  23  24  25  26
            27  28  29
            30  31  32
    """
    def __init__(self):
        self.dict = {
                    0 : (0,1), 1 : (0,4), 2 : (0,3), 3 : (0,2), 4 : (0,10), 5 : (0,8),
                    6 : (1,2), 7 : (1,4), 8 : (1,0), 9 : (1,9),
                    10 : (2,5), 11 : (2,4), 12 : (2,1), 13 : (2,10), 14 : (2,8), 15 : (2,0),
                    16 : (3,0), 17 : (3,4), 18 : (3,8), 19 : (3,5), 20 : (3,15),
                    21 : (4,1), 22 : (4,2), 23 : (4,5), 24 : (4,10), 25 : (4,9), 26 : (4,8), 27 : (4,3), 28 : (4,0), 29 : (4,18), 30 : (4,16), 31 : (4,14),
                    32 : (5,2), 33 : (5,10), 34 : (5,4), 35 : (5,17), 36 : (5,3),
                    37 : (6,7), 38 : (6,14), 39 : (6,13), 40 : (6,8), 41 : (6,22), 42 : (6,20),
                    43 : (7, 8), 44 : (7, 14), 45 : (7, 6), 46 : (7, 9), 47 : (7, 21),
                    48 : (8, 3), 49 : (8, 4), 50 : (8, 9), 51 : (8, 16), 52 : (8, 15), 53 : (8, 14), 54 : (8, 7), 55 : (8, 0), 56 : (8, 2), 57 : (8, 10), 58 : (8, 24), 59 : (8, 22), 60 : (8, 20), 61 : (8, 6),
                    62 : (9, 4), 63 : (9, 19), 64 : (9, 16), 65 : (9, 8), 66 : (9, 1), 67 : (9, 11), 68 : (9, 23), 69 : (9, 7),
                    70 : (10, 11), 71 : (10, 18), 72 : (10, 17), 73 : (10, 16), 74 : (10, 9), 75 : (10, 4), 76 : (10, 5), 77 : (10, 12), 78 : (10, 26), 79 : (10, 24), 80 : (10, 22), 81 : (10, 8), 82 : (10, 0), 84 : (10, 2),
                    85 : (11, 12), 86 : (11, 18), 87 : (11, 10), 88 : (11, 25), 89 : (11, 9),
                    90 : (12, 19), 91 : (12, 18), 92 : (12, 11), 93 : (12, 26), 94 : (12, 24), 95 : (12, 10),
                    96 : (13, 6), 97 : (13, 14), 98 : (13, 20), 99 : (13, 15),
                    100 : (14, 7), 101 : (14, 8), 102 : (14, 15), 103 : (14, 22), 104 : (14, 21), 105 : (14, 20), 106 : (14, 13), 107 : (14, 6), 108 : (14, 4), 109 : (14, 16), 110 : (14, 28),
                    111 : (15, 8), 112 : (15, 16), 113 : (15, 22), 114 : (15, 14), 115 : (15, 3), 116 : (15, 17), 117 : (15, 27), 118 : (15, 13), 
                    119 : (16, 9), 120 : (16, 10), 121 : (16, 17), 122 : (16, 24), 123 : (16, 23), 124 : (16, 22), 125 : (16, 15), 126 : (16, 8), 127 : (16, 4), 128 : (16, 18), 129 : (16, 28), 130 : (16, 14),
                    131 : (17, 10), 132 : (17, 18), 133 : (17, 24), 134 : (17, 16), 135 : (17, 5), 136 : (17, 19), 137 : (17, 29), 138 : (17, 15), 
                    139 : (18, 11), 140 : (18, 12), 141 : (18, 19), 142 : (18, 26), 143 : (18, 25), 144 : (18, 24), 145 : (18, 17), 146 : (18, 10), 147 : (18, 16), 148 : (18, 28), 149 : (18, 4),
                    150 : (19, 12), 151 : (19, 26), 152 : (19, 18), 153 : (19, 17),
                    154 : (20, 13), 155 : (20, 14), 156 : (20, 21), 157 : (20, 6), 158 : (20, 8), 159 : (20, 22),
                    160 : (21, 20), 161 : (21, 14), 162 : (21, 22), 163 : (21, 7), 164 : (21, 23),
                    165 : (22, 21), 166 : (22, 14), 167 : (22, 15), 168 : (22, 16), 169 : (22, 23), 170 : (22, 28), 171 : (22, 27), 172 : (22, 20), 173 : (22, 6), 174 : (22, 8), 175 : (22, 10), 176 : (22, 24), 177 : (22, 32), 178 : (22, 30),
                    179 : (23, 16), 180 : (23, 24), 181 : (23, 28), 182 : (23, 22), 183 : (23, 9), 184 : (23, 25), 185 : (23, 31), 186 : (23, 21),  
                    187 : (24, 17), 188 : (24, 25), 189 : (24, 29), 190 : (24, 23), 191 : (24, 18), 192 : (24, 28), 193 : (24, 16), 194 : (24, 26), 195 : (24, 32), 196 : (24, 30), 197 : (24, 22), 198 : (24, 8), 199 : (24, 10), 200 : (24, 12),
                    201 : (25, 26), 202 : (25, 24), 203 : (25, 18), 204 : (25, 23), 205 : (25, 11),
                    206 : (26, 25), 207 : (26, 18), 208 : (26, 29), 209 : (26, 24), 210 : (26, 10), 211 : (26, 12),
                    212 : (27, 22), 213 : (27, 28), 214 : (27, 30), 215 : (27, 15), 216 : (27, 29),
                    217 : (28, 23), 218 : (28, 24), 219 : (28, 29), 220 : (28, 32), 221 : (28, 31), 222 : (28, 30), 223 : (28, 27), 224 : (28, 22), 225 : (28, 14), 226 : (28, 16), 227 : (28, 18),
                    228 : (29, 24), 229 : (29, 32), 230 : (29, 28), 231 : (29, 27), 232 : (29, 17),
                    233 : (30, 27), 234 : (30, 28), 235 : (30, 31), 236 : (30, 22), 237 : (30, 24), 238 : (30, 32),
                    239 : (31, 30), 240 : (31, 28), 241 : (31, 32), 242 : (31, 23),
                    243 : (32, 31), 244 : (32, 28), 245 : (32, 29), 246 : (32, 30), 247 : (32, 22), 248 : (32, 24)
                    }

    def __helper(self, tpl):
        x, y = [0,0], [0,0]
        for i in range(2):
            if tpl[i] <= 5 or tpl[i] >= 27:
                x[i] = tpl[i] % 3 + 2
            else:
                x[i] = (tpl[i] - 6) % 7
            if tpl[i] < 3:
                y[i] = 0
            elif tpl[i] < 6:
                y[i] = 1
            elif tpl[i] < 13:
                y[i] = 2
            elif tpl[i] < 20:
                y[i] = 3
            elif tpl[i] < 27:
                y[i] = 4
            elif tpl[i] < 30:
                y[i] = 5
            elif tpl[i] < 33:
                y[i] = 6
        return (x[0], y[0]), (x[1], y[1])

            


    def convert_action_to_move(self, action):
        """Converts an action to a move,
        action is the index of the output with highest activation"""
        return self.__helper(self.dict[action])
