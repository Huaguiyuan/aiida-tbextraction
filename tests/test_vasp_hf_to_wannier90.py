"""
Tests for the workflow that calculates the Wannier90 input from VASP with hybrid functionals.
"""

from insb_sample import get_insb_input  # pylint: disable=unused-import


def test_vasp_hf_wannier_input(
    configure_with_daemon,  # pylint: disable=unused-argument
    assert_finished,
    get_insb_input  # pylint: disable=redefined-outer-name
):
    """
    Runs the workflow that calculates Wannier90 inputs from VASP + hybrids on InSb with a coarse grid.
    """
    from aiida.orm import DataFactory
    from aiida.orm.data.base import List
    from aiida.work.launch import run_get_pid
    from aiida_tbextraction.fp_run.wannier_input import VaspWannierInput

    kpoints_mesh = DataFactory('array.kpoints')()
    kpoints_mesh.set_kpoints_mesh([2, 2, 2])

    wannier_projections = List()
    wannier_projections.extend(['In : s; px; py; pz', 'Sb : px; py; pz'])

    result, pid = run_get_pid(
        VaspWannierInput,
        kpoints_mesh=kpoints_mesh,
        wannier_parameters=DataFactory('parameter')(
            dict=dict(num_wann=14, num_bands=36, spinors=True)
        ),
        wannier_projections=wannier_projections,
        **get_insb_input
    )
    assert_finished(pid)
    assert all(
        key in result for key in
        ['wannier_input_folder', 'wannier_parameters', 'wannier_bands']
    )
    folder_list = result['wannier_input_folder'].get_folder_list()
    assert all(
        filename in folder_list
        for filename in ['wannier90.amn', 'wannier90.mmn', 'wannier90.eig']
    )
