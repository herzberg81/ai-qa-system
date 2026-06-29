# -*- coding: utf-8 -*-
"""
通用工具模块
提供标点过滤、停用词过滤、集合处理等工具函数
"""

import string


def remove_punctuation(text):
    """
    清除中英文标点符号
    :param text: 输入文本
    :return: 去除标点后的文本
    """
    result = []
    for char in text:
        if char not in string.punctuation and not is_chinese_punctuation(char):
            result.append(char)
    return ''.join(result)


def is_chinese_punctuation(char):
    """
    判断字符是否为中文标点
    :param char: 单个字符
    :return: True/False
    """
    chinese_punctuations = '，。！？；：""''【】（）《》、—…·'
    return char in chinese_punctuations


def filter_stopwords(words):
    """
    过滤停用词（无意义助词）
    :param words: 词语列表
    :return: 过滤后的词语列表
    """
    stopwords = {
        '什么', '怎', '么', '是', '和', '的', '了', '在', '有', '我', '你', '他',
        '她', '它', '们', '这', '那', '哪', '个', '一', '二', '三', '不', '就',
        '都', '也', '要', '会', '能', '可', '以', '可', '而', '与', '或', '但',
        '还', '又', '再', '已', '经', '曾', '将', '把', '被', '让', '给', '向',
        '从', '到', '对', '为', '因', '所', '以', '之', '其', '此', '彼', '如',
        '若', '虽', '然', '则', '即', '乃', '于', '上', '下', '左', '右', '前',
        '后', '里', '外', '中', '内', '间', '旁', '边', '面', '头', '尾', '首',
        '末', '个', '位', '本', '该', '各', '每', '某', '另', '其', '它',
        '可以', '怎么', '怎样', '如何', '为什么', '吗', '呢', '吧', '啊', '哦',
        '嗯', '哈', '呀', '嘛', '呗', '啦', '请', '请问', '一下', '一些',
        '比较', '很', '非常', '最', '更', '越', '只', '仅仅', '大概', '可能',
        '或者', '还是', '以及', '等等', '之类', '今天', '明天', '昨天',
        '天气', '怎么样', '什么样', '多少', '几', '谁', '哪里', '什么时候'
    }
    return [word for word in words if word not in stopwords]


def simple_segment(text):
    """
    简单分词：按字符拆分中文，按空格拆分英文
    :param text: 输入文本
    :return: 词语列表
    """
    text = remove_punctuation(text)
    words = []
    current_word = ''
    
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            if current_word:
                words.append(current_word)
                current_word = ''
            words.append(char)
        elif char == ' ' or char == '\t':
            if current_word:
                words.append(current_word)
                current_word = ''
        else:
            current_word += char
    
    if current_word:
        words.append(current_word)
    
    return words


def count_intersection(set1, set2):
    """
    计算两个集合的交集元素数量
    :param set1: 集合1
    :param set2: 集合2
    :return: 交集元素数量
    """
    return len(set1 & set2)


def extract_keywords_simple(text):
    """
    简单关键词提取：分词 + 去停用词 + 转集合
    :param text: 输入文本
    :return: 关键词集合
    """
    words = simple_segment(text)
    words = filter_stopwords(words)
    return set(words)
