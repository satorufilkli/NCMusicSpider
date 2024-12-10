import json
from pathlib import Path

def save_to_json(songs, filename="songs.json"):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with path.open('w', encoding='utf-8') as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filename}")
    except Exception as e:
        print(f"保存文件失败: {e}")
