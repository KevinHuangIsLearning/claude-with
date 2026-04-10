#!/usr/bin/env python3
import sys
import json
import re
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def do_save(model_key, log_file):
    # 简单清洗，防止 Shell 传参时带入意外的空白
    model_key = model_key.strip()
    
    if not os.path.exists(log_file) or not model_key:
        return

    with open(log_file, 'r', errors='replace') as f:
        content = f.read()

    # 清洗 ANSI 控制字符
    clean_content = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', content)
    
    # 正则提取 UUID
    match = re.search(r'claude\s+--resume\s+([a-f0-9\-]{36})', clean_content)
    if not match:
        return

    uuid = match.group(1)
    history = load_history()
    
    # 排除重复并置顶
    history = [h for h in history if h['uuid'] != uuid]
    history.append({
        'uuid': uuid,
        'model': model_key,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    save_history(history[-20:])
    print(f"\n[claude-with] Session saved to history (Model: {model_key})", file=sys.stderr)
    
def do_menu():
    history = load_history()
    if not history:
        print("No history found.", file=sys.stderr)
        sys.exit(1)
        
    print("\n=== Claude Session History ===", file=sys.stderr)
    # 倒序显示
    for i, item in enumerate(reversed(history), 1):
        print(f"  {i}. [{item['time']}] Model: {item['model']} (ID: {item['uuid'][:8]}...)", file=sys.stderr)
        
    try:
        # 强制从终端读取输入
        sys.stderr.write("\nEnter number to resume (or Enter to cancel): ")
        sys.stderr.flush()
        choice = sys.stdin.readline().strip()
        
        if not choice:
            sys.exit(1)
            
        idx = int(choice) - 1
        if 0 <= idx < len(history):
            selected = history[len(history) - 1 - idx]
            # 这是唯一输出到 stdout 的内容，会被 Zsh 变量捕获
            sys.stdout.write(f"{selected['model']} {selected['uuid']}\n")
        else:
            print("Invalid choice.", file=sys.stderr)
            sys.exit(1)
    except (ValueError, KeyboardInterrupt, EOFError):
        sys.exit(1)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "save" and len(sys.argv) == 4:
        do_save(sys.argv[2], sys.argv[3])
    elif cmd == "menu":
        do_menu()