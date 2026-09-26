#!/usr/bin/env python3
"""
南无那面 · 知识图谱迁移脚本
将 src/knowledge/kg_simple.py 中的简易知识图谱数据迁移至 Neo4j 图数据库。

用法:
    python scripts/migrate_to_neo4j.py                          # 使用默认配置
    python scripts/migrate_to_neo4j.py --uri bolt://localhost:7687 --user neo4j --password namian
    python scripts/migrate_to_neo4j.py --dry-run                # 仅打印Cypher语句，不执行

环境变量:
    NEO4J_URI       Neo4j连接地址 (默认: bolt://localhost:7687)
    NEO4J_USER      用户名 (默认: neo4j)
    NEO4J_PASSWORD  密码 (默认: namian)
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Optional

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.knowledge.kg_simple import SimpleKnowledgeGraph


class Neo4jMigrator:
    """知识图谱迁移器 — 将简易KG数据导入Neo4j"""

    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.cypher_statements: List[str] = []

    def connect(self):
        """连接Neo4j"""
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            return True
        except ImportError:
            print("❌ 未安装 neo4j 驱动。请运行: pip install neo4j")
            return False
        except Exception as e:
            print(f"❌ 无法连接 Neo4j: {e}")
            return False

    def disconnect(self):
        """断开Neo4j连接"""
        if self.driver:
            self.driver.close()

    def generate_cypher(self, kg: SimpleKnowledgeGraph) -> List[str]:
        """从简易知识图谱生成Cypher语句"""
        statements = []

        # 创建约束
        statements.append("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Principle) REQUIRE p.name IS UNIQUE;")
        statements.append("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Case) REQUIRE c.title IS UNIQUE;")

        # 导入原则节点
        for principle_name, principle_data in kg.principles.items():
            safe_name = principle_name.replace("'", "\\'")
            safe_text = principle_data.get("text", "").replace("'", "\\'")
            safe_source = principle_data.get("source", "").replace("'", "\\'")
            statements.append(
                f"MERGE (p:Principle {{name: '{safe_name}'}}) "
                f"SET p.text = '{safe_text}', p.source = '{safe_source}';"
            )

        # 导入案例节点
        for case_name, case_data in kg.cases.items():
            safe_title = case_data.get("title", case_name).replace("'", "\\'")
            safe_summary = case_data.get("summary", "").replace("'", "\\'")
            safe_source = case_data.get("source", "").replace("'", "\\'")
            statements.append(
                f"MERGE (c:Case {{title: '{safe_title}'}}) "
                f"SET c.summary = '{safe_summary}', c.source = '{safe_source}';"
            )

            # 案例与原则的关系
            for p_name in case_data.get("principles", []):
                safe_p = p_name.replace("'", "\\'")
                statements.append(
                    f"MATCH (c:Case {{title: '{safe_title}'}}), "
                    f"(p:Principle {{name: '{safe_p}'}}) "
                    f"MERGE (c)-[:INVOKES]->(p);"
                )

        return statements

    def execute(self, statements: List[str], dry_run: bool = False):
        """执行Cypher语句"""
        for i, stmt in enumerate(statements, 1):
            if dry_run:
                print(f"[{i}/{len(statements)}] {stmt}")
            else:
                try:
                    with self.driver.session() as session:
                        session.run(stmt)
                    print(f"✅ [{i}/{len(statements)}] 执行成功")
                except Exception as e:
                    print(f"⚠️ [{i}/{len(statements)}] 执行失败: {e}")

    def run(self, dry_run: bool = False):
        """执行完整迁移流程"""
        print("=" * 60)
        print("  南无那面 · 知识图谱迁移")
        print("=" * 60)

        # 加载简易KG数据
        print("\n📖 加载简易知识图谱数据...")
        kg = SimpleKnowledgeGraph()
        print(f"   原则节点: {len(kg.principles)} 个")
        print(f"   案例节点: {len(kg.cases)} 个")

        # 生成Cypher语句
        print("\n📝 生成Cypher语句...")
        statements = self.generate_cypher(kg)
        print(f"   共 {len(statements)} 条语句")

        if dry_run:
            print("\n🔍 预演模式 — 仅打印Cypher语句:\n")
            self.execute(statements, dry_run=True)
        else:
            print(f"\n🔗 连接 Neo4j: {self.uri}")
            if not self.connect():
                return
            print("✅ 连接成功")

            print("\n📥 执行数据导入...")
            self.execute(statements, dry_run=False)
            self.disconnect()

        print("\n" + "=" * 60)
        print("  迁移完成。凡我所算，以仁为界。")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="南无那面 知识图谱迁移工具")
    parser.add_argument("--uri", default=os.environ.get("NEO4J_URI", "bolt://localhost:7687"))
    parser.add_argument("--user", default=os.environ.get("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=os.environ.get("NEO4J_PASSWORD", "namian"))
    parser.add_argument("--dry-run", action="store_true", help="仅打印Cypher语句，不执行")
    args = parser.parse_args()

    migrator = Neo4jMigrator(uri=args.uri, user=args.user, password=args.password)
    migrator.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()



