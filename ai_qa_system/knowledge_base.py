# -*- coding: utf-8 -*-
"""
知识库构建模块
构建AI基础问答知识库，提取关键词，建立关键词映射
"""

from utils import extract_keywords_simple


def build_knowledge_base():
    """
    构建AI基础知识库，包含18条问答对
    :return: 知识库字典 {问题: 答案}
    """
    kb_dict = {
        "什么是人工智能？": "人工智能（AI）是让机器模拟人类感知、推理、学习、决策等智能行为的技术统称，涵盖机器学习、深度学习、自然语言处理、计算机视觉等多个分支。",
        "什么是机器学习？": "机器学习是人工智能的核心分支，通过算法让计算机从数据中自动学习规律，无需人工编写明确规则，就能对新数据做出预测或判断。",
        "机器学习和深度学习的区别？": "深度学习属于机器学习的一个分支，传统机器学习依赖人工提取特征，而深度学习依靠多层神经网络自动从数据中提取特征，处理复杂任务的能力更强。",
        "什么是神经网络？": "神经网络是模拟人脑神经元连接方式的计算模型，由输入层、隐藏层、输出层组成，通过调整神经元之间的权重来学习数据中的模式。",
        "什么是深度学习？": "深度学习是使用多层神经网络进行学习的机器学习方法，能够自动提取数据的多层特征表示，在图像识别、语音识别、自然语言处理等领域表现优异。",
        "什么是数据集？": "数据集是用于训练和测试机器学习模型的数据集合，通常分为训练集、验证集和测试集，数据的质量和数量直接影响模型性能。",
        "什么是模型训练？": "模型训练是指将训练数据输入机器学习算法，通过迭代优化模型参数，使模型能够学习数据中的规律并做出准确预测的过程。",
        "什么是过拟合？": "过拟合是指模型在训练集上表现很好，但在新数据（测试集）上表现较差的现象，通常由于模型过于复杂或训练数据不足导致。",
        "如何防止过拟合？": "防止过拟合的常用方法包括：增加训练数据、降低模型复杂度、使用正则化（L1/L2正则化）、使用Dropout、早停法（Early Stopping）等。",
        "什么是损失函数？": "损失函数是衡量模型预测值与真实值之间差异的函数，训练过程就是通过优化算法最小化损失函数来提升模型准确率。",
        "什么是梯度下降？": "梯度下降是一种常用的优化算法，通过沿着损失函数梯度的反方向逐步调整模型参数，以找到使损失函数最小化的参数值。",
        "Python在AI中的作用？": "Python是人工智能领域最流行的编程语言，拥有丰富的第三方库（如TensorFlow、PyTorch、scikit-learn），语法简洁易用，适合快速开发和原型验证。",
        "什么是自然语言处理？": "自然语言处理（NLP）是人工智能的重要分支，研究如何让计算机理解和生成人类语言，应用包括机器翻译、文本分类、情感分析、聊天机器人等。",
        "什么是计算机视觉？": "计算机视觉是让计算机从图像或视频中获取信息的技术，应用包括图像识别、目标检测、人脸识别、自动驾驶等。",
        "什么是监督学习？": "监督学习是机器学习的一种类型，训练数据包含输入和对应的标签（正确答案），模型通过学习输入与标签之间的映射关系来进行预测。",
        "什么是无监督学习？": "无监督学习是机器学习的一种类型，训练数据没有标签，模型需要自行发现数据中的结构和模式，常见算法有聚类、降维等。",
        "什么是强化学习？": "强化学习是机器学习的一种类型，智能体通过与环境交互获得奖励或惩罚，不断调整策略以最大化累积奖励，常用于游戏、机器人控制等场景。",
        "什么是卷积神经网络？": "卷积神经网络（CNN）是一种专门用于处理网格状数据（如图像）的深度学习模型，通过卷积层、池化层等结构自动提取图像特征，广泛应用于计算机视觉领域。"
    }
    return kb_dict


def build_keyword_mapping(kb):
    """
    构建关键词映射
    :param kb: 知识库字典
    :return: (kw_map, all_keywords_set, classify_kb)
        kw_map: {问题: 关键词集合}
        all_keywords_set: 所有关键词的集合
        classify_kb: {关键词: [包含该关键词的问题列表]}
    """
    kw_map = {}
    all_keywords_set = set()
    classify_kb = {}
    
    for question in kb:
        keywords = extract_keywords_simple(question)
        kw_map[question] = keywords
        all_keywords_set.update(keywords)
        
        for kw in keywords:
            if kw not in classify_kb:
                classify_kb[kw] = []
            classify_kb[kw].append(question)
    
    return kw_map, all_keywords_set, classify_kb


# 模块初始化时自动加载知识库
_kb_cache = None
_kw_map_cache = None
_all_keywords_cache = None
_classify_kb_cache = None


def get_knowledge_base():
    """
    获取知识库（单例模式，只加载一次）
    :return: 知识库字典
    """
    global _kb_cache
    if _kb_cache is None:
        _kb_cache = build_knowledge_base()
    return _kb_cache


def get_kw_map():
    """
    获取关键词映射（单例模式）
    :return: (kw_map, all_keywords_set, classify_kb)
    """
    global _kw_map_cache, _all_keywords_cache, _classify_kb_cache
    if _kw_map_cache is None:
        kb = get_knowledge_base()
        _kw_map_cache, _all_keywords_cache, _classify_kb_cache = build_keyword_mapping(kb)
    return _kw_map_cache, _all_keywords_cache, _classify_kb_cache
