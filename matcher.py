from utils import *
import difflib
import argparse


def use_info(path):
    # TODO 冗余代码过多
    cont = readTxt(path).split('\n')
    cont = [i for i in cont if i != '']
    cont = [i for i in cont if 'A.' not in i]
    cont = [i for i in cont if 'B.' not in i]
    cont = [i for i in cont if 'C.' not in i]
    cont = [i for i in cont if 'D.' not in i]
    cont = [i for i in cont if 'E.' not in i]
    cont = [i for i in cont if 'F.' not in i]
    cont = [i for i in cont if 'G.' not in i]
    cont = [i for i in cont if 'A．' not in i]
    cont = [i for i in cont if 'B．' not in i]
    cont = [i for i in cont if 'C．' not in i]
    cont = [i for i in cont if 'D．' not in i]
    cont = [i for i in cont if 'E．' not in i]
    cont = [i for i in cont if 'F．' not in i]
    cont = [i for i in cont if 'G．' not in i]
    cont = [i for i in cont if 'T、正确F、错误' not in i]
    return cont


def adjust_format(contents):
    # 调整表格格式
    for idx, content in enumerate(contents):
        contents[idx] = content[content.find('：') + 1:]
        contents[idx] = content[:content.find('（1分）')]
        contents[idx] = content[:content.find('（1.5分')]
    return contents


def match(look_qs, sample_qs, save_title=None):
    """
    匹配模拟题库和总题库的题目，保留模拟题库与正确答案的行数
    :param look_qs: 需要匹配的模拟题库
    :param sample_qs: 样本总题库
    :param save_title: 保留有模拟题库题目的总题库的行数列表
    :return:
    """
    if save_title is None:
        save_title = []
    for item in look_qs:
        for index, row in sample_qs.iterrows():
            if get_equal_rate(item, row['题目内容']) > 0.8:
                # TODO 这里的key和相似阈值应该是变量
                save_title.append(index)
    return save_title


def get_equal_rate(str1, str2):
    """
    对比str1和str的相似度
    :param str1: 字符串1
    :param str2: 字符串2
    :return: 相似度
    """
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


def parse_args():
    """
    :return:进行参数的解析
    """
    description = "you should add those parameter"
    parser = argparse.ArgumentParser(description=description)
    help = "The path of address"
    parser.add_argument('--addresses', help=help)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # 读取表格和文本
    # TODO 直接用args获取命令行参数
    dataframe_xls = read_excel('./附件2.新入职员工通关考试应知应会试题库2021版.xlsx')
    content = use_info('./t1-t4.txt')

    # 多个文件文本组合
    all_content = content

    saved_list = match(all_content, dataframe_xls)
    saved_list = list(set(saved_list))
    saved_list.sort()
    filtered_data = dataframe_xls.loc[saved_list, '题目内容':'正确选项']

    # 保存为excel
    filtered_data.to_excel('filtered_data.xlsx')


if __name__ == '__main__':
    main()