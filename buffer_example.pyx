from libc cimport stdint
from libc.stdlib cimport calloc, free

cimport cython

@cython.extended_buffer_name("cyexample", "MyDateTime")
ctypedef struct MyDateTime:
    stdint.int64_t seconds_since_1970

@cython.extended_buffer_regex("cyexample", r"MyStringClass_\d+")
ctypedef struct MyStringClass:
    stdint.int64_t length

cdef class DateTimeVector:
    cdef Py_ssize_t n
    cdef Py_ssize_t stride
    cdef MyDateTime *data

    def __cinit__(self, n):
        self.n = n
        self.data = <MyDateTime*>calloc(sizeof(MyDateTime), n)
        self.stride = sizeof(MyDateTime)

    def __dealloc__(self):
        free(self.data)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = sizeof(MyDateTime)

        buffer.buf = <char*>self.data
        buffer.format = "[cyexample$MyDateTime]"
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

cdef class SingleString:
    cdef Py_ssize_t n
    cdef Py_ssize_t stride
    cdef MyStringClass data
    cdef char* actual_string_data
    cdef format_string

    def __cinit__(self):
        self.n = 1
        self.actual_string_data = <char*>calloc(1, 50)
        self.actual_string_data[0] = 'h'
        self.actual_string_data[1] = 'e'
        self.actual_string_data[2] = 'l'
        self.actual_string_data[3] = 'l'
        self.actual_string_data[4] = 'o'
        self.data.length = 5
        self.format_string = f"[cyexample$MyStringClass_{<stdint.uintptr_t>self.actual_string_data}]".encode("ascii")

    def __dealloc__(self):
        free(self.actual_string_data)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = sizeof(MyStringClass)

        buffer.buf = <char*>&self.data
        buffer.format = self.format_string
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

def example_func(MyDateTime[::1] dts):
    print(dts[0].seconds_since_1970)
    print(dts.format)

cdef convert_my_string_to_py_string(MyStringClass s, format):
    # assume format is basically right
    start, end = format.split(b"MyStringClass_")
    assert end.endswith(b']')
    end = end[:-1]
    end_as_int = int(end)
    ptr = <char*><stdint.uintptr_t>end_as_int
    return ptr[:s.length]

def example_func2(MyStringClass[::1] s):
    print(convert_my_string_to_py_string(s[0], s.format))