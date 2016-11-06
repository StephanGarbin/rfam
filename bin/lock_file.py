# Copyright 2014 Tom SF Haines

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import random
import time



lock_dir_prefix = '.lock_'



class LockFile:
  """Rather simple lock file system, based on lock directories (as directory creation is atomic) - whilst crude this is about as safe a locking system as its possible to create."""
  def __init__(self, fn, mode='r'):
    self.fn = fn
    self.mode = mode
  
  def __enter__(self):
    # Keep trying to create a lock directory - this is safe on all platforms as directory creation is always atomic...
    # Calculate lock dircectory name...
    head, tail = os.path.split(self.fn)
    self.lock_dir = os.path.join(head, lock_dir_prefix + tail)
    
    # Get the lock...
    while True:
      try:
        os.mkdir(self.lock_dir)
        break
      except OSError:
        # Its locked - sleep for a slightly random period of milliseconds...
        time.sleep(1e-3 * random.randrange(1,9))
    
    # We are safe - open the file...
    try:
      self.f = open(self.fn, self.mode)
    except IOError:
      self.f = None
    
    return self.f
  
  def __exit__(self, etype, value, traceback):
    # Close file...
    if self.f!=None:
      self.f.close()
    
    # Terminate lock...
    os.rmdir(self.lock_dir)
    
    return etype==None



if '__main__'==__name__:
  with LockFile('test1.txt','w') as f:
    f.write('Hello\n')
  
  try:
    with LockFile('test2.txt','w') as f:
      f.write('Hello again\n')
      raise LookupError
  except LookupError:
    print('Lookup error received as expected')
