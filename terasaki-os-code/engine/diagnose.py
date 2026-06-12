# -*- coding: utf-8 -*-
"""
diagnose.py — 寺嵜流 提案の数値診断エンジン

入力(inputs.json)の plans.A / plans.B から、
  ・自己負担   = 投資総額 − 補助金
  ・回収(現状) = 自己負担 ÷ 年間削減額(現状入居率)
  ・回収(満床) = 自己負担 ÷ 年間削減額(満床/フル稼働)
  ・20年累計   = 年間削減額(満床) × 20 − 自己負担
を算出する。すべて「万円」「年」。係数は明示・再現可能（盛らない）。

KIZUNA実績との答え合わせ:
  A: 自己負担1671 / 回収6.0 / 4.1 / 20年6489
  B: 自己負担2448 / 回収7.6 / 4.4 / 20年8712  ← 提案書の「約8,712万円」と一致

使い方:
  python engine/diagnose.py customers/kizuna-home/inputs.json
"""
import json
import sys

YEARS = 20  # 効果累計の評価年数（寺嵜流の標準）


def diagnose_plan(plan: dict) -> dict:
    """1プランぶんの派生指標を計算して返す。"""
    inv = plan["investment_man"]
    sub = plan["subsidy_man"]
    sc = plan["savings_current_man"]
    sf = plan["savings_full_man"]

    self_pay = inv - sub
    payback_current = self_pay / sc if sc else None
    payback_full = self_pay / sf if sf else None
    cumulative_20yr = sf * YEARS - self_pay

    return {
        "name": plan.get("name", ""),
        "composition": plan.get("composition", ""),
        "investment_man": inv,
        "subsidy_man": sub,
        "self_pay_man": self_pay,
        "savings_current_man": sc,
        "savings_full_man": sf,
        "payback_current_yr": round(payback_current, 1) if payback_current else None,
        "payback_full_yr": round(payback_full, 1) if payback_full else None,
        "cumulative_20yr_man": cumulative_20yr,
    }


def diagnose(inputs: dict) -> dict:
    """inputs全体を受け取り、A/Bの診断結果を返す。"""
    plans = inputs["plans"]
    result = {key: diagnose_plan(plans[key]) for key in plans}
    # 提案全体で最大の20年累計（まとめスライドの「最大で約◯◯万円」に使う）
    result["_max_cumulative_20yr_man"] = max(
        p["cumulative_20yr_man"] for p in result.values() if isinstance(p, dict)
    )
    return result


def _fmt(n) -> str:
    """万円を 1,671 のようにカンマ区切りで。"""
    return f"{int(round(n)):,}" if n == int(n) else f"{n:,}"


def main(argv):
    if len(argv) < 2:
        print("usage: python engine/diagnose.py <inputs.json>")
        return 1
    with open(argv[1], encoding="utf-8") as f:
        inputs = json.load(f)
    res = diagnose(inputs)
    print(f"=== {inputs['meta'].get('customer','')} 診断結果 ===")
    for key in ("A", "B"):
        if key not in res:
            continue
        p = res[key]
        print(
            f"[{key}プラン/{p['name']}] 投資{_fmt(p['investment_man'])}万 "
            f"補助{_fmt(p['subsidy_man'])}万 自己負担{_fmt(p['self_pay_man'])}万 "
            f"回収(現状){p['payback_current_yr']}年→(満床){p['payback_full_yr']}年 "
            f"20年累計{_fmt(p['cumulative_20yr_man'])}万"
        )
    print(f"20年累計の最大: 約{_fmt(res['_max_cumulative_20yr_man'])}万円")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
