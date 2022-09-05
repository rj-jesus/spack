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
    version('0.2.1', sha256='de69819b6aa48515ffb33e6d36dfc01c795ebdc0133ee9c35a0182253d3690a6')

    # note: this could be picked up from the environment, or at least raise a
    # conflict if the wrong compiler is being used
    variant('cmp', default='gnu', description='Compilation environment',
                   values=('cray', 'gnu', 'intel'), multi=False)

    depends_on('mpi')
    depends_on('petsc@3.14.2')
    depends_on('adios2+hdf5')
    depends_on('kahip')

    depends_on('makedepf90', type='build')
    depends_on('fortran-yaml-cpp', type='build')
    depends_on('py-pyyaml', type='build')

    def patch(self):
        filter_file(r'${FYAML}/build', r'${FYAML}', 'Makefile', string=True)

    def setup_build_environment(self, env):
        env.set('CCS_DIR',   self.stage.source_path)
        env.set('PETSC_DIR', self.spec['petsc'].prefix)
        env.set('FYAML',     self.spec['fortran-yaml-cpp'].prefix)
        env.set('ADIOS2',    self.spec['adios2'].prefix)
        env.set('PARHIP',    self.spec['kahip'].prefix)

    def install(self, spec, prefix):
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc

        make('CMP=%s' % spec.variants['cmp'].value, 'all')

        mkdirp(prefix.bin)
        install('ccs_app', prefix.bin)
        install_tree('tests', prefix.share.tests)
