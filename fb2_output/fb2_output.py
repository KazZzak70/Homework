from pdf_output.pdf_output import define_the_mode, get_image
import xml.etree.ElementTree as XML
import xml.etree.ElementTree
from PIL import Image
import pathlib
import base64
import json
import os


def create_folder():
    output_data_path = pathlib.Path(pathlib.Path.home(), "output_files")
    if not output_data_path.exists():
        output_data_path.mkdir()


def insert_picture(*, key: int, image_url: str, section: xml.etree.ElementTree.Element, root: xml.etree.ElementTree.Element):
    image = get_image(image_url)
    with open(f"image{key}.jpg", "wb") as file:
        file.write(image)
    im = Image.open(f"image{key}.jpg")
    im.save(f"image{key}.png")
    os.remove(f"image{key}.jpg")
    with open(f"image{key}.png", "rb") as fp:
        encoded_data = base64.b64encode(fp.read())
    os.remove(f"image{key}.png")
    p = XML.SubElement(section, "p")
    image = XML.SubElement(p, "image", attrib={"l:href": f"#img_{key}"})
    binary = XML.Element("binary", attrib={"id": f"img_{key}", "content-type": "image/png"})
    binary.text = str(encoded_data).replace("b'", "").replace("'", "")
    root.append(binary)


def offline_mode(*, section: xml.etree.ElementTree.Element, src_data_list: list, date: int, limit: int):
    iteration = 0
    for item in src_data_list:
        if (date is not None and item["pubdate"] == date) or date is None:
            iteration += 1
            for key in item.keys():
                p = XML.SubElement(section, "p")
                if key != "links":
                    p.text = f"{key.capitalize()}: {item[key]}"
                else:
                    try:
                        p.text = f"Image link: {item[key]['2']}"
                    except KeyError:
                        continue
        if iteration == limit:
            break
        empty_line = XML.SubElement(section, "p")
        empty_line.text = ' '


def online_mode(*, section: xml.etree.ElementTree.Element, root: xml.etree.ElementTree.Element, src_data_list: list, date: int, limit: int):
    iteration = 0
    for key, item in enumerate(src_data_list):
        if (date is not None and item["pubdate"] == date) or date is None:
            iteration += 1
            try:
                if item["links"]["2"] is not None:
                    insert_picture(key=key, image_url=item["links"]["2"], section=section, root=root)
            except KeyError:
                pass
            for dict_key in item.keys():
                p = XML.SubElement(section, "p")
                if dict_key != "links":
                    p.text = f"{dict_key.capitalize()}: {item[dict_key]}"
            if iteration == limit:
                break
            empty_line = XML.SubElement(section, "p")
            empty_line.text = ' '


def output_data_fb2(file_path: pathlib.Path, date: int = None, limit: int = None):
    create_folder()
    with open(file_path) as src_file:
        src = json.load(src_file)
    offline_mode_flag = define_the_mode()
    attrib = {"xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
              "xmlns:l": "http://www.w3.org/1999/xlink",
              "xmlns:xs": "http://www.w3.org/2001/XMLSchema"}
    root = XML.Element("FictionBook", attrib=attrib)
    description = XML.SubElement(root, "description")
    title_info = XML.SubElement(description, "title-info")
    book_title = XML.SubElement(title_info, "book-title")
    book_title.text = src["feed"]
    body = XML.Element("body")
    root.append(body)
    body_title = XML.SubElement(body, "title")
    body_title_text = XML.SubElement(body_title, "p")
    body_title_text.text = src["feed"]
    section = XML.SubElement(body, "section")

    if offline_mode_flag:
        offline_mode(section=section, src_data_list=src["items"], date=date, limit=limit)
    else:
        online_mode(section=section, root=root, src_data_list=src["items"], date=date, limit=limit)
    tree = XML.ElementTree(root)
    file_name = src["feed"].replace(" ", "_").lower()
    tree.write(f"{file_name}.fb2", encoding="UTF-8", xml_declaration=True)
    old_path = pathlib.Path(pathlib.Path.cwd(), f"{file_name}.fb2")
    new_path = pathlib.Path(pathlib.Path.cwd(), "output_files", f"{file_name}.fb2")
    os.replace(old_path, new_path)
