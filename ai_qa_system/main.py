# -*- coding: utf-8 -*-
"""
AI基础问答系统 - 主程序入口
使用Tkinter构建可视化GUI界面
"""

import sys
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

from knowledge_base import get_knowledge_base, get_kw_map
from match_engine import match_answer
from record_log import add_record, save_record, get_all_records


class AIQAApp:
    """
    AI基础问答系统GUI主类
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI基础问答系统")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # 加载知识库
        try:
            self.kb = get_knowledge_base()
            self.kw_map, self.all_keywords, self.classify_kb = get_kw_map()
        except Exception as e:
            messagebox.showerror("错误", f"知识库初始化失败：{e}")
            sys.exit(1)
        
        self.create_widgets()
        self.show_welcome()
    
    def create_widgets(self):
        """
        创建界面组件
        """
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="AI 基础问答系统",
            font=("微软雅黑", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=12)
        
        tip_label = tk.Label(
            self.root,
            text="请输入人工智能相关问题，输入【退出】结束问答",
            font=("微软雅黑", 10),
            fg="#7f8c8d"
        )
        tip_label.pack(pady=5)
        
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            font=("微软雅黑", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ecf0f1"
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        self.chat_text.tag_config("user", foreground="#2980b9", font=("微软雅黑", 11, "bold"))
        self.chat_text.tag_config("bot", foreground="#27ae60", font=("微软雅黑", 11, "bold"))
        self.chat_text.tag_config("system", foreground="#e67e22", font=("微软雅黑", 10, "italic"))
        
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("微软雅黑", 12),
            width=50
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.input_entry.bind("<Return>", lambda event: self.submit_question())
        self.input_entry.focus_set()
        
        submit_btn = tk.Button(
            input_frame,
            text="提交",
            font=("微软雅黑", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=8,
            command=self.submit_question
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(
            input_frame,
            text="退出",
            font=("微软雅黑", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=8,
            command=self.exit_program
        )
        exit_btn.pack(side=tk.LEFT)
        
        status_frame = tk.Frame(self.root, bg="#bdc3c7", height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"知识库: {len(self.kb)} 条问答 | 已提问: 0 次",
            font=("微软雅黑", 9),
            fg="#2c3e50",
            bg="#bdc3c7"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def show_welcome(self):
        """
        显示欢迎消息
        """
        self._append_text("system", "【系统】欢迎使用AI基础问答系统！\n")
        self._append_text("system", f"【系统】当前知识库共 {len(self.kb)} 条问答，涵盖人工智能基础知识。\n")
        self._append_text("system", "【系统】您可以输入问题进行提问，输入【退出】结束程序。\n\n")
    
    def _append_text(self, tag, text):
        """
        向聊天文本框追加内容
        :param tag: 文本标签（user/bot/system）
        :param text: 文本内容
        """
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, text, tag)
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def submit_question(self):
        """
        提交问题并获取答案
        """
        user_input = self.input_entry.get().strip()
        
        if not user_input:
            messagebox.showwarning("提示", "请输入有效问题")
            return
        
        if user_input == "退出":
            self.exit_program()
            return
        
        self._append_text("user", f"【你】{user_input}\n\n")
        self.input_entry.delete(0, tk.END)
        
        answer = match_answer(user_input, self.kb, self.kw_map)
        
        add_record(user_input, answer)
        
        self._append_text("bot", f"【AI助手】{answer}\n\n")
        
        self._update_status()
    
    def _update_status(self):
        """
        更新状态栏
        """
        record_count = len(get_all_records())
        self.status_label.config(text=f"知识库: {len(self.kb)} 条问答 | 已提问: {record_count} 次")
    
    def exit_program(self):
        """
        退出程序，保存日志
        """
        records = get_all_records()
        if records:
            success, result = save_record()
            if success:
                messagebox.showinfo("提示", f"已保存 {len(records)} 条提问记录到：\n{result}")
            else:
                messagebox.showwarning("警告", f"保存记录失败：{result}")
        
        self.root.destroy()
        sys.exit(0)


def main():
    """
    主函数
    """
    root = tk.Tk()
    app = AIQAApp(root)
    
    root.protocol("WM_DELETE_WINDOW", app.exit_program)
    
    root.mainloop()


if __name__ == "__main__":
    main()
