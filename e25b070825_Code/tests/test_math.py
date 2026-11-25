"""Mathematical verification tests for The Product Rule explainer (SymPy + pytest)."""

from __future__ import annotations

import sympy as sp


def test_hook_example_x_times_x():
    x = sp.Symbol("x", real=True)
    f = x
    g = x
    fp = sp.diff(f, x)
    gp = sp.diff(g, x)
    assert fp == 1 and gp == 1
    wrong_guess = fp * gp
    assert wrong_guess == 1

    real_deriv = sp.diff(f * g, x)
    assert sp.simplify(real_deriv - 2 * x) == 0
    assert real_deriv.subs(x, 3) == 6
    assert wrong_guess.subs(x, 3) == 1

    # Tangent at (3, 9): y - 9 = 6(x - 3) -> y = 6x - 9
    tangent_line = 9 + 6 * (x - 3)
    assert sp.simplify(tangent_line - (6 * x - 9)) == 0
    assert tangent_line.subs(x, 3) == 9

    # Guess secant/line through (3, 9) with slope 1: y - 9 = 1(x - 3) -> y = x + 6
    guess_line = 9 + 1 * (x - 3)
    assert sp.simplify(guess_line - (x + 6)) == 0
    assert guess_line.subs(x, 3) == 9


def test_growing_rectangle_identity():
    f, g, df, dg = sp.symbols("f g df dg")
    expanded = sp.expand((f + df) * (g + dg) - f * g)
    expected = g * df + f * dg + df * dg
    assert sp.simplify(expanded - expected) == 0


def test_worked_example_x2_x3():
    x = sp.Symbol("x", real=True)
    f = x ** 2
    g = x ** 3
    fp = sp.diff(f, x)
    gp = sp.diff(g, x)
    assert fp == 2 * x
    assert gp == 3 * x ** 2

    via_rule = sp.expand(fp * g + f * gp)
    via_direct = sp.diff(x ** 5, x)
    assert sp.simplify(via_rule - 5 * x ** 4) == 0
    assert sp.simplify(via_direct - 5 * x ** 4) == 0
    assert sp.simplify(via_rule - via_direct) == 0

    # At x = 1: two parts are 2*1 and 1*3 -> 2 + 3 = 5
    part_width = (fp * g).subs(x, 1)
    part_height = (f * gp).subs(x, 1)
    assert part_width == 2
    assert part_height == 3
    assert via_rule.subs(x, 1) == 5


def test_scene5_convergence_table():
    # Exact values from Rational arithmetic, then rounded to 3 decimal places as displayed
    expected_rows = [
        (sp.Rational("0.1"), ("2.100", "3.310", "0.695", "6.105")),
        (sp.Rational("0.01"), ("2.010", "3.030", "0.061", "5.101")),
        (sp.Rational("0.001"), ("2.001", "3.003", "0.006", "5.010")),
    ]
    for dx, expected_strs in expected_rows:
        df = (1 + dx) ** 2 - 1
        dg = (1 + dx) ** 3 - 1
        right_rate = (1 * df) / dx
        top_rate = (1 * dg) / dx
        corner_rate = (df * dg) / dx
        total_rate = ((1 + dx) ** 5 - 1) / dx

        assert sp.simplify(right_rate + top_rate + corner_rate - total_rate) == 0

        got_strs = tuple(f"{float(val):.3f}" for val in (right_rate, top_rate, corner_rate, total_rate))
        assert got_strs == expected_strs

    # Limit row -> 0
    dx_sym = sp.Symbol("dx", positive=True)
    df_sym = (1 + dx_sym) ** 2 - 1
    dg_sym = (1 + dx_sym) ** 3 - 1
    assert sp.limit(df_sym / dx_sym, dx_sym, 0) == 2
    assert sp.limit(dg_sym / dx_sym, dx_sym, 0) == 3
    assert sp.limit((df_sym * dg_sym) / dx_sym, dx_sym, 0) == 0
    assert sp.limit(((1 + dx_sym) ** 5 - 1) / dx_sym, dx_sym, 0) == 5


def test_optional_x2_sin_x():
    x = sp.Symbol("x", real=True)
    f = x ** 2
    g = sp.sin(x)
    via_rule = sp.diff(f, x) * g + f * sp.diff(g, x)
    direct = sp.diff(f * g, x)
    expected = 2 * x * sp.sin(x) + x ** 2 * sp.cos(x)
    assert sp.simplify(via_rule - expected) == 0
    assert sp.simplify(direct - expected) == 0
