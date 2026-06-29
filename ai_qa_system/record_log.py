# -*- coding: utf-8 -*-
"""
用户提问日志记录模块
负责存储、读取、保存用户提问记录
"""

import os
from datetime import datetime


# 全局提问记录列表
question_record_list = []


def add_record(question, answer):
    """
    添加一条提问记录
    :param question: 用户问题
    :param answer: 系统回答
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "time": timestamp,
        "question": question,
        "answer": answer
    }
    question_record_list.append(record)


def get_all_records():
    """
    获取所有提问记录
    :return: 提问记录列表
    """
    return question_record_list


def save_record(record_list=None, filename="question_log.txt"):
    """
    将提问记录保存到本地文件
    :param record_list: 要保存的记录列表，为None则使用全局列表
    :param filename: 保存的文件名
    :return: 是否保存成功
    """
    if record_list is None:
        record_list = question_record_list
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("AI基础问答系统 - 用户提问记录\n")
            f.write(f"记录数量: {len(record_list)} 条\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, record in enumerate(record_list, 1):
                f.write(f"【第 {i} 条提问】\n")
                f.write(f"时间: {record['time']}\n")
                f.write(f"问题: {record['question']}\n")
                f.write(f"回答: {record['answer']}\n")
                f.write("-" * 60 + "\n\n")
        
        return True, filepath
    except Exception as e:
        print(f"保存提问记录失败: {e}")
        return False, str(e)


def load_record(filename="question_log.txt"):
    """
    从本地文件加载提问记录（可选功能）
    :param filename: 文件名
    :return: 加载的记录列表
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        if not os.path.exists(filepath):
            return []
        
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        return records
    except Exception as e:
        print(f"加载提问记录失败: {e}")
        return []


def clear_records():
    """
    清空所有记录
    """
    global question_record_list
    question_record_list = []
