/*
 *
 * Copyright (C) 2002 Ichiro Fujinaga, Michael Droettboom, and Karl MacMillan
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

#include "gameramodule.hpp"

using namespace Gamera;

extern "C" {
  static PyObject* dimensions_new(PyTypeObject* pytype, PyObject* args,
			    PyObject* kwds);
  static void dimensions_dealloc(PyObject* self);
  static int dimensions_set_nrows(PyObject* self, PyObject* value);
  static PyObject* dimensions_get_nrows(PyObject* self);
  static int dimensions_set_ncols(PyObject* self, PyObject* value);
  static PyObject* dimensions_get_ncols(PyObject* self);
  static PyObject* dimensions_richcompare(PyObject* a, PyObject* b, int op);
  static PyObject* dimensions_repr(PyObject* self);
}

static PyTypeObject DimensionsType = {
  PyObject_HEAD_INIT(NULL)
  0,
};

static PyGetSetDef dimensions_getset[] = {
  { "nrows", (getter)dimensions_get_nrows, (setter)dimensions_set_nrows,
    "the current number of rows", 0},
  { "ncols", (getter)dimensions_get_ncols, (setter)dimensions_set_ncols,
    "the current number of columns", 0},
  { NULL }
};

bool is_DimensionsObject(PyObject* x) {
  if (PyObject_TypeCheck(x, &DimensionsType))
    return true;
  else
    return false;
}

PyObject* create_DimensionsObject(const Dimensions& p) {
  DimensionsObject* so;
  so = (DimensionsObject*)DimensionsType.tp_alloc(&DimensionsType, 0);
  so->m_x = new Dimensions(p);
  return (PyObject*)so;
}

static PyObject* dimensions_new(PyTypeObject* pytype, PyObject* args,
			  PyObject* kwds) {
  int x, y;
  if (PyArg_ParseTuple(args, "ii", &x, &y) <= 0)
    return 0;
  DimensionsObject* so;
  so = (DimensionsObject*)pytype->tp_alloc(pytype, 0);
  so->m_x = new Dimensions((size_t)x, (size_t)y);
  return (PyObject*)so;
}

static void dimensions_dealloc(PyObject* self) {
  if (!is_DimensionsObject(self)) {
    PyErr_SetString(PyExc_TypeError, "self not a Dimensions object");
  }
  DimensionsObject* x = (DimensionsObject*)self;
  delete x->m_x;
  self->ob_type->tp_free(self);
}

#define CREATE_GET_FUNC(name) static PyObject* dimensions_get_##name(PyObject* self) {\
  if (!is_DimensionsObject(self)) { \
    PyErr_SetString(PyExc_TypeError, "Object is not a Dimensions object!"); \
    return 0; \
  } \
  Dimensions* x = ((DimensionsObject*)self)->m_x; \
  return Py_BuildValue("i", (int)x->name()); \
}

#define CREATE_SET_FUNC(name) static int dimensions_set_##name(PyObject* self, PyObject* value) {\
  if (!is_DimensionsObject(self) || !PyInt_Check(value)) { \
    PyErr_SetString(PyExc_TypeError, "Type Error!"); \
    return -1; \
  } \
  Dimensions* x = ((DimensionsObject*)self)->m_x; \
  x->name((size_t)PyInt_AS_LONG(value)); \
  return 0; \
}

CREATE_GET_FUNC(nrows)
CREATE_SET_FUNC(nrows)
CREATE_GET_FUNC(ncols)
CREATE_SET_FUNC(ncols)

static PyObject* dimensions_richcompare(PyObject* a, PyObject* b, int op) {
  if (!is_DimensionsObject(a) || !is_DimensionsObject(b)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  Dimensions& ap = *((DimensionsObject*)a)->m_x;
  Dimensions& bp = *((DimensionsObject*)b)->m_x;

  /*
    Only equality and inequality make sense.
  */
  bool cmp;
  switch (op) {
  case Py_LT:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  case Py_LE:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  case Py_EQ:
    cmp = ap == bp;
    break;
  case Py_NE:
    cmp = ap != bp;
    break;
  case Py_GT:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  case Py_GE:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  default:
    return 0; // cannot happen
  }
  if (cmp) {
    Py_INCREF(Py_True);
    return Py_True;
  } else {
    Py_INCREF(Py_False);
    return Py_False;
  }
}

static PyObject* dimensions_repr(PyObject* self) {
  if (!is_DimensionsObject(self)) {
    PyErr_SetString(PyExc_TypeError, "Self if not a Dimensions object!");
    return 0;
  }
  Dimensions* x = ((DimensionsObject*)self)->m_x;
  return PyString_FromFormat("<gamera.Dimensions nrows: %i ncols: %i>",
			     x->nrows(), x->ncols());
}

void init_DimensionsType(PyObject* module_dict) {
  DimensionsType.ob_type = &PyType_Type;
  DimensionsType.tp_name = "gamera.Dimensions";
  DimensionsType.tp_basicsize = sizeof(DimensionsObject);
  DimensionsType.tp_dealloc = dimensions_dealloc;
  DimensionsType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
  DimensionsType.tp_new = dimensions_new;
  DimensionsType.tp_getattro = PyObject_GenericGetAttr;
  DimensionsType.tp_alloc = PyType_GenericAlloc;
  DimensionsType.tp_richcompare = dimensions_richcompare;
  DimensionsType.tp_getset = dimensions_getset;
  DimensionsType.tp_free = _PyObject_Del;
  DimensionsType.tp_repr = dimensions_repr;
  PyDict_SetItemString(module_dict, "Dimensions", (PyObject*)&DimensionsType);
}
