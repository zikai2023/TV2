import time
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re

# url = 'https://taoiptv.com/source/iptv.txt?token=8zlxhttq9h01ahww'
# r = requests.get(url)
# with open("iptv1.txt", "wb") as code:
#     code.write(r.content)

# url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/Meroser/IPTV/main/IPTV-tvbox.txt'
# r = requests.get(url)
# with open("ipv6.txt", "wb") as code:
#     code.write(r.content)

urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki",                # 河 北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iYmVpamluZyI%3D",          # 北 京
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iZ3Vhbmdkb25nIg%3D%3D",    # 广 东
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbmdoYWki",            # 上 海
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0idGlhbmppbiI%3D",          # 天 津
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iY2hvbmdxaW5nIg%3D%3D",    # 重 庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbnhpIg%3D%3D",        # 山 西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D",          # 陕 西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iamlhbmdzdSI%3D",          # 江 苏
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iemhlamlhbmci",            # 浙 江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D",        # 福 建
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rGf6KW%2FIg%3D%3D",      # 江 西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bGx5LicIg%3D%3D",        # 山 东
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D",        # 河 南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5YyXIg%3D%3D",        # 湖 北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5Y2XIg%3D%3D",        # 湖 南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9ImNoYW5nc2hhIg%3D%3D",        # 长 沙
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22hebei%22",         # 河 北
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22beijing%22",       # 北 京
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22guangdong%22",     # 广 东
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shanghai%22",      # 上 海
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22tianjin%22",       # 天 津
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22chongqing%22",     # 重 庆
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shanxi%22",        # 山 西
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shaanxi%22",       # 陕 西
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22liaoning%22",      # 辽 宁
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22jiangsu%22",       # 江 苏
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22zhejiang%22",      # 浙 江
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22anhui%22",         # 安 徽
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22fujian%22",        # 福 建
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22jiangxi%22",       # 江 西
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shandong%22",      # 山 东
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22henan%22",         # 河 南
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22hubei%22",         # 湖 北
    # "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22hunan%22",         # 湖 南
]


def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls


