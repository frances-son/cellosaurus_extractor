from datetime import datetime
import ncit_module as nm
import cellosaurus_module as cm
spliter = "\t"


def get_elements_to_str(elements):
    # print(elements)
    # print(len(elements))
    if len(elements) == 0:
        return "";
    ele_list = []
    for ele in elements:
        ele_list.append(ele.text)
        ele_list.append(",")
    ele_list.pop(-1)
    ele_str = ''.join(ele_list)
    return ele_str


def append_to_str_list(item_list, item):
    if len(item) == 0:
        item = ""
    item_list.append(str(item))
    item_list.append(spliter)
    return list


def make_output_file_name(path, type):
    ## get datetime
    now = datetime.now()
    dt = now.strftime('%Y%m%d%H%M%S')

    if type == 'csr':
        csr_output_filename = cm.cellosaurus_make_file_name(path, dt)
        return csr_output_filename

    elif type == 'ncit':
        ncit_output_filename = nm.ncit_make_file_name(path, dt)
        return ncit_output_filename



def get_cell_lines_info(cell_line):
    line_str_list = []
    # type(cellLine) : <class 'xml.etree.ElementTree.Element'>
    # get atrributes of cellLine
    cl_attrib = cell_line.attrib

    # get species
    species = cell_line.findall(".//species-list/")
    species_str = get_elements_to_str(species)
    append_to_str_list(line_str_list, species_str)

    # get identifier name
    identifier_name = cell_line.findtext(".//name-list/*[@type='identifier']")
    append_to_str_list(line_str_list, identifier_name)

    # get synonym list
    synonyms = cell_line.findall(".//name-list/*[@type='synonym']")
    synonyms_str = get_elements_to_str(synonyms)
    append_to_str_list(line_str_list, synonyms_str)

    # get accession name
    accession_name = cell_line.findtext(".//*[@type='primary']")
    append_to_str_list(line_str_list, accession_name)

    # get category
    category = cl_attrib.get("category")
    append_to_str_list(line_str_list, category)

    # get disease
    disease = cell_line.findall(".//disease-list/")
    disease_str = get_elements_to_str(disease)
    append_to_str_list(line_str_list, disease_str)

    # get derived-from
    # derived_from = cell_line.findall(".//derived-from/")
    # derived_from_str = get_elements_to_str(derived_from)
    # append_to_str_list(line_str_list, derived_from_str)

    # get created date
    created = cl_attrib.get("created")
    append_to_str_list(line_str_list, created)

    # get last_updated date
    last_updated = cl_attrib.get("last-updated")
    append_to_str_list(line_str_list, last_updated)

    # get entry_version
    entry_version = cl_attrib.get("entry-version")
    append_to_str_list(line_str_list, entry_version)

    # if final line, remove final spliter and append '\n'
    line_str_list.pop(-1)
    line_str_list.append('\n')

    # list to str
    line_str = ''.join(line_str_list)

    # return str
    return line_str
