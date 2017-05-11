#!/usr/bin/env python2
# vim: ts=4 et sw=4 sts=4 :

# Standard library modules.
from __future__ import print_function
from __future__ import with_statement
import sys
import argparse
import cPickle as pickle

error_msg = "The module %s could not be found. Please use your system's package manager or pip to install it."



def main(sys_args):
    description = "View a data dump of any single node."
    parser = argparse.ArgumentParser(prog=sys_args, description=description)

    description = "The scanned data dump from the file that will get modified."
    parser.add_argument("-i", "--input", required=True, type=str, help=description)

    args = parser.parse_args()

    enrich_if_necessary(node_str, collected_data_dict, args.input)



def enrich_if_necessary(file_name):

    (node_str, collected_data_dict) = read_data(file_name)

    if is_enriched(collected_data_dict):
        return

    pids = collected_data_dict["proc_data"].keys()
    parents = collected_data_dict["parents"]
    collected_data_dict["children"] = parents_to_children(pids, parents)

    with open(file_name, "w") as fi:
        pickle.dump({node_str:collected_data_dict}, fi)



def read_data(file_name):

    with open(file_name, "r") as my_file:
        datastructure = pickle.load(my_file)


    assert len(datastructure.keys()) == 1

    node_str = datastructure.keys()[0]
    collected_data_dict = datastructure[node_str]

    return (node_str, collected_data_dict)



def is_enriched(collected_data_dict):
    enriched_keys = ["children","uid_name","gid_name"]

    for key in enriched_keys:
        if key not in collected_data_dict.keys():
            return False

    return True



def parents_to_children(pids, parents):
    children = {}
    for p in pids:
        if p in parents.keys():
            the_parent = parents[p]
            if not the_parent in children.keys():
                children[the_parent] = []
            children[the_parent].append(p)
        else:
            continue

    return children



if __name__ == "__main__":
    main(sys.argv[0])
