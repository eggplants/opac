require 'cgi'
require 'sqlite3'
require 'open-uri'
require 'json'

#検索語の受け取り整形
def makewords(cgi)
  word="NBC:#{cgi["nbc"]} TITLE:#{cgi["title"]} AUTH:#{cgi["auth"]}\s
ED:#{cgi["ed"]} PUB:#{cgi["pub"]} PUBDATE:#{cgi["pubdate"]}\s
PHYS:#{cgi["phys"]} NOTE:#{cgi["note"]} SERIES:#{cgi["series"]}\s
ISBN:#{cgi["isbn"]} TITLEHEADING:#{cgi["titleheading"]}\s
AUTHORHEADING:#{cgi["authorheading"]}\s
HOLDINGSRECORD:#{cgi["holdingsrecord"]} HOLDINGPHYS:#{cgi["holdingphys"]}\s
HOLDINGLOC:#{cgi["holdingloc"]} #{cgi["search"]}"
  words=word.gsub(/[\r\n]/,"").gsub(/<[a-zA-Z]+>|\"|\'/,"").split(/[\+\s 　]+/).
         delete_if{|i|i=~/[aA][nN][dD]/||i=~/^[A-Z]+:$/||i==""}
  if cgi["andor"]=="or"
    (words.size-1).times{|i|words.insert(i*2+1, "OR")}
  end
  return words
end
#検索語の分別
def makekeys(words)
  keys=[]
  words.each{|i|
    if i=="OR"||i=="or"
      keys.push("OR")
    elsif i=~/([A-Z]+?):/
      keys.push(Hash[*i.split(":")])
    else
      keys.push(i)
    end
  }
  return keys
end
#全てのフィールドから探す奴の文生成する関数:返り値は
def all_any_search(key,db)
  sql= <<SQL
  select NBC
  from bibdata
  where NBC like '%#{key}%'
  or TITLE like '%#{key}%'
  or AUTH like '%#{key}%'
  or ED like '%#{key}%'
  or PUB like '%#{key}%'
  or PUBDATE like '%#{key}%'
  or PHYS like '%#{key}%'
  or NOTE like '%#{key}%'
  or SERIES like '%#{key}%'
  or ISBN like '%#{key}%'
  or TITLEHEADING like '%#{key}%'
  or AUTHORHEADING like '%#{key}%'
  or HOLDINGSRECORD like '%#{key}%'
  or HOLDINGLOC like '%#{key}%'
SQL
  data=[]
  db.execute(sql).each{|row|
    data<<row[0]
  }
  return data
end
#指定したフィールドから個別検索
def field_search_s(key,db)
  sql = <<SQL
  select NBC
  from bibdata
  where #{key.keys[0]} like '%#{key.values[0]}%';
SQL
  data=[]
  begin
  db.execute(sql).each{|row|
    data<<row[0]
  }
  rescue
    data<<[]
  end
  return data
end
#検索実行
def andor(keys,db)
  result_each=[]
  keys.each{|i|
    result_each<<
    if i=="OR"
      i
    elsif i.kind_of?(Hash)
      field_search_s(i,db)
    else
      all_any_search(i,db)
    end
  }
  return result_each
end
#検索式解釈
def strinterpret(keys)
  hit,f="",0
  keys.each{|i|
    if hit.empty? && i!="OR"
      hit=i
    elsif i=="OR"
      f=1
    elsif f==1
      hit=i|hit
      f=0
    else
      hit=i&hit
    end
  }
  return hit
end
#ヒットしたデータ(NBCのみ)を元に問い合わせ
def retr_hitdata(hit,db)
  data=[]
  hit.each{|a|
    sql= <<SQL
    select *
    from bibdata
    where NBC = '#{a}'
    order by TITLE
SQL
    db.execute(sql).each{|row|
      data<<row.each{|i|}
    }
  }
  return data
end
#ページリンクの生成
def create_paging_link(hits,par)
  par["ps"]=["20"] if par["ps"]==[""]
  par["ps"]=["20"] if par["ps"][0]=~/[^0-9]/
  # par["ps"]||=["20"]
  # par["ps"]=["20"] if par["ps"][0].to_i<0
  p_now,p_size,hits=par["p"][0].to_i,par["ps"][0].to_i,hits.to_i
  begin
  hmp=hits%p_size!=0&&hits!=0? (hits/p_size)+1 : hits/p_size
  rescue ZeroDivisionError
    hmp=0
  end
  pagelinks="<table><tr>\n"
  hmp.times{|i|
      link="https://cgi.u.tsukuba.ac.jp/~s1811528/opac/cgi/search.cgi?"
      par["p"]=[i]
      par.each{|k,v|link+="#{k}=#{v[0]}&"}
      pagelinks+="<td><a href=\"#{link.chop}\"><b>#{i+1}</b></a></td>\n"
      pagelinks+="</tr>\n<tr>" if i%30==0&&i!=0
  }
  par["p"]=[p_now.to_s]
  pagelinks+="</tr></table>\n"
  return pagelinks
end
#表作る
def create_table_html(data,par)
  tab=""
  data[par["p"][0].to_i*par["ps"][0].to_i,par["ps"][0].to_i].each{|row|
    d=row[4].size>10?"...":""
    tab+= <<-EOS
    <tr>
    <td class="result"><a href="accurate.cgi?NBC=#{row[0]}">#{row[2].gsub(/""/,'"')}</a></td>
    <td class="result"><a href="search.cgi?authorheading=#{row[11].split("＞")[0]}&ps=&p=0">#{row[11].split("＞")[0]}</a></td>
    <td class="result"><a href="search.cgi?authorheading=#{row[11].split("＞")[1]}&ps=&p=0">#{row[11].split("＞")[1]}</a></td>
    <td class="result"><a href="search.cgi?pub=#{row[4]}&ps=&p=0">#{row[4][0,10].gsub(/""/,'"')}#{d}</a></td>
    <td class="result">#{row[5]}</td>
    </tr>
EOS
  }
  return tab
end
#GET値を引継/保存しておく
def rep_hide(per)
  h=""
  v=per.delete("ps")
  per.each{|k,v|
    h+="<input type=\"hidden\" name=\"#{k}\" value=\"#{v[0]}\">\n"
  }
  per.merge!({"ps"=>v})
return h
end
#ISBN変換
def isbnto13(isbn10)
  isbn = "978"+isbn10.gsub(/[^\d]/,'').gsub(/\d$/,'')
  r = isbn.split(//).map(&:to_i).zip([1,3].cycle).map{|e|e[0]*e[1]
  }.reduce(:+)%10
  isbn+=((10-r)%10).to_s
  return isbn
end
#指定したフィールドから個別検索
def field_search_a(key,db)
  sql = <<SQL
  select *
  from bibdata
  where NBC = "#{key}";
SQL
  data=[]
  db.execute(sql).each{|row|
    data<<row
  }
  return data
end
#書影取得
def bibimage(isbn13,per)
  img=""
  bibhash=JSON.load(open("https://api.openbd.jp/v1/get?isbn=#{isbn13}"))
  if per[1]!=""&&bibhash!=[nil]
    begin
      img='<img src="'+
      bibhash[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink']+
      '" width="200" height="287" alt="OpenDB API"/>'
    rescue NoMethodError#書誌データがあるが書影がないとき
      img='<img src="https://1.bp.blogspot.com/-d3vDLBoPktU/WvQHWMBRhII/AAAAAAABL6E/Grg-XGzr9jEODAxkRcbqIXu-mFA9gTp3wCLcBGAs/s800/internet_404_page_not_found.png" width="500" height="287" alt="404"/>'
    end
  else
    img='<img src="https://1.bp.blogspot.com/-d3vDLBoPktU/WvQHWMBRhII/AAAAAAABL6E/Grg-XGzr9jEODAxkRcbqIXu-mFA9gTp3wCLcBGAs/s800/internet_404_page_not_found.png" width="200" height="287" alt="404"/>'
  end
end
