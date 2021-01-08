# ReadME


## 목적

이 코드는 오니온 한국 커뮤니티 사이트를 감시하기 위해 만들어 졌다. 

## url list

* http://xdb3grkzc2fpo7ymzvru7v2rdahtcyaocldwr5rp27ag2bsfjo24anad.onion // 남성 가족부
* http://ihwlvcggyxlrgkphbaf44aegwprl6lppxojxfr4rjjfog2ts76apvuqd.onion // 로리웹
* http://55adq4ncecjgxfymv4tdl54g4t2dayqju65wgqpik67suvtiz67kpzad.onion // 코챈
* http://za3tilbgqdbl53g5ihodcllixvzzlsxge63eqe2dm6pntgqjzaedqvid.onion //한국사이트    

## 추출 데이터

* url이 살아있을 경우
```
{
    "onion" : onion url
    "title" : 게시글 타이틀,
    "writer" : 작성자,
    "date"   : 작성일자,
    "contents" : 내용,
    "comment"   : [{
        "writer" : 작성자,
        "date"   : 작성일자,
        "contents" : 내용
    }]        // 댓글
    "checkonoff" : "on"
}
```

* url이 죽었을 경우

```
{
    "onion" : onion url
    "title" : "",
    "writer" : "",
    "date"   : "",
    "contents" : "",
    "comment"   : [{
        "writer" : "",
        "date"   : "",
        "contents" : ""
    }]        // 댓글
    "checkonoff" : "off" 
}
```

## elasticseach mapping 

```
{
    "mappings":{
        "properties":{
            "onion" :{
                "type":"keyword"
            },
            "title" :{
                "type":"keyword"
            },
            "writer" :{
                "type":"keyword"
            },
            "date"  :{
                "type":"date",
                "format" : "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            "contents" :{
                "type":"keyword"
            },
            "comment"   : {
                "properties": {
                    "writer" : {
                        "type":"keyword"
                    },
                    "date"   : {
                        "type": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "contents" : {
                        "type":"keyword"
                    },
                }
            },    
            "checkonoff" :{
                "type":"keyword"
            },
            "hash":{
                "type" : "keyword"
            }
        }
    }
}
```