def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    urls = set(x_urls)  # 去重得到唯一的URL列表

    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)

    for url in valid_urls:
        print(url)
    # 遍历网址列表，获取JSON文件并解析
    for url in valid_urls:
        try:
            # 发送GET请求获取JSON文件，设置超时时间为0.5秒
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]  # http:// or https://
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"

            json_url = f"{url}"
            response = requests.get(json_url, timeout=0.5)
            json_data = response.json()

            try:
                # 解析JSON文件，获取name和url字段
                for item in json_data['data']:
                    if isinstance(item, dict):
                        name = item.get('name')
                        urlx = item.get('url')
                        if ',' in urlx:
                            urlx = f"aaaaaaaa"

                        # if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                        if 'http' in urlx:
                            urld = f"{urlx}"
                        else:
                            urld = f"{url_x}{urlx}"

                        if name and urld:
                            # 删除特定文字
                            name = name.replace("中央", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("超高", "")
                            name = name.replace("频道", "")
                            name = name.replace("-", "")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace(")", "")
                            name = name.replace("L", "")
                            name = name.replace("CMIPTV", "")
                            name = name.replace("cctv", "CCTV")
                            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV4欧洲", "CCTV4")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7农业", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV8纪录", "CCTV9")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("央视14少儿", "CCTV14")
                            name = name.replace("CCTV少儿超", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV17军农", "CCTV17")
                            name = name.replace("CCTV17农业", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            name = name.replace("CCTV5+赛事", "CCTV5+")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV5赛事", "CCTV5+")
                            name = name.replace("凤凰中文台", "凤凰中文")
                            name = name.replace("凤凰资讯台", "凤凰资讯")
                            name = name.replace("CCTV4K测试）", "CCTV4")
                            name = name.replace("CCTV164K", "CCTV16")
                            name = name.replace("上海东方卫视", "上海卫视")
                            name = name.replace("东方卫视", "上海卫视")
                            name = name.replace("内蒙卫视", "内蒙古卫视")
                            name = name.replace("福建东南卫视", "东南卫视")
                            name = name.replace("广东南方卫视", "南方卫视")
                            name = name.replace("金鹰卡通卫视", "金鹰卡通")
                            name = name.replace("湖南金鹰卡通", "金鹰卡通")
                            name = name.replace("炫动卡通", "哈哈炫动")
                            name = name.replace("卡酷卡通", "卡酷少儿")
                            name = name.replace("卡酷动画", "卡酷少儿")
                            name = name.replace("BRTVKAKU少儿", "卡酷少儿")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("嘉佳卡通", "佳嘉卡通")
                            name = name.replace("世界地理", "地理世界")
                            name = name.replace("CCTV世界地理", "地理世界")
                            name = name.replace("BTV北京卫视", "北京卫视")
                            name = name.replace("BTV冬奥纪实", "冬奥纪实")
                            name = name.replace("东奥纪实", "冬奥纪实")
                            name = name.replace("卫视台", "卫视")
                            name = name.replace("湖南电视台", "湖南卫视")
                            name = name.replace("少儿科教", "少儿")
                            name = name.replace("影视剧", "影视")
                            results.append(f"{name},{urld}")
            except:
                continue
        except:
            continue

results = set(results)  # 去重得到唯一的URL列表
results = sorted(results)
with open("iptv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        print(result)


print("频道列表文件iptv.txt获取完成！")

import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

# 读取IPTV1.txt文件
results = []
result_counter = 15  # 每个频道需要的个数
with open("iptv1.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            channel_name, channel_url = line.split(',')
            if 'genre' not in channel_url:
                results.append((channel_name, channel_url))


# 将IPTV1文件内容写入到ipv4.txt
channel_counters = {}
with open("ipv4_list.txt", 'w', encoding='utf-8') as file:
    file.write('IPV4频道,#genre#\n')
    for result in results:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or '卫视' in channel_name or '凤凰' in channel_name or '翡翠' in channel_name or 'TVB' in channel_name or 'CHC' in channel_name or '影视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 将IPTV1文件内容写入到cctv.m3u
with open("ipv4_list.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    for result in results:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or '卫视' in channel_name or '凤凰' in channel_name or '翡翠' in channel_name or 'TVB' in channel_name or 'CHC' in channel_name or '影视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"IPV4频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"IPV4频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1


# # 将IPTV1文件内容写入到cctv.txt
# channel_counters = {}
# with open("cctv.txt", 'w', encoding='utf-8') as file:
#     file.write('央视频道,#genre#\n')
#     for result in results:
#         channel_name, channel_url = result
#         if 'CCTV' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"{channel_name},{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"{channel_name},{channel_url}\n")
#                 channel_counters[channel_name] = 1
#
# # 将IPTV1文件内容写入到cctv.m3u
# with open("cctv.m3u", 'w', encoding='utf-8') as file:
#     channel_counters = {}
#     for result in results:
#         channel_name, channel_url = result
#         if 'CCTV' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
#                     file.write(f"{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
#                 file.write(f"{channel_url}\n")
#                 channel_counters[channel_name] = 1
#
# # 将IPTV1文件内容写入到weishi.txt
# channel_counters = {}
# with open("weishi.txt", 'w', encoding='utf-8') as file:
#     file.write('卫视频道,#genre#\n')
#     for result in results:
#         channel_name, channel_url = result
#         if '卫视' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"{channel_name},{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"{channel_name},{channel_url}\n")
#                 channel_counters[channel_name] = 1
#
# # 将IPTV1文件内容写入到weishi.m3u
# with open("weishi.m3u", 'w', encoding='utf-8') as file:
#     channel_counters = {}
#     for result in results:
#         channel_name, channel_url = result
#         if '卫视' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
#                     file.write(f"{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
#                 file.write(f"{channel_url}\n")
#                 channel_counters[channel_name] = 1
#
# # 将IPTV1文件内容写入到gangao.txt
# channel_counters = {}
# with open("gangao.txt", 'w', encoding='utf-8') as file:
#     file.write('港澳频道,#genre#\n')
#     for result in results:
#         channel_name, channel_url = result
#         if '凤凰' in channel_name or '翡翠' in channel_name or 'TVB' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"{channel_name},{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"{channel_name},{channel_url}\n")
#                 channel_counters[channel_name] = 1
#
# # 将IPTV1文件内容写入到gangao.m3u
# with open("gangao.m3u", 'w', encoding='utf-8') as file:
#     channel_counters = {}
#     for result in results:
#         channel_name, channel_url = result
#         if '凤凰' in channel_name or '翡翠' in channel_name or 'TVB' in channel_name:
#             if channel_name in channel_counters:
#                 if channel_counters[channel_name] >= result_counter:
#                     continue
#                 else:
#                     file.write(f"#EXTINF:-1 group-title=\"港澳频道\",{channel_name}\n")
#                     file.write(f"{channel_url}\n")
#                     channel_counters[channel_name] += 1
#             else:
#                 file.write(f"#EXTINF:-1 group-title=\"港澳频道\",{channel_name}\n")
#                 file.write(f"{channel_url}\n")
#                 channel_counters[channel_name] = 1

# 读取ipv6.txt文件
results = []
result_counter = 5  # 每个频道需要的个数
with open("ipv6.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            channel_name, channel_url = line.split(',')
            if 'genre' not in channel_url:
                results.append((channel_name, channel_url))

# 将ipv6.txt文件地方频道内容写入到hunan.txt
channel_counters = {}
with open("hunan.txt", 'w', encoding='utf-8') as file:
    file.write('湖南频道,#genre#\n')
    for result in results:
        channel_name, channel_url = result
        if '湖南经视' in channel_name or '湖南都市' in channel_name or '湖南爱晚' in channel_name or '湖南国际' in channel_name or '湖南娱乐' in channel_name or '湖南电影' in channel_name or '湖南电视剧' in channel_name or '长沙' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 将ipv6.txt文件地方频道内容写入到hunan.m3u
with open("hunan.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    for result in results:
        channel_name, channel_url = result
        if '湖南经视' in channel_name or '湖南都市' in channel_name or '湖南爱晚' in channel_name or '湖南国际' in channel_name or '湖南娱乐' in channel_name or '湖南电影' in channel_name or '湖南电视剧' in channel_name or '长沙' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"湖南频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"湖南频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1

# 将ipv6.txt文件其余频道内容写入到ipv6_list.txt
with open("ipv6_list.txt", 'w', encoding='utf-8') as file:
    file.write('IPV6频道,#genre#\n')
    for result in results:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or '卫视' in channel_name or '凤凰' in channel_name or 'CHC' in channel_name or '求索' in channel_name or 'NewTV' in channel_name or '咪咕' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 将ipv6.txt文件其余频道内容写入到ipv6_list.txt.m3u
with open("ipv6_list.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    for result in results:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or '卫视' in channel_name or '凤凰' in channel_name or 'CHC' in channel_name or '求索' in channel_name or 'NewTV' in channel_name or '咪咕' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"IPV6频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"IPV6频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1


# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
# 从iptv.txt文件内提取其他频道进行检测并分组
with open("iptv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            channel_name, channel_url = line.split(',')
            if 'CCTV' not in channel_name and '卫视' not in channel_name and '湖南' not in channel_name and '长沙' not in channel_name:
                channels.append((channel_name, channel_url))


# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                # print(f"文件大小：{file_size} 字节")
                download_speed = file_size / response_time / 1024
                # print(f"下载速度：{download_speed:.3f} kB/s")
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                # print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(
                    f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(
                f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    # t = threading.Thread(target=worker, args=(event,len(channels)))  # 将工作线程设置为守护线程
    t.start()
    # event.set()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
# results.sort(key=lambda x: channel_key(x[0]))
now_today = datetime.date.today()

result_counter = 10  # 每个频道需要的个数

with open("iptv_list.txt", 'w', encoding='utf-8') as file:
    # channel_counters = {}
    # file.write('少儿频道,#genre#\n')
    # for result in results:
    #     channel_name, channel_url, speed = result
    #     if '卡通' in channel_name or '少儿' in channel_name or '动画' in channel_name or '炫动' in channel_name or '动漫' in channel_name:
    #         if channel_name in channel_counters:
    #             if channel_counters[channel_name] >= result_counter:
    #                 continue
    #             else:
    #                 file.write(f"{channel_name},{channel_url}\n")
    #                 channel_counters[channel_name] += 1
    #         else:
    #             file.write(f"{channel_name},{channel_url}\n")
    #             channel_counters[channel_name] = 1

    # channel_counters = {}
    # file.write('求索纪实,#genre#\n')
    # for result in results:
    #     channel_name, channel_url, speed = result
    #     if '求索' in channel_name or '纪实' in channel_name or '地理' in channel_name:
    #         if channel_name in channel_counters:
    #             if channel_counters[channel_name] >= result_counter:
    #                 continue
    #             else:
    #                 file.write(f"{channel_name},{channel_url}\n")
    #                 channel_counters[channel_name] += 1
    #         else:
    #             file.write(f"{channel_name},{channel_url}\n")
    #             channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('影视综合,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '电影' in channel_name or '影院' in channel_name or '戏剧' in channel_name or '戏曲' in channel_name or '影视' in channel_name or '梨园' in channel_name or '电视剧' in channel_name or '综艺' in channel_name or '剧场' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '地理' not in channel_name and 'BTV卡酷' not in channel_name and '凤凰' not in channel_name and '翡翠' not in channel_name and 'TVB' not in channel_name and '求索' not in channel_name and '纪实' not in channel_name and '钓' not in channel_name and '锦至' not in channel_name and '测试' not in channel_name and '演示' not in channel_name and '茶' not in channel_name and '购物' not in channel_name and '理财' not in channel_name and '湖南' not in channel_name and '长沙' not in channel_name and '卡通' not in channel_name and '少儿' not in channel_name and '动画' not in channel_name and '炫动' not in channel_name and '动漫' not in channel_name and '剧场' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '戏剧' not in channel_name and '戏曲' not in channel_name and '影视' not in channel_name and '梨园' not in channel_name and '电视剧影' not in channel_name and '综艺' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

with open("iptv_list.m3u", 'w', encoding='utf-8') as file:
    # channel_counters = {}
    # # file.write('少儿频道,#genre#\n')
    # for result in results:
    #     channel_name, channel_url, speed = result
    #     if '卡通' in channel_name or '少儿' in channel_name or '动画' in channel_name or '炫动' in channel_name or '动漫' in channel_name:
    #         if channel_name in channel_counters:
    #             if channel_counters[channel_name] >= result_counter:
    #                 continue
    #             else:
    #                 file.write(f"#EXTINF:-1 group-title=\"少儿频道\",{channel_name}\n")
    #                 file.write(f"{channel_url}\n")
    #                 channel_counters[channel_name] += 1
    #         else:
    #             file.write(f"#EXTINF:-1 group-title=\"少儿频道\",{channel_name}\n")
    #             file.write(f"{channel_url}\n")
    #             channel_counters[channel_name] = 1
    #
    # channel_counters = {}
    # # file.write('求索纪实,#genre#\n')
    # for result in results:
    #     channel_name, channel_url, speed = result
    #     if '求索' in channel_name or '纪实' in channel_name or '地理' in channel_name:
    #         if channel_name in channel_counters:
    #             if channel_counters[channel_name] >= result_counter:
    #                 continue
    #             else:
    #                 file.write(f"#EXTINF:-1 group-title=\"求索纪实\",{channel_name}\n")
    #                 file.write(f"{channel_url}\n")
    #                 channel_counters[channel_name] += 1
    #         else:
    #             file.write(f"#EXTINF:-1 group-title=\"求索纪实\",{channel_name}\n")
    #             file.write(f"{channel_url}\n")
    #             channel_counters[channel_name] = 1

    channel_counters = {}
    # file.write('影视综合,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '电影' in channel_name or '影院' in channel_name or '戏剧' in channel_name or '戏曲' in channel_name or '影视' in channel_name or '梨园' in channel_name or '电视剧' in channel_name or '综艺' in channel_name or '剧场' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"影视综合\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"影视综合\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    # file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '地理' not in channel_name and 'BTV卡酷' not in channel_name and '凤凰' not in channel_name and '翡翠' not in channel_name and 'TVB' not in channel_name and '求索' not in channel_name and '纪实' not in channel_name and '钓' not in channel_name and '锦至' not in channel_name and '测试' not in channel_name and '演示' not in channel_name and '茶' not in channel_name and '购物' not in channel_name and '理财' not in channel_name and '湖南' not in channel_name and '长沙' not in channel_name and '卡通' not in channel_name and '少儿' not in channel_name and '动画' not in channel_name and '炫动' not in channel_name and '动漫' not in channel_name and '剧场' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '戏剧' not in channel_name and '戏曲' not in channel_name and '影视' not in channel_name and '梨园' not in channel_name and '电视剧影' not in channel_name and '综艺' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1

    # 合并自定义频道文件内容
    file_contents = []
    file_paths = ["ipv6_list.txt", "ipv4_list.txt", "hunan.txt", "iptv_list.txt", "zdy.txt"]  # 替换为实际的文件路径列表
    for file_path in file_paths:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)

    # 写入合并后的文件
    with open("iptv_list.txt", "w", encoding="utf-8") as output:
        output.write('\n'.join(file_contents))

        output.write(f"更新日期,#genre#\n")
        output.write(f"{now_today},url\n")

    # 合并自定义频道文件内容
    file_contents = []
    file_paths = ["ipv6_list.m3u", "ipv4_list.m3u", "hunan.m3u", "iptv_list.m3u"]  # 替换为实际的文件路径列表
    for file_path in file_paths:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)

    # 写入合并后的文件
    with open("iptv_list.m3u", "w", encoding="utf-8") as output:
        output.write('\n'.join(file_contents))

        output.write(f"#EXTINF:-1 group-title=\"更新日期\",{now_today}\n")
        output.write(f"url\n")

    os.remove("iptv.txt")
    os.remove("ipv6.txt")
    os.remove("iptv1.txt")
    os.remove("ipv6_list.txt")
    os.remove("ipv4_list.txt")
    os.remove("hunan.txt")
    os.remove("ipv6_list.m3u")
    os.remove("ipv4_list.m3u")
    os.remove("hunan.m3u")
