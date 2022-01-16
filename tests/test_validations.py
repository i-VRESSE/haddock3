"""Test specific validations modules."""
import pytest

from haddock.gear.validations import v_rundir


@pytest.mark.parametrize(
    "rundir",
    [
        "some/folder",
        "some_folder/other",
        "some_folder_2/other",
        r"some\folder\on\windows",
        ]
    )
def test_v_rundir_okay(rundir):
    """Test rundir validation okay."""
    v_rundir(rundir)


@pytest.mark.parametrize(
    "rundir",
    [
        "some/folder with spaces",
        "some_folder/ðßæ",
        "joão/folder",
        ]
    )
def test_v_rundir_invalid(rundir):
    """Test rundir validation okay."""
    with pytest.raises(ValueError):
        v_rundir(rundir)
