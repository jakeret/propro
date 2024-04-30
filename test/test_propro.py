import glob
import os
import time

import pytest

import propro


# Mock function for testing
def mem_hungry(size):
    # Simulate memory-intensive operation
    time.sleep(0.1)


@pytest.mark.parametrize("fmt", [
    "txt",
    "png",
    "txt,png"
])
def test_profile_output_created(fmt):
    callname = "test_function"

    @propro.profile(sample_rate=0.1, fmt="txt", callname=callname)
    def profiled_function():
        mem_hungry(100)

    profiled_function()

    txt_files = glob.glob(f"propro_{callname}_*.txt")
    png_files = glob.glob(f"propro_{callname}_*.png")

    assert txt_files or png_files
    assert len(txt_files) == 1 or len(png_files) == 1
    assert len(txt_files) + len(png_files) == 1


@pytest.fixture(autouse=True)
def cleanup_profiling_outputs():
    yield  # Execute the test
    for file in glob.glob("propro_*"):
        os.remove(file)
