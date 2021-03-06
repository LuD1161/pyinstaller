# -*- mode: python -*-
import sys
import os

CTYPES_DIR = "ctypes"
TEST_LIB = os.path.join(CTYPES_DIR, "testctypes")
if sys.platform == "linux2":
    TEST_LIB += ".so"
elif sys.platform[:6] == "darwin":
    TEST_LIB += ".dylib"
elif sys.platform == "win32":
    TEST_LIB += ".dll"
else:
    raise NotImplementedError

# If the required dylib does not reside in the current directory, the Analysis
# class machinery, based on ctypes.util.find_library, will not find it. This was
# done on purpose for this test, to show how to give Analysis class a clue.
os.environ["DYLD_LIBRARY_PATH"] = CTYPES_DIR
os.environ["LD_LIBRARY_PATH"] = CTYPES_DIR

# Check for presence of testctypes shared library, build it if not present
if not os.path.exists(TEST_LIB):
    os.chdir(CTYPES_DIR)
    if sys.platform[:6] == "darwin":
        os.system("gcc -Wall -dynamiclib testctypes.c -o testctypes.dylib -headerpad_max_install_names")
        id_dylib = os.path.abspath("testctypes.dylib")
        os.system("install_name_tool -id %s testctypes.dylib" % (id_dylib,))
    elif sys.platform == "linux2":
        os.system("gcc -fPIC -shared testctypes.c -o testctypes.so")
    else:
        raise NotImplementedError
    os.chdir("..")

__testname__ = 'test15'

a = Analysis(['../support/_mountzlib.py',
              '../support/useUnicode.py',
              'test15.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          name=os.path.join('dist', __testname__),
          debug=False,
          strip=False,
          upx=False,
          console=1 )
