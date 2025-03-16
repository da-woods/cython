cimport cython

from libc.stdlib cimport calloc, free
from libc.stdint cimport uintptr_t

cdef extern from *:
    """
    struct OpaqueStruct;
    """
    @cython.extended_buffer_name("cyexample", "OpaqueStruct")
    struct OpaqueStruct:
        pass

cdef class SingleOpaqueStruct:
    cdef Py_ssize_t n
    cdef Py_ssize_t stride
    cdef OpaqueStruct* data

    def __cinit__(self):
        self.n = 1
        self.data = <OpaqueStruct*>calloc(1, 1)

    def __dealloc__(self):
        free(self.data)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = 1

        buffer.buf = <char*>&self.data
        buffer.format = b"[cyexample$OpaqueStruct]"
        buffer.itemsize = itemsize
        buffer.internal = NULL
        buffer.ndim = 1
        buffer.readonly = 0
        buffer.shape = &self.n
        buffer.strides = &self.stride
        buffer.suboffsets = NULL
        buffer.obj = self

    def __releasebuffer__(self,  Py_buffer *buffer):
        pass

# Note, can't be contiguous because that relies on the itemsize
# to implement indexing.
def f(OpaqueStruct[:] os):
    print(<uintptr_t>(&os[0]))
