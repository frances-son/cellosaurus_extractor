import json
import requests




def call_ncit_api(path, method, getversion):
    if getversion is True:
        url = "https://api-evsrest.nci.nih.gov/version"
    else:
        api_host = "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/"
        url = api_host + path

    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        "key1":"value1",
        "key2":"value2"
    }

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, verify=False)
        elif method == 'POST':
            response = requests.get(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"),
                                    verify=False)
        # print("response status %r" % response.status_code)
        # print("response text %r" % response.text)
        return response.text

    except Exception as e:
        print(e)


def make_first_line():
    column_list = [
        "NCIt Code",
        "NCIt Preferred Name",
        "Level",
        "Parent"
    ]
    first_list_str = "\t".join(column_list)
    first_list_str.join("\n")
    # print(first_list_str)
    return first_list_str


# 한 번 call 할 때 children들을 읽어 나가는 방식
def ncit_make_file_name(path, dt):
    ver_response = call_ncit_api(None, "POST", True)
    ver_response_json = json.loads(ver_response)
    ver_str = ver_response_json["version"].split(".RELEASE")[0]
    # print(ver_str)

    list = []
    list.append(path)
    list.append("NCIt_cellLine")
    list.append("_ver")
    list.append(ver_str)
    list.append("_")
    list.append(dt)
    list.append(".tsv")

    final_str = ''.join(list)
    # print(final_str)
    return final_str


def ncit_api_get_children(ncit_code, ncit_output_file, level):
    print(ncit_code)
    previous_level = level;

    # call API
    cl_children = call_ncit_api(ncit_code + "/children", "POST", False)

    if cl_children is None:
        print("cl_children has no children.")

    else:
        level += 1
        cl_children_json = json.loads(cl_children)
        # print(cl_children_json)
        # cell_line_children_json_cnt = len(cl_children_json)
        # print(cell_line_children_json_cnt)
        cl_children_json_len = len(cl_children_json)
        for idx, cl_child in enumerate(cl_children_json):
            cl_list = []
            code = cl_child["code"]
            name = cl_child["name"]
            leaf = cl_child["leaf"]

            cl_list.append(code)
            cl_list.append("\t")
            cl_list.append(name)
            cl_list.append("\t")
            cl_list.append(str(level))
            cl_list.append("\t")
            # parent ncit code
            cl_list.append(ncit_code)
            cl_list.append("\n")

            cl_str = ''.join(cl_list)
            ncit_output_file.write(cl_str)

            if leaf is True:
                if (level != 1) & (cl_children_json_len == (idx-1)):
                    level = previous_level
                continue

            # This Concept has children
            elif leaf is False:
                previous_level = level;
                ncit_api_get_children(code, ncit_output_file, level)

