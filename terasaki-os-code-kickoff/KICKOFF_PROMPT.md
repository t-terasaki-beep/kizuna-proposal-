# 新セッション 初日に貼る「キックオフ指示」

claude.ai/code で `t-terasaki-beep/terasaki-os-code` を選んで新セッションを作り、
最初のメッセージに以下をそのまま貼ってください。

---

terasaki-os-code を「寺嵜流 提案自動生成OS」として立ち上げてください。

このリポジトリのルートに置く `CLAUDE.md` の内容は、別途お渡しする設計図（terasaki-os-code-kickoff/CLAUDE.md）の通りです。まずそれを `CLAUDE.md` として作成してください。

そのうえで、以下を順に進めてください。

1. README.md を作成（OSの目的・使い方・毎月の更新ループを簡潔に）。
2. ディレクトリ雛形を作成: knowledge/ templates/ engine/ customers/ data/
3. data/inputs.schema.json と data/inputs.example.json を作成（KIZUNA案件の数値を例に）。
   - 例: 年間電気代700万円 / 年間使用量18万kWh / 24時間稼働 / 冬の早朝ピーク / 入居率30% /
     満床時 約2100万円規模。
4. engine/diagnose.py を作成: 入力JSON → A/Bプランの算出
   （投資総額・補助金・自己負担・回収年数・年間削減額(現状/満床)・20年累計効果）。
   KIZUNA実績で答え合わせ: Aプラン 投資2167万/補助496万/自己負担1671万/回収6.0年、
   Bプラン 自己負担2448万/回収7.6年。年間削減 現状A277万・B322万 / 満床A408万・B558万。
5. templates/deck.html: KIZUNAの index.html をテンプレ化（差し込み箇所を変数化）。
6. engine/build_proposal.py: inputs.json + diagnose結果 → index.html を生成。
7. engine/mp3gen.py: ナレーション台本(7〜8本) → audio/NN.mp3（edge-tts ja-JP-NanamiNeural）。
8. customers/kizuna-home/ に一連を再現し、生成物が元のKIZUNA提案に一致することを確認。

各ステップはコミットして、指定ブランチにプッシュしてください。
最後に「次の顧客の提案を作る手順」を README にまとめてください。

毎月の運用として、成約/失注の理由を customers/<顧客名>/outcome.md に記録し、
効いた表現・数字・補助金情報を knowledge/ に昇格して、OSを継続的に賢くしてください。

---

## 補足（任意で添える一文）

「KIZUNAの index.html / ナレーション台本 / mp3gen_kizuna.py を参考資料として渡します。
これを“型”として一般化してください」と添えると、移植がスムーズです。
（kizuna-proposal リポジトリから index.html・mp3gen_kizuna.py をコピーして渡せばOK）
