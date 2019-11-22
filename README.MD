# 知識情報演習I レポート課題 201811528 春名航亨(水曜組)
- このリポジトリは…
- 知識情報演習Ⅰの課題「OPACの構築」で作成した課題.
- 授業内で最優秀賞として表彰されました.(2019年度)
     - (リンク)[https://klis.tsukuba.ac.jp/1158.html]
# はじめに

このページは,知識情報・図書館学類春ABモジュール開設「[**知識情報演習Ⅰ**](http://klis.tsukuba.ac.jp/klib/index.php?KIRL-I)」の課題「OPACの構築」についてのレポートです.
# 内容

- [1. 構築したOPACのURL](#1)
- [2. CGIプログラムのソースリストとその説明](#2)
- [3. リレーション(テーブル)の構造とその説明](#3)
- [4. 工夫した点](#4)
- [5. 得られた知見](#5)
# 1. <a name="1">構築したOPACのURL</a>

構築したOPACシステム「**Simple OPAC**」のindexページは,
[**https://cgi.u.tsukuba.ac.jp/~s1811528/opac/index.html**](https://cgi.u.tsukuba.ac.jp/~s1811528/opac/index.html)です.

以下は,**opacディレクトリ以下の階層構造**と,**各ファイルの説明**をまとめた図です.
```cmd

W:\wwws\cgi-bin\opac>tree /F
フォルダー パスの一覧:  ボリューム vol_home01
ボリューム シリアル番号は 000000FB 8082:1532 です
W:.
│  .htaccess...ユーザのサーバ設定ファイル
│  report.html...レポートページ
│  index.html...トップページ
│  sitemap.xml...サイトの構造文書
│  yet_list.html...未実装/実装したい機能のメモ
│
├─.git
│
│（省略）
│
├─data
│      bib_sche.sql...opac.dbスキーマ
│      kakou.rb...jbisc.txtをcsvに成形するプログラム
│      isbn.txt...isbn(10桁)を抽出したもの
│      jbisc.txt...書誌情報の元データ
│      kd.csv...DBにimportできる形式にしたもの
│      opac.db...書誌データベース
│
├─css
│      index.css...index.htmlのCSS
│      search.css...search.cgi
│      accurate.css...accurate.cgi
│      yet_list.css...yet_list.html
│      report.css...report.html
│
├─img
│      icon.png...ページicon
│      notfound.png...書誌画像がnullの時表示される画像
│      requirement.png...要件のスクリーンショット
│
├─cgi
│      accurate.cgi...書誌の詳細表示ページ
│      search.cgi...検索結果一覧ページ
│      def.rb...上記2つのcgi内で用いる関数を集めたもの
│
└─md
        yet_list.md...yet_list.htmlの雛型
        report.md...report.htmlの雛型
```
<div style="text-align:center;">▲図1, OPACシステムの階層構造</div>

# 2. <a name="2">CGIプログラムのソースリストとその説明</a>

## ソースリスト
以下は,作成したcgiプログラムの**ページ**と**ソースコード**のリストです.
- **search.cgi**
  - ページリンク
    - [opac/cgi/search.cgi](https://cgi.u.tsukuba.ac.jp/~s1811528/opac/cgi/search.cgi)
  - ソースコード
    - [github](https://github.com/eggplants/simple_opac/blob/master/cgi/search.cgi)
    
- **accurate.cgi**
    - ページリンク
      - [opac/cgi/accurate.cgi](https://cgi.u.tsukuba.ac.jp/~s1811528/opac/cgi/accurate.cgi)
    - ソースコード
        - [github](https://github.com/eggplants/simple_opac/blob/master/cgi/accurate.cgi)

## 説明

### search.cgi(各関数はdef.rbに記述)
- makeword(cgi)
  - index.htmlからGETしたデータを検索語の分別がしやすいように加工するもの
  - \<field>:\<value>の形
  - gsub(/[\r\n]/,"")で,変数word内の改行を削除している
  - delete_if{|i|...}はAND,andやnullの項目を削除している
  - 返り値は加工した検索文
- makekeys(words)
  - makeword()から受け取った検索文を,SQLクエリに投げるための各キーワードに分割し,配列に挿入する
  - or,ORが来たらそのまま挿入
  - TITLE:<val>やED:<val>が来たら{"TITLE"=>"val"}などのハッシュにして挿入
  - フィールドの指定がないものが来たらそのまま挿入
  - 返り値はハッシュや文字列が格納された配列
- all_any_search(key,db)
  - ANY検索(全てのフィールドから検索)を行い,DBからデータを取得する
  - 返り値はヒットしたデータのNBC(全国書誌番号)が格納された2次元配列[[NBC1],[NBC2],...,[NBCn]]
- field_search_s(key,db)
  - 指定したフィールドの個別検索を行う
  - 返り値はヒットしたデータのNBC(全国書誌番号)が格納された2次元配列
- andor(keys,db)
  - makekeys()から受け取った値をイテレートして,all_any_search(),all_any_search()にそれぞれ適切に渡し検索結果を配列に挿入
  - or,ORが渡されたらそのまま配列に挿入
  - 返り値は返り値はヒットしたデータのNBC(全国書誌番号)が格納された2次元配列
- strinterpret(keys)
  - andor(keys,db)の返り値のORやANDを解釈して最終的な検索結果を作る
  - [DATAn]の次に[DATAn+1]が来たら和集合([DATAn]|[DATAn+1])をとる
  - [DATAn]の次にor,ORが来たらその次の[DATAn+1]と積集合([DATAn]&[DATAn+1])をとる
  - 返り値は一次元配列
- retr_hitdata(hit,db)
  - strinterpret(keys)で作成した,ヒットした書誌データのNBCから完全な書誌フィールドのデータを取得
  - 返り値はヒットした書誌データの全体
- create_paging_link(hits,par)
  - ページネイション機能のためのページリンクの生成
  - indexページやsearch.cgiから受け取ったps(pagesize)の値が空なら20に設定する
  - p(page)は今いるページ数の値
  - hmpに,検索件数とpsを考慮して必要なページ数(=ページリンクの数)を代入
  - p_size=0ならhmp=0
  - pagelinksにページリンクを挿入
  - 返り値はtableにしたページリンクのhtml
- create_table_html(data,par)
  - 検索結果をhtmlのtableに成型
  - accurate.cgiにNBCを送信するために各TITLEにはリンクを付与する
  - pとpsを考慮して必要な文をdata(=retr_hitdata(hit,db))から切り出す
  - 返り値はtableのhtml
- rep_hide(per)
  - GETの値を,psを変更して再読み込みした時のために引継/保存しておく
  - \<input type="hidden">に埋め込んでおく
  - 返り値はps以外のGET値を埋め込んだ\<input type="hidden">のhtml
- main()(#main()とsearch.cgi内に書いている部分)
  - 各関数の実行部分
  - db,cgiでそれぞれSQLiteモジュールのDatabaseオブジェクトとしてopac.dbを指定したものと,CGIオブジェクトを持っておく
  - cgi_valuesにはcgi.instance_variable_get(:@params)で全てのGET値を持っておく
  - begin~rescue~endでは,検索フォームになにも記入されていないときのエラーを回避している
  - hit_numは,ヒット件数を代入
  - search_displayには検索ワードを持っておく
  - hit_numが0の時は,pagenationと結果tableのheading表示をしない
  - title要素と\<h1 />のなかで検索ワードを変えて表示
  - rep_hideを「再読み込みする」をクリックした時(か,psの入力フォームでEnterした時)に送信する
        
### accurate.cgi(各関数はdef.rbに記述)

- isbnto13(isbn10)
  - [openDB](https://openbd.jp/)をたたくためにISBNを10桁から13桁に変換する
  - 返り値はString(13桁の数字)
- field_search_a(key,db)
  - search.cgiからNBCを受け取って書誌データ全体を取得
  - 返り値は1冊の全体の書誌データが入った配列
- bibimage(isbn13,per)
  - 書影画像の取得
  - openDBの[エンドポイント](http://api.openbd.jp/v1/)にアクセスして,書誌データがあるか(=画像があるか)確認
  - JSONがnilならbibhashに404画像表示htmlを渡す
  - JSONがnilでなければbibhashに書影表示htmlを渡す
  - 返り値は\<img ... />のhtml
- main()(#main()とaccurate.cgi内に書いている部分)
  - db,cgiでそれぞれSQLiteモジュールのDatabaseオブジェクトとしてopac.dbを指定したものと,CGIオブジェクトを持っておく
  - rowにfield_search_a(key,db)[0]でsearch.cgiから渡されたGET値(NBC)から取得した全てのフィールドの書誌データ
  - row[1].scan(/[0-9]/).join[0,10]で,ISBNフィールドの数字のみを先頭から10桁とって,rowと一緒にisbnto13に渡しrowと一緒にisbnto13に渡して画像表示htmlを呼んでいる
  - 各項目をtableにして表示している
# 3. <a name="3">リレーション(テーブル)の構造とその説明</a>

## 構造

以下に,opac.dbにテーブルbibdataを作成した際のSQL(data/bib_sche.sql)を示します.
```sql
CREATE TABLE bibdata(
    NBC TEXT primary key,
    ISBN TEXT,
    TITLE TEXT,
    AUTH TEXT,
    PUB TEXT,
    PUBDATE TEXT,
    ED TEXT,
    PHYS TEXT,
    SERIES TEXT,
    NOTE TEXT,
    TITLEHEADING TEXT,
    AUTHORHEADING TEXT,
    HOLDINGSRECORD TEXT,
    HOLDINGPHYS TEXT,
    HOLDINGLOC TEXT);
```
<div style="text-align:center;">▲図2, テーブルbibdataを作成するSQL</div>

## 説明

各値について説明します.
- NBC
  - 全国書誌番号
  - ex)JP20564340
- ISBN
  - ISBN番号(10桁)
  - ex)4-86004-040-6
- TITLE
  - タイトル
  - ex)先生と生徒の交友物語
- AUTH
  - 著者
  - ex)大森正男著
- PUB
  - 出版・頒布
  - ex)土浦筑波書林
- PUBDATE
  - 出版年
  - ex)2004.1
- ED
  - 版
  - ex)第1次改訂
- PHYS
  - 形態
  - ex)248p;19cm
- SERIES
  - シリーズ
  - ex)Kobunshapaperbacks;41
- NOTE
  - 注記
  - ex)奥付のタイトル(誤植)教師と生徒の交友物語
- TITLEHEADING
  - タイトルの読み
  - ex)センセイトセイトノコウユウモノガタリ
- AUTHORHEADING
  - 著者の読み
  - ex)オオモリ,マサオ(大森,正男)
- HOLDINGSRECORD
  - 個別資料の識別番号
  - ex)JP20564340-01
- HOLDINGPHYS
  - 所在棚名
  - ex)21世紀に向うアフリカ連合
- HOLDINGLOC
  - 分類番号
  - ex)F9-128

*複数値を持つ可能性があるフィールドは,挿入する値を結合して挿入しました.*

*正規化も何も行っていないので反省したいです.*

*常に一意な値になるのはNBCのみ(TITLEやHOLDINGLOCは一意でない)なのでprimary keyに指定しました.*
# 4. <a name="4">工夫した点</a>

## AND/OR検索に対応

- AND/OR演算子でAND/OR検索できるようにしました.

## ページングの件数を選択/入力で指定

- \<datalist>を用いてページの表示件数の任意入力/選択を可能にしました.
##検索窓でフィールド指定検索
- フィールドごとに検索できるようにしました.
- 最初はフォームからフィールドごとに検索することを考えていなかったので,「TITLE:筑波」のように特定のフィールドを指す演算子をつけることを考えました.

## デザイン

- 全体的に見やすく,スマホで見ても表示が崩れないようにしました.
- また視覚障害の方でも見やすい配色/サイズにしました.

## サイトの階層構造のサイトマップ作成

-  [sitemap.xml](https://cgi.u.tsukuba.ac.jp/~s1811528/opac/sitemap.xml)を作成しました.
- クローラの本を読んでいて「書くべき」と書いてあったので書きました.

## HTMLとCSSのバリデーション/標準化

- HTML文書は基本エラーが出ないので,形式や継承関係,階層構造に問題がないか,HTMLタグ内にCSSに書くべき内容を含んでいないかを確認するため,W3CのValidator([HTML](http://validator.w3.org/)/[CSS](https://jigsaw.w3.org/css-validator/))を用いて標準化を行いました.

# 5. <a name="5">得られた知見</a>

## サーバーサイドシステムの構築

ㅤ普段,私たちが目にするWebページはフロントエンドであって,HTML/CSS/JSで構成されています.そのサーバーでのプログラムやシステムを見ることはできません.今回の演習で動的なページを作成するにあたって,その内部のプログラムの作成によって,その仕組みをしることができました.また,同時に履修していたPHP＋MySQLの授業での知識もより深めることができました.

## Webページのスタイルシートを用いたデザイン

ㅤこれまで私がWebページを作る,となった時にはMarkDownやBootstrapを用いてあまりCSSを書くことはありませんでした.しかし今回デザインをこだわるにあたってCSSを1から書き起こしました.スタイルシートを用いたWebページデザインの基礎知識を得られたと思います.

## 構造化文書の作成

ㅤHTMLやXMLの構造化文書のマークアップについての知識を得られました.

## SQLiteを用いたDB構築

ㅤこれまでPythonやRubyではMySQLを基本的に用いてきましたが,SQLiteには初めて触りました.記法,組み込み変数,挿入形式の違いを知ることができました.

## Webサイトのgithubでの差分管理

ㅤ(eggplants/opac)[https://github.com/eggplants/opac] として差分管理を行いました.
