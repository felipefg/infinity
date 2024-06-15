import numpy as np

from infinity import vector_db


def test_should_find_nearest():

    vdb = vector_db.VectorDB()

    v0 = np.zeros((vdb.dimensions,), dtype=vdb.dtype)
    vdb.add_vector('vector0', v0)

    v1 = np.zeros((vdb.dimensions,), dtype=vdb.dtype)
    v1[0] = 0.1
    vdb.add_vector('vector1', v1)

    v2 = np.zeros((vdb.dimensions,), dtype=vdb.dtype)
    v2[0] = 0.15
    nearest, dist = vdb.get_nearest_key(v2)

    assert nearest == 'vector1'
