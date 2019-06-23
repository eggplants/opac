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
puts <<-EOS
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
   <head>
      <title>[#{row[2]}]の詳細表示</title>
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
   </head>
   <body>
      #{bibimage(isbnto13(row[1].scan(/[0-9]/).join[0,13]),row)}<br>
      <table>
         <tbody>
         <tr>
         <th>フィールド名</th>
         <th>内容</th>
         </tr>
            <tr>
               <td>NBC:</td>
               <td>#{row[0]}</td>
            </tr>
            <tr>
               <td>ISBN:</td>
               <td>#{row[1].gsub(/＞/,",")}</td>
            </tr>
            <tr>
               <td>TITLE:</td>
               <td>#{row[2]}</td>
            </tr>
            <tr>
               <td>AUTH:</td>
               <td>#{row[3]}</td>
            </tr>
            <tr>
               <td>PUB:</td>
               <td>#{row[4]}</td>
            </tr>
            <tr>
               <td>PUBDATE:</td>
               <td>#{row[5]}</td>
            </tr>
            <tr>
               <td>ED:</td>
               <td>#{row[6]}</td>
            </tr>
            <tr>
               <td>PHYS:</td>
               <td>#{row[7]}</td>
            </tr>
            <tr>
               <td>SERIES:</td>
               <td>#{row[8]}</td>
            </tr>
            <tr>
               <td>NOTE:</td>
               <td>#{row[9].gsub(/＞/,",")}</td>
            </tr>
            <tr>
               <td>TITLEHEADING:</td>
               <td>#{row[10].gsub(/＞/,",")}</td>
            </tr>
            <tr>
               <td>AUTHORHEADING:</td>
               <td>#{row[11].gsub(/＞/,",")}</td>
            </tr>
            <tr>
               <td>HOLDINGSRECORD:</td>
               <td>#{row[12]}</td>
            </tr>
            <tr>
               <td>HOLDINGPHYS:</td>
               <td>#{row[13]}</td>
            </tr>
            <tr>
               <td>HOLDINGLOC:</td>
               <td>#{row[14]}</td>
            </tr>
            <tr>
            <td><button type="button" onclick="history.back()" style="font-size:20px;width:242px;height:50px">検索結果一覧へ戻る</button></td>
            <td></td>
            </tr>
         </tbody>
      </table>
   </body>
</html>
EOS
