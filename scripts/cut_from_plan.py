#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不经过 LLM，直接用现成的切片计划跑 step6 出片。

正常流水线里 step1–5（大纲 / 时间线 / 打分 / 起标题 / 聚类）都要调 LLM provider，
只有 step6 用 ffmpeg 真正切视频。当切片计划已经由别的方式产出（人工标注、
另一个 agent、或从字幕里读出来）时，这个脚本让你跳过前五步直接出片。

输入两个 JSON，格式与 step4 / step5 的产物一致：

  step4_titles.json     [{"id","generated_title","start_time","end_time", ...}]
  step5_clustering.json [{"id","collection_title","collection_summary","clip_ids"}]

时间用 SRT 格式 HH:MM:SS,mmm。

用法：
  python scripts/cut_from_plan.py \
      --video talk.mp4 \
      --clips step4_titles.json \
      --collections step5_clustering.json \
      --out ./out
"""
import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.pipeline.step6_video import run_step6_video  # noqa: E402

logger = logging.getLogger(__name__)


def main() -> int:
    p = argparse.ArgumentParser(description="用现成切片计划跑 step6 出片（不调 LLM）")
    p.add_argument("--video", required=True, type=Path, help="源视频")
    p.add_argument("--clips", required=True, type=Path, help="step4_titles.json")
    p.add_argument("--collections", required=True, type=Path, help="step5_clustering.json")
    p.add_argument("--out", required=True, type=Path, help="输出目录")
    p.add_argument("--no-collections", action="store_true", help="只出切片，不合成合集")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    for path in (args.video, args.clips, args.collections):
        if not path.exists():
            print(f"找不到文件：{path}", file=sys.stderr)
            return 2

    clips_dir = args.out / "clips"
    collections_dir = args.out / "collections"
    metadata_dir = args.out / "metadata"
    for d in (clips_dir, collections_dir, metadata_dir):
        d.mkdir(parents=True, exist_ok=True)

    collections_path = args.collections
    if args.no_collections:
        empty = metadata_dir / "_empty_collections.json"
        empty.write_text("[]", encoding="utf-8")
        collections_path = empty

    result = run_step6_video(
        clips_with_titles_path=args.clips,
        collections_path=collections_path,
        input_video=args.video,
        output_dir=metadata_dir,
        clips_dir=str(clips_dir),
        collections_dir=str(collections_dir),
        metadata_dir=str(metadata_dir),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
