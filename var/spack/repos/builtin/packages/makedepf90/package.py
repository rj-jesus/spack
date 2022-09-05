# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Makedepf90(AutotoolsPackage):
    """Makedepf90 is a program for automatic creation of Makefile-style
    dependency lists for Fortran source code."""

    homepage = "https://salsa.debian.org/science-team/makedepf90"
    url = "https://salsa.debian.org/science-team/makedepf90/-/archive/debian/3.0.0-2/makedepf90-debian-3.0.0-2.tar.gz"
    git = 'https://salsa.debian.org/science-team/makedepf90.git'

    maintainers = ['rj-jesus']

    version('latest', branch='debian/latest')
    version('3.0.0-2', sha256='7e7b54aba06e58183e9473a437d90fa06a0dc295287a9080e28b3d754e1b79a8')
