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
with open(f"./config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
class DouyinCrawler:
    def __init__(self):
        """初始化"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
            'Cookie': ''  # 可选：添加登录后的Cookie以获取更多权限
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