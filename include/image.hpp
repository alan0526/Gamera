/*
 *
 * Copyright (C) 2001 Ichiro Fujinaga, Michael Droettboom, and Karl MacMillan
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

#ifndef kwm11162001_image_hpp
#define kwm11162001_image_hpp

#include "pixel.hpp"
#include <stddef.h>

namespace Gamera {

  /*
    imageBase

    This is the base class for all matrices.
  */
  template<class T> class ImageBase : public Rect {
  public:

    ImageBase(size_t origin_y = 0, size_t origin_x = 0, size_t nrows = 1,
	      size_t ncols = 1)
      : Rect(origin_y, origin_x, nrows, ncols) { }
    ImageBase(const Point& upper_left, const Point& lower_right)
      : Rect(upper_left, lower_right) { }
    ImageBase(const Point& upper_left, const Size& size)
      : Rect(upper_left, size) { }
    ImageBase(const Point& upper_left, const Dimensions& dim)
      : Rect(upper_left, dim) { }

    ImageBase(const Rect& rect) : Rect(rect) { }
    size_t depth() const { return sizeof(T) * 8; }
    size_t ncolors() const { return 1; }
    float resolution() const { return m_resolution; }
    void resolution(float r) { m_resolution = r; }
  protected:
    float m_resolution;
  };

  size_t ImageBase<OneBitPixel>::depth() const { return 1; }
  size_t ImageBase<RGBPixel>::ncolors() const { return 3; }
  size_t ImageBase<RGBPixel>::depth() const { return 8; }

};

#endif
