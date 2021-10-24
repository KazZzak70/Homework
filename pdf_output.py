from parser_engine import Parser
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import requests
import json
import os

total_page_height = FPDF().h - 20


def define_the_mode():
    offline_mode_flag = False
    try:
        requests.get(url="http://httpbin.org/status/200", headers=Parser.HEADERS)
    except requests.ConnectionError:
        offline_mode_flag = True
    return offline_mode_flag


def get_image(url: str):
    try:
        response = requests.get(url=url, headers=Parser.HEADERS)
    except requests.ConnectionError:
        raise requests.ConnectionError("HTTP Connection error")
    else:
        return response.content


def generate_a_row(*, row_content: str, header_name: str, max_line_len: int, online_mode_flag: bool) -> list:
    row_list = list()
    if len(row_content) > max_line_len:
        iteration = 0
        char_start = 0
        char_end = max_line_len
        while True:
            iteration += 1
            try:
                if row_content[char_end] != " ":
                    while row_content[char_end] != " ":
                        char_end -= 1
            except IndexError:
                char_end = len(row_content)
            if online_mode_flag:
                row_list.append([" ", header_name, row_content[char_start:char_end]])
            else:
                row_list.append([header_name, row_content[char_start:char_end]])
            header_name = " "
            if char_end == len(row_content):
                break
            char_start = char_end + 1
            char_end += max_line_len
    else:
        if online_mode_flag:
            row_list.append([" ", header_name, row_content])
        else:
            row_list.append([header_name, row_content])
    return row_list


def link_separator(*, link: str, header_name: str, max_line_len: int, online_mode_flag: bool) -> list:
    link_list = list()
    if len(link) > max_line_len:
        iteration = 0
        char_start = 0
        char_end = max_line_len
        while True:
            iteration += 1
            try:
                link[char_end].isalpha()
            except IndexError:
                char_end = len(link)
            if online_mode_flag:
                link_list.append([" ", header_name, link[char_start:char_end]])
            else:
                link_list.append([header_name, link[char_start:char_end]])
            if char_end == len(link):
                break
            char_start = char_end
            char_end += max_line_len
            header_name = " "
    else:
        if online_mode_flag:
            link_list.append([" ", header_name, link])
        else:
            link_list.append([header_name, link])
    return link_list


def get_data_list(item: dict, online_mode: bool, max_line_len: int) -> list[list]:
    data_list = list()
    for key in item.keys():
        if key in ["title", "description"] and item[key] is not None:
            data_list.extend(
                generate_a_row(row_content=item[key], header_name=f"{key.capitalize()}:", max_line_len=max_line_len,
                               online_mode_flag=online_mode))
        elif key == "link":
            data_list.extend(link_separator(link=item[key], max_line_len=max_line_len + 5, online_mode_flag=online_mode,
                                            header_name=f"{key.capitalize()}:"))
        elif key == "pubdate":
            if online_mode:
                data_list.append([" ", f"{key.capitalize()}:", item[key]])
            else:
                data_list.append([f"{key.capitalize()}:", item[key]])
    return data_list


def item_online_mode(pdf, item: dict, key: int, indent: int):
    online_mode = True
    global total_page_height
    data_list = get_data_list(item, online_mode, 49)
    if data_list.__len__() * pdf.font_size > total_page_height:
        pdf.add_page()
        pdf.cell(0, 5, ln=1)
        total_page_height = pdf.h
        indent = 15
    if item["links"]["2"] is not None:
        image = get_image(item["links"]["2"])
        with open(f"image{key}.jpg", "wb") as file:
            file.write(image)
        im = Image.open(f"image{key}.jpg")
        im.save(f"image{key}.png")
        pdf.image(f"image{key}.png", x=10, y=indent, w=30)
        os.remove(f"image{key}.png")
        os.remove(f"image{key}.jpg")
    for row in data_list:
        for key, item in enumerate(row):
            if key == 0:
                col_width = 35
            elif key == 1:
                col_width = 28
            else:
                col_width = pdf.w - 65
            pdf.cell(col_width, pdf.font_size,
                     txt=str(item), border=0)
        pdf.ln(pdf.font_size)
    pdf.cell(0, 15, ln=1)
    total_page_height -= (data_list.__len__() * pdf.font_size + 20)
    return 15 + indent + data_list.__len__() * pdf.font_size


def item_offline_mode(pdf, item: dict, indent: int) -> float:
    online_mode = False
    global total_page_height
    data_list = get_data_list(item, online_mode, 60)
    data_list.extend(
        link_separator(link=item["links"]["2"], header_name="Image link:", max_line_len=65, online_mode_flag=online_mode))
    if data_list.__len__() * pdf.font_size > total_page_height:
        pdf.add_page()
        pdf.cell(0, 5, ln=1)
        total_page_height = pdf.h
        indent = 15
    for row in data_list:
        for key, item in enumerate(row):
            if key == 0:
                col_width = 30
            else:
                col_width = pdf.w - 30
            pdf.cell(col_width, pdf.font_size,
                     txt=str(item), border=0)
        pdf.ln(pdf.font_size)
    pdf.cell(0, 15, ln=1)
    total_page_height -= (data_list.__len__() * pdf.font_size + 20)
    return 15 + indent + data_list.__len__() * pdf.font_size


def output_data_pdf(output_data: dict):
    offline_mode = define_the_mode()
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 5, txt=f"Feed: {output_data['feed']}", ln=1, align="L")
    pdf.cell(0, 5, ln=1)
    indent = 20
    for key, item in enumerate(output_data["items"]):
        if offline_mode:
            indent = item_offline_mode(pdf, item, indent)
        else:
            indent = item_online_mode(pdf, item, key, indent)
        if indent >= pdf.h:
            indent -= pdf.h
    output_file_name = output_data["feed"].replace(" ", "_").lower()
    output_file_path = Path(Path.cwd(), "output_files", f"{output_file_name}.pdf")
    pdf.output(output_file_path)


if __name__ == '__main__':
    with open("result_data.json") as src_file:
        src_dict = json.load(src_file)
    output_data_pdf(src_dict)
