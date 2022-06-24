import xml.etree.ElementTree as ET
import util as ut

# --- source file path
spliter = "\t"
global csr_doc, csr_root


def cellosaurus_load(input_file):
    global csr_doc, csr_root
    # --- parse xml file
    csr_doc = ET.parse(input_file)

    # --- get root node
    csr_root = csr_doc.getroot()


def make_first_line():
    column_list = [
        "SPECIES",
        "IDENTIFIER NAME",
        "SYNONYMS",
        "ACCESSION NAME",
        "CATEGORY",
        "DISEASE",
        "CREATED DATE",
        "LAST_UPDATED DATE",
        "ENTRY VERSION"
    ]
    first_list_str = "\t".join(column_list)
    first_list_str.join("\n")
    # print(first_list_str)
    return first_list_str


def cellosaurus_parse(output_file):
    # make first line and write file
    first_line_str = make_first_line();
    output_file.write(first_line_str)
    output_file.write("\n")

    for cellLine in csr_root.iter('cell-line'):
        # list for making each line string
        line_str = get_cell_lines_info(cellLine)
        output_file.write(line_str)
        # print(line_str)
        # break


def cellosaurus_make_file_name(path, now, dt):
    ## mae file name using header tag
    # get terminology name
    term_name = csr_root.findtext(".//header/terminology-name")
    # make release list
    header_list = []
    # get release information
    release = csr_root.findall(".//header/release")
    rel_attrib = release[0].attrib
    version = rel_attrib.get("version")
    updated = rel_attrib.get("updated")

    # make str
    header_list.append(path)
    header_list.append(term_name)
    header_list.append("_")
    header_list.append("ver ")
    header_list.append(version)
    header_list.append("(")
    header_list.append(updated)
    header_list.append(")_")
    header_list.append(dt)
    header_list.append(".tsv")
    final_str = ''.join(header_list)
    return final_str


def get_cell_lines_info(cell_line):
    line_str_list = []
    # type(cellLine) : <class 'xml.etree.ElementTree.Element'>
    # get atrributes of cellLine
    cl_attrib = cell_line.attrib

    # get species
    species = cell_line.findall(".//species-list/")
    species_str = ut.get_elements_to_str(species)
    ut.append_to_str_list(line_str_list, species_str)

    # get identifier name
    identifier_name = cell_line.findtext(".//name-list/*[@type='identifier']")
    ut.append_to_str_list(line_str_list, identifier_name)

    # get synonym list
    synonyms = cell_line.findall(".//name-list/*[@type='synonym']")
    synonyms_str = ut.get_elements_to_str(synonyms)
    ut.append_to_str_list(line_str_list, synonyms_str)

    # get accession name
    accession_name = cell_line.findtext(".//*[@type='primary']")
    ut.append_to_str_list(line_str_list, accession_name)

    # get category
    category = cl_attrib.get("category")
    ut.append_to_str_list(line_str_list, category)

    # get disease
    disease = cell_line.findall(".//disease-list/")
    disease_str = ut.get_elements_to_str(disease)
    ut.append_to_str_list(line_str_list, disease_str)

    # get derived-from
    # derived_from = cell_line.findall(".//derived-from/")
    # derived_from_str = get_elements_to_str(derived_from)
    # append_to_str_list(line_str_list, derived_from_str)

    # get created date
    created = cl_attrib.get("created")
    ut.append_to_str_list(line_str_list, created)

    # get last_updated date
    last_updated = cl_attrib.get("last-updated")
    ut.append_to_str_list(line_str_list, last_updated)

    # get entry_version
    entry_version = cl_attrib.get("entry-version")
    ut.append_to_str_list(line_str_list, entry_version)

    # if final line, remove final spliter and append '\n'
    line_str_list.pop(-1)
    line_str_list.append('\n')

    # list to str
    line_str = ''.join(line_str_list)

    # return str
    return line_str
