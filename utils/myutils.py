import os
import pickle
import xml.etree.ElementTree as ET
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import numpy as np
import pandas as pd


def read_excel(Path):
    data = pd.read_excel(Path)
    # print(data.keys())
    return data


def make_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)


def py_cpu_nms(dets, thresh):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    scores = dets[:, 4]

    keep = []
    index = scores.argsort()[::-1]

    while index.size > 0:
        i = index[0]  # every time the first is the biggst, and add it directly
        keep.append(i)

        x11 = np.maximum(x1[i], x1[index[1:]])  # calculate the points of overlap
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])

        w = np.maximum(0, x22 - x11 + 1)
        h = np.maximum(0, y22 - y11 + 1)
        overlaps = w * h
        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)

        idx = np.where(ious <= thresh)[0]
        index = index[idx + 1]  # because index start from 1
    return keep


def read_pkl(path):
    f = open(path, 'rb')
    pkl_info = pickle.load(f)
    f.close()
    return pkl_info


def write_pkl(path, pklInfo):
    with open(path, 'wb') as f:
        pickle.dump(pklInfo, f)
    f.close()


def read_txt(path):
    with open(path, 'r', encoding='UTF-8')as f:
        txtinfo = f.readlines()
    f.close()
    return txtinfo


def readTxt(Path):
    content = open(Path, encoding='utf-8').read()
    return content


def write_txt(path, txtInfo):
    f = open(path, 'w')
    if isinstance(txtInfo, list):
        for i in txtInfo:
            f.write(i + '\n')
    else:
        f.write(txtInfo)
    f.close()


def read_xml(path):
    Cls, new_box = [], []
    tree = ET.parse(path)
    root = tree.getroot()
    size = root.find('size')
    filename, width, height = root.find('filename').text, size.find('width').text, size.find('height').text
    for obj in root.iter('object'):
        Cls.append(obj.find('name').text)

        xmlbox = obj.find('bndbox')
        new_box.append(
            [xmlbox.find('xmin').text, xmlbox.find('ymin').text, xmlbox.find('xmax').text, xmlbox.find('ymax').text])

    return filename, width, height, Cls, new_box


def write_xml(filename, width, height, Cls, new_box, path, xml_name):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'GTSDB'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = filename

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(width)
    node_height = SubElement(node_size, 'height')
    node_height.text = str(height)
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    for index, cls in enumerate(Cls):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = str(cls)
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(new_box[index][0])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(new_box[index][1])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(new_box[index][2])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(new_box[index][3])
    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    f = open(os.path.join(path, xml_name), 'w')
    # f = open(os.path.join(path, xml_name), 'w', encoding='utf-8')
    dom.writexml(f)
    f.close()
    return
