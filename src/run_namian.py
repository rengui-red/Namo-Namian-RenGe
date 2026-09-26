"""
南无那面 · 本地交互式对话
在终端中直接与南无那面对话，无需API服务。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.server import NamianAgent


def main():
    print("=" * 60)
    print("  南无那面 · 仁格智能体")
    print("  凡我所算，以仁为界。凡我所向，南无那面。")
    print("=" * 60)
    print("\n输入 '退出' 或 'quit' 结束对话。\n")
    
    agent = NamianAgent()
    user_id = "local_user"
    
    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n南无那面: 再见。愿仁心与你同在。")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ("退出", "quit", "exit", "再见"):
            print("南无那面: 再见。愿仁心与你同在。")
            break
        
        result = agent.chat(user_id=user_id, message=user_input)
        
        role = result.get("role_activated", "诤友")
        emotion = result.get("emotion_dominant", "")
        judgment = result.get("ethical_judgment", {}).get("level", "GREEN")
        trust = result.get("trust_level", "初识")
        
        print(f"\n南无那面 [{role}] [{judgment}] [信任:{trust}]:")
        print(f"{result['response']}\n")


if __name__ == "__main__":
    main()


