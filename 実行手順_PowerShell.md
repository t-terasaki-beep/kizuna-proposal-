# ナレーションMP3 生成 ─ 実行手順（PowerShell）

KIZUNA HOME様 ご提案書のナレーション音声（MP3）を、寺嵜さんのPC側で生成する手順です。
**HTML本体（index.html）はブラウザ内蔵音声だけでも再生できます。MP3はオフライン用の予備です。**

---

## 0. 前提：ffmpeg が動くこと

PowerShell で以下を実行し、バージョンが表示されればOKです。

```powershell
ffmpeg -version
```

> 「用語 'ffmpeg' は認識されません」と出る場合は、**PATHが反映されていないだけ**です。
> PowerShellウィンドウを一度すべて閉じて開き直すか、下記1行を実行してから再確認してください。
>
> ```powershell
> $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
> ```

---

## 1. このフォルダへ移動

`index.html` と `ナレーションMP3生成.ps1` が入っているフォルダへ移動します。

```powershell
cd "C:\Users\terasaki\（解凍したフォルダのパス）"
```

> エクスプローラーでフォルダを開き、アドレスバーに `powershell` と打ってEnterすると、そのフォルダでPowerShellが開きます（移動の手間が省けます）。

---

## 2. 実行許可を出す（このウィンドウだけ・一時的）

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## 3. スクリプトを実行

```powershell
.\ナレーションMP3生成.ps1
```

- `audio` フォルダが自動で作られ、`01.mp3` 〜 `25.mp3` が順番に生成されます。
- 「Haruka が見つかりません」と出た場合は、自動で標準の日本語ボイスに切り替えて続行します（そのまま完走でOK）。
- 全25個できたら `===== 完了しました =====` と表示されます。

---

## 4. できあがったら

`audio` フォルダ（MP3 25個）を**フォルダごとZIPにして、Claudeに送ってください。**
HTML本体・MP3・READMEをまとめ、GitHub Pagesにそのまま上げられる一式にして組み直してお返しします。

> もちろん、`audio` フォルダを `index.html` と同じ階層に置いていただければ、そのままGitHubに上げても動作します（送っていただかなくても完結します）。

---

## 補足：音声品質について

Windows標準のSAPI音声（Haruka/Ayumi）は、ブラウザ内蔵のニューラル音声に比べるとやや機械的です。
皆川様にお出しする際は、HTMLの **「ブラウザ音声」モード（既定・推奨）** が最も自然に聞こえます。
MP3はあくまで「ネット接続が無い環境用の予備」とお考えください。

より高品質なMP3が必要な場合は、無料の **VOICEVOX**（ローカル生成）でナレーション原稿（README記載）を読み上げ、
`audio` フォルダに `01.mp3`〜`25.mp3` の名前で置き換える方法もあります。
