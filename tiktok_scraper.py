"""Main Scraper File"""
import traceback
import re
import asyncio
from typing import Union
import urllib.parse
import execjs
import aiohttp

class Scraper:
    """
    Define headers
    """
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
        self.douyin_api_headers = {
            'accept-encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.douyin.com/',
            'cookie': "s_v_web_id=verify_leytkxgn_kvO5kOmO_SdMs_4t1o_B5ml_BUqtWM1mP6BF;"
        }
        self.tiktok_api_headers = {
            'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'
        }

    @staticmethod
    def get_share_url(text: str) -> Union[str, None]:
        """
        # Regex 
        use regex to get url from string
        """
        try:
            print('text:', text)
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            print('url:', url)
            if len(url) > 0 :
                return url[0]
        except Exception as re_error:
            print('Error in get_url:', re_error)
            return None

    async def convert_share_url(self, url: str) -> Union[str, None]:
        """
        # Convert Share Link to Original Link
        """
        url = self.get_share_url(url)
        if url is None:
            print("Unable to retrieve link")
            return None

        if 'douyin' in url:
            if 'v.douyin' in url:
                url = re.compile(r'(https://v.douyin.com/)\w+', re.I).match(url).group()
                print('getting original url by parsing share url')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, allow_redirects=False, timeout=10) as response:
                            if response.status == 302:
                                url = response.headers['location'].split('?')[0] if '?' in response.headers['location'] else response.headers['location']
                                print('Gotcha! original url:', url)
                                return url

                except Exception as err :
                    print('Unable to get original url')
                    print(err)
                    raise err
        elif 'tiktok' in url:
            if '@' in url:
                return url
            else:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers,  allow_redirects=False,
                                                timeout=10) as response:
                            if response.status == 301:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    return None
                        

    def generate_x_bogus_url(self, url: str) -> str:
        """
        生成抖音X-Bogus签名
        :param url: 视频链接
        :return: 包含X-Bogus签名的URL
        """
        # 调用JavaScript函数
        query = urllib.parse.urlparse(url).query
        xbogus = execjs.compile(open('./X-Bogus.js', encoding="utf8").read()).call('sign', query, self.headers['User-Agent'])
        print('生成的X-Bogus签名为: {}'.format(xbogus))
        new_url = url + "&X-Bogus=" + xbogus
        return new_url

    async def get_douyin_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: url
        :return: video_id
        """
        try:
            video_url = await self.convert_share_url(original_url)
            if '/video/' in video_url:
                # 链接类型:
                # 视频页 https://www.douyin.com/video/7086770907674348841
                video_id = re.findall(r'video/(\d+)?', video_url)[0]
                print('There you go! video id:', video_id)
                return video_id
            # 发现页 https://www.douyin.com/discover?modal_id=7086770907674348841
            elif 'discover?' in video_url:
                video_id = re.findall(r'modal_id=(\d+)', video_url)[0]
                print('There you go !: {}'.format(video_id))
                return video_id

        except Exception as err:
            print('Unable to get video id')
            print(err)
            return None

    async def get_douyin_video_data(self, video_id: str) -> Union[dict, None]:
        print('Getting video data')
        try:
            api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={video_id}&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1344&screen_height=756&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_version=110.0&browser_online=true&engine_name=Gecko&engine_version=109.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=&platform=PC&webid=7158288523463362079&msToken=abL8SeUTPa9-EToD8qfC7toScSADxpg6yLh2dbNcpWHzE0bT04txM_4UwquIcRvkRb9IU8sifwgM1Kwf1Lsld81o9Irt2_yNyUbbQPSUO8EfVlZJ_78FckDFnwVBVUVK"
            
            api_url = self.generate_x_bogus_url(api_url)
            # print('api_url:', api_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.douyin_api_headers, timeout=10) as response:
                    response = await response.json()
                    video_data = response['aweme_detail']
                    # print('video_data:', video_data)
                    return video_data
        except Exception as err:
            print('Unable to get video data')
            print(err)
            return None

    async def get_tiktok_video_id(self, original_url: str) -> str | None:
        try:
            # 转换链接/Convert link
            original_url = await self.convert_share_url(original_url)
            # 获取视频ID/Get video ID
            print(f'tiktok_original_url:{original_url}')
            if '/video/' in original_url:
                video_id = re.findall(r'/video/(\d+)', original_url)[0]
            elif '/v/' in original_url:
                video_id = re.findall(r'/v/(\d+)', original_url)[0]
            print(f'获取到的TikTok视频ID是{video_id}')
            # 返回视频ID/Return video ID
            return video_id
        except Exception as e:
            print(f'获取TikTok视频ID出错了:{e}')
            return None

    async def get_tiktok_video_data(self, video_id: str) -> dict | None:
        try:
            # 构造访问链接/Construct the access link
            api_url = f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
            print("正在获取视频数据API: {}".format(api_url))
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.tiktok_api_headers,timeout=10) as response:
                    response = await response.json()
                    video_data = response['aweme_list'][0]
                    print('获取视频信息成功！')
                    return video_data
        except Exception as e:
            print('获取视频信息失败！原因:{}'.format(e))
            # return None
            raise e

    
    async def link_parse(self, video_url:str) -> dict:
        url_platform = 'douyin' if 'douyin' in video_url else 'tiktok'
        print('url_platform:', url_platform)
        video_id = await self.get_douyin_video_id(video_url) if url_platform == 'douyin' else await self.get_tiktok_video_id(video_url)
        if video_id:
            print('getting video data')
            data = await self.get_douyin_video_data(video_id) if url_platform == 'douyin' else await self.get_tiktok_video_data(video_id)
            if data:
                print("get video data succeed")
                url_type_code = data['aweme_type']
                url_type_code_dict = {
                    2: 'image',
                    4: 'video',
                    68: 'image',
                    # TikTok
                    0: 'video',
                    51: 'video',
                    55: 'video',
                    58: 'video',
                    61: 'video',
                    150: 'image'
                }
                url_type = url_type_code_dict.get(url_type_code, 'video')
                print('url_type_code:', url_type_code)
                print("starting to parse video url")

                result_data = {
                    'status': 'success',
                    'type': url_type,
                    'platform': url_platform,
                    'aweme_id': video_id,
                    'official_api_url':
                        {
                            "User-Agent": self.headers["User-Agent"],
                            "api_url": f"https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&Github=Evil0ctal&words=FXXK_U_ByteDance"
                        },
                    'desc': data.get("desc"),
                    'create_time': data.get("create_time"),
                    'author': data.get("author"),
                    'music': data.get("music"),
                    'statistics': data.get("statistics"),
                    'cover_data': {
                        'cover': data.get("video").get("cover"),
                        'origin_cover': data.get("video").get("origin_cover"),
                        'dynamic_cover': data.get("video").get("dynamic_cover")
                    },
                    'hashtags': data.get('text_extra'),
                }
                api_data = None
                try:
                    if url_platform == 'douyin':
                        if url_type == 'video':
                            # TikTok视频数据处理/TikTok video data processing
                            uri = data['video']['play_addr']['uri']
                            wm_video_url = data['video']['play_addr']['url_list'][0]
                            wm_video_url_HQ = f"https://aweme.snssdk.com/aweme/v1/playwm/?video_id={uri}&radio=1080p&line=0"
                            nwm_video_url = wm_video_url.replace('playwm', 'play')
                            nwm_video_url_HQ = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={uri}&ratio=1080p&line=0"
                            api_data = {
                                'video_data':
                                    {
                                        'wm_url': wm_video_url,
                                        'wm_url_HQ': wm_video_url_HQ,
                                        'nwm_url': nwm_video_url,
                                        'nwm_url_HQ': nwm_video_url_HQ
                                    }
                            }
                        # 抖音图片数据处理/Douyin image data processing
                        elif url_type == 'image':
                            print("正在处理抖音图片数据...")
                            # 无水印图片列表/No watermark image list
                            no_watermark_image_list = []
                            # 有水印图片列表/With watermark image list
                            watermark_image_list = []
                            # 遍历图片列表/Traverse image list
                            for i in data['images']:
                                no_watermark_image_list.append(i['url_list'][0])
                                watermark_image_list.append(i['download_url_list'][0])
                            api_data = {
                                'image_data':
                                    {
                                        'no_watermark_image_list': no_watermark_image_list,
                                        'watermark_image_list': watermark_image_list
                                    }
                            }
                    elif url_platform == 'tiktok':
                        # TikTok视频数据处理/TikTok video data processing
                        if url_type == 'video':
                            print("正在处理TikTok视频数据...")
                            # 将信息储存在字典中/Store information in a dictionary
                            wm_video = data['video']['download_addr']['url_list'][0]
                            api_data = {
                                'video_data':
                                    {
                                        'wm_video_url': wm_video,
                                        'wm_video_url_HQ': wm_video,
                                        'nwm_video_url': data['video']['play_addr']['url_list'][0],
                                        'nwm_video_url_HQ': data['video']['bit_rate'][0]['play_addr']['url_list'][0]
                                    }
                            }
                        # TikTok图片数据处理/TikTok image data processing
                        elif url_type == 'image':
                            print("正在处理TikTok图片数据...")
                            # 无水印图片列表/No watermark image list
                            no_watermark_image_list = []
                            # 有水印图片列表/With watermark image list
                            watermark_image_list = []
                            for i in data['image_post_info']['images']:
                                no_watermark_image_list.append(i['display_image']['url_list'][0])
                                watermark_image_list.append(i['owner_watermark_image']['url_list'][0])
                            api_data = {
                                'image_data':
                                    {
                                        'no_watermark_image_list': no_watermark_image_list,
                                        'watermark_image_list': watermark_image_list
                                    }
                            }
                    # 更新数据/Update data
                    result_data.update(api_data)
                    # 返回数据/Return data
                    # print(result_data)
                    return result_data
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                    return {'status': 'failed', 'message': '数据处理失败！/Data processing failed!'}

    @staticmethod
    def hybird_parsing_minimal(data: dict):
        """return minimal data

        Args:
            data (dict): _description_

        Returns:
            _type_: _description_
        """
        if data['status'] == 'success':
            result = {
                'status': 'success',
                'message': data.get('message'),
                'platform': data.get('platform'),
                'type': data.get('type'),
                'desc': data.get('desc'),
                'wm_video_url': data['video_data']['wm_video_url'] if data['type'] == 'video' else None,
                'wm_video_url_HQ': data['video_data']['wm_video_url_HQ'] if data['type'] == 'video' else None,
                'nwm_video_url': data['video_data']['nwm_video_url'] if data['type'] == 'video' else None,
                'nwm_video_url_HQ': data['video_data']['nwm_video_url_HQ'] if data['type'] == 'video' else None,
                'no_watermark_image_list': data['image_data']['no_watermark_image_list'] if data[
                                                                                                'type'] == 'image' else None,
                'watermark_image_list': data['image_data']['watermark_image_list'] if data['type'] == 'image' else None
            }
            return result
        else:
            return data


if __name__ == '__main__':
    api = Scraper()
    # 运行测试
    # params = "device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7153585499477757192&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1344&screen_height=756&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_version=110.0&browser_online=true&engine_name=Gecko&engine_version=109.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=&platform=PC&webid=7158288523463362079"
    # api.generate_x_bogus(params)
    douyin_url = 'https://v.douyin.com/rLyrQxA/6.66'
    tiktok_url = 'https://vt.tiktok.com/ZSRwWXtdr/'
    asyncio.run(api.link_parse(douyin_url))
