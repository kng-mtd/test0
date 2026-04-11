# dbt

## setup

```bash
mkdir dbt0
cd dbt0

python -m venv venv0
source venv0/bin/activate

pip install dbt-snowflake   # or dbt-duckdb
```

```bash
mkdir -p ~/.dbt
dbt init pj0
```

### profiles.yml

```yaml
pj0:
  outputs:
    dev:
      type: duckdb # or snowflake
      path: db.duckdb
  target: dev
```

```bash
dbt debug
```

---

### 最小構成（dbt init 直後）

```
pj0/
├── dbt_project.yml
├── models/
│   └── example/
│       └── my_first_dbt_model.sql
├── analyses/
├── seeds/
├── snapshots/
├── tests/
├── macros/
└── target/
```

### 実務でよく使う構成（推奨）

```
pj0/
├── dbt_project.yml
├── profiles.yml        # 通常は ~/.dbt に置く

├── models/
│   ├── sources/        # source定義
│   │   └── src.yml
│   │
│   ├── stage/          # raw整形
│   │   ├── stg_users.sql
│   │   └── schema.yml
│   │
│   ├── fact/           # 中間層
│   │   ├── fact_orders.sql
│   │   └── schema.yml
│   │
│   ├── mart/           # 最終（BI用）
│   │   ├── mart_sales.sql
│   │   └── schema.yml
│   │
│   └── docs.md         # 共通ドキュメント

├── seeds/              # CSV → テーブル
│   └── codes.csv

├── snapshots/          # 履歴管理
│   └── users_snapshot.sql

├── tests/              # singular / generic
│   ├── test_null.sql
│   └── generic/
│       └── custom_test.sql

├── macros/             # Jinja関数
│   └── util.sql

├── analyses/           # ad-hoc SQL
│   └── check.sql

├── target/             # 生成物
└── logs/
```

---

### 各ディレクトリの役割

models/

- `.sql` → テーブル/ビュー生成
- `.yml` → tests / docs

---

seeds/

CSV → テーブル化（dbt seed）

---

snapshots/

履歴管理（SCD Type2）

---

tests/

- singular test（SQL）
- generic test（再利用）

---

macros/

Jinja 関数（再利用ロジック）

---

analyses/

一時的な分析 SQL（DB に保存されない）

---

target/

コンパイル結果・docs（自動生成）

.gitignore 対象

---

### models の中の設計（重要）

```
source
  ↓
stage
  ↓
fact
  ↓
mart
```

| 層    | prefix         |
| ----- | -------------- |
| stage | stg\_          |
| fact  | fct\_          |
| mart  | dim\_ / mart\_ |

---

### schema.yml の配置

```
models/
  stage/
    stg_users.sql
    schema.yml   ← 同じ階層に置く
```

---

## dbt で使う YAML 一覧

- dbt_project.yml ← プロジェクト設定（必須）
- profiles.yml ← DB 接続設定（~/.dbt）
- models/schema.yml ← models の定義（tests / docs）
- models/src.yml ← sources 定義
- seeds/\*.yml ← seeds 設定
- snapshots/\*.yml ← snapshots 設定（任意）

### dbt_project.yml

プロジェクト全体設定

例

```yaml
name: pj0
version: 1.0
config-version: 2

profile: pj0

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
macro-paths: ["macros"]

models:
  pj0:
    stage:
      +schema: stage
    fact:
      +schema: fact
    mart:
      +schema: mart
      +materialized: table

seeds:
  pj0:
    +schema: seed
```

ポイント

- `+` は設定（materialized など）
- ディレクトリ単位で設定できる

### profiles.yml（接続設定）

通常は `~/.dbt/profiles.yml`

例（DuckDB）

```yaml
pj0:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: db.duckdb
```

例（Snowflake）

```yaml
pj0:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xxx
      user: xxx
      password: xxx
      role: xxx
      database: xxx
      warehouse: xxx
      schema: public
```

### schema.yml（models 定義）

models/ 配下に置く

- tests
- description（docs）
- カラム定義

例

```yaml
version: 2

models:
  - name: stage0
    description: "stage table"
    columns:
      - name: id
        description: "primary key"
        tests:
          - not_null
          - unique

  - name: fact0
    columns:
      - name: user_id
        tests:
          - relationships:
              to: { { ref('stage0') } }
              field: id
```

### sources（src.yml）

外部テーブル定義

例

```yaml
version: 2

sources:
  - name: src0
    schema: raw
    tables:
      - name: users
        identifier: user_table
        description: "raw users"
```

使用

```sql
select *
from {{ source('src0', 'users') }}
```

### seeds.yml

seeds/ 配下

例

```yaml
version: 2

seeds:
  - name: ext0
    description: "master data"
    columns:
      - name: code
        tests:
          - unique
```

### snapshots.yml（任意）

snapshot 自体は SQL で書くが、設定も YAML で可能

