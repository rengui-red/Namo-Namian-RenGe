"""
南无那面 · 知识系统演示
演示知识图谱与角色系统的协同工作。
"""

import sys
sys.path.insert(0, '.')

from roles.role_loader import RoleLoader
from knowledge.kg_simple import SimpleKnowledgeGraph


def run_demo():
    print("=" * 60)
    print("  南无那面 · 知识系统演示")
    print("=" * 60)
    
    # 初始化
    role_loader = RoleLoader()
    kg = SimpleKnowledgeGraph()
    
    # 演示角色系统
    print("\n【角色系统】可用角色：")
    for role_info in role_loader.list_roles():
        print(f"  · {role_info['name']} ({role_info['role_id']})")
        print(f"    {role_info['core_quality'][:60]}...")
    
    # 场景到角色的映射
    print("\n【场景-角色映射】")
    test_scenes = ["conflict_mediation", "education", "counseling", "consulting"]
    for scene in test_scenes:
        role = role_loader.get_role(scene)
        print(f"  {scene} → {role.name} ({role.role_id})")
    
    # 演示知识图谱查询
    print("\n【知识图谱查询】")
    test_situations = [
        {"scene_type": "conflict_mediation"},
        {"scene_type": "counseling"},
        {"scene_type": "education"},
    ]
    
    for situation in test_situations:
        results = kg.query(situation, "")
        case_titles = [c['title'] for c in results['similar_cases']]
        print(f"  场景 {situation['scene_type']}:")
        print(f"    相关判例: {case_titles}")
        if results['suggestions']:
            for sug in results['suggestions']:
                print(f"    ⚠️ {sug['message']}")
    
    # 演示角色风格指南
    print("\n【角色风格指南】")
    for role_id in ["mediator", "mentor", "friend"]:
        style = role_loader.get_style_guide(role_id)
        print(f"  {role_id}:")
        print(f"    前缀: \"{style['prefix_style']}\"")
        print(f"    后缀: \"{style['suffix_style']}\"")
        print(f"    语调: {style['tone']}")
    
    print(f"\n{'=' * 60}")
    print("  演示完成。知识系统已就绪。")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()



