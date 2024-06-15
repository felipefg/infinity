"""
Simple in-memory vector db for Infinity Project
"""
import numpy as np
from numpy.typing import NDArray

DIMENSIONS = 512


class VectorDB:

    def __init__(self, dimensions: int = DIMENSIONS, dtype: str = 'float16'):
        self.dimensions: int = dimensions
        self.dtype: str = dtype
        self.vectors: NDArray = np.empty(shape=(0, dimensions), dtype=dtype)
        self.keys: list[str] = []

    def _ensure_mat(self, vector: NDArray) -> NDArray:
        shape = vector.shape
        if len(shape) == 1:
            vector = vector.reshape((1, -1))

        if vector.shape[1] != self.dimensions:
            raise ValueError("Input vector has invalid dimensions.")

        if str(vector.dtype) != self.dtype:
            vector = vector.astype(self.dtype)

        return vector

    def add_vector(self, key: str, vector: NDArray):

        vector = self._ensure_mat(vector)
        self.vectors = np.append(self.vectors, vector, axis=0)
        self.keys.append(key)

    def get_nearest_key(self, vector: NDArray) -> tuple[str, float]:

        vector = self._ensure_mat(vector)

        diff = self.vectors - vector
        dist = np.power(diff, 2).sum(axis=1)

        nearest = dist.argmin()

        return self.keys[nearest], dist[nearest]
