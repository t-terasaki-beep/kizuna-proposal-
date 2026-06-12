# terasaki-os-code — 寺嵜流 提案自動生成OS

顧客の電気データを入れるだけで、**寺嵜流の省エネ・脱炭素 提案書**（スライド＋ナレーション台本＋MP3）を自動生成する仕組みです。KIZUNA HOME 提案を「型」として一般化しています。

> 詳しい設計思想・口調・運用ルールは [`CLAUDE.md`](./CLAUDE.md) を参照。

## クイックスタート

```bash
# 1) 顧客フォルダに入力を用意（data/inputs.schema.json に準拠）
cp -r customers/kizuna-home customers/<新顧客>
$EDITOR customers/<新顧客>/inputs.json

# 2) 数値診断（自己負担・回収年数・20年累計を検算表示）
python engine/diagnose.py customers/<新顧客>/inputs.json

# 3) 提案スライド + ナレーション台本を生成 → index.html
python engine/build_proposal.py customers/<新顧客>/inputs.json

# 4) ナレーションをMP3化（任意・オフライン予備音声）
pip install edge-tts
python engine/mp3gen.py customers/<新顧客>/inputs.json
```

生成物（顧客フォルダ内）:
- `index.html` … 単一ファイルの提案デッキ（ブラウザ音声＝高品質／MP3＝予備）
- `narration.txt` … ナレーション台本（確認・修正用）
- `audio/01.mp3 …` … ナレーション音声

`index.html` はブラウザで開くだけで動作（外部依存はGoogle Fontsのみ）。商談ではこれを画面共有/送付します。

## 仕組み（3部品）

| ファイル | 役割 |
|---|---|
| `engine/diagnose.py` | 入力 → A/Bプランの数値算出。自己負担＝投資−補助金、回収＝自己負担÷年間削減、20年累計＝満床削減×20−自己負担 |
| `engine/build_proposal.py` | 入力＋診断 → 寺嵜流8枚スライド＋ナレーションを `templates/shell.html` に流し込み `index.html` 生成 |
| `engine/mp3gen.py` | ナレーション → `ja-JP-NanamiNeural` でMP3化 |

`templates/shell.html` はKIZUNAの `index.html` からCSS/JSをそのまま継承し、データ部分だけトークン化したものです（デザインは一切変えずに中身だけ差し替わる）。

## 寺嵜流8枚の型

表紙 → 現状の課題 → 減らす/作る/貯める → A/Bプラン → 削減効果と回収 → 停電時の備え → 進め方と補助金スケジュール → まとめ＋連絡先。
（順番・論法・口調は `CLAUDE.md` に定義。崩さないこと）

## 検算（KIZUNA実績との一致）

`python engine/diagnose.py customers/kizuna-home/inputs.json` の出力は、元提案書と一致します:

- Aプラン: 自己負担 1,671万 / 回収 6.0年 → 満床4.1年 / 20年 6,489万
- Bプラン: 自己負担 2,448万 / 回収 7.6年 → 満床4.4年 / **20年 8,712万**（提案書の「約8,712万円」と一致）

## 毎月の更新ループ（OSを賢くする）

1. 成約/失注の理由を `customers/<顧客>/outcome.md` に記録。
2. 効いた表現・数字・補助金情報を `knowledge/` に昇格。
3. テンプレ・単価・補助金カレンダーを最新化し、この変更履歴を残す。

## 注意

- 年間削減額（`savings_*`）は**省エネ診断の実値**を入れる。OSが勝手に盛らない（回収年数等は診断値から機械的に算出）。
- 補助金の締切・要件は一次情報で確認し、`knowledge/subsidies.md` に出典付きで記録。
- 顧客情報を外部サービスに送らない。