### よくある構成

```
models/
  stage/
    stg_users.sql
    schema.yml
  fact/
    fact_orders.sql
    schema.yml

models/
  sources/
    src.yml
```

### よくあるミス

- version 忘れ

```yaml
version: 2
```

- ref に {{ }} 付け忘れ

```yaml
to: { { ref('stage0') } }
```

- モデル名にパスを書く

## models

ディレクトリ構成

```
pj0/
  models/
    stage/
      stage0.sql
      stage1.sql
    fact/
      fact0.sql
    mart/
      result0.sql
```

### SQL ルール

stage（raw 整形）

```sql
with src as (
    select * from raw_table
)

select *
from src
```

セミコロン不要

fact（中間）

```sql
select
    a.id,
    b.value
from {{ ref('stage0') }} a
join {{ ref('stage1') }} b
  on a.id = b.id
```

mart（最終）

```sql
{{ config(materialized='table') }}

select *
from {{ ref('fact0') }}
```

### materialization

```sql
{{ config(materialized='view') }}   -- default
{{ config(materialized='table') }}
{{ config(materialized='incremental') }}
```

### dbt_project.yml

```yaml
models:
  pj0:
    stage:
      +schema: stage
    fact:
      +schema: fact
    mart:
      +schema: mart
      +materialized: table
```

ポイント

- `+` を付ける（dbt の設定）
- ディレクトリ名と一致させる
- schema は論理的に分ける

### 実行

```bash
dbt run
```

部分実行

```bash
dbt run --select result0
```

または依存込み

```bash
dbt run --select +result0
```

### ref

```sql
{{ ref('stage0') }}
{{ ref('fact0') }}
```

### stage / fact / mart の役割

| 層    | 役割                         |
| ----- | ---------------------------- |
| stage | 生データ整形（rename, cast） |
| fact  | join・集約                   |
| mart  | BI 用の最終テーブル          |

### source を使う（推奨）

```sql
select *
from {{ source('raw', 'users') }}
```

### incremental

```sql
{{ config(materialized='incremental') }}

select *
from source_table

{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

## seeds

### ディレクトリ

```
pj0/seeds/ext0.csv
```

### 実行

```bash
dbt seed --select ext0
```

**CSV → テーブル作成**

### モデルから参照

```sql
{{ ref('ext0') }}
```

seeds は

- 小さなマスタデータ（コード表など）
- lookup table

### schema 指定

```yaml
seeds:
  pj0:
    +schema: seed
```

## analysis

```
pj0/analysis/test.sql
```

- DB には**保存されない**
- SELECT 結果だけ確認

### 実行

```bash
dbt compile
```

または

```bash
dbt run-operation
```

- 検証用クエリ
- データチェック
- 一時的な分析 SQL

## sources

```yaml
version: 2

sources:
  - name: src0
    tables:
      - name: ref0
        identifier: table0
```

| 項目       | 意味               |
| ---------- | ------------------ |
| name       | dbt 内の名前       |
| identifier | 実 DB のテーブル名 |

```sql
select *
from {{ source('src0', 'ref0') }}
```

これは内部的に以下になる

```sql
select *
from table0
```

schema も指定できる

```yaml
version: 2

sources:
  - name: src0
    schema: raw
    tables:
      - name: ref0
        identifier: table0
```

これは内部的に以下になる

```sql
from raw.table0
```

---

### よくある構成（実務）

```
models/
  sources/
    src.yml
  stage/
    stg_users.sql
```

source → stage

```sql
select *
from {{ source('src0', 'ref0') }}
```

stage → fact

```sql
select *
from {{ ref('stg_users') }}
```

## test

### built-in tests（標準テスト）

| テスト          | 意味      |
| --------------- | --------- |
| unique          | 重複禁止  |
| not_null        | NULL 禁止 |
| accepted_values | 値制限    |
| relationships   | 外部キー  |

### よくある構成（実務）

```bash
models/
  stage/
    stage0.sql
  stage/schema.yml   ← testsここに書く

tests/
  generic/
    not_null_if.sql
```

**models 配下に書くのが主流**

```yaml
version: 2

models:
  - name: stage0
    columns:
      - name: column0
        tests:
          - unique
          - not_null
          - accepted_values:
              values: ["val1", "val2"]
          - relationships:
              to: { { ref('stage1') } }
              field: column00

  - name: fact0
    columns:
      - name: column1
        tests:
          - not_null
