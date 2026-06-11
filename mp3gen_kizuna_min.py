# -*- coding: utf-8 -*-
# =============================================================================
# KIZUNA HOME 様 ご提案（ミニマム版・4枚）ナレーションMP3生成スクリプト
# 音声: ja-JP-NanamiNeural (edge-tts)
# 出力: ./audio/01.mp3 〜 04.mp3  (index-min.html と同じ階層に置く)
# 事前準備: pip install edge-tts
# 実行    : python mp3gen_kizuna_min.py
#  ※ ブラウザ音声（推奨）で再生できるため、MP3はオフライン予備用です。
# =============================================================================
import asyncio, os
import edge_tts

VOICE  = "ja-JP-NanamiNeural"
RATE   = "+0%"
VOLUME = "+0%"
OUTDIR = "audio"

NARRATIONS = [
    "皆川様、本日はご覧いただきありがとうございます。株式会社シスコムネットの寺嵜より、先日の省エネルギー診断の結果を踏まえ、KIZUNA HOME様の電気代削減のご提案を、要点だけ短くお伝えいたします。",
    "まず現状です。KIZUNA HOME様の年間電気代は約700万円、入居率はまだ約30パーセントですが、満床に近づくと約2100万円規模まで増える見込みです。そこで、窓のコーティングで減らし、太陽光78.75キロワットで作り、蓄電池40.5キロワットアワーで貯める。この3段階で電気代を下げ、停電時にもご入居者様を守ります。",
    "費用と効果です。千葉県の補助金約496万円を活用し、自己負担はAプラン1671万円、Bプラン2448万円。年間の電気代削減は現状でAプラン277万円からBプラン322万円、満床時にはさらに広がり、投資回収は4年台まで短縮します。20年間の累計では最大で約8700万円の効果が見込めます。",
    "まとめです。ひとつ、電気代は確実に下がります。ふたつ、補助金で実質負担を抑えられます。みっつ、停電時もご入居者様を守れます。ひとつだけ、補助金は交付決定の前に契約や着工をすると対象外になる点にご注意ください。申請の手続きは寺嵜が代行いたします。お問い合わせは、電話043-261-8033、メールt-terasaki@syscomnet.co.jpまで。寺嵜が最後まで伴走いたします。",
]

async def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for i, text in enumerate(NARRATIONS, start=1):
        num = f"{i:02d}"
        out = os.path.join(OUTDIR, f"{num}.mp3")
        print(f"[{i}/{len(NARRATIONS)}] スライド{num} を生成中...")
        c = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME)
        await c.save(out)
    print("")
    print("===== 完了しました =====")
    print(f"MP3 {len(NARRATIONS)}個を {OUTDIR}/ に出力しました。")

if __name__ == "__main__":
    asyncio.run(main())
