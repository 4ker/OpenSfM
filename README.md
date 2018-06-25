```python
heaviest = max([(self.weights[r],r) for r in roots])[1]

class Pose(object):
    def __init__(self, rotation=np.zeros(3), translation=np.zeros(3)):
        self.rotation = rotation
        self.translation = translation

    # cool!
    def transform(self, point):
        """Transform a point from world to this pose coordinates."""
        return self.get_rotation_matrix().dot(point) + self.translation

    # cool^2!
    def transform_many(self, points):
        """Transform points from world coordinates to this pose."""
        return points.dot(self.get_rotation_matrix().T) + self.translation

    def get_Rt(self):
        """Get pose as a 3x4 matrix (R|t)."""
        Rt = np.empty((3, 4))
        Rt[:, :3] = self.get_rotation_matrix()
        Rt[:, 3] = self.translation
        return Rt

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.__class__.__name__,
            self.id, self.projection_type, self.width, self.height,
            self.focal, self.k1, self.k2,
            self.focal_prior, self.k1_prior, self.k2_prior)

    def project_many(self, points):
        """Project 3D points in camera coordinates to the image plane."""
        distortion = np.array([self.k1, self.k2, 0, 0, 0])
        K, R, t = self.get_K(), np.zeros(3), np.zeros(3)
        pixels, _ = cv2.projectPoints(points, R, t, K, distortion)
        return pixels.reshape((-1, 2))



```

## Overview
OpenSfM is a Structure from Motion library written in Python on top of [OpenCV][]. 

It also integrates external sensor (e.g. GPS, accelerometer) measurements for
geographical alignment and robustness. 

A JavaScript viewer is provided to preview the models and debug the pipeline.

* [OpenCV][]
* [OpenGV][]
* [Ceres Solver][]
* [Boost Python][]
* [NumPy][], [SciPy][], [Networkx][], PyYAML, exifread


Things you can do from there:
- Use datasets with more images
- Click twice on an image to see it. Then use arrows to move between images.
