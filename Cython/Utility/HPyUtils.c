/////////////// HPyInitCode ///////////////
//@substitute: naming

#if CYTHON_COMPILING_IN_HPY
  //HPy Context Macros 
  #define __PYX_CONTEXT_TYPE HPyContext *
  #define __PYX_CONTEXT_ONLY_ARG_DEF __PYX_CONTEXT_TYPE $context_cname
  #define __PYX_CONTEXT_FIRST_ARG_DEF __PYX_CONTEXT_TYPE $context_cname,
  #define __PYX_CONTEXT_FIRST_ARG_MACRO_DEF $context_cname,
  #define __PYX_CONTEXT_CALL(maybe_comma) $hpy_context_cname maybe_comma

  //HPy to/from PyObject Functions (these should eventually be deleted)
  #define __PYX_HPY_LEGACY_OBJECT_FROM(o) HPy_FromPyObject(__PYX_CONTEXT_TYPE, o)
  #define __PYX_HPY_LEGACY_OBJECT_AS(o) HPy_AsPyObject(__PYX_CONTEXT_TYPE, o)
  #define __PYX_HPY_LEGACY_OBJECT_ARRAY_AS(o, ssize) HPy_AsPyObjectArray(__PYX_CONTEXT_TYPE, o, ssize)
#else
  //HPy Context Macros
  #define __PYX_CONTEXT_ONLY_ARG_DEF void
  #define __PYX_CONTEXT_FIRST_ARG_DEF
  #define __PYX_CONTEXT_FIRST_ARG_MACRO_DEF
  #define __PYX_CONTEXT_CALL(maybe_comma)

  //HPy to/from PyObject Functions (again, should eventually be deleted)
  #define __PYX_HPY_LEGACY_OBJECT_FROM(o) o
  #define __PYX_HPY_LEGACY_OBJECT_AS(o) o
  #define __PYX_HPY_LEGACY_OBJECT_ARRAY_AS(o, ssize) o
#endif
  