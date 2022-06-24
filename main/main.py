import xml.etree.ElementTree as ET
import cellosaurus_module as cm
import ncit_module as nm
import util

csr_input_file_path = "../resources/cellosaurus_220509.xml"
output_file_path = '../output/'

# --- pre-define NCIt code
ncit_cell_line_code = "C16403"


# ** PART 1 : Cellosaurus
# # initialize cm module
# cm.cellosaurus_load(csr_input_file_path)
# # make file name
# csr_file_name = util.make_file_name(output_file_path, 'csr')
# # make output file
# csr_output_file = open(csr_file_name, 'w')
# # file write
# cm.cellosaurus_parse(csr_output_file);


# ** PART 2 : NCIt
# initialize nm module
# make file name
ncit_file_name = util.make_output_file_name(output_file_path, 'ncit')
# make output file
ncit_output_file = open(ncit_file_name, 'w')
# write first line
ncit_first_line = nm.make_first_line()
ncit_output_file.write(ncit_first_line + "\n")
# file write
nm.ncit_api_get_children(ncit_cell_line_code, ncit_output_file, 0)


print("The End")
