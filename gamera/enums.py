#
# Copyright (C) 2001-2005 Ichiro Fujinaga, Michael Droettboom, and Karl MacMillan
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

ONEBIT = 0
GREYSCALE = 1
GREY16 = 2
RGB = 3
FLOAT = 4
COMPLEX = 5
ALL = [ONEBIT, GREYSCALE, GREY16, RGB, FLOAT, COMPLEX]
NON_COMPLEX_TYPES = ALL[:]
NON_COMPLEX_TYPES.remove(COMPLEX)
NONIMAGE = -1

DENSE = 0
RLE = 1
