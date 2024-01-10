import numpy as np
from collections import namedtuple
from collections import defaultdict
import json
import math
import argparse

'''
This python script converts gmsh (format 2.2) to kratos mesh format (mdpa).
'''


def find_lines_between_strings(filename, begin_string, end_string):
    start_index = 0
    end_index = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if begin_string in line:
            start_index = i + 1
        if end_string in line:
            end_index = i
    return lines[start_index:end_index]


Node = namedtuple('Node', ['id', 'x', 'y', 'z'])


class Element:
    Geometry = namedtuple('geometry', ['gmsh_name', 'size'])
    Line3D2N = Geometry(gmsh_name='2-node line', size=2)
    Tri3D3N = Geometry(gmsh_name='3-node triangle', size=3)
    Quad3D4N = Geometry(gmsh_name='4-node quadrangle', size=4)
    Tet3D4N = Geometry(gmsh_name='4-node tetrahedraon', size=4)
    Hex3D8N = Geometry(gmsh_name='8-node hexahedron', size=8)
    Line3D3N = Geometry(gmsh_name='3-node line', size=3)
    Tri3D6N = Geometry(gmsh_name='6-node triangle', size=6)
    geometry_dict = {1: Line3D2N,
                     2: Tri3D3N,
                     3: Quad3D4N,
                     4: Tet3D4N,
                     5: Hex3D8N,
                     8: Line3D3N,
                     9: Tri3D6N}

    def __init__(self, id, element_type_tag):
        self.geometry = Element.geometry_dict[element_type_tag]
        self.id = id
        self.__nodes = None

        @property
        def nodes():
            return self.__nodes

        @nodes.setter
        def nodes(nodes):
            if len(nodes) == self.geometry.size:
                self.__nodes = nodes
            else:
                raise RuntimeError(f'Wrong number of nodes given for the element.\n'
                                   f'Number of nodes: {len(nodes)}\n'
                                   f'Number of nodes for element tag {element_type_tag}: {self.geometry.size}')


SubModelPart = namedtuple('SubModelPart',
                          ['name', 'physical_group_name', 'node_ids', 'element_ids', 'condition_ids'])


