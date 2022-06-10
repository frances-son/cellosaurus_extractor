import xml.etree.ElementTree as ET
import util


# define file path
filePath = "../resources/cellosaurus_220509.xml"
# filePath = "../resources/test_mc38.xml"
spliter = "\t"

# parse xml file
doc = ET.parse(filePath)
# get root node
root = doc.getroot()

file_path = '../output/'
file_name = util.make_file_name(file_path, root)
print(file_name)
output_file = open(file_name, 'w')

# make first line and write to file
first_line_str = util.make_first_line()
output_file.write(first_line_str)
output_file.write("\n")

for cellLine in root.iter('cell-line'):
    # list for making each line string
    line_str = util.get_cell_lines_info(cellLine)
    output_file.write(line_str)
    # print(line_str)
    # break

print("The End")
    
    
