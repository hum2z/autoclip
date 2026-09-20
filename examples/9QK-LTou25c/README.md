# 示例：无 LLM 的切片计划

这是一份用于 `scripts/cut_from_plan.py` 的样例输入，对应一期 3 小时 21 分的长访谈
（YouTube `9QK-LTou25c`，Jack Noil 播客）。

## 它证明了什么

正常流水线里 step1–5 都要调 LLM provider，只有 step6 用 ffmpeg 真正切视频。
当切片计划已经由别的方式产出时（人工标注、另一个 agent、从字幕里读出来），
可以跳过前五步直接出片：

```bash
python scripts/cut_from_plan.py \
    --video source.mp4 \
    --clips  examples/9QK-LTou25c/step4_titles.json \
    --collections examples/9QK-LTou25c/step5_clustering.json \
    --out ./out
```

28 个切片 + 6 个合集。已用同长度合成视频（关键帧间隔 2 秒）验证：
切片时长与计划的最大偏差 1.04 秒。

## 关于偏差

`extract_clip` 用 `-c:v copy` 流复制，切点会吸附到最近的关键帧，
所以起点可能比计划早几秒。上限取决于源视频的关键帧间隔：
2 秒间隔 → 偏差 ≤ 约 1 秒；间隔越大偏差越大。需要逐帧精确就得重编码。

## 关于内容

`step4_titles.json` 里的标题是**转述，不是断言**。这期访谈是当事人对仍在进行中的
刑事程序和一桩未结诉讼的单方面陈述，标题按「他说……」的口径写，
不要改成把争议主张当既成事实的说法。其中几段涉及自杀话题。

计划本身由 `make_plan.py` 生成，时间点来自该视频自带的英文字幕。