class GMshToMdpaConverter:

    def __init__(self, msh_filename):
        self.filename = msh_filename
        self.physical_names_dict = {}
        self.__nodes = {}
        self.physical_group_elements = defaultdict(list)
        self.physical_group_nodes = {}

    @property
    def nodes(self):
        return self.__nodes.values()

    def read_all(self):
        self.read_nodes()
        self.read_physical_group_entities()

    def read_physical_names(self):
        physical_name_lines = find_lines_between_strings(self.filename, '$PhysicalNames', '$EndPhysicalNames')
        nr_physical_names = int(physical_name_lines[0])
        for line in physical_name_lines[1:]:
            dimension, tag, name = line.strip().split()
            self.physical_names_dict[int(tag)] = name.replace('"', '')

        if not (nr_physical_names == len(self.physical_names_dict.keys())):
            raise RuntimeError(f'Error in parsing physical names\n'
                               f'Number of physical names given in {self.filename}: {nr_physical_names}\n'
                               f'Number of physical names: {len(self.physical_names_dict.keys())}')

    def read_nodes(self):
        node_lines = find_lines_between_strings(self.filename, '$Nodes', '$EndNodes')
        nr_nodes = int(node_lines[0].strip())
        for line in node_lines[1:]:
            node_id = int(line.strip().split()[0])
            nodal_coord = list(map(float, line.strip().split()[1:]))
            self.__nodes[node_id] = Node(id=node_id, x=nodal_coord[0], y=nodal_coord[1], z=nodal_coord[2])

        if not (len(self.nodes) == nr_nodes):
            raise RuntimeError(f'Error in parsing nodes\n'
                               f'Number of nodes given in {self.filename}: {nr_nodes}\n'
                               f'Number of nodal coordinates: {len(self.nodes)}')

    def read_physical_group_entities(self):
        self.read_physical_names()
        element_lines = find_lines_between_strings(self.filename, '$Elements', '$EndElements')
        for line in element_lines[1:]:
            element_line = line.strip().split()
            element_id = int(element_line[0])
            element_type_tag = int(element_line[1])
            physical_tag = int(element_line[3])
            element_i = Element(element_id, element_type_tag)
            node_ids = list(map(int, element_line[-element_i.geometry.size:]))
            element_i.nodes = [self.__nodes[node_id] for node_id in node_ids]
            phy_grp_name = self.physical_names_dict[physical_tag]
            self.physical_group_elements[phy_grp_name].append(element_i)

        for phy_grp_name in self.physical_names_dict.values():
            node_ids = [node.id for elem in self.physical_group_elements[phy_grp_name] for node in elem.nodes]
            node_ids = list(set(node_ids))
            nodes = [self.__nodes[node_id] for node_id in node_ids]
            self.physical_group_nodes[phy_grp_name] = nodes

    def write(self, parameter_file):

        with open(parameter_file, 'r') as f:
            parameters = json.load(f)

        for sub_mp_param in parameters['sub_model_parts']:
            phy_grp_name = sub_mp_param['physical_group_name']
            if phy_grp_name not in self.physical_names_dict.values():
                raise RuntimeError(f'Physical group: {phy_grp_name} does not exist in {self.filename}')

        precision = parameters.get('precision', 10)
        out_filename = self.filename.replace('.msh', '.mdpa')
        nodal_width = self.get_width(np.arange(1, len(self.nodes) + 1))
        x_coords = np.array([node.x for node in self.nodes])
        y_coords = np.array([node.y for node in self.nodes])
        z_coords = np.array([node.z for node in self.nodes])
        x_coord_width = self.get_width(x_coords, precision=precision)
        y_coord_width = self.get_width(y_coords, precision=precision)
        z_coord_width = self.get_width(z_coords, precision=precision)

        with open(out_filename, 'w') as out_file:
            out_file.write(f'Begin ModelPartData\n'
                           f'//  VARIABLE_NAME value\n'
                           f'End ModelPartData\n')
            out_file.write(f'Begin Properties 0\n'
                           f'End Properties\n')

            out_file.write(f'Begin Nodes\n')
            for node in self.nodes:
                out_file.write(
                    f'{node.id:>{nodal_width}}\t{node.x:> {x_coord_width}.{precision}f}\t'
                    f'{node.y:> {y_coord_width}.{precision}f}\t{node.z:> {z_coord_width}.{precision}f}\n')
            out_file.write(f'End Nodes\n')

            sub_model_part_list = []
            elem_id = 1
            cond_id = 1
            for sub_mp_param in parameters['sub_model_parts']:
                element_name = sub_mp_param.get('element_name', '')
                condition_name = sub_mp_param.get('condition_name', '')
                if element_name and condition_name:
                    raise RuntimeError(
                        'condition_name and element_name in one sub_model_part dictionary is not allowed.')
                elif element_name:
                    elem_ids = []
                    phy_grp_name = sub_mp_param['physical_group_name']
                    prop_id = sub_mp_param['property_id']
                    elements = self.physical_group_elements[phy_grp_name]
                    out_file.write(f'Begin Elements {element_name} // GUI group identifier: {phy_grp_name}\n')
                    for elem in elements:
                        elem_ids.append(elem_id)
                        out_file.write(f'{elem_id:>{nodal_width}}\t{prop_id:>3}\t')
                        for node in elem.nodes:
                            out_file.write(f'{node.id:>{nodal_width}}\t')
                        out_file.write('\n')
                        elem_id += 1
                    out_file.write(f'End Elements\n')
                    sub_mp_name = sub_mp_param['sub_model_part_name']
                    sub_mp_node_ids = [node.id for node in self.physical_group_nodes[phy_grp_name]]
                    sub_model_part = SubModelPart(name=sub_mp_name, physical_group_name=phy_grp_name,
                                                  node_ids=sub_mp_node_ids, element_ids=elem_ids, condition_ids=[])
                    sub_model_part_list.append(sub_model_part)
                elif condition_name:
                    cond_ids = []
                    phy_grp_name = sub_mp_param['physical_group_name']
                    prop_id = sub_mp_param['property_id']
                    conditions = self.physical_group_elements[phy_grp_name]
                    out_file.write(f'Begin Conditions {condition_name} // GUI group identifier: {phy_grp_name}\n')
                    for cond in conditions:
                        cond_ids.append(cond_id)
                        out_file.write(f'{cond_id:>{nodal_width}}\t{prop_id:>3}\t')
                        for node in cond.nodes:
                            out_file.write(f'{node.id:>{nodal_width}}\t')
                        out_file.write('\n')
                        cond_id += 1
                    out_file.write(f'End Conditions\n')
                    sub_mp_name = sub_mp_param['sub_model_part_name']
                    sub_mp_node_ids = [node.id for node in self.physical_group_nodes[phy_grp_name]]
                    sub_model_part = SubModelPart(name=sub_mp_name, physical_group_name=phy_grp_name,
                                                  node_ids=sub_mp_node_ids, element_ids=[], condition_ids=cond_ids)
                    sub_model_part_list.append(sub_model_part)
                else:
                    phy_grp_name = sub_mp_param['physical_group_name']
                    sub_mp_name = sub_mp_param['sub_model_part_name']
                    sub_mp_node_ids = [node.id for node in self.physical_group_nodes[phy_grp_name]]
                    sub_model_part = SubModelPart(name=sub_mp_name, physical_group_name=phy_grp_name,
                                                  node_ids=sub_mp_node_ids, element_ids=[], condition_ids=[])
                    sub_model_part_list.append(sub_model_part)

            for sub_mp in sub_model_part_list:
                out_file.write(f'Begin SubModelPart {sub_mp.name} // Group {sub_mp.physical_group_name}\n')

                out_file.write('Begin SubModelPartNodes\n')
                for node_id in sub_mp.node_ids:
                    out_file.write(f'{node_id}\n')
                out_file.write('End SubModelPartNodes\n')

                out_file.write('Begin SubModelPartElements\n')
                for elem_id in sub_mp.element_ids:
                    out_file.write(f'{elem_id}\n')
                out_file.write('End SubModelPartElements\n')

                out_file.write('Begin SubModelPartConditions\n')

                for cond_id in sub_mp.condition_ids:
                    out_file.write(f'{cond_id}\n')
                out_file.write('End SubModelPartConditions\n')

                out_file.write(f'End SubModelPart // Group {sub_mp.physical_group_name}\n')

    def get_width(self, values, precision=0):
        max_value = np.max(np.abs(values))
        try:
            width = math.ceil(math.log10(max_value)) + precision + 2  # sign + decimal
        except ValueError:
            width = precision + 2
        return width


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This python script converts gmsh (format 2.2) to kratos mesh format(mdpa)',
        usage='python gmsh_to_mdpa.py <mesh_filepath> <parameters_filepath> \n'
              'or execute python gmsh_to_mdpa.py -h for help.')
    parser.add_argument('mesh_filepath', type=str, help='path of the gmsh file (.msh) written in 2.2 mesh format')
    parser.add_argument('parameters_filepath', type=str,
                        help='path of the parameter file in json format listing the details of the SubModelParts')
    args = parser.parse_args()
    converter = GMshToMdpaConverter(msh_filename=args.mesh_filepath)
    converter.read_all()
    converter.write(parameter_file=args.parameters_filepath)
