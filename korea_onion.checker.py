
import asyncio, aiohttp, logging, json, copy, hashlib
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from bs4 import BeautifulSoup

async def crawling(url:str):
    print(url)
    connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')
    session = aiohttp.ClientSession(connector=connector,  timeout=aiohttp.ClientTimeout(total=30))    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return [await response.read(), url]
                
            else:
                pass
    except Exception as e:
        logging.error(e)
    finally:
        await session.close()

async def data_refine(url:str, raw_html:str):
    result = []
    raw_html_hr_list = raw_html.split('<hr>')
    for data in raw_html_hr_list[1:-1]:
        data_dict = {
                "onion" : url,
                "title" : "",
                "writer" : "",
                "date"   : "",
                "contents" : "",
                "comment"   : [],    
                "checkonoff" : "on",
                "hash" : ""
            }
        data_list = data.split('<table>')
        main_data = data_list[0]
        main_data_bs = BeautifulSoup(main_data, 'lxml')
        
        try: data_dict['title'] = main_data_bs.find("span", class_="filetitle").text
        except: data_dict['title'] = ''
        write_dayAND_name = main_data_bs.find("label").text

        data_dict['writer'] = write_dayAND_name.split(' ')[1].replace('\n', '').strip()
        date_data = write_dayAND_name.split(' ')[-1].replace('\n', '').strip().replace('(', ")").split(')')
        data_dict['date'] = f"20{date_data[0].replace('/', '-')} {date_data[-1]}"

        data_dict['contents'] = main_data_bs.find('div', class_="message").text

        if len(data_list) > 1:
            for comment in data_list[1:]:
                comment_data = {
                    "writer" : "",
                    "date"   : "",
                    "contents" : ""
                }
                
                comment_bs = BeautifulSoup(comment.replace('</table>', ''), 'lxml')
                write_dayAND_name = comment_bs.find("label").text
                comment_data['writer'] = write_dayAND_name.split(' ')[1].replace('\n', '').strip()
                date_data = write_dayAND_name.split(' ')[2].replace('\n', '').strip().replace('(', ")").split(')')
                comment_data['date'] = f"20{date_data[0].replace('/', '-')} {date_data[-1]}"

                comment_data['contents'] = comment_bs.find('div', class_="message").text
                data_dict["comment"].append(comment_data)

        data_dict["hash"] = hashlib.sha256(str(data_dict).encode('utf-8')).hexdigest()
        result.append(data_dict)
    
    file_name = url.split('.')[0].replace('http://', '')
    if '/' in file_name: file_name = file_name.split('/')[0].replace('.onion', '')

    with open(f'{file_name}.json', 'a') as f:
        for data in result:
            f.write(str({"index" : "korea_onion_checker"}))
            f.write('\n')
            f.write(str(data))
            f.write('\n')

    temp_bs = BeautifulSoup(raw_html_hr_list[-1], 'lxml')
    page_str = temp_bs.findAll('td')[2].text
    last_page = int(page_str.replace('[', '').replace(']', '').strip().split(' ')[-1])
    
    plus_url = []
    if last_page == 0: pass
    elif last_page == 1: plus_url.append(f'{url}{last_page}.html') 
    else : 
        for i in range(1, last_page+1): plus_url.append(f'{url}{i}.html') 
    
    return plus_url

async def main():
    task = []
    url_list2 = copy.deepcopy(url_list)
    flag = True
    while True:
        loop = asyncio.get_event_loop()
        for url in url_list2: task.append(loop.create_task(crawling(url=url)))
        
        url_list2 = []
        result_crawling = await asyncio.gather(*task)
        # print(result_crawling)
        for result in result_crawling:
            try:
                try: url_list2.extend(await data_refine(url = result[1],raw_html=result[0].decode('utf-8')))
                except UnicodeDecodeError: url_list2.extend(await data_refine(url = result[1],raw_html=result[0].decode('ISO-8859-1')))
                except Exception as e: print(e)
            except Exception as e: pass
        if not flag : break
        else: flag = False
    # print(result)

if __name__ == "__main__":

    url_list = [
        # "http://ok3dw7mbxkobxsyo4fjjzmn4p5spd23om3mlfw3gpgxmowfyhxhavead.onion/",       # test용...
        "http://xdb3grkzc2fpo7ymzvru7v2rdahtcyaocldwr5rp27ag2bsfjo24anad.onion/",  # 남성 가족부
        # "http://ihwlvcggyxlrgkphbaf44aegwprl6lppxojxfr4rjjfog2ts76apvuqd.onion/", # 로리웹
        # "http://55adq4ncecjgxfymv4tdl54g4t2dayqju65wgqpik67suvtiz67kpzad.onion/", # 코챈
        # "http://2mu7qwudmq6he6mkvwysqwqkw5zhwecfayosftcauodzpfpkpb7rf5yd.onion/", # 다크 메갈리아
        # "http://za3tilbgqdbl53g5ihodcllixvzzlsxge63eqe2dm6pntgqjzaedqvid.onion" # 한국사이트
    ]
    asyncio.run(main())    