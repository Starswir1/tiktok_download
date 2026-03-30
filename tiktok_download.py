import requests
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import xml.etree.ElementTree as ET
import requests
import json
import re
import os
import argparse
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
import asyncio  # 异步I/O
import os  # 系统操作
import time  # 时间操作
from urllib.parse import urlencode, quote  # URL编码
import yaml  # 配置文件
# with open(f"./config.yaml", "r", encoding="utf-8") as f:
#     config = yaml.safe_load(f)
class DouyinCrawler:
    def __init__(self):
        """初始化"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
            'Cookie': 'enter_pc_once=1; UIFID_TEMP=41de20d2c8c0372836b7333ed3b868523ae3b3b747399417a35ee29432002d5cc5d72113465524edee98641d4f2566b578ac9a2af6569e70957e4f900804304c499aa398c821b734bf4a8b96721b5a78; s_v_web_id=verify_mna3cljj_hEYZfXOV_7QfE_4uRC_By06_x6ZY7roDfO75; hevc_supported=true; dy_swidth=1707; dy_sheight=960; fpk1=U2FsdGVkX18vx8lxoa/zw4P/ePCJt4X92iG89UyEflmNG3RdzbJoNAMGGVOWFrMV+sY5+F9AI70791XoAepP0w==; fpk2=8e253f85246590342756399a57054cb8; is_dash_user=1; passport_csrf_token=6cab04ee916aa5b2c8a55283ebbf012a; passport_csrf_token_default=6cab04ee916aa5b2c8a55283ebbf012a; UIFID=41de20d2c8c0372836b7333ed3b868523ae3b3b747399417a35ee29432002d5cc5d72113465524edee98641d4f2566b50f6db98c88edd6e425c271f170075e8775e79cbec4633d2311f41f66233a270ec348cfb5dff401fcbe47e142a4872cddadfbdd844768b7d6afb9fd7938659a941526bebfbb74b6c33cad0d8c74a841a7fecf7fadec76d75dc863a02825300d33375ca796320e5d34ae3e5259d4882158; bd_ticket_guard_client_web_domain=2; _bd_ticket_crypt_cookie=19551094da194d1ca26e4a4c4c8e7a12; __security_mc_1_s_sdk_sign_data_key_web_protect=df38080b-4ca2-8c0a; __security_mc_1_s_sdk_cert_key=f57582ad-45f7-9e55; __security_mc_1_s_sdk_crypt_sdk=fbcca068-4354-8e6c; __security_server_data_status=1; SelfTabRedDotControl=%5B%7B%22id%22%3A%227568417064023853108%22%2C%22u%22%3A18%2C%22c%22%3A0%7D%5D; publish_badge_show_info=%220%2C0%2C0%2C1774690019026%22; __ac_nonce=069c8db7f004a5996e433; __ac_signature=_02B4Z6wo00f013pya7wAAIDA99rSNPVqQmt6Um8AALdf6b; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A960%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; strategyABtestKey=%221774771074.126%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAABXUJ4-tUA4E-xMqSiyKTrVNjrn-lXPfpC6oOZcJZh12MRxgXHYfkUAj7AQBj2Uh%2F1774800000000%2F0%2F1774771074370%2F0%22; gulu_source_res=eyJwX2luIjoiNjU5NTEzOWNiNWY3ZDAzY2U1YmNkZjNlM2M2MDQwZjk0N2JiNGVkYWUzZjc5N2FhNzAzZjczZDcwZjlmODQyMSJ9; login_time=1774771084066; download_guide=%223%2F20260329%2F0%22; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCUHZycVcyUXA3eXY5SkFXQ080WUtWcndOSGdlbnN3NXJNNnVhS1o2NTUrTXFnRGVvZXJRS0UzUE1RZlcxRFcwNms0eXdoWUJ2RjltajhHZ1RWWWkxVVE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJQdnJxVzJRcDd5djlKQVdDTzRZS1Zyd05IZ2Vuc3c1ck02dWFLWjY1NStNcWdEZW9lclFLRTNQTVFmVzFEVzA2azR5d2hZQnZGOW1qOEdnVFZZaTFVUT0iLCJ0c19zaWduIjoidHMuMi4yNDE1Y2U4ZWQzMzY1NzE0N2NiNWIwZWIzNTE2YWRjNzM3OGIzMTVjNWMwZTAxMzdmMTU2ZGFkMmYxYmY2MmRjYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJjVk1XU0JpdGpYdmNvemtRN2J0eXJGL3dpbmNRUTJ6WUhnOHZFdUdOWmtzPSIsInNlY190cyI6IiM3ejkxdDJnMldZdXpjTi8xTHMvczBhTlNUNEFabHBLWHRsWmUyNmgyUW5IZk5tZ01yZTBUQkpOejJJb20ifQ%3D%3D; record_force_login=%7B%22timestamp%22%3A1774771085405%2C%22force_login_video%22%3A2%2C%22force_login_live%22%3A0%2C%22force_login_direct_video%22%3A1%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; biz_trace_id=bdfd416d; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e5927666d776a686028607d71606b766c6a6b3f2a2a696267696b636c61646d6661666f61616c60756e666e6663616d756e6b6b6f6d2a666a6b71606b712a756a75707576287666776c75712b6f765927295927666d776a686028607d71606b766c6a6b3f2a2a61676f67606875696f6d66686d69637563646664696a686a6b6f756469756e6a2a7666776c7571762a6c6b76756066716a772b6f76592758272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2733303334373634323231323234272927676c715a75776a716a666a69273f2763646976602778; bit_env=tx5hJHuFFBmGwUya1FwgoIPato0Nu6Fc1hQWxdMxHWT2uOLHXLMSXlUJoZz75UZs_vV8lAiBuz_P9urHyENR8KyxFBmb-xnpfYX79QIrBwd7-n4gTlQL6RfpGwKWOOwgX9rQBeBeJm6tg7m7sSncC_VsSh3ileoJbA0nI6Ybwmr5KV5wzhPZZ1VeoMrSW9g9fJk17qCXnX5uykWrLBzYVD8bu7qFks-KWLkcMg6GJVz_cfPu-5f2BLBLzzGAw5yXCajqmH6QTL95m26iU3pZ3c3oqAVuxlQm9fJR64i_BOySe-tjYyu9e0sokrDk4W37FaalAm6ZlOwQi-doott9PtFSPfY5-2xePlBQ07UhA_Lw-9UnO-pmXdIg71J_h0AYEnkgbTky4ODDfCjgPbfHpzgyaz9ogeDrbbVClpGY32yO-f094cZigJTVUtAl0rAP0Cai8WDkqkaLHRkeYOz_4BbRPyCLspr1vSbmuFTH209J8wyUNWFNiCrrHUbzVOqL; passport_auth_mix_state=stf3eeco041imkppi3421h2szp9vo33s; IsDouyinActive=true'  # 可选：添加登录后的Cookie以获取更多权限
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.model = 'video'

        # self.model = 'video'
    
    def get_video_id(self, url):
        """从URL中提取ID"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        # 匹配不同格式的抖音URL
        if self.model == 'note':
            video_id_match = re.search(r'/note/([0-9]+)', path)
        elif self.model == 'video':
            video_id_match = re.search(r'/video/([0-9]+)', path)
        if video_id_match:
            return video_id_match.group(1)
        # 处理短链接格式
        if 'v.douyin.com' in url:
            response = self.session.get(url, allow_redirects=False)
            if 'Location' in response.headers:
                redirected_url = response.headers['Location']
                return self.get_video_id(redirected_url)
        return None
    
    def get_video_info(self, video_id):
        """获取信息"""
        # try:
            # 构建API请求URL
        api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}"
        response = self.session.get(api_url)
        print(response.text)
        breakpoint()
        response.raise_for_status()
        
        video_data = response.json()
        # breakpoint()        
        if 'aweme_detail' in video_data:
            aweme_detail = video_data['aweme_detail']
            title = aweme_detail.get('desc', f"视频_{video_id}")
            # 获取视频播放地址
            if 'video' in aweme_detail and 'play_addr' in aweme_detail['video']:
                play_addr = aweme_detail['video']['play_addr']
                if 'url_list' in play_addr and len(play_addr['url_list']) > 0:
                    video_url = play_addr['url_list'][0]
                    return {
                        'title': title,
                        'video_url': video_url
                    }
        
        # 如果API请求失败，尝试从网页中提取
        page_url = f"https://www.douyin.com/video/{video_id}"
        response = self.session.get(page_url)
        response.raise_for_status()

        # 提取视频信息
        title_match = re.search(r'<title>(.*?)</title>', response.text)
        title = title_match.group(1).replace(' - 抖音', '') if title_match else f"视频_{video_id}"
        # breakpoint()        
        # 提取视频链接
        video_match = re.search(r'"playAddr":"(.*?)"', response.text)
        if video_match:
            video_url = video_match.group(1).replace('\\u002F', '/')
            return {
                'title': title,
                'video_url': video_url
            }
        
        return None
        # except Exception as e:
        #     print(f"获取视频信息失败: {e}")
        #     return None
    
    def download_video(self, url, filename):
        """下载视频"""
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            with open(filename, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
            return True
        except Exception as e:
            print(f"下载视频失败: {e}")
            return False
    
    def crawl(self, url, output_dir='downloads'):
        """主爬取函数"""
        # 获取视频ID
        video_id = self.get_video_id(url)
        if not video_id:
            print("无法从URL中提取视频ID")
            return
        
        # 获取视频信息
        video_info = self.get_video_info(video_id)
        if not video_info:
            print("无法获取视频信息")
            return
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 下载视频
        filename = os.path.join(output_dir, f"{video_info['title']}.mp4")
        # 清理文件名中的非法字符
        filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
        print(f"正在下载: {filename}")
        self.download_video(video_info['video_url'], filename)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='抖音视频爬虫')
    parser.add_argument('url', help='抖音视频URL', nargs='?', default=None)
    parser.add_argument('--output', '-o', default='downloads', help='输出目录')

    args = parser.parse_args()
    args.url = 'https://www.douyin.com/video/7619756095514430771'    
    # if args.url is None:
    #     try:
    #         tree = ET.parse('config.xml')
    #         root = tree.getroot()
    #         tiktok_info = root.find('tiktok-info')
    #         if tiktok_info is not None:
    #             url_elem = tiktok_info.find('url')
    #             if url_elem is not None and url_elem.text:
    #                 args.url = url_elem.text
    #             else:
    #                 print("错误：配置文件中未找到URL")
    #                 return
    #         else:
    #             print("错误：配置文件格式不正确")
    #             return
    #     except Exception as e:
    #         print(f"读取配置文件失败: {e}")
    #         return
    crawler = DouyinCrawler()
    crawler.crawl(args.url, args.output)

