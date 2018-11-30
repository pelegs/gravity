import numpy as np
cimport numpy as np
from libc.math cimport sqrt, exp, log, pi
from tqdm import tqdm


cdef double norm(np.ndarray[double, ndim=1] vec):
    return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)


cdef np.ndarray[double, ndim=1] normalize(np.ndarray[double, ndim=1] vec):
    cdef double N = norm(vec)
    if N != 0:
        return vec_scale(vec, 1/N)
    else:
        return np.zeros(3).astype(np.float64)


cdef np.ndarray[double, ndim=1] vec_add(np.ndarray[double, ndim=1] v1,
                                        np.ndarray[double, ndim=1] v2):
    cdef np.ndarray[double, ndim=1] v_return = np.zeros(3).astype(np.float64)
    v_return[0] = v1[0] + v2[0]
    v_return[1] = v1[1] + v2[1]
    v_return[2] = v1[2] + v2[2]
    return v_return


cdef np.ndarray[double, ndim=1] vec_sub(np.ndarray[double, ndim=1] v1,
                                        np.ndarray[double, ndim=1] v2):
    cdef np.ndarray[double, ndim=1] v_return = np.zeros(3).astype(np.float64)
    v_return[0] = v1[0] - v2[0]
    v_return[1] = v1[1] - v2[1]
    v_return[2] = v1[2] - v2[2]
    return v_return


cdef np.ndarray[double, ndim=1] vec_scale(np.ndarray[double, ndim=1] vec,
                                          double scale):
    cdef np.ndarray[double, ndim=1] v_return = np.zeros(3).astype(np.float64)
    v_return[0] = scale * vec[0]
    v_return[1] = scale * vec[1]
    v_return[2] = scale * vec[2]
    return v_return


cdef vec_sum(np.ndarray[double, ndim=1] v1,
             np.ndarray[double, ndim=1] v2,
             np.ndarray[double, ndim=1] v3):
    return vec_add(vec_add(v1, v2), v3)


cdef np.ndarray[double, ndim=1] gravity_force(np.ndarray[double, ndim=1] pos1,
                                              np.ndarray[double, ndim=2] pos2,
                                              double mass1, double mass2,
                                              double G):
    cdef np.ndarray[double, ndim=1] norm_dist_vec = normalize(vec_sub(pos2, pos1))
    cdef double F_magnitude = G * mass1 * mass2 / dist2(pos1, pos2)
    return vec_scale(norm_dist_vec, F_magnitude)


cdef double dist2(np.ndarray[double, ndim=1] v1,
                  np.ndarray[double, ndim=1] v2):
    return (v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2


class body:
    def __init__(self, pos, vel, mass, color):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.mass_ = 1/mass

        self.Force = np.zeros(3).astype(np.float64)
        self.acc = np.zeros(3).astype(np.float64)
        self.acc2 = np.zeros(3).astype(np.float64)

        self.color = color

    def add_force(self, F):
        self.Force = vec_add(self.Force, F)

    def reset_forces(self):
        self.Force = np.zeros(3).astype(np.float64)

    def move1(self, dt):
        self.acc = vec_scale(self.Force, self.mass_)
        self.pos = vec_sum(self.pos, vec_scale(self.vel, dt), vec_scale(self.acc, 0.5*dt**2))
        self.reset_forces()

    def move2(self, dt):
        self.vel = vec_add(self.vel, vec_scale(vec_add(self.acc, self.acc2), 0.5*dt**2))
