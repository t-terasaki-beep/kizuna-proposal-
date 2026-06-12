# .claude — スキル / エージェント一覧

このリポジトリ（kizuna-proposal）の Claude Code 用 設定。
省エネ提案資料を **Notion へアウトプット連携** するための構成。

## スキル (`.claude/skills/`)
| 名前 | 役割 |
|------|------|
| `notion-export` | 提案資料（index.html の8スライド＋mp3gen_kizuna.py のナレーション）を構造化して Notion ページに作成／更新する。Notion MCP の `notion-search` / `notion-fetch` / `notion-create-pages` / `notion-update-page` を利用。 |

## エージェント (`.claude/agents/`)
| 名前 | 役割 |
|------|------|
| `proposal-notion-sync` | 提案データの抽出から Notion 出力までを一貫して担当する専用エージェント。`notion-export` スキルの手順に従って実行する。 |

## Notion 連携が動く条件
1. Notion MCP サーバーが接続済みであること。
2. 出力先（親ページ）への書き込み権限があること。
3. 接続・権限が無い場合は、書き込まず利用者に報告して停止する設計。
