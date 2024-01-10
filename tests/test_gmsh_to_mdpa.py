from gmsh_to_mdpa import GMshToMdpaConverter

import unittest
import os


class TestGmshToMdpaConverter2D(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'test_2d')
        mesh_filepath = os.path.join(cls.dir_path, 'mesh2d.msh')
        cls.converter = GMshToMdpaConverter(msh_filename=mesh_filepath)
        cls.converter.read_all()
        cls.parameter_filepath = os.path.join(cls.dir_path, 'mesh_parameters.json')

    @classmethod
    def tearDownClass(cls):
        out_path = os.path.join(cls.dir_path, 'mesh2d.mdpa')
        os.remove(out_path)

    def test_read_physical_names(self):
        ref_dict = {1: 'quad_elems',
                    2: 'tri_elems',
                    3: 'edges'}

        self.assertListEqual(list(self.converter.physical_names_dict.keys()), list(ref_dict.keys()))
        for phy_tag, phy_name in self.converter.physical_names_dict.items():
            self.assertEqual(ref_dict[phy_tag], phy_name)

    def test_read_nodes(self):
        ref_nodes = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [2, 0, 0], [2, 1, 0]]
        nodal_coordinates = [[node.x, node.y, node.z] for node in self.converter.nodes]
        self.assertListEqual(nodal_coordinates, ref_nodes)

    def test_read_physical_group_entities(self):
        ref_node_ids = [1, 2, 3, 4, 5, 6]
        phy_names = ['quad_elems', 'tri_elems', 'edges']
        ref_elements = {'quad_elems': [[1, 2, 3, 4], [2, 5, 6, 3]],
                        'tri_elems': [[1, 2, 4], [4, 2, 3], [2, 5, 3], [3, 5, 6]],
                        'edges': [[1, 2], [2, 5], [5, 6], [6, 3], [3, 4], [4, 1]]}
        for name in phy_names:
            node_ids = self.converter.physical_group_nodes[name]
            elements = [[node.id for node in elem.nodes] for elem in self.converter.physical_group_elements[name]]
            self.assertListEqual([node.id for node in node_ids], ref_node_ids)
            self.assertListEqual(elements, ref_elements[name])

    def test_write(self):
        self.converter.write(self.parameter_filepath)
        with open(os.path.join(self.dir_path, 'ref_mesh2d.mdpa'), 'r') as f:
            ref_lines = [line.strip() for line in f.readlines()]
        with open(os.path.join(self.dir_path, 'mesh2d.mdpa'), 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        self.assertListEqual(ref_lines, lines)


class TestGmshToMdpaConverter3D(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'test_3d')
        mesh_filepath = os.path.join(cls.dir_path, 'mesh3d.msh')
        cls.converter = GMshToMdpaConverter(msh_filename=mesh_filepath)
        cls.converter.read_all()
        cls.parameter_filepath = os.path.join(cls.dir_path, 'mesh_parameters.json')

    @classmethod
    def tearDownClass(cls):
        out_path = os.path.join(cls.dir_path, 'mesh3d.mdpa')
        os.remove(out_path)

    def test_read_physical_names(self):
        ref_dict = {1: 'hex_elems',
                    2: 'left_faces',
                    3: 'right_faces',
                    4: 'bottom_faces',
                    5: 'top_faces',
                    6: 'side_faces'}

        self.assertListEqual(list(self.converter.physical_names_dict.keys()), list(ref_dict.keys()))
        for phy_tag, phy_name in self.converter.physical_names_dict.items():
            self.assertEqual(ref_dict[phy_tag], phy_name)

    def test_read_nodes(self):
        ref_nodes = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], [2, 0, 0],
                     [2, 1, 0], [2, 1, 1], [2, 0, 1]]
        nodal_coordinates = [[node.x, node.y, node.z] for node in self.converter.nodes]
        self.assertListEqual(nodal_coordinates, ref_nodes)

    def test_read_physical_group_entities(self):
        phy_names = ['hex_elems', 'top_faces', 'bottom_faces', 'side_faces']
        ref_elements = {'hex_elems': [[1, 2, 3, 4, 5, 6, 7, 8], [2, 9, 10, 3, 6, 12, 11, 7]],
                        'top_faces': [[5, 6, 7, 8], [6, 12, 11, 7]],
                        'bottom_faces': [[1, 4, 3, 2], [2, 3, 10, 9]],
                        'side_faces': [[10, 3, 7, 11], [3, 4, 8, 7], [1, 2, 6, 5], [2, 9, 12, 6]]}
        ref_nodes = {'hex_elems': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                     'top_faces': [5, 6, 7, 8, 11, 12],
                     'bottom_faces': [1, 2, 3, 4, 9, 10],
                     'side_faces': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
        for name in phy_names:
            node_ids = self.converter.physical_group_nodes[name]
            elements = [[node.id for node in elem.nodes] for elem in self.converter.physical_group_elements[name]]
            self.assertListEqual([node.id for node in node_ids], ref_nodes[name])
            self.assertListEqual(elements, ref_elements[name])

    def test_write(self):
        self.converter.write(self.parameter_filepath)
        with open(os.path.join(self.dir_path, 'ref_mesh3d.mdpa'), 'r') as f:
            ref_lines = [line.strip() for line in f.readlines()]
        with open(os.path.join(self.dir_path, 'mesh3d.mdpa'), 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        self.assertListEqual(ref_lines, lines)


if __name__ == '__main__':
    unittest.main()
