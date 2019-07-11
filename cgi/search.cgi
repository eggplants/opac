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
      <a href="../index.html"><img src="../img/logo.png" alt="logo"/></a><hr>
      EOS
      puts "<br><h1 class='word'>[<span style=' ;color:#ff0000;'> #{search_display}</span>]の検索結果:<span style='color:#ff0000;'>#{hit_num}</span>件</h1>" if hit_num==0
      head=<<EOS
      <h1 class="word">[<span style="color:#ff0000;">#{search_display}</span>]の検索結果:<span style="color:#ff0000;">#{hit_num}</span>件</h1>
      <form action="#" method="GET">
         <div class="center"><input type="text" name="ps" list="case-numbers1" placeholder="1ページの表示件数:" style="font-size:23px;">
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
         <input type="submit" value="再読込する" style="font-size:20px;"></div>
      </form>
      <div class="center">#{create_paging_link(hit_num,cgi_values)}</div>
      <div class="center"><table class="result" frame="border">
        <tr>
            <th class="result">タイトル:[TITLE]</th>
            <th class="result">著者標目1:[AUTHHEAD1]</th>
            <th class="result">著者標目2:[AUTHHEAD2]</th>
            <th class="result">出版社:[PUB]</th>
            <th class="result">出版年:[PUBDATE]</th>
        </tr>
EOS
puts head if hit_num!=0
puts create_table_html(data,cgi_values)
puts "</table></div>" if hit_num!=0
puts '<br><div class="center"><button type="button" onclick="location.href=\'../index.html\'" style="font-size:20px;width:200px;height:50px">検索画面へ戻る</button></div>'
puts <<-EOS
	<br><hr>
      <br>
      <div class="center">このページは,春AB必修科目「<a href="http://klis.tsukuba.ac.jp/klib/index.php?KIRL-I">知識情報演習I</a>」の演習課題です.(Chrome/Firefox対応.)</div>
      <div class="center">Copyright © 2019 春名航亨(<a href="https://www.u.tsukuba.ac.jp/~s1811528/">201811528</a>) All Rights Reserved.</div>
      <br><br></body></html>
EOS
