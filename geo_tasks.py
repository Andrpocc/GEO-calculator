# -*- coding: utf-8 -*-

import math
from sympy import Segment, Point


def ogz(xa, ya, xb, yb):
    """Обратная геодезическая задача"""
    delx = xb - xa
    dely = yb - ya
    S = math.sqrt(delx ** 2 + dely ** 2)
    if dely == 0 and delx > 0:
        alf = 0
    elif dely == 0 and delx < 0:
        alf = 180
    elif delx == 0 and dely > 0:
        alf = 90
    elif delx == 0 and dely < 0:
        alf = 270
    else:
        rumb = math.fabs(math.degrees(math.atan(dely / delx)))

        if delx > 0 and dely > 0:
            alf = rumb

        elif delx < 0 and dely > 0:
            alf = 180 - rumb

        elif delx < 0 and dely < 0:
            alf = 180 + rumb

        elif delx > 0 and dely < 0:
            alf = 360 - rumb

    G = math.trunc(alf)
    M = math.trunc((alf - G) * 60)
    C = round(((alf - G) - M/60) * 60 * 60)
    return G, M, C, S



def pgz(X1, Y1, G, M, C, S):
    """Прямая геодезическая задача"""
    angle = G + M/60 + C/(60*60)
    angle = math.radians(angle)
    X2 = X1 + S * math.cos(angle)
    Y2 = Y1 + S * math.sin(angle)
    return X2, Y2


def polygon_square(points):
    """Площадь полигона по координатам точек"""
    sx = 0
    sy = 0
    n = len(points)

    for i in range(n):
        if i != n-1:
            sx += points[i][0] * points[i+1][1]
        elif i == n-1:
            sx += points[i][0] * points[0][1]

    for i in range(n):
        if i != n-1:
            sy -= points[i][1] * points[i+1][0]
        elif i == n-1:
            sy -= points[i][1] * points[0][0]

    s = math.fabs(sx + sy) / 2
    return s


def midpoint(x1, y1, x2, y2):
    """Координаты середины отрезка"""
    xm = (x1 + x2)/2
    ym = (y1 + y2)/2
    return xm, ym

def intersection_of_segments(p1_x, p1_y, p2_x, p2_y):
    """Координаты точки пересечения двух отрезков"""
    s1 = Segment(p1_y, p1_x)
    s2 = Segment(p2_y, p2_x)
    intersection = s1.intersection(s2)
    if len(intersection) != 0:
        intersection = intersection[0]
        return float(intersection.y), float(intersection.x)
    else:
        return 0, 0