if __name__ == '__main__':
    main()

# # 代码大纲

# ## 1. 项目结构
# - `douyin_crawler.py` - 主爬虫文件

# ## 2. 核心功能模块

# ### 2.1 初始化模块
# - 定义请求头和会话
# - 设置User-Agent和Referer
# - 可选：添加Cookie以获取更多权限

# ### 2.2 URL处理模块
# - 从视频URL中提取视频ID
# - 处理短链接重定向

# ### 2.3 视频信息获取模块
# - 访问API获取视频数据
# - 从网页中提取视频信息（备用方案）
# - 解析JSON格式的视频数据

# ### 2.4 视频下载模块
# - 处理视频流数据
# - 显示下载进度
# - 保存视频文件
# - 清理文件名中的非法字符

# ### 2.5 主控制模块
# - 命令行参数解析
# - 调用各功能模块
# - 异常处理

# ## 3. 技术要点
# - 使用requests库发送HTTP请求
# - 使用正则表达式提取页面信息
# - 解析JSON格式数据
# - 处理短链接重定向
# - 处理流式下载
# - 显示下载进度条

# ## 4. 使用方法
# ```bash
# python douyin_crawler.py https://www.douyin.com/video/1234567890
# ```

# ## 5. 依赖库
# - requests - 发送HTTP请求
# - tqdm - 显示下载进度条

