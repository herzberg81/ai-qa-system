# -*- coding: utf-8 -*-
"""
关键词匹配引擎模块
基于集合交集的关键词匹配算法，计算用户问题与知识库问题的匹配度
"""

from utils import extract_keywords_simple, count_intersection


def match_answer(user_input, kb, kw_map, min_match=1):
    """
    匹配最佳答案
    使用集合交集计算用户问题与知识库中每个问题的匹配关键词数量，
    返回匹配度最高的问题对应的答案。
    
    :param user_input: 用户输入的问题字符串
    :param kb: 知识库字典 {问题: 答案}
    :param kw_map: 关键词映射字典 {问题: 关键词集合}
    :param min_match: 最小匹配关键词数量，默认为1
    :return: 匹配结果文本（答案或提示语）
    """
    if not user_input or not user_input.strip():
        return "请输入有效问题。"
    
    user_kw = extract_keywords_simple(user_input)
    
    if not user_kw:
        return "抱歉，未找到相关答案，请尝试其他问题。"
    
    best_question = None
    max_match_count = 0
    
    for question, q_kw in kw_map.items():
        match_count = count_intersection(user_kw, q_kw)
        if match_count > max_match_count:
            max_match_count = match_count
            best_question = question
    
    if max_match_count >= min_match and best_question:
        return kb[best_question]
    else:
        return "抱歉，未找到相关答案，请尝试其他问题。"


def match_answer_with_detail(user_input, kb, kw_map):
    """
    匹配最佳答案（带详细匹配信息，用于调试）
    :param user_input: 用户输入
    :param kb: 知识库
    :param kw_map: 关键词映射
    :return: (答案, 匹配详情列表)
    """
    user_kw = extract_keywords_simple(user_input)
    
    match_details = []
    for question, q_kw in kw_map.items():
        intersection = user_kw & q_kw
        match_count = len(intersection)
        match_details.append((question, match_count, intersection))
    
    match_details.sort(key=lambda x: x[1], reverse=True)
    
    if match_details and match_details[0][1] > 0:
        best_question = match_details[0][0]
        return kb[best_question], match_details
    else:
        return "抱歉，未找到相关答案，请尝试其他问题。", match_details
