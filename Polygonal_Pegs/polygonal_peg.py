"""Code associated with lyx doc Square_Peg_in_a_Round_Hole. For details see:

  https://github.com/ruminations/Essays/tree/master/Polygonal_Pegs

The code in this file is placed in the Public Domain - 2017"""

from math import pi,cos,sin,tan,sqrt

def qsolve(a,b,c):
  """Solve quadratic equation ax^2+bx+c=0."""
  p,q = -b/2/a,c/a
  r=sqrt(p*p-q)
  return p+r,p-r

class PolygonalPeg(object):
  """Encapsulate calculations related to creating a polygonal hole
     using circular drills. The side length of the polygon defaults
     to a length of two units.
  """# hash marks permit error free cut and paste into interpreter command line
  def __init__(self,n,side=2.0):
    """'n' is the number of sides to the polygon."""
    self._n=float(n); self._h=side/2.0
  #
  @property
  def alpha(self):
    """Return the central angle subtended by the side of this 'n'-gon."""
    return 2.0*pi/self._n
  #
  @property
  def beta(self):
    """Return the angle between adjacent sides of an 'n'-gon."""
    return pi-self.alpha
  #
  @property
  def a(self):
    """The quadratic coefficient for n-gon peg r/R quadratic"""
    beta=self.beta
    u=2.0*cos(beta/2.0)+sin(2.0*beta)/2.0
    v=sin(beta); v=v*v
    return u*u+v*v
  #
  @property
  def b(self):
    """The linear coefficient for n-gon peg r/R quadratic"""
    beta=self.beta; u=cos(beta/2.0)
    return -2.0*u*(4.0*u+sin(2.0*beta))
  #
  @property
  def c(self):
    """The constant coefficient for n-gon peg r/R quadratic"""
    u=cos(self.beta/2.0)
    return 4*u*u*u*u
  #
  @property
  def r_R(self):
    """The invariant r/R for n-gon peg problem"""
    return min(qsolve(self.a,self.b,self.c))
  #
  @property
  def h_R(self):
    beta=self.beta
    u,v = cos(beta/2.0),sin(beta)
    rR=self.r_R
    x,y = 2.0*rR*u*u*u,u*sqrt(1.0-rR*rR*v*v)
    return max(x+y,x-y)
  #
  @property
  def R(self):
    """Return the radius of the large drill."""
    return round(self._h/self.h_R,14)
  #
  @property
  def r(self):
    """Return the radius of the small drill."""
    return round(self.R*self.r_R,14)
  #
  @property
  def vertex(self):
    """Return the distance from the center to a vertex."""
    return round(self._h/cos(self.beta/2.0),14)
  #
  @property
  def side_center(self):
    """Return the distance from the center to the center of a side."""
    return round(self.vertex*sin(self.beta/2.0),14)
  #
  @property
  def inscribe(self):
    """Return the side length of the clearance polygon."""
    return 2.0*self._h
  #
  @property
  def circumscribe(self):
    """Return the side length of the interference polygon."""
    return round(2.0*self.R/tan(self.beta/2.0),14)
  #
  @property
  def intersection(self):
    """Return the canonical intersection point of the small and large
       drills as a complex number. This assumes the primary vertex is
       on the y-axis and the polygon is symmetric on the x-axis."""
    delta=complex(sin(self.beta/2.0),-cos(self.beta/2.0)) # unit vector
    delta=2.0*self.r*cos(self.beta/2.0)*delta # scale by projection
    return self.vertex*1j+delta
  #
  @property
  def mesh(self):
    """Return the radius of a circle tangent to all small drill openings.
       This is the pitch radius of a gear that meshes with gears having a
       pitch radius he same as the small drill opening."""
    return self.vertex-2*self.r
 
