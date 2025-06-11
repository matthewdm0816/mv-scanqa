import json
import random

# 读取完整的JSON文件
# with open('static/tripalign/annotations_with_score_70.0_train.json', 'r') as f:
with open('static/tripalign/annotations_gpt4o_train.json', 'r') as f:
    full_data = json.load(f)

# 指定要提取的场景
target_scenes = ['scene0000_00', 'scene0013_00', 'scene0029_00']

# 按场景分组数据
scene_data = {}
for item in full_data:
    scene_id = item['scene_id']
    if scene_id in target_scenes:
        if scene_id not in scene_data:
            scene_data[scene_id] = []
        scene_data[scene_id].append(item)

# 为每个场景选择3-5个不同frame的数据
sampled_data = []
for scene_id, items in scene_data.items():
    # 按frame_id分组
    frame_groups = {}
    for item in items:
        frame_id = item['frame_id']
        if frame_id not in frame_groups:
            frame_groups[frame_id] = []
        frame_groups[frame_id].append(item)
    
    # 随机选择3-5个不同的frames
    selected_frames = random.sample(list(frame_groups.keys()), 
                                  min(random.randint(5, 8), len(frame_groups)))
    
    # 从每个frame选择最高分的描述
    for frame_id in selected_frames:
        frame_items = frame_groups[frame_id]
        best_item = max(frame_items, key=lambda x: x.get('itm_score', 0))
        sampled_data.append(best_item)

# 保存采样后的数据
with open('static/tripalign/sampled_annotations.json', 'w') as f:
    json.dump(sampled_data, f, indent=2)

print(f"Sampled {len(sampled_data)} items from {len(target_scenes)} scenes")

