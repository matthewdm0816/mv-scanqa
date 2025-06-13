import json
import re
from typing import List, Dict, Tuple

class TripAlignAnnotator:
    def __init__(self):
        # 定义关键词模式
        self.spatial_patterns = [
            # 位置关系词
            r'\b(above|below|beside|between|behind|in front of|next to|adjacent to|near|far from|left|right|top|bottom|center|corner|opposite|facing|against|along|around|across from|on the left|on the right|in the background|in the foreground)\b',
            # 位置动词
            r'\b(positioned|located|placed|sits|stands|mounted|arranged|aligned|leaning against|hanging|rests|topped with|set against)\b',
            # 方向词
            r'\b(left side|right side|center of|edge of|beneath|underneath|surrounding|through)\b'
        ]
        
        self.object_property_patterns = [
            # 材质
            r'\b(wooden|wood|metal|glass|plastic|leather|fabric|stone|ceramic|chrome|brass|polished|textured|tiled)\b',
            # 颜色
            r'\b(white|black|gray|grey|beige|brown|blue|green|red|yellow|orange|purple|pink|light-colored|dark-colored|light blue|dark blue|natural)\b',
            # 尺寸
            r'\b(large|small|big|tiny|huge|medium|tall|short|wide|narrow|thick|thin|single|multiple)\b',
            # 形状
            r'\b(round|square|rectangular|circular|oval|triangular|curved|straight|irregular|flat|folded)\b',
            # 风格/质感
            r'\b(modern|vintage|classic|contemporary|traditional|rustic|minimalist|comfortable|cozy|soft|hard|smooth|rough|shiny|matte|clean|neat|tidy|warm|fluffy|cushioned)\b',
            # 状态
            r'\b(open|closed|filled|empty|visible|partially visible|blurred|organized|scattered)\b'
        ]
        
        self.contextual_patterns = [
            # 房间类型
            r'\b(bathroom|living room|bedroom|kitchen|dining room|office|hallway|entrance|lobby|lounge|waiting area)\b',
            # 功能区域
            r'\b(living space|entertainment area|dining area|work space|reading nook|seating area|storage area|bathroom corner|room corner)\b',
            # 空间描述
            r'\b(scene|space|area|room|corner|section|zone|setting|ambiance|appearance|decor)\b',
            # 氛围描述
            r'\b(homey|cozy|inviting|functional|practical|intimate|casual|warm|simple|minimalistic)\b',
            # 用途描述
            r'\b(for relaxation|for conversation|for drying|used for)\b'
        ]
        
        # Multi-object patterns - 物体名词/短语
        self.multi_object_patterns = [
            # 家具类
            r'\b(sofa|couch|chair|armchair|stool|stools|bench|ottoman|office chair)s?\b',
            r'\b(table|tables|desk|counter|cabinet|shelf|shelves|bookshelf|dresser|wardrobe|coffee table|wooden table|entertainment unit|entertainment center)s?\b',
            r'\b(bed|mattress|nightstand|headboard)s?\b',
            
            # 卫浴设施
            r'\b(toilet|sink|bathtub|tub|shower|pedestal sink|faucet|drain|shower curtain|bath mat)s?\b',
            r'\b(towel|towels|bathrobe|hand towel|toilet paper|towel rack)s?\b',
            
            # 电器类
            r'\b(TV|television|computer|monitor|screen|lamp|lamps|light|lights|fixture|chandelier|floor lamp|light fixture|flat-screen TV|coffee maker)s?\b',
            r'\b(refrigerator|fridge|oven|stove|microwave|dishwasher)s?\b',
            
            # 装饰品类
            r'\b(painting|picture|photo|frame|framed artwork|mirror|clock|vase|plant|flower)s?\b',
            r'\b(curtain|curtains|drape|blind|rug|carpet|mat|cushion|pillow)s?\b',
            r'\b(book|books|magazine|decoration|ornament|paper|papers|notepad|booklet|card)s?\b',
            
            # 日常用品
            r'\b(backpack|bag|shoes|phone|bicycle|bike|guitar|wheel|handlebars|seat)s?\b',
            r'\b(trash can|trash bin|liner|coaster|coin|hook|hinge|doorknob)s?\b',
            
            # 建筑元素
            r'\b(door|doors|window|wall|walls|ceiling|floor|floors|stairs|railing|tiles)s?\b',
            r'\b(fireplace|mantel|column|beam)s?\b',
            
            # 带数量的物体短语
            r'\b(two|three|four|five|six|several|multiple|many|various)\s+(?:matching\s+)?\w*\s*(chairs?|stools?|tables?|lamps?|shelves?|books?|pictures?|plants?|towels?|lights?|armchairs?)\b',
            
            # 复合物体名称
            r'\b(bar counter|bar stools?|dining chairs?|coffee table|side table|end table|TV stand|book collection|wooden door|silver doorknob|plastic liner|decorative manner)\b',
        ]
        
        # 根据HTML中的标签颜色定义
        self.tag_templates = {
            'spatial': '<span style="color: #00d1b2;">{}</span>',      # primary
            'property': '<span style="color: #3298dc;">{}</span>',     # info
            'contextual': '<span style="color: #48c774;">{}</span>',   # success
            'multi_object': '<span style="color: #f14668;">{}</span>'  # danger
        }
    
    def find_matches(self, text: str, patterns: List[str]) -> List[Tuple[int, int, str]]:
        """找到所有匹配的文本片段及其位置"""
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append((match.start(), match.end(), match.group()))
        return sorted(matches, key=lambda x: x[0])
    
    def annotate_text(self, text: str) -> str:
        """标注文本中的不同类别"""
        # 收集所有匹配
        all_matches = []
        
        # 查找各类匹配
        spatial_matches = self.find_matches(text, self.spatial_patterns)
        for start, end, match_text in spatial_matches:
            all_matches.append((start, end, 'spatial', match_text))
        
        property_matches = self.find_matches(text, self.object_property_patterns)
        for start, end, match_text in property_matches:
            all_matches.append((start, end, 'property', match_text))
        
        contextual_matches = self.find_matches(text, self.contextual_patterns)
        for start, end, match_text in contextual_matches:
            all_matches.append((start, end, 'contextual', match_text))
        
        multi_object_matches = self.find_matches(text, self.multi_object_patterns)
        for start, end, match_text in multi_object_matches:
            all_matches.append((start, end, 'multi_object', match_text))
        
        # 按位置排序并去除重叠
        all_matches.sort(key=lambda x: (x[0], -x[1]))  # 先按开始位置，再按长度降序
        
        # 去除重叠的匹配（保留更长的）
        filtered_matches = []
        last_end = -1
        for start, end, category, match_text in all_matches:
            if start >= last_end:
                filtered_matches.append((start, end, category, match_text))
                last_end = end
        
        # 构建标注后的文本
        if not filtered_matches:
            return text
        
        annotated_text = ""
        last_pos = 0
        
        for start, end, category, match_text in filtered_matches:
            # 添加未标注的部分
            annotated_text += text[last_pos:start]
            # 添加标注的部分
            annotated_text += self.tag_templates[category].format(match_text)
            last_pos = end
        
        # 添加最后剩余的部分
        annotated_text += text[last_pos:]
        
        return annotated_text
    
    def process_dataset(self, input_file: str, output_file: str):
        """处理整个数据集"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理每个条目
        for item in data:
            original_description = item['description']
            annotated_description = self.annotate_text(original_description)
            item['annotated_description'] = annotated_description
            
            # 添加统计信息
            item['annotation_stats'] = {
                'spatial_relations': len(re.findall(r'color: #00d1b2', annotated_description)),
                'object_properties': len(re.findall(r'color: #3298dc', annotated_description)),
                'contextual_understanding': len(re.findall(r'color: #48c774', annotated_description)),
                'multi_object_alignment': len(re.findall(r'color: #ffdd57', annotated_description))
            }
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"处理完成！共处理 {len(data)} 条数据")
        print(f"结果保存到: {output_file}")

# 使用示例
if __name__ == "__main__":
    annotator = TripAlignAnnotator()
    
    # 测试单个文本
    test_text = "The image shows a cozy living space with a wooden bar counter and four matching bar stools. Adjacent to the bar is a comfortable blue couch, and behind it, a built-in wooden entertainment center with shelves filled with books and a TV."
    
    print("原始文本:")
    print(test_text)
    print("\n标注后的文本:")
    print(annotator.annotate_text(test_text))
    
    # 处理整个数据集
    annotator.process_dataset('static/tripalign/sampled_annotations.json', 'static/tripalign/annotated_tripalign.json')
