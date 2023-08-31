# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AsimovCcs(Package):
    """ASiMoV-CCS is a new Computation Fluid Dynamics (CFD) and Combustion
    modelling code that aims to achieve the world's first high fidelity
    simulation of a complete gas-turbine engine during operation,
    simultaneously including the effects of thermo-mechanics, electro-magnetics
    and CFD."""

    homepage = "https://github.com/asimovpp/asimov-ccs"
    url = "https://github.com/asimovpp/asimov-ccs/archive/refs/tags/v0.2.1.tar.gz"
    git = "https://github.com/asimovpp/asimov-ccs.git"

    maintainers = ['rj-jesus']

    version('develop', branch='develop')
    version('0.4', commit='fe50cdd0abfa5887a47fe0efe714cf1811dfe55b')
    version('20220908', commit='fbdaa943292a1077a68122436399c58334b0f654')
    version('0.2.1', sha256='de69819b6aa48515ffb33e6d36dfc01c795ebdc0133ee9c35a0182253d3690a6')

    variant('uvp_debug', default=False, description='Generates u, v and p files for debug')

    # Comment out code that generates u, v and p files
    patch('uvp_debug.patch', when='~uvp_debug')

    # Supported compilers and corresponding build option
    compilers = {
        'gcc': 'gnu',
        'cce': 'cray',
        'intel': 'intel',
    }

    depends_on('mpi')
    depends_on('petsc@3.17:')
    depends_on('adios2+hdf5')
    depends_on('kahip')
    depends_on('fortran-yaml-c')

    depends_on('makedepf90', type='build')
    depends_on('py-pyyaml', type='build')

    def patch(self):
        filter_file(r'${FYAML}/build', r'${FYAML}', 'Makefile', string=True)

    def setup_build_environment(self, env):
        env.set('CCS_DIR',   self.stage.source_path)
        env.set('PETSC_DIR', self.spec['petsc'].prefix)
        env.set('FYAML',     self.spec['fortran-yaml-c'].prefix)
        env.set('ADIOS2',    self.spec['adios2'].prefix)
        env.set('PARHIP',    self.spec['kahip'].prefix)

    def install(self, spec, prefix):
        compiler = self.compilers[spec.compiler.name]
        make('CMP=%s' % compiler, 'all')

        install_tree('.', prefix)
