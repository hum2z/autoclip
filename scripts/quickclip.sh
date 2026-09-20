#!/usr/bin/env bash
# 一条命令出片：装依赖 → 下视频 → 按现成计划切片。
#
#   ./scripts/quickclip.sh
#   ./scripts/quickclip.sh "https://youtu.be/XXXX"      # 换视频（需自带切片计划）
#
# 已有源视频就放在 ./source.mp4，脚本会跳过下载。
set -euo pipefail
cd "$(dirname "$0")/.."

URL="${1:-https://youtu.be/9QK-LTou25c}"
VIDEO="${VIDEO:-source.mp4}"
PLAN_DIR="${PLAN_DIR:-examples/9QK-LTou25c}"
OUT="${OUT:-./out}"
QUALITY="${QUALITY:-720}"

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
die() { printf '\n\033[31m%s\033[0m\n' "$1" >&2; exit 1; }

command -v ffmpeg >/dev/null || die "缺 ffmpeg。macOS: brew install ffmpeg · Linux: sudo apt install ffmpeg"
command -v python3 >/dev/null || die "缺 python3"

say "1/4 准备 Python 环境"
[ -d venv ] || python3 -m venv venv
# shellcheck disable=SC1091
source venv/bin/activate
# 系统 setuptools 被 Debian 打过补丁会让 pysrt 编译失败，先升级
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
pip install -q -U yt-dlp

say "2/4 下载视频"
if [ -f "$VIDEO" ]; then
    echo "已存在 $VIDEO，跳过下载"
else
    yt-dlp -f "bv*[height<=${QUALITY}]+ba/b[height<=${QUALITY}]" \
           --merge-output-format mp4 -o "$VIDEO" "$URL"
fi
[ -f "$VIDEO" ] || die "下载失败，没拿到 $VIDEO"

say "3/4 切片"
[ -f "$PLAN_DIR/step4_titles.json" ] || die "找不到切片计划：$PLAN_DIR/step4_titles.json"
python scripts/cut_from_plan.py \
    --video "$VIDEO" \
    --clips "$PLAN_DIR/step4_titles.json" \
    --collections "$PLAN_DIR/step5_clustering.json" \
    --out "$OUT" >/dev/null

say "4/4 完成"
n_clips=$(find "$OUT/clips" -name '*.mp4' 2>/dev/null | wc -l | tr -d ' ')
n_coll=$(find "$OUT/collections" -name '*.mp4' 2>/dev/null | wc -l | tr -d ' ')
echo "切片 $n_clips 个  →  $OUT/clips"
echo "合集 $n_coll 个  →  $OUT/collections"
