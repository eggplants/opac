#!/usr/bin/ruby
# coding: utf-8
require 'cgi'
require 'sqlite3'
require_relative "./def.rb"

#main()
db=SQLite3::Database.new("../data/opac.db")
cgi=CGI.new
cgi_values=cgi.instance_variable_get(:@params)
keys=makekeys(makewords(cgi))
result_each=andor(keys,db)
begin
hit=strinterpret(result_each).flatten
rescue
  hit=[]
end
data=retr_hitdata(hit,db)
hit_num=data.size
search_display=makewords(cgi).join(" ").gsub(/[A-Z]+:[A-Z]+:/,"").sub(/^[ ]+/,"")
puts <<-EOS
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
<head>
   <title>[#{search_display}]の検索結果</title>
   <meta charset="utf-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="description" content="シンプルなOPAC検索結果.">
   <meta name="keywords" content="OPAC,シンプル,使いやすい,簡単,筑波大学">
   <meta name="author" content="春名航亨">
   <meta name="generator" content="atom">
   <meta name="twitter:card" content="summary_large_image" />
   <meta name="twitter:site" content="@egpl0" />
   <meta property="og:url" content="https://cgi.u.tsukuba.ac.jp/~s1811528/opac/search.cgi" />
   <meta property="og:title" content="simple OPAC" />
   <meta property="og:description" content="シンプルなOPAC検索システム." />
   <meta property="og:image" content="./icon.png" />
   <meta name="twitter:card" content="summary_large_image" />
   <meta name="twitter:site" content="@egpl0" />
   <link rel="shortcut icon" href="../img/icon.png" >
   <link rel="stylesheet" type="text/css" href="../css/search.css">
</head>
<body>
<div class="center"><button type="button" onclick="location.href='../index.html'" style="font-size:20px;width:200px;height:50px">検索結果一覧へ戻る</button></div>
EOS
puts "<h1>[<span style='color:#ff0000;'>#{search_display}</span>]の検索結果:<span style='color:#ff0000;'>#{hit_num}</span>件</h1>" if hit_num==0
head=<<EOS
<h1>[<span style="color:#ff0000;">#{search_display}</span>]の検索結果:<span style="color:#ff0000;">#{hit_num}</span>件</h1>
<form action="#" method="GET">
           <input type="text" name="ps" list="case-numbers1" placeholder="1ページの表示件数:入力/選択" style="font-size:20px;">
         <datalist id="case-numbers1">
            <option value="20">けっこう少ない</option>
            <option value="50">少ない</option>
            <option value="100">ちょっと少ない</option>
            <option value="200">ちょうどいい</option>
            <option value="500">ちょっと多い</option>
            <option value="1000">多い</option>
            <option value="5000">多い</option>
         </datalist>
#{rep_hide(cgi_values)}
<input type="submit" value="再読込する" style="font-size:20px;">
</form>
#{create_paging_link(hit_num,cgi_values)}
<table class="result">
<tr>
    <td class="result">TITLE</td>
    <td class="result">AUTH</td>
    <td class="result">PUB</td>
    <td class="result">PUBDATE</td>
</tr>
EOS
puts head if hit_num!=0
puts create_table_html(data,cgi_values)
puts "</table>" if hit_num!=0
puts "</body></html>"