```

- `version: 2` 必須
- `ref()` は Jinja なので `{{ }}` が必要

### singular tests

pj0/tests/test0.sql

```sql
select *
from {{ ref('stage0') }}
where column0 is null   -- エラー条件
```

```bash
dbt test --select test0
```

### generic tests（カスタム）

pj0/tests/generic/gentest0.sql

```sql
{% test gentest0(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} is null

{% endtest %}
```

```yaml
version: 2

models:
  - name: stage0
    columns:
      - name: column0
        tests:
          - gentest0
```

## document

```yaml
version: 2

models:
  - name: stage0
    description: "stage table"
    columns:
      - name: column0
        description: "column description"

  - name: fact0
    description: "fact table"
```

```yaml
version: 2

sources:
  - name: src0
    description: "source tables"
    tables:
      - name: ref0
        description: "raw table"
```

### docs ブロック（再利用ドキュメント）

pj0/models/docs.md

```
{% docs doc0 %}
This is shared documentation.
{% enddocs %}
```

doc の適用例

```yaml
version: 2

models:
  - name: stage0
    description: "{{ doc('doc0') }}"
    columns:
      - name: column0
        description: "{{ doc('doc0') }}"
```

### docs 生成

```bash
dbt docs generate
```

出力

```bash
target/catalog.json
target/index.html
```

### docs 表示

```bash
dbt docs serve
```

ブラウザで UI 表示

docs で見えるもの

- モデル構造
- カラム説明
- lineage（依存関係）
- tests 結果

### よくある構成（実務）

```bash
models/
  stage/
    stage0.sql
    schema.yml
  fact/
    fact0.sql
    schema.yml

models/docs.md
```

schema.yml に description を書くのが基本

## jinja

### Jinja の基本構文

```jinja
{% ... %}   # control statement（制御）
{{ ... }}   # expression（出力）
{# ... #}   # comment（コメント）
```

### 制御構文

```jinja
{% if condition %}
  ...
{% elif condition %}
  ...
{% else %}
  ...
{% endif %}
```

```jinja
{% for i in list %}
  ...
{% endfor %}
```

### 出力

```jinja
{{ variable }}
{{ function() }}
```

### dbt での Jinja

- SQL の動的生成
- ref / source
- config
- macro

ref

```sql
select *
from {{ ref('stage0') }}
```

source

```sql
select *
from {{ source('src0', 'users') }}
```

config

```sql
{{ config(materialized='table') }}
```

### 実務でよく使う Jinja パターン

条件分岐（環境差分）

開発環境だけ制限

```jinja
{% if target.name == 'dev' %}
  limit 100
{% endif %}
```

ループ（列展開）

```jinja
{% for col in ['a', 'b', 'c'] %}
  {{ col }}{% if not loop.last %}, {% endif %}
{% endfor %}
```

```sql
a, b, c
```

カラム自動生成

```jinja
{% set cols = ['col1', 'col2', 'col3'] %}

select
{% for c in cols %}
  sum({{ c }}) as {{ c }}{% if not loop.last %}, {% endif %}
{% endfor %}
from table
```

変数

```jinja
{% set threshold = 10 %}

select *
from table
where value > {{ threshold }}
```

## macro

### 定義

```jinja
{% macro add_prefix(col) %}
  prefix_{{ col }}
{% endmacro %}
```

使用

```sql
select {{ add_prefix('id') }}
```

### dbt 特有の変数

target

```jinja
{{ target.name }}
{{ target.schema }}
```

this（現在モデル）

テーブル名になる

```jinja
{{ this }}
```

var

```yaml
vars:
  threshold: 100
```

```sql
where value > {{ var('threshold') }}
```

---

```bash
pj0/macros/macro.sql
```

```jinja
{% macro macro0(arg1, arg2) %}

-- return SQL fragment
{{ arg1 }} + {{ arg2 }}

{% endmacro %}
```

```sql
select
  {{ macro0('col1', 'col2') }} as result
from table
```

展開後

```sql
select
  col1 + col2 as result
from table
```

---

① macro は「文字列を返す」

**SQL を生成するテンプレート**

② 引数はそのまま埋め込まれる

```jinja
{{ macro0('a', 'b') }}
```

`'a'` はそのまま入る

### 実務パターン

共通ロジック

```jinja
{% macro safe_divide(a, b) %}
case when {{ b }} = 0 then null
     else {{ a }} / {{ b }}
end
{% endmacro %}
```

使用

```sql
select {{ safe_divide('sales', 'count') }}
from table
```

カラム変換

```jinja
{% macro prefix(col) %}
prefix_{{ col }}
{% endmacro %}
```

条件付き SQL

```jinja
{% macro filter_recent(column) %}
{{ column }} > current_date - interval '7 days'
{% endmacro %}
```

### return を使うパターン

```jinja
{% macro get_columns() %}
  {% set cols = ['a', 'b', 'c'] %}
  {{ return(cols) }}
{% endmacro %}
```

```jinja
{% for c in get_columns() %}
  {{ c }}
{% endfor %}
```

### adapter 分岐

DB 差分対応

```jinja
{% macro current_timestamp() %}
  {% if target.type == 'snowflake' %}
    current_timestamp()
  {% elif target.type == 'duckdb' %}
    now()
  {% endif %}
{% endmacro %}
```
