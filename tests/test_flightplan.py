import pytest
import pyproj
import numpy as np
import numpy.testing as npt
import orcestra.flightplan as fp


@pytest.fixture
def geod():
    return pyproj.Geod(ellps="WGS84")


def test_point_at_distance(geod):
    a = fp.LatLon(0, 0)
    b = fp.LatLon(0, 1)
    path = [a, a.towards(b, distance=50e3), b]
    spath = fp.simplify_path(path)
    print(spath)

    assert spath[1].lat == 0
    assert spath[1].lon == geod.fwd(0, 0, 90, 50e3)[0]

    path = [a, b.towards(a, distance=50e3), b]
    spath = fp.simplify_path(path)

    npt.assert_allclose(spath[1].lat, 0)
    npt.assert_allclose(spath[1].lon, geod.fwd(1, 0, -90, 50e3)[0])


def test_assign_label_old():
    a = fp.LatLon(3, 7, fl=300)
    b = a.assign_label("test")
    assert b.label == "test"
    assert a.label is None
    assert a.lat == b.lat == 3
    assert a.lon == b.lon == 7
    assert a.fl == b.fl == 300


def test_assign_label():
    a = fp.LatLon(3, 7, fl=300)
    b = a.assign(label="test")
    assert b.label == "test"
    assert a.label is None
    assert a.lat == b.lat == 3
    assert a.lon == b.lon == 7
    assert a.fl == b.fl == 300


def test_assign_flightlevel():
    a = fp.LatLon(3, 7, label="test")
    b = a.assign(fl=350)
    assert b.fl == 350
    assert a.fl is None
    assert a.lat == b.lat == 3
    assert a.lon == b.lon == 7
    assert a.label == b.label == "test"


def test_fix_waypoint_time():
    a = fp.LatLon(0, 0, fl=300)
    b = fp.LatLon(0, 1, fl=300, time="2014-01-01T00:00:00")
    path = fp.expand_path([a, b], max_points=2)
    print(path)
    assert path.time.values[-1] == np.datetime64("2014-01-01T00:00:00")
    assert path.time.values[0] < path.time.values[-1]


def test_float_type_cast():
    assert isinstance(fp.LatLon(0, 0).lat, float)
    assert isinstance(fp.LatLon(0.0, 0).lat, float)
    assert isinstance(fp.LatLon(np.float64(0), 0).lat, float)
