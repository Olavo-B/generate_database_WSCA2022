from grn2dot.grn2dot import Grn2dot
import statistics as st 
import networkx as nx
import os
import pathlib
import csv
import time


'''
Expected input:

Seed 1656949570
ARCH 0|F_ID 0|LIMIT 4
12
67/130
1.925
2
before: 
4(2)
(8x9)
Number of not routing: 992 (99.20%)
after: 
4(2)
(8x9)
'''



def GRN_paths(path) -> dict:
    ''' Return a list with all nx.Digraph object of all GRN found in path
    '''

    GRN = []
    p = pathlib.Path(path)
    paths = list(p.glob('**/expressions.ALL.txt'))


    if not paths:
        print("ERROR: Paths to GRNs do not exist")
        quit

    names = get_grn_names(paths)
    for path in paths:
        grn2dot = Grn2dot(path)
        GRN.append(grn2dot.get_nx_digraph())


    return GRN,names


def get_grn_names(GRN: list) -> list:

    grn_names = []

    for grn in GRN:
        rato = str(grn)
        aux = rato.split('/')
        grn_names.append(aux[3])

    return grn_names


def find_all(name, path):
    ''' Find all path that have the file name, stating in the root path
    '''
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def read_file(path,grn_paths,table,arch=0):
    ''' Grab all result_mesh.txt from all grn and all functions, return a dict where
        the key is the grn name and the value is a list with results before and after 
        rooting

        Path: root_path -> results_by_function -> results_by_grn -> result_mesh.txt
    
    '''

    sorted_list = []
    list_of_grn = {}

    if arch == 0: results_paths = find_all('results_mesh.txt',path)
    elif arch == 1: results_paths = find_all('results_1-hop.txt',path)
    elif arch == 2: results_paths = find_all('results_chess.txt',path)

    GRN,grn_names = GRN_paths(grn_paths)

    aux = {}
    for grn,name in zip(GRN,grn_names):
        name = name.replace(' ','_')
        aux[name] = grn.number_of_nodes()

    aux = dict( sorted(aux.items(), key=lambda x:  x[1]))
    sorted_list = list(aux.keys())
    list_of_grn = {k:[] for k in sorted_list }

    for path in results_paths:
        aux = str(path).split('/')
        grn_name = aux[7]

    
        list_of_grn[grn_name].append(path)
    

    if table == 1: csv_header,row_scv = get_table_one(list_of_grn)
    elif table == 2: csv_header,row_scv = get_table_two(list_of_grn)

    timestr = time.strftime("%Y%m%d-%H%M%S")


    path = f"benchmark"  
    file_name = f'values_{timestr}.csv'


    isExist = os.path.exists(path)

    if not isExist:
  
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    completeName = os.path.join(path, file_name)


    with open(completeName, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(row_scv)

    return completeName

def get_table_one(list_of_grn):

    row_scv = []
    csv_hearder = ['name','A/V','mean_degree','best_square','best']


    for grn_name,i in zip(list_of_grn.keys(),range(len(list_of_grn))):
        grn = {}
        grn['name'] = grn_name
        grn_paths = list_of_grn[grn_name]

        for path in grn_paths:
            aux = str(path).split('/')
            f_name = aux[6]
            if(f_name != 'linear'): continue
            with open(path) as file:
                lines = file.readlines()
                grn['A/V'] = lines[3][:-1]
                grn['mean_degree'] = lines[4][:-1]
                grn['best'] = f'{lines[-1][:-1]} {lines[11][:-1]}'
        row_scv.append(grn)

    return csv_hearder,row_scv


        

def get_table_two(list_of_grn):

    row_scv = []
    csv_hearder = ['name','A/V','min_neigh','max_degree','linear_antes','linear_depois','poly_antes','poly_depois','exp_antes','exp_depois','limiar_antes','limiar_depois']
    

    for grn_name,i in zip(list_of_grn.keys(),range(len(list_of_grn))):
        grn = {}
        grn['name'] = grn_name
        grn_paths = list_of_grn[grn_name]
        for path in grn_paths:
            aux = str(path).split('/')
            f_name = aux[6]
            
            with open(path) as file:
                lines = file.readlines()
                grn['A/V'] = lines[3][:-1]
                grn['min_neigh'] = lines[5][:-1]
                grn['max_degree'] = lines[2][:-1]
                grn[f'{f_name}_antes'] = lines[7][:-1]
                grn[f'{f_name}_depois'] = lines[11][:-1]
        
        row_scv.append(grn)



    return csv_hearder,row_scv


        


    