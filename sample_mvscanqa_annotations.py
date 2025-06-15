import json
import random

# 读取MV-ScanQA数据
with open('static/ScanQA_mv_train_0.5_filtered_w_viewinfo.json', 'r') as f:
    full_data = json.load(f)

# 指定要提取的场景
target_scenes = ['scene0000_00', 'scene0001_00', 'scene0002_00', 'scene0003_00', 
                    'scene0004_00', 'scene0005_00', 'scene0006_00', 'scene0007_00',
                    'scene0013_00', 'scene0029_00']

# 按场景分组并采样
sampled_data = []
for scene in target_scenes:
    scene_items = [item for item in full_data if item['scene_id'] == scene]
    if scene_items:
        # 每个场景选3-4个样本
        n_samples = min(random.randint(4, 7), len(scene_items))
        sampled = random.sample(scene_items, n_samples)
        sampled_data.extend(sampled)

# 保存采样数据
with open('static/mvscanqa/sampled_mvscanqa_w_viewinfo.json', 'w') as f:
    json.dump(sampled_data, f, indent=2)

print(f"Sampled {len(sampled_data)} MV-ScanQA examples")
