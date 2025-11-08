#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import json
import time
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, Button, Entry

bgNX_SoftwareName = "ChatGoGoGo(ChatBot_GUI)_v1.0"
bgSign = "Created by @DeepThinker（川）(2025_11_8)"

# Main Window Settings (创建主窗口)
root = tk.Tk()
root.title(bgNX_SoftwareName)
root.geometry("800x600")

# Voice Engine (初始化语音引擎)
engine = pyttsx3.init()

def chat_with_ollama(prompt):
    # Ollama API URL (Ollama API的URL)
    url = "http://localhost:11434/api/generate"

    # Request Parameters (发送请求到Ollama API)
    response = requests.post(url, json={"model": "qwen2.5:latest", "prompt": prompt}, stream=True)

    # Response Status Code Check (检查响应状态码)
    if response.status_code == 200:
        # Response Data Processing (逐行读取响应数据)
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    result = json.loads(decoded_line)
                    for char in result['response']:
                        full_response += char
                        text_box.insert(tk.END, char)
                        text_box.see(tk.END)
                        text_box.update_idletasks()
                        time.sleep(0.05)  # Control Output Speed (控制输出速度)
                except json.JSONDecodeError:
                    continue
        return ""
    else:
        # Response Error Handling (如果请求失败，返回错误信息)
        return f"Error: {response.status_code}"

def play_response():
    response = text_box.get("1.0", tk.END).strip()
    if response:
        engine.say(response)
        engine.runAndWait()

def submit_prompt():
    text_box.delete("1.0", tk.END)
    user_prompt = prompt_box.get()
    if user_prompt:
        # Clear Text Box (清空文本框)
        text_box.delete("1.0", tk.END)
        # Get AI Response (获取AI回答)
        response = chat_with_ollama(user_prompt)
        # Display Response in Text Box (在文本框中显示回答)
        text_box.insert(tk.END, response)
        
# Create Text Box (创建文本框)
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
text_box.pack(padx=10, pady=10)

# 创建播放按钮
play_button = Button(root, text="播放回答", command=play_response)
play_button.pack(pady=10)

# Create Prompt Input Box (创建问题输入文本框)
prompt_box = Entry(root, width=80)
prompt_box.pack(padx=10, pady=10)

# Create Submit Button (创建提交按钮)
submit_button = Button(root, text="提交问题", command=submit_prompt)
submit_button.pack(pady=10)

# Example Usage (示例用法)

# Run Main Loop (运行主循环)
root.mainloop()
