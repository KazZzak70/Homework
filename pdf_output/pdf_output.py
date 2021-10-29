from importlib.resources import read_binary
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import requests
import pathlib
import json
import os

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
           'accept': '*/*'}
total_page_height = FPDF().h - 20


def create_folder():
    output_data_path = pathlib.Path(pathlib.Path.home(), "output_files")
    fonts_path = pathlib.Path(pathlib.Path.home(), "output_files", "fonts")
    if not output_data_path.exists():
        output_data_path.mkdir()
        fonts_path.mkdir()


def define_the_mode():
    offline_mode_flag = False
    try:
        requests.get(url="http://httpbin.org/status/200", headers=HEADERS)
    except requests.ConnectionError:
        offline_mode_flag = True
    return offline_mode_flag


def get_image(url: str):
    try:
        response = requests.get(url=url, headers=HEADERS)
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
    new_indent = 15 + indent + data_list.__len__() * pdf.font_size
    try:
        if item["links"]['2'] is not None:
            image = get_image(item["links"]["2"])
            with open(f"image{key}.jpg", "wb") as file:
                file.write(image)
            im = Image.open(f"image{key}.jpg")
            im.save(f"image{key}.png")
            pdf.image(f"image{key}.png", x=10, y=indent, w=30)
            os.remove(f"image{key}.png")
            os.remove(f"image{key}.jpg")
    except KeyError:
        pass
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
    return new_indent


def item_offline_mode(pdf, item: dict, indent: int) -> float:
    online_mode = False
    global total_page_height
    data_list = get_data_list(item, online_mode, 60)
    try:
        data_list.extend(link_separator(link=item["links"]["2"], header_name="Image link:", max_line_len=65,
                                        online_mode_flag=online_mode))
    except KeyError:
        pass
    if data_list.__len__() * pdf.font_size > total_page_height:
        pdf.add_page()
        pdf.cell(0, 5, ln=1)
        total_page_height = pdf.h
        indent = 15
    new_indent = 15 + indent + data_list.__len__() * pdf.font_size
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
    return new_indent


def output_data_pdf(file_path: pathlib.Path, date: int = None, limit: int = None):
    create_folder()
    with open(file_path) as src_json:
        output_data = json.load(src_json)
    offline_mode = define_the_mode()
    iteration = 0
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    pdf.add_page()
    font = read_binary(package="pdf_output.fonts", resource="DejaVuSansCondensed.ttf")
    new_font_path = pathlib.Path(pathlib.Path.home(), "output_files", "fonts", "DejaVuSansCondensed.ttf")
    with open(new_font_path, "wb") as new_font:
        new_font.write(font)
    pdf.add_font('DejaVu', '', fname=new_font_path, uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 5, txt=f"Feed: {output_data['feed']}", ln=1, align="L")
    pdf.cell(0, 5, ln=1)
    indent = 20
    for key, item in enumerate(output_data["items"]):
        if (date is not None and item["pubdate"] == date) or date is None:
            iteration += 1
            if offline_mode:
                indent = item_offline_mode(pdf, item, indent)
            else:
                indent = item_online_mode(pdf, item, key, indent)
            if indent >= pdf.h:
                indent -= pdf.h
            if iteration == limit:
                break
    output_file_name = output_data["feed"].replace(" ", "_").lower()
    output_file_path = Path(Path.home(), "output_files", f"{output_file_name}.pdf")
    pdf.output(output_file_path)
