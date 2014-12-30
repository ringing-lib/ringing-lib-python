#define PY_SSIZE_T_CLEAN
#include "Python.h"
#ifndef Py_PYTHON_H
    #error Python headers needed to compile C extensions, please install development version of Python.
#elif PY_VERSION_HEX < 0x02060000 || (0x03000000 <= PY_VERSION_HEX && PY_VERSION_HEX < 0x03020000)
    #error Cython requires Python 2.6+ or Python 3.2+.
#else

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC initringing(void); /*proto*/

PyMODINIT_FUNC initrow(void);
PyMODINIT_FUNC initchange(void);

PyMODINIT_FUNC initringing(void)
{
	initrow();
	initchange();
}
#else
PyMODINIT_FUNC PyInit_ringing(void); /*proto*/

PyMODINIT_FUNC PyInit_row(void);
PyMODINIT_FUNC PyInit_change(void);

PyMODINIT_FUNC PyInit_ringing(void)
{
	PyInit_row();
	PyInit_change();
}
#endif

#endif /* Py_PYTHON_H */