# ## 6. 注意事项
# - 本爬虫仅供学习使用
# - 请遵守抖音的使用条款
# - 大量爬取可能会被封禁IP
# - 视频版权归原作者所有
# - 抖音的API可能会频繁变化，需要及时更新代码

# # 爬虫代码设计大纲

# ## 1. 设计目标
# - 爬取抖音网页端视频
# - 支持多种抖音URL格式
# - 提供友好的命令行界面
# - 显示下载进度
# - 处理异常情况

# ## 2. 技术选型
# - 语言：Python 3
# - 核心库：requests, re, json, os, argparse, tqdm
# - 架构：面向对象设计

# ## 3. 详细设计

# ### 3.1 类设计
# - `DouyinCrawler`类
#   - 成员变量：headers, session
#   - 成员方法：
#     - `__init__()`: 初始化爬虫
#     - `get_video_id(url)`: 提取视频ID
#     - `get_video_info(video_id)`: 获取视频信息
#     - `download_video(url, filename)`: 下载视频
#     - `crawl(url, output_dir)`: 主爬取函数

# ### 3.2 流程设计
# 1. 解析命令行参数
# 2. 初始化爬虫
# 3. 提取视频ID
# 4. 获取视频信息
# 5. 创建输出目录
# 6. 下载视频
# 7. 保存视频文件

# ### 3.3 异常处理
# - 网络请求异常
# - 视频信息解析异常
# - 下载异常
# - 文件保存异常

# ### 3.4 性能优化
# - 使用会话保持连接
# - 流式下载大文件
# - 显示下载进度

# ### 3.5 扩展性考虑
# - 支持批量下载
# - 支持代理设置
# - 支持自定义请求头
# - 支持不同质量的视频下载