# -*- coding: utf-8 -*-
"""
mp3gen.py — ナレーション台本 → MP3 音声（edge-tts）

inputs.json から寺嵜流ナレーションを再構成し、ja-JP-NanamiNeural で
audio/01.mp3 〜 NN.mp3 を生成する（index.html と同じ顧客フォルダの audio/ に出力）。

事前準備: pip install edge-tts
使い方  : python engine/mp3gen.py customers/kizuna-home/inputs.json
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagnose import diagnose          # noqa: E402
from build_proposal import build_narrations  # noqa: E402

VOICE = "ja-JP-NanamiNeural"
RATE = "+0%"
VOLUME = "+0%"


async def generate(inputs_path: str):
    with open(inputs_path, encoding="utf-8") as f:
        inp = json.load(f)
    narrations = build_narrations(inp, diagnose(inp))

    outdir = os.path.join(os.path.dirname(os.path.abspath(inputs_path)), "audio")
    os.makedirs(outdir, exist_ok=True)

    import edge_tts  # 遅延import: 未インストール時に分かりやすく案内
    for i, text in enumerate(narrations, start=1):
        num = f"{i:02d}"
        out = os.path.join(outdir, f"{num}.mp3")
        print(f"[{i}/{len(narrations)}] スライド{num} を生成中...")
        c = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME)
        await c.save(out)
    print("\n===== 完了 =====")
    print(f"MP3 {len(narrations)}個を {outdir}/ に出力しました。")


def main(argv):
    if len(argv) < 2:
        print("usage: python engine/mp3gen.py <inputs.json>")
        return 1
    try:
        asyncio.run(generate(argv[1]))
    except ImportError:
        print("edge-tts が見つかりません。`pip install edge-tts` を実行してください。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
