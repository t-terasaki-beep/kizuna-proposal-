# -*- coding: utf-8 -*-
"""
build_proposal.py — inputs.json + 診断結果 → 寺嵜流スライド(index.html) を生成

寺嵜流の8枚構成（表紙／現状／3段階／A・Bプラン／削減効果／停電時／進め方／まとめ）を、
顧客データから自動で組み立てる。テンプレートは templates/shell.html（CSS/JS共通）。

使い方:
  python engine/build_proposal.py customers/kizuna-home/inputs.json
  → 同じフォルダに index.html とナレーション台本 narration.txt を出力
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagnose import diagnose  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, "..", "templates", "shell.html")


def fmt(n) -> str:
    """万円・kWh等を 1,671 / 78.75 のように整形。"""
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,}"
    return f"{int(round(n)):,}"


def surname(name: str) -> str:
    """『寺嵜 忠弘』→『寺嵜』。"""
    return name.split()[0] if name else name


# ----------------------------------------------------------------------------
# ナレーション（寺嵜流の語り・1スライド1メッセージ）
# ----------------------------------------------------------------------------
def build_narrations(inp: dict, dx: dict) -> list:
    m, c, me = inp["meta"], inp["current"], inp["measures"]
    bcp, plans = inp["bcp"], inp["plans"]
    A, B = dx["A"], dx["B"]
    sn = surname(m["proposer_name"])
    person = m.get("contact_person", f"{m['customer']}{m.get('customer_honorific','様')}")
    cust = f"{m['customer']}{m.get('customer_honorific','様')}"
    kwh_man = c["annual_kwh"] / 10000
    backup = str(bcp["backup_hours"]).replace("〜", "から").replace("～", "から")
    diag = me.get("diagnosis_note", "省エネ診断")

    sched_txt = "、".join(f"{s['date']}に{s['label']}" for s in inp["schedule"])
    # 注意喚起は「申請代行」の一文を二重にしないよう、前半（対象外の注意）だけ語りに使う
    warn = inp.get("schedule_warning", "").split("申請")[0]

    return [
        # 1 表紙・挨拶
        f"{person}、本日はご覧いただきありがとうございます。{m['proposer_company']}の{sn}より、"
        f"先日の省エネルギー診断の結果を踏まえ、{cust}の電気代削減のご提案を、要点を絞ってお伝えいたします。",
        # 2 現状
        f"まず現状です。{cust}の年間電気代は約{fmt(c['annual_cost_man'])}万円、"
        f"年間使用量は約{fmt(kwh_man)}万キロワットアワー。{c.get('operation','24時間稼働')}で、"
        f"特に{c.get('peak_note','ピーク')}があります。入居率はまだ約{fmt(c['occupancy_pct'])}パーセントですが、"
        f"満床に近づくと電気代は約{fmt(c['full_annual_cost_man'])}万円規模まで増える見込みです。"
        f"だからこそ、減らす、作る、貯める、の3段階が効いてきます。",
        # 3 3段階
        f"ご提案の柱は3段階です。第1に、窓の遮熱・断熱コーティングで熱の出入りを抑え、電気を減らす。"
        f"第2に、太陽光発電{fmt(me.get('solar_kw',0))}キロワットで電気を作る。"
        f"第3に、蓄電池{fmt(me.get('battery_kwh',0))}キロワットアワーで貯めて、夕方から夜に使う。"
        f"いずれも{diag}の結果を踏まえた組み合わせです。",
        # 4 A/Bプラン
        f"ご提案は2つのプランです。Aプランは{plans['A']['name']}を図った構成で、"
        f"投資総額{fmt(A['investment_man'])}万円、補助金{fmt(A['subsidy_man'])}万円を差し引いた"
        f"自己負担は{fmt(A['self_pay_man'])}万円、投資回収は現状ベースで{A['payback_current_yr']}年。"
        f"Bプランは{plans['B']['name']}を狙い、自己負担{fmt(B['self_pay_man'])}万円、回収{B['payback_current_yr']}年です。"
        f"どちらを選ばれても正解になるよう設計しております。",
        # 5 削減効果
        f"電気代の削減効果です。現状の入居率では年間でAプラン{fmt(A['savings_current_man'])}万円、"
        f"Bプラン{fmt(B['savings_current_man'])}万円。満床時にはAプラン{fmt(A['savings_full_man'])}万円、"
        f"Bプラン{fmt(B['savings_full_man'])}万円まで広がります。投資回収は満床達成で"
        f"{A['payback_full_yr']}年から{B['payback_full_yr']}年程度に短縮し、"
        f"20年間の累計では最大で約{fmt(dx['_max_cumulative_20yr_man'])}万円の効果が見込めます。"
        f"入居率の改善と一緒に進めるほど、効果が高まります。",
        # 6 停電時
        f"金額に表れない価値が、停電時の備えです。{m.get('facility_type','本施設')}のご入居者様は"
        f"環境の変化が大きな負担となり、停電や避難は健康リスクに直結します。"
        f"本提案の蓄電池{fmt(bcp['battery_kwh'])}キロワットアワーは、停電時に特定の回路を{backup}時間バックアップし、"
        f"太陽光と連携すれば晴天時は無期限で自立できます。ご入居者様とご家族の安心に直結いたします。",
        # 7 進め方
        f"進め方です。スケジュールは、{sched_txt}、という流れです。"
        f"ひとつだけご注意は、{warn}申請の手続きは{sn}が代行いたしますので、ご負担は最小限です。",
        # 8 まとめ
        f"まとめです。ひとつ、電気代は確実に下がります。ふたつ、補助金で実質負担を抑えられます。"
        f"みっつ、停電時もご入居者様を守れます。まずはこのご提案にお目通しいただき、ご不明な点をお聞かせください。"
        f"ご判断は{person}のペースで構いません。{sn}が最後まで伴走いたします。"
        f"お問い合わせは、電話{m['tel']}、メール{m['email']}まで。",
    ]


# ----------------------------------------------------------------------------
# スライド（寺嵜流の型・8枚）
# ----------------------------------------------------------------------------
def build_slides(inp: dict, dx: dict) -> list:
    m, c, me = inp["meta"], inp["current"], inp["measures"]
    bcp, plans = inp["bcp"], inp["plans"]
    A, B = dx["A"], dx["B"]
    cust = f"{m['customer']} {m.get('customer_honorific','様')}"
    kwh_man = c["annual_kwh"] / 10000
    occ_detail = c.get("occupancy_detail", "")
    diag = me.get("diagnosis_note", "省エネ診断")

    tl = "".join(
        f'<div class="tl"><span class="d">{s["date"]}</span><b>{s["label"]}</b></div>'
        for s in inp["schedule"]
    )

    slides = [
        {"bg": "dark", "cls": "cover", "html": f"""
  <div class="inner" style="text-align:center">
    <div class="eyebrow" style="justify-content:center">ENERGY SAVING PROPOSAL</div>
    <div class="brandmark">省エネルギー・<br>電気代削減 ご提案</div>
    <div class="sub">{cust}</div>
    <div class="badge">省エネ診断の結果を踏まえた 要点ご提案</div>
    <div class="meta">{m['proposer_company']}　担当 {m['proposer_name']}<br>ご提案日：{m.get('proposal_date','')}</div>
  </div>"""},

        {"bg": "light", "html": f"""
  <div class="inner">
    <div class="eyebrow">THE CHALLENGE</div><h2 class="title">現状の電気代と課題</h2><div class="rule"></div>
    <div class="grid g4">
      <div class="card stat"><div class="n">約{fmt(c['annual_cost_man'])}<span class="u">万円</span></div><div class="lab">年間電気代（現状）</div></div>
      <div class="card stat"><div class="n">約{fmt(kwh_man)}<span class="u">万kWh</span></div><div class="lab">年間使用量</div></div>
      <div class="card stat"><div class="n">約{fmt(c['occupancy_pct'])}<span class="u">%</span></div><div class="lab">入居率（{occ_detail}）</div></div>
      <div class="card stat"><div class="n">{fmt(c.get('winter_peak_kw',0))}<span class="u">kW</span></div><div class="lab">冬の早朝ピーク</div></div>
    </div>
    <div class="callout">{c.get('operation','24時間稼働')}＋冬の暖房ピークが負担に。入居率が<b>満床(100%)に近づくと電気代は約{fmt(c['full_annual_cost_man'])}万円規模</b>へ。だからこそ「減らす×作る×貯める」が効きます。</div>
  </div>"""},

        {"bg": "dark", "html": f"""
  <div class="inner">
    <div class="eyebrow">OUR APPROACH</div><h2 class="title">3段階で電気代を下げる</h2><div class="rule"></div>
    <div class="grid g3" style="margin-top:22px">
      <div class="card"><h3>① 減らす</h3><p>{me['reduce']}</p></div>
      <div class="card"><h3>② 作る</h3><p>{me['generate']}</p></div>
      <div class="card"><h3>③ 貯める・使う</h3><p>{me['store']}</p></div>
    </div>
    <div class="callout">いずれも <b>{diag}</b> の結果を踏まえた組み合わせです。</div>
  </div>"""},

        {"bg": "light", "html": f"""
  <div class="inner">
    <div class="eyebrow">PLAN A / PLAN B</div><h2 class="title">2つのプランをご用意しました</h2><div class="rule"></div>
    <table class="data">
      <thead><tr><th>項目</th><th>Aプラン<br>{plans['A']['name']}</th><th>Bプラン<br>{plans['B']['name']}</th></tr></thead>
      <tbody>
        <tr><td>構成</td><td>{plans['A']['composition']}</td><td>{plans['B']['composition']}</td></tr>
        <tr><td>投資総額（税抜）</td><td>{fmt(A['investment_man'])}万円</td><td>{fmt(B['investment_man'])}万円</td></tr>
        <tr><td>補助金（見込）</td><td class="hi">▲{fmt(A['subsidy_man'])}万円</td><td class="hi">▲{fmt(B['subsidy_man'])}万円</td></tr>
        <tr class="total"><td>自己負担</td><td>{fmt(A['self_pay_man'])}万円</td><td>{fmt(B['self_pay_man'])}万円</td></tr>
        <tr><td>投資回収（現状）</td><td>{A['payback_current_yr']}年</td><td>{B['payback_current_yr']}年</td></tr>
      </tbody>
    </table>
    <div class="callout">どちらを選ばれても正解になるよう設計しています。<span class="note">※消費税は補助対象外。補助金は交付決定により確定します。</span></div>
  </div>"""},

        {"bg": "light", "html": f"""
  <div class="inner">
    <div class="eyebrow">SAVINGS & PAYBACK</div><h2 class="title">電気代はどれだけ下がるか</h2><div class="rule"></div>
    <table class="data">
      <thead><tr><th>項目</th><th>Aプラン</th><th>Bプラン</th></tr></thead>
      <tbody>
        <tr><td>年間削減（現状 {fmt(c['occupancy_pct'])}%）</td><td>{fmt(A['savings_current_man'])}万円</td><td>{fmt(B['savings_current_man'])}万円</td></tr>
        <tr><td>年間削減（満床 100%）</td><td class="hi">{fmt(A['savings_full_man'])}万円</td><td class="hi">{fmt(B['savings_full_man'])}万円</td></tr>
        <tr><td>投資回収（現状 → 満床）</td><td>{A['payback_current_yr']} → {A['payback_full_yr']}年</td><td>{B['payback_current_yr']} → {B['payback_full_yr']}年</td></tr>
      </tbody>
    </table>
    <div class="callout"><b>20年間の累計純効果は最大で約{fmt(dx['_max_cumulative_20yr_man'])}万円。</b>入居率の改善と一緒に進めるほど、効果が高まります。</div>
  </div>"""},

        {"bg": "dark", "html": f"""
  <div class="inner">
    <div class="eyebrow">RESILIENCE / BCP</div><h2 class="title">停電時も、入居者を守る</h2><div class="rule"></div>
    <div class="grid g3">
      <div class="card stat"><div class="n">{fmt(bcp['battery_kwh'])}<span class="u">kWh</span></div><div class="lab">蓄電容量</div></div>
      <div class="card stat"><div class="n">{bcp['backup_hours']}<span class="u">時間</span></div><div class="lab">停電時バックアップ</div></div>
      <div class="card stat"><div class="n">無期限<span class="u">自立</span></div><div class="lab">太陽光連携・晴天時</div></div>
    </div>
    <div class="callout">{bcp.get('value_note','停電対策はご入居者・ご家族の安心に直結します。')}</div>
  </div>"""},

        {"bg": "light", "html": f"""
  <div class="inner">
    <div class="eyebrow">SCHEDULE</div><h2 class="title">進め方と補助金スケジュール</h2><div class="rule"></div>
    <div class="timeline">{tl}</div>
    <div class="callout warn"><b>ご注意：</b>{inp.get('schedule_warning','')}</div>
  </div>"""},

        {"bg": "dark", "html": f"""
  <div class="inner">
    <div class="eyebrow">CONCLUSION & NEXT STEP</div><h2 class="title">ご検討のお願い</h2><div class="rule"></div>
    <div class="grid g3">
      <div class="card"><h3>① 電気代が下がる</h3><p>年間{fmt(A['savings_current_man'])}〜{fmt(B['savings_current_man'])}万円、満床時はさらに拡大。</p></div>
      <div class="card"><h3>② 負担を抑える</h3><p>補助金 約{fmt(A['subsidy_man'])}万円の交付見込み。</p></div>
      <div class="card"><h3>③ 入居者を守る</h3><p>停電時も{bcp['backup_hours']}時間バックアップ。</p></div>
    </div>
    <div class="contact-card">
      <div class="co">まずはお目通しのうえ、ご不明点をお聞かせください</div>
      <div class="row"><span class="k">担当</span><span>{m['proposer_company']}　{m['proposer_name']}</span></div>
      <div class="row"><span class="k">TEL</span><span>{m['tel']}</span></div>
      <div class="row"><span class="k">Mail</span><span>{m['email']}</span></div>
    </div>
  </div>"""},
    ]
    return slides


TITLES = ["表紙", "現状の電気代と課題", "3段階で電気代を下げる", "2つのプラン（A・B）",
          "電気代削減効果と投資回収", "停電時の備え（BCP）", "進め方と補助金スケジュール", "ご検討のお願い"]


def build(inputs_path: str) -> str:
    with open(inputs_path, encoding="utf-8") as f:
        inp = json.load(f)
    dx = diagnose(inp)
    m = inp["meta"]

    narrations = build_narrations(inp, dx)
    slides = build_slides(inp, dx)

    shell = open(SHELL, encoding="utf-8").read()
    welcome_sub = (f"省エネルギー・脱炭素化 ご提案書<br>{m['proposer_company']}の"
                   f"{surname(m['proposer_name'])}より、実データに基づくご提案を差し上げます。")
    repl = {
        "{{TITLE}}": m.get("title", f"{m['customer']}{m.get('customer_honorific','様')} ご提案書"),
        "{{CUSTOMER}}": m["customer"],
        "{{WELCOME_SUB}}": welcome_sub,
        "{{FOOT_LEFT}}": f"{m['proposer_company']}　{m['proposer_name']}",
        "{{FOOT_RIGHT}}": f"{m['customer']}{m.get('customer_honorific','様')} ご提案書",
        "{{NARRATIONS_JSON}}": json.dumps(narrations, ensure_ascii=False, indent=0),
        "{{SLIDES_JSON}}": json.dumps(slides, ensure_ascii=False, indent=0),
        "{{TITLES_JSON}}": json.dumps(TITLES, ensure_ascii=False),
    }
    for k, v in repl.items():
        shell = shell.replace(k, v)

    outdir = os.path.dirname(os.path.abspath(inputs_path))
    out_html = os.path.join(outdir, "index.html")
    open(out_html, "w", encoding="utf-8").write(shell)

    # ナレーション台本も出力（mp3gen.py / 確認用）
    out_txt = os.path.join(outdir, "narration.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        for i, n in enumerate(narrations, 1):
            f.write(f"# スライド{i:02d} {TITLES[i-1]}\n{n}\n\n")

    return out_html


def main(argv):
    if len(argv) < 2:
        print("usage: python engine/build_proposal.py <inputs.json>")
        return 1
    out = build(argv[1])
    print(f"生成しました: {out}")
    print(f"台本: {os.path.join(os.path.dirname(out), 'narration.txt')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
