#!/usr/bin/ruby
# coding: utf-8
require "cgi"
require 'sqlite3'
require_relative "./def.rb"

#main()
db=SQLite3::Database.new("../data/opac.db")
key=CGI.new["NBC"]
key="JP20592050" if key==""
row=field_search_a(key,db)[0]
isbn10=row[1].gsub(/＞/,",")
isbn13=isbnto13(row[1].scan(/[0-9]/).join[0,10])
isbn13="" if isbn10.scan(/[0-9]/).size<10
puts <<-EOS
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
   <head>
      <title>[#{row[2]}]の詳細情報</title>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="description" content="シンプルな詳細書誌情報.">
      <meta name="keywords" content="OPAC,シンプル,使いやすい,簡単,筑波大学">
      <meta name="author" content="春名航亨">
      <meta name="generator" content="atom">
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@egpl0" />
      <meta property="og:url" content="https://cgi.u.tsukuba.ac.jp/~s1811528/opac/cgi/accurate.cgi" />
      <meta property="og:title" content="simple OPAC" />
      <meta property="og:description" content="検索結果." />
      <meta property="og:image" content="./icon.png" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@egpl0" />
      <link rel="shortcut icon" href="../img/icon.png" >
      <link rel="stylesheet" type="text/css" href="../css/accurate.css">
      <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">
   </head>
   <body>
      <a href="../index.html"><img src="../img/logo.png" width="180px"/></a><hr>
      <h1 class="word">
[<span style="color:#ff0000;">#{row[2].gsub(/""/,'"')}<br>\< #{key} \></span>]の詳細表示</h1>
      <div class="center">
         <button type="button" onclick="history.back()" style="font-size:20px;width:242px;height:50px">検索結果一覧へ戻る</button>
         <button type="button" onclick="window.location.href='../index.html'" style="font-size:20px;width:242px;height:50px">検索画面へ戻る</button></div>
<div class="center"><a class="btn-twitter" href="https://twitter.com/share?url=https://cgi.u.tsukuba.ac.jp/~s1811528/opac/cgi/accurate.cgi?NBC=#{key}&text=[#{row[2].gsub(/""/,'"')}]の詳細書誌情報%20%23SimpleOPAC%20(筑波大学内限定アクセス)" rel="nofollow" target="_blank">
<span class="btn-twitter__square"><i class="fab fa-twitter"></i></span>Twitterでシェアする</a>
      </div>

	<table>
         <tbody>
            <tr>
               <th><b>フィールド名</b></th>
               <th><b>内容</b></th>
            </tr>
            <tr>
               <td>書影:<br>[openBD API]<br><br>*書影がない場合404画像.</td>
               <td>#{bibimage(isbn13,row)}</td>
            </tr>
<tr>
	    <td>検索:[Amazon,Rakuten,CiNii Booksなど]</td>
           <td><a href="https://www.amazon.co.jp/s?i=stripbooks&rh=p_66%3A#{isbn13}&rh=p_28%3A#{row[2].gsub(/""/,'"').gsub(/\./," ")}"><img src="../img/amazon.png" width="100px" alt="amazon"/></a>
              <a href="https://books.rakuten.co.jp/search?g=001&isbnJan=#{isbn13}&title=#{row[2].gsub(/""/,'"').gsub(/\./," ")}"><img src="../img/rakuten.png" width="140px" alt="rakuten"/></a>
              <a href="https://ci.nii.ac.jp/books/search?advanced=true&isbn=#{isbn13}&title=#{row[2].gsub(/""/,'"').gsub(/\./," ")}"><img src="../img/cinii.png" width="150px" alt="cinii"/></a>
        <a href="https://iss.ndl.go.jp/books?search_mode=advanced&rft.isbn=#{isbn13}&rft.title=#{row[2].gsub(/""/,'"').gsub(/\./," ")}"><img src="../img/ndl.png" width="150px" alt="ndl"/></a>
              <a href="https://www.tulips.tsukuba.ac.jp/search/?isbn=#{isbn13}&title=#{row[2].gsub(/""/,'"').gsub(/\./," ")}"><img src="../img/tulips.png" width="150px" alt="tulips"/></a>
 <a href="https://www.google.co.jp/search?hl=ja&tbo=p&tbm=bks&q=isbn:#{isbn13}+intitle:#{row[2].gsub(/""/,'"').gsub(/\./," ")}&num=10"><img src="../img/google.png" width="100px" alt="google"/></a>
              <a href="https://www.worldcat.org/search?q=bn%3A#{isbn13}+ti%3A#{row[2].gsub(/""/,'"').gsub(/\./," ")}&num=10"><img src="../img/worldcat.png" width="150px" alt="worldcat"/></a></td>
</tr>
            <tr>
               <td>タイトル:<br>[TITLE]</td>
               <td>#{row[2].gsub(/""/,'"')}</td>
            </tr>
            <tr>
               <td>タイトル標目:<br>[TITLEHEADING]</td>
               <td>#{row[10].gsub(/＞/,",")}</td>
            </tr>
            <tr>
               <td>著者:<br>[AUTH]</td>
               <td>#{row[3].gsub(/""/,'"')}</td>
            </tr>
            <tr>
               <td>著者標目:<br>[AUTHORHEADING]</td>
               <td><a href="search.cgi?authorheading=#{row[11].split("＞")[0]}&ps=&p=0">#{row[11].split("＞")[0]}</a><br>
               <a href="search.cgi?authorheading=#{row[11].split("＞")[1]}&ps=&p=0">#{row[11].split("＞")[1]}</a><br>
	       <a href="search.cgi?authorheading=#{row[11].split("＞")[2]}&ps=&p=0">#{row[11].split("＞")[2]}</a><br></td>
            </tr>
            <tr>
               <td>出版社:[PUB]</td>
               <td><a href="search.cgi?pub=#{row[4]}&ps=&p=0">#{row[4]}</a></td>
            </tr>
            <tr>
               <td>出版年:[PUBDATE]</td>
               <td>#{row[5]}</td>
            </tr>
            <tr>
               <td>版:[ED]</td>
               <td>#{row[6]}</td>
            </tr>
            <tr>
               <td>シリーズ:[SERIES]</td>
               <td><a href="search.cgi?series=#{row[8].gsub(/""/,'"').split(";")[0]}&ps=&p=0">#{row[8].gsub(/""/,'"').split(";")[0]}</a>#{row[8].gsub(/""/,'"').scan(/;[0-9]+/)[0]}</td>
            </tr>
            <tr>
               <td>分類番号:[HOLDINGLOC]</td>
               <td>#{row[14]}</td>
            </tr>
            <tr>
               <td>形態:[PHYS]</td>
               <td>#{row[7]}</td>
            </tr>
            <tr>
               <td>ISBN番号:<br>[ISBN]</td>
               <td>ISBN10:#{row[1].gsub(/＞/,",")}
                  <br>ISBN13:#{isbn13}
               </td>
            </tr>
            <tr>
               <td>全国書誌番号:[NBC]</td>
               <td>#{row[0]}</td>
            </tr>
            <tr>
               <td>個別資料の識別番号:[HOLDINGSRECORD]</td>
               <td>#{row[12]}</td>
            </tr>
            <tr>
               <td>所在棚名:[HOLDINGPHYS]</td>
               <td>#{row[13]}</td>
            </tr>
            <tr>
               <td>注記:[NOTE]</td>
               <td><details><summary>詳細</summary>#{row[9].gsub(/＞/,",")} </details></td>
            </tr>
        </tbody>
      </table>
      　<br>
<div class="center">
         <button type="button" onclick="history.back()" style="font-size:20px;width:242px;height:50px">検索結果一覧へ戻る</button>
         <button type="button" onclick="window.location.href='../index.html'" style="font-size:20px;width:242px;height:50px">検索画面へ戻る</button></div>
<br>
      <hr>
      <br>
      <div class="center">このページは,春AB必修科目「<a href="http://klis.tsukuba.ac.jp/klib/index.php?KIRL-I">知識情報演習I</a>」の演習課題です.(Chrome/Firefox対応.)</div>
      <div class="center">Copyright © 2019 春名航亨(<a href="https://www.u.tsukuba.ac.jp/~s1811528/">201811528</a>) All Rights Reserved.</div>
      <br><br>
   </body>
</html>
EOS
