#!/usr/bin/env python
import re, os, sys

def parse_support_file_line(line):
    """Gets the corresponding fields from a given line"""
    line = line.rstrip(os.linesep).strip()
    fields = line.split()
    try:
        atom_id = fields[0].strip()
        amber_type = fields[1].strip()
        charge = float(fields[2].strip())
        mass = float(fields[3].strip())
        radius = float(fields[4].strip())
        return atom_id, amber_type, charge, mass, radius
    except:
        raise SupportFileParsingError("Can not parse line: '%s'" % line)

def read_support_file(file_name):
    """Loads support file information into protein, i.e, amber type, charge and mass for each atom."""
    support_file = open(file_name)
    lines = support_file.readlines()
    support_file.close()
    latom_id, lamber_type, lcharge, lmass, lradius = [],[],[],[],[]
    for line in lines:
        atom_id, amber_type, charge, mass, radius = parse_support_file_line(line)
        latom_id.append(atom_id)
        lamber_type.append(amber_type)
        lcharge.append(charge)
        lmass.append(mass)
        lradius.append(radius)
    return latom_id, lamber_type, lcharge, lmass, lradius

def check_support_file(file_name):
    """Loads support file information into protein, i.e, amber type, charge and mass for each atom."""
    support_file = open(file_name)
    lines = support_file.readlines()
    support_file.close()
    for line in lines:
        atom_id, amber_type, charge, mass, radius = parse_support_file_line(line)
        if re.match("[A-Z]\.[A-Z][A-Z][A-Z]\.[0-9]*\.[A-Z0-9]*",atom_id) and re.match("[A-Z0-9]*",amber_type) and re.match("[-0-9]*\.[0-9]*",str(charge)) and re.match("[0-9]*\.[0-9]*",str(mass)) and re.match("[0-9]*\.[0-9]*",str(radius)):
            Bool = True
        else:
            Bool = False
    return Bool

def write_support_file(file_name, ids, amber_types, charges, masses, radii):
    """Writes to file_name the values of charges and masses lists.
    Each line of file_name represents an atom and the columns its values.
    """
    output_file = open(file_name, 'w')
    for atom_id, amber_type, charge, mass, radius in zip(ids, amber_types, charges, masses, radii):
        line = "%-20s%7s%14.6f%14.6f%14.6f%s" % (atom_id, amber_type, charge, mass, radius, os.linesep)
        output_file.write(line)
    output_file.close()

def amberatom_new2olf(file_name):
    amber_new2old={}
    f=open(file_name,"r")
    lines = f.readlines()
    for line in lines:
        if re.search("^[A-Za-z0-9]", line):
            if re.search("^[A-Za-z0-9]", line.split()[1]):
                new_amber_type = line.split()[0]
                old_amber_type = line.split()[1]
                amber_new2old[new_amber_type] = old_amber_type
            else:
                print ("The map file is incorrect")
                exit(0)
    return amber_new2old


if __name__ == "__main__":
    if len(sys.argv[1:]) < 1 or len(sys.argv[1:]) > 2 :
        print ("usage: %s lig.pdb.amber [amber_map_file] optional" % sys.argv[0])
        exit(0)
    if len(sys.argv[1:]) == 1:
        amberfile = sys.argv[1]
        Amber_dic = {'p3': 'P', 's6': 'S', 'CS': 'CM', 'nf': 'NA', 'c2': 'CD', 'nx': 'N3', 'CP': 'CK', 'nz': 'N3', 'cc': 'CC', 'TJ': 'CT', 'p2': 'P', 'TH': 'H', 'Oh': 'OH', 'h4': 'H4', 'Oy': 'OS', '2C': 'CT', 'cd': 'CC', 'Os': 'OS', 'OD': 'O', 'OA': 'OH', 'OP': 'O2', 'HZ': 'HC', '3C': 'CT', 'Hp': 'HP', 'Ho': 'HO', 'Hc': 'HC', 'Ha': 'HC', 'Cs+': 'Cs', 'br': 'Br', 'c': 'C', 'oh': 'OH', 'h2': 'H2', 'nq': 'NT', 's': 'S', 'ow': 'OW', 'os': 'OS', 'oq': 'OS', 'op': 'OS', 'ch': 'CZ', 'cl': 'Cl', 'K+': 'K', 'h3': 'H3', 'ca': 'CA', 'h1': 'H1', 'cg': 'CZ', 'cf': 'CD', 'ce': 'CD', 'Ng': 'N', 'cz': 'CA', 'cy': 'CT', 'cx': 'CT', 'Rb+': 'Rb', 'cs': 'C', 'cq': 'CA', 'cp': 'CA', 'cv': 'CD', 'cu': 'CD', 'NL': 'N3', 'px': 'P', 'py': 'P', 'ND': 'N', 'pb': 'P', 'pc': 'P', 'C8': 'CT', 'pf': 'P', 'pd': 'P', 'pe': 'P', 'C3': 'CT', 'C2': 'CM', 'C1': 'CK', 'C5': 'CK', 'C4': 'CM', 'Cl-': 'Cl', 'hx': 'HP', 'CO': 'C', 'hs': 'HS', 'hp': 'HP', 'hw': 'HW', 'CE': 'CT', 'CX': 'CT', 'hn': 'H', 'ho': 'HO', 'Sm': 'S', 'c3': 'CT', 'hc': 'HC', 'c1': 'CZ', 'ha': 'HA', 'Ck': 'CD', 'Cj': 'CD', 'p4': 'P', 'f': 'F', 'Cg': 'CT', 'n': 'N', 'ss': 'S', 'Cy': 'CT', 'Cp': 'CT', 'F-': 'F', 'CI': 'CT', 'o': 'O', 'nh': 'NT', 'ni': 'NT', 'nj': 'NT', 'nk': 'NT', 'nl': 'NT', 'nm': 'NT', 'nn': 'NT', 'no': 'NT', 'na': 'NA', 'nb': 'NB', 'nc': 'NC', 'nd': 'NC', 'ne': 'NA', 'TP': 'CT', 's4': 'S', 'TN': 'NT', 'ny': 'N3', 'Br-': 'Br', 'TM': 'CT', 'I-': 'I', 'LP': 'Cl', 'np': 'NT', 'TG': 'CT', 'ns': 'NT', 'nt': 'N', 'nu': 'NT', 'nv': 'NT', 'TA': 'CT', 'h5': 'H5', 'p5': 'P', 'Na+': 'Na', 'Li+': 'Li', 'n+': 'N3', 'sy': 'S', 'sx': 'S', 'i': 'I', 'sq': 'S', 'sp': 'S', 'n8': 'NT', 'n9': 'NT', 'sh': 'SH', 's2': 'S', 'n1': 'NY', 'n2': 'N2', 'n3': 'NT', 'n4': 'N3', 'n5': 'NT', 'n6': 'NT', 'n7': 'NT'}
    elif len(sys.argv[1:]) == 2:
       amberfile = sys.argv[1]
       atmmap = sys.argv[2]
       Amber_dic = amberatom_new2olf(atmmap)
    if check_support_file(amberfile):
        atom_id, amber_type, charge, mass, radius = read_support_file(amberfile)
        Amber_dic_subs = { k:v for k,v in Amber_dic.items()}
        mod_amber_type = [Amber_dic_subs.get(item,item)  for item in amber_type]
        os.rename(amberfile, amberfile+".old")
        write_support_file(amberfile,atom_id, mod_amber_type, charge, mass, radius)
    else:
        print ("The .amber file is incorrect.")
