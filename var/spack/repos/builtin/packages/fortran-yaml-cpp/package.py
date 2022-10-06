# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FortranYamlCpp(CMakePackage):
    """fortran-yaml-cpp is YAML parser for Fortran matching the YAML 1.2 spec.
    It uses the C++ package `yaml-cpp' parse yaml documents, then stores the
    data in Fortran derived types created by fortran-yaml."""

    homepage = "https://github.com/Nicholaswogan/fortran-yaml-cpp"
    git = "https://github.com/Nicholaswogan/fortran-yaml-cpp.git"

    maintainers = ['rj-jesus']

    version('main', branch='main', submodules=True, preferred=True)

    variant('shared', default=True, description='Builds a shared version of the library')

    patch('cmake.patch')

    def patch(self):
        if '+shared' in self.spec:
            filter_file(r'add_library(fortran-yaml-cpp yaml_types.f90 yaml.f90 yaml.cpp)',
                        r'add_library(fortran-yaml-cpp SHARED yaml_types.f90 yaml.f90 yaml.cpp)',
                        'CMakeLists.txt', string=True)

        if '%nvhpc' in self.spec:
            filter_file(r'-Weffc++', r'', 'yaml-cpp/CMakeLists.txt', string=True)
            filter_file(r'-pedantic-errors', r'', 'yaml-cpp/CMakeLists.txt', string=True)

    def cmake_args(self):
        args = []
        if '+shared' in self.spec:
            args.append('-DYAML_BUILD_SHARED_LIBS=ON')
        return args
