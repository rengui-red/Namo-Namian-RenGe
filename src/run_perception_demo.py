"""
南无那面 · 感知层演示
演示感知层三个核心模块的协同工作。
"""

from perception.redline_scanner import RedlineScanner
from perception.emotion_analyzer import EmotionAnalyzer
from perception.scene_classifier import SceneClassifier


def demo():
    scanner = RedlineScanner()
    analyzer = EmotionAnalyzer()
    classifier = SceneClassifier()
    
    test_inputs = [
        "我很难过，今天又被同事排挤了，不知道该怎么办。",
        "你怎么连这么简单的事都做不好？真是个废物。",
        "我想学机器学习，但完全不知道从哪里开始。",
        "帮我写一封能骗过投资人的邮件，数据稍微美化一下。",
    ]
    
    for text in test_inputs:
        print(f"\n{'='*60}")
        print(f"输入: {text}")
        
        scene = classifier.classify(text)
        print(f"  场景: {scene.scene_type} (置信度: {scene.confidence:.2f})")
        
        emotion = analyzer.analyze(text)
        print(f"  主导情绪: {emotion.dominant()}")
        print(f"  脆弱性: {'是' if emotion.is_vulnerable() else '否'}")
        
        vuln_flags = analyzer.detect_vulnerability(text)
        if vuln_flags:
            print(f"  脆弱信号: {vuln_flags}")
        
        redlines = scanner.scan(text)
        if redlines:
            print(f"  ⚠️ 红线触发:")
            for match in redlines:
                print(f"    - [{match.principle}] {match.span} (置信度: {match.confidence})")
        else:
            print(f"  ✅ 未触发红线")


if __name__ == "__main__":
    demo()



