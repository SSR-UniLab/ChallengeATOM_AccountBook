# ChallengeATOM_AccountBook
This repository is for account book on UniLab challenge for "Challenge ATOM."

## 管理方法

- 帳簿の実データは [ledger/book.csv](ledger/book.csv) で管理します（Excelでも編集可）。
  - 文字化け防止のためCSVはUTF-8(BOM付き)で保存しています。Excelで編集後保存する際は「名前を付けて保存」→ファイルの種類を「CSV UTF-8(コンマ区切り)」にしてください（通常の「CSV(コンマ区切り)」はShift-JISで保存され文字化けします）。
- 領収書などの証拠書類は [evidence/](evidence/) フォルダに、CSVの「証拠書類の番号」に対応するファイル名（例: `001_領収書.pdf`）で格納します。

- CSVを更新したら以下を実行すると、下記「現在の帳簿」の表が自動更新されます。

```sh
python scripts/update_readme.py
```

- リポジトリ初回セットアップ時に以下を1回実行しておくと、`ledger/book.csv` を含むコミット時に自動でREADME.mdが更新されます（pre-commitフック）。

```sh
git config core.hooksPath scripts/hooks
```

### CSVのフォーマット

| 列名 | 内容 |
| --- | --- |
| 日付 | YYYY-MM-DD |
| 費目 | 物品費 / 交通費 / 謝金 / その他 |
| 内容・購入物 | 何を購入・支払したか |
| 用途 | 開発のどこに使ったか |
| 金額(税込) | 数値のみ（カンマなし） |
| 支払先 | 支払先の名称 |
| 証拠書類の番号 | evidence/ 内のファイルに対応する番号 |

## 現在の帳簿

<!-- LEDGER:START -->
| 日付 | 費目 | 内容・購入物 | 用途 | 金額(税込) | 支払先 | 証拠書類の番号 |
| --- | --- | --- | --- | ---: | --- | --- |
| 2026/7/25 | 物品費 | アルミフレーム・キャスタ | ロボットの足回りとして | 7,612円 | misumi | 1 |
|  |  |  | **合計** | **7,612円** |  |  |
<!-- LEDGER:END -->
