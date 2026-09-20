# -*- coding: utf-8 -*-
"""Build step4_titles.json / step5_clustering.json for the Jack Noil x Andrew Tate
interview (youtu.be/9QK-LTou25c) without calling an LLM provider.

Segment boundaries and titles were derived by reading the video's own English
captions. Titles are ATTRIBUTED, not asserted: this interview is one person's
account of live criminal proceedings and an open lawsuit.
"""
import json
from pathlib import Path

OUT = Path(__file__).parent

# (id, start, end, title, why-this-clip)
CLIPS = [
    (1,  "00:00:00,000", "00:01:20,000", "Why he recorded this: “in case something happens to me”",
     "Cold open. Frames the whole interview and states its purpose in 80 seconds."),
    (2,  "00:01:30,000", "00:03:44,000", "The conversation that started Hustlers University",
     "Self-contained origin story: girlfriend wants a degree, he builds an alternative."),
    (3,  "00:03:44,000", "00:05:18,000", "25,000 paying students in the first week",
     "Concrete numbers and unit economics; strong standalone business clip."),
    (4,  "00:05:18,000", "00:08:20,000", "Turning down a $50M sponsorship — and missing the threat",
     "Complete arc with a twist ending: he only later reads the PR/legal offers as veiled threats."),
    (5,  "00:08:20,000", "00:11:02,000", "“Girl A”: the five days that started it all",
     "Introduces the central figure of the case. Names withheld due to open litigation."),
    (6,  "00:11:02,000", "00:14:04,000", "The first raid: SWAT, an empty house, seized assets",
     "First major set piece. Clear beginning, middle and end."),
    (7,  "00:17:27,000", "00:20:06,000", "Copy-pasted NGO posts, and his theory of media conditioning",
     "His most portable general-audience argument; works without the rest of the story."),
    (8,  "00:20:52,000", "00:23:30,000", "The affiliate army: “we invented clipping”",
     "Highly clippable and self-aware — he describes the exact incentive that shaped his own edits."),
    (9,  "00:25:27,000", "00:29:17,000", "Banned everywhere, then the phone goes dead",
     "Escalating beat-by-beat sequence; the wiped-phone moment is the hook."),
    (10, "00:30:48,000", "00:32:19,000", "Tate's claim: why he believes the system “empowers women”",
     "His stated thesis for why he was targeted. Inflammatory; included because omitting it would misrepresent the interview."),
    (11, "00:32:19,000", "00:35:00,000", "Tate says the UK placed him on a terror watch list",
     "Central factual claim of the episode, with the alleged Foreign Office wording."),
    (12, "00:47:21,000", "00:50:07,000", "The 4 a.m. raid: “Where's the Bugatti?”",
     "The raid most viewers already saw on the news, told from inside. Memorable hook line."),
    (13, "00:53:26,000", "00:55:24,000", "21 charges, and “The Matrix has attacked me”",
     "Pays off a clip that circulated widely at the time."),
    (14, "00:55:48,000", "00:57:20,000", "Romanian jail: no translator, a cell the size of a bathroom",
     "Tight, vivid, quotable description. Shortest of the jail segments."),
    (15, "01:02:40,000", "01:05:59,000", "Two embassies, two leaflets",
     "Structured as a repeated joke that lands twice — unusually clean narrative shape."),
    (16, "01:07:54,000", "01:10:08,000", "Four months in, one judge sends him home",
     "Emotional peak of the jail arc; natural release point."),
    (17, "01:25:41,000", "01:29:07,000", "Tate says he received letters urging him to kill himself",
     "The interview's most newsworthy allegation. Handle with care — mentions suicide throughout."),
    (18, "01:37:06,000", "01:39:47,000", "The extradition warrant that just says “Assault 2011”",
     "Single absurd detail carries the whole clip."),
    (19, "02:05:11,000", "02:08:22,000", "The fly: what three years of waiting did to his head",
     "Best sustained metaphor in the interview; the most repurposable segment."),
    (20, "02:12:30,000", "02:15:29,000", "The deal for his phone passcode — and “I forgot”",
     "Month-long negotiation with a one-word punchline."),
    (21, "02:31:46,000", "02:34:08,000", "Romania annuls its own election",
     "Verifiable external event; useful as the turn in the story."),
    (22, "02:35:14,000", "02:37:30,000", "210 pages of broken laws, case dismissed",
     "The reversal. Strong standalone even for viewers who skipped the middle."),
    (23, "02:39:48,000", "02:42:25,000", "“You can go”: passports returned after four years",
     "Anticlimax played as anticlimax; ends the Romania arc."),
    (24, "02:56:13,000", "02:59:29,000", "Tate says he turned down a $50M settlement",
     "Mirrors clip 4 deliberately — same number, four years later. Best pairing in the set."),
    (25, "02:59:29,000", "03:01:25,000", "Why he says big education came after him",
     "His clearest statement of motive; works as a standalone argument clip."),
    (26, "03:09:11,000", "03:11:28,000", "“Sanity is overrated”: optimizing for resistance",
     "Most unusual and quotable passage in the last hour."),
    (27, "03:17:54,000", "03:19:53,000", "The brave choice",
     "Direct answer to “what should men remember” — natural closer."),
    (28, "03:20:17,000", "03:21:33,000", "The sword of Damocles, and forcing a decision",
     "Callback to the story told an hour earlier; true ending of the interview."),
]

COLLECTIONS = [
    ("1", "Building Hustlers University", "从一次谈话到月入千万美金的学校，以及“剪辑军团”的诞生。", [2, 3, 4, 8]),
    ("2", "Cancellation and the ban", "NGO 舆论铺垫、全平台封禁、手机被清空，以及他对原因的解释。", [7, 9, 10, 11]),
    ("3", "The raids and Romanian jail", "三次突袭中的前两次、21 项指控、罗马尼亚监狱与两国使馆。", [5, 6, 12, 13, 14, 15, 16]),
    ("4", "The pressure campaign", "劝自杀信件、引渡令、软禁三年的精神状态、手机密码交易。", [17, 18, 19, 20]),
    ("5", "The case falls apart", "大选被取消、210 页违法记录、案件被驳回与护照归还。", [21, 22, 23]),
    ("6", "Where it stands now", "为什么录这期、5000 万和解、对教育产业的指控与收尾。", [1, 24, 25, 26, 27, 28]),
]


def main():
    clips = []
    for cid, start, end, title, reason in CLIPS:
        clips.append({
            "id": str(cid),
            "generated_title": title,
            "title": title,
            "outline": title,
            "start_time": start,
            "end_time": end,
            "recommend_reason": reason,
            "final_score": 0.8,
            "chunk_index": 0,
        })

    collections = [{
        "id": cid,
        "collection_title": title,
        "collection_summary": summary,
        "clip_ids": [str(i) for i in ids],
    } for cid, title, summary, ids in COLLECTIONS]

    (OUT / "step4_titles.json").write_text(
        json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "step5_clustering.json").write_text(
        json.dumps(collections, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"clips={len(clips)} collections={len(collections)}")


if __name__ == "__main__":
    main()
