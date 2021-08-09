"""Test point of contact (POC) estimation"""
import pathlib

import numpy as np
import pytest

from nanite import poc, IndentationGroup


data_path = pathlib.Path(__file__).resolve().parent / "data"


@pytest.mark.parametrize("method,contact_point", [
    ["scheme_2020", 1805],
    ["gradient_zero_crossing", 1902],
    ["fit_constant_line", 1838],
    ["deviation_from_baseline", 1805],
    ])
def test_correct_split_approach_retract(method, contact_point):
    fd = IndentationGroup(data_path / "spot3-0192.jpk-force")[0]
    fd.apply_preprocessing(["compute_tip_position",
                            "correct_force_offset"])
    assert poc.compute_poc(fd["force"], method)


@pytest.mark.parametrize("method,contact_point", [
    ["scheme_2020", 1805],
    ["gradient_zero_crossing", 1902],
    ["fit_constant_line", 1838],
    ["deviation_from_baseline", 1805],
    ])
def test_correct_split_approach_retract_via_indent(method, contact_point):
    fd = IndentationGroup(data_path / "spot3-0192.jpk-force")[0]
    fd.apply_preprocessing(["compute_tip_position",
                            "correct_force_offset",
                            "correct_tip_offset"],
                           options={"correct_tip_offset": {"method": method}})
    assert np.argmin(np.abs(fd["tip position"])) == contact_point
