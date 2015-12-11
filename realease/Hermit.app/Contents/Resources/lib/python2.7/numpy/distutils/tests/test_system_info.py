from __future__ import division, print_function

import os
import shutil
from tempfile import mkstemp, mkdtemp

from numpy.distutils import ccompiler
from numpy.testing import TestCase, run_module_suite, assert_, assert_equal
from numpy.testing.decorators import skipif
from numpy.distutils.system_info import system_info, ConfigParser
from numpy.distutils.system_info import default_lib_dirs, default_include_dirs


def get_class(name, notfound_action=1):
    """
    notfound_action:
      0 - do nothing
      1 - display warning message
      2 - raise error
    """
    cl = {'temp1': TestTemp1,
          'temp2': TestTemp2
          }.get(name.lower(), test_system_info)
    return cl()

simple_site = """
[ALL]
library_dirs = {dir1:s}{pathsep:s}{dir2:s}
libraries = {lib1:s},{lib2:s}
extra_compile_args = -I/fake/directory
runtime_library_dirs = {dir1:s}

[temp1]
library_dirs = {dir1:s}
libraries = {lib1:s}
runtime_library_dirs = {dir1:s}

[temp2]
library_dirs = {dir2:s}
libraries = {lib2:s}
extra_link_args = -Wl,-rpath={lib2:s}
rpath = {dir2:s}
"""
site_cfg = simple_site

fakelib_c_text = """
/* This file is generated from numpy/distutils/testing/test_system_info.py */
#include<stdio.h>
void foo(void) {
   printf("Hello foo");
}
void bar(void) {
   printf("Hello bar");
}
"""


class test_system_info(system_info):

    def __init__(self,
                 default_lib_dirs=default_lib_dirs,
                 default_include_dirs=default_include_dirs,
                 verbosity=1,
                 ):
        self.__class__.info = {}
        self.local_prefixes = []
        defaults = {}
        defaults['library_dirs'] = ''
        defaults['include_dirs'] = ''
        defaults['runtime_library_dirs'] = ''
        defaults['rpath'] = ''
        defaults['src_dirs'] = ''
        defaults['search_static_first'] = "0"
        defaults['extra_compile_args'] = ''
        defaults['extra_link_args'] = ''
        self.cp = ConfigParser(defaults)
        # We have to parse the config files afterwards
        # to have a consistent temporary filepath

    def _check_libs(self, lib_dirs, libs, opt_libs, exts):
        """Override _check_libs to return with all dirs """
        info = {'libraries': libs, 'library_dirs': lib_dirs}
        return info


class TestTemp1(test_system_info):
    section = 'temp1'


class TestTemp2(test_system_info):
    section = 'temp2'


class TestSystemInfoReading(TestCase):

    def setUp(self):
        """ Create the libraries """
        # Create 2 sources and 2 libraries
        self._dir1 = mkdtemp()
        self._src1 = os.path.join(self._dir1, 'foo.c')
        self._lib1 = os.path.join(self._dir1, 'libfoo.so')
        self._dir2 = mkdtemp()
        self._src2 = os.path.join(self._dir2, 'bar.c')
        self._lib2 = os.path.join(self._dir2, 'libbar.so')
        # Update local site.cfg
        global simple_site, site_cfg
        site_cfg = simple_site.format(**{
            'dir1': self._dir1,
            'lib1': self._lib1,
            'dir2': self._dir2,
            'lib2': self._lib2,
            'pathsep': os.pathsep
        })
        # Write site.cfg
        fd, self._sitecfg = mkstemp()
        os.close(fd)
        with open(self._sitecfg, 'w') as fd:
            fd.write(site_cfg)
        # Write the sources
        with open(self._src1, 'w') as fd:
            fd.write(fakelib_c_text)
        with open(self._src2, 'w') as fd:
            fd.write(fakelib_c_text)
        # We create all class-instances

        def site_and_parse(c, site_cfg):
            c.files = [site_cfg]
            c.parse_config_files()
            return c
        self.c_default = site_and_parse(get_class('default'), self._sitecfg)
        self.c_temp1 = site_and_parse(get_class('temp1'), self._sitecfg)
        self.c_temp2 = site_and_parse(get_class('temp2'), self._sitecfg)

    def tearDown(self):
        # Do each removal separately
        try:
            shutil.rmtree(self._dir1)
        except:
            pass
        try:
            shutil.rmtree(self._dir2)
        except:
            pass
        try:
            os.remove(self._sitecfg)
        except:
            pass

    def test_all(self):
        # Read in all information in the ALL block
        tsi = self.c_default
        assert_equal(tsi.get_lib_dirs(), [self._dir1, self._dir2])
        assert_equal(tsi.get_libraries(), [self._lib1, self._lib2])
        assert_equal(tsi.get_runtime_lib_dirs(), [self._dir1])
        extra = tsi.calc_extra_info()
        assert_equal(extra['extra_compile_args'], ['-I/fake/directory'])

    def test_temp1(self):
        # Read in all information in the temp1 block
        tsi = self.c_temp1
        assert_equal(tsi.get_lib_dirs(), [self._dir1])
        assert_equal(tsi.get_libraries(), [self._lib1])
        assert_equal(tsi.get_runtime_lib_dirs(), [self._dir1])

    def test_temp2(self):
        # Read in all information in the temp2 block
        tsi = self.c_temp2
        assert_equal(tsi.get_lib_dirs(), [self._dir2])
        assert_equal(tsi.get_libraries(), [self._lib2])
        # Now from rpath and not runtime_library_dirs
        assert_equal(tsi.get_runtime_lib_dirs(key='rpath'), [self._dir2])
        extra = tsi.calc_extra_info()
        assert_equal(extra['extra_link_args'], ['-Wl,-rpath=' + self._lib2])

    def test_compile1(self):
        # Compile source and link the first source
        c = ccompiler.new_compiler()
        try:
            # Change directory to not screw up directories
            previousDir = os.getcwd()
            os.chdir(self._dir1)
            c.compile([os.path.basename(self._src1)], output_dir=self._dir1)
            # Ensure that the object exists
            assert_(os.path.isfile(self._src1.replace('.c', '.o')) or
                    os.path.isfile(self._src1.replace('.c', '.obj')))
            os.chdir(previousDir)
        except OSError:
            pass

    @skipif('msvc' in repr(ccompiler.new_compiler()))
    def test_compile2(self):
        # Compile source and link the second source
        tsi = self.c_temp2
        c = ccompiler.new_compiler()
        extra_link_args = tsi.calc_extra_info()['extra_link_args']
        try:
            # Change directory to not screw up directories
            previousDir = os.getcwd()
            os.chdir(self._dir2)
            c.compile([os.path.basename(self._src2)], output_dir=self._dir2,
                      extra_postargs=extra_link_args)
            # Ensure that the object exists
            assert_(os.path.isfile(self._src2.replace('.c', '.o')))
            os.chdir(previousDir)
        except OSError:
            pass

if __name__ == '__main__':
    run_module_suite()
