# -*- coding: utf-8 -*-
"""王一然工作台 - 后端 API 服务"""
import json, os, time, random, socket, re
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get('PORT', 8000))

# ====== 18-30岁女生热点 + 好物种草 ======
HOT_VIDEOS = [
    # 好物测评/种草/护发
    {"title":"沙发发质终于有救了！冷雾直板夹一夹就顺不伤发","author":"护发小达人","likes":185000,"comments":5200,"shares":12000,"tag":"爆款","tags":["好物测评","护发","直板夹"],"match":"96%","style":"痛点开场+真人出镜+前后对比","videoUrl": "https://www.douyin.com/search/%E6%B2%99%E5%8F%91%E5%8F%91%E8%B4%A8%E7%BB%88%E4%BA%8E%E6%9C%89%E6%95%91%E4%BA%86%EF%BC%81%E5%86%B7%E9%9B%BE%E7%9B%B4%E6%9D%BF%E5%A4%B9%E4%B8%80%E5%A4%B9%E5%B0%B1%E9%A1%BA%E4%B8%8D%E4%BC%A4%E5%8F%91"},
    {"title":"165cm女生好物分享！这些平价神器让我每天多睡半小时","author":"懒人好物","likes":230000,"comments":6800,"shares":18000,"tag":"爆款","tags":["好物分享","平价","种草"],"match":"94%","style":"身高标签+场景痛点+清单体","videoUrl": "https://www.douyin.com/search/165cm%E5%A5%B3%E7%94%9F%E5%A5%BD%E7%89%A9%E5%88%86%E4%BA%AB%EF%BC%81%E8%BF%99%E4%BA%9B%E5%B9%B3%E4%BB%B7%E7%A5%9E%E5%99%A8%E8%AE%A9%E6%88%91%E6%AF%8F%E5%A4%A9%E5%A4%9A%E7%9D%A1%E5%8D%8A%E5%B0%8F%E6%97%B6"},
    {"title":"真人实测！网红护发产品到底值不值得买","author":"实测君","likes":156000,"comments":4200,"shares":9800,"tag":"热门","tags":["测评","护发","避坑"],"match":"92%","style":"真人实测+真实体验+避坑","videoUrl": "https://www.douyin.com/search/%E7%9C%9F%E4%BA%BA%E5%AE%9E%E6%B5%8B%EF%BC%81%E7%BD%91%E7%BA%A2%E6%8A%A4%E5%8F%91%E4%BA%A7%E5%93%81%E5%88%B0%E5%BA%95%E5%80%BC%E4%B8%8D%E5%80%BC%E5%BE%97%E4%B9%B0"},
    {"title":"用了3个月才敢说！这个直板夹真的不伤发","author":"真实体验派","likes":310000,"comments":8900,"shares":25000,"tag":"爆款","tags":["好物测评","直板夹","长期使用"],"match":"98%","style":"长期跟踪+信任感","videoUrl": "https://www.douyin.com/search/%E7%94%A8%E4%BA%863%E4%B8%AA%E6%9C%88%E6%89%8D%E6%95%A2%E8%AF%B4%EF%BC%81%E8%BF%99%E4%B8%AA%E7%9B%B4%E6%9D%BF%E5%A4%B9%E7%9C%9F%E7%9A%84%E4%B8%8D%E4%BC%A4%E5%8F%91"},
    {"title":"千万别买！网红护发产品踩雷合集大公开","author":"避雷指南针","likes":195000,"comments":7200,"shares":14000,"tag":"爆款","tags":["测评","护发","避坑"],"match":"93%","style":"反向标题+争议引流","videoUrl": "https://www.douyin.com/search/%E5%8D%83%E4%B8%87%E5%88%AB%E4%B9%B0%EF%BC%81%E7%BD%91%E7%BA%A2%E6%8A%A4%E5%8F%91%E4%BA%A7%E5%93%81%E8%B8%A9%E9%9B%B7%E5%90%88%E9%9B%86%E5%A4%A7%E5%85%AC%E5%BC%80"},
    {"title":"不到50块！学生党好物从邋遢变精致","author":"平价好物挖掘机","likes":275000,"comments":6100,"shares":21000,"tag":"爆款","tags":["好物分享","平价","学生党","种草"],"match":"88%","style":"极限价格+前后对比","videoUrl": "https://www.douyin.com/search/%E4%B8%8D%E5%88%B050%E5%9D%97%EF%BC%81%E5%AD%A6%E7%94%9F%E5%85%9A%E5%A5%BD%E7%89%A9%E4%BB%8E%E9%82%8B%E9%81%A2%E5%8F%98%E7%B2%BE%E8%87%B4"},
    {"title":"沉浸式开箱！护发好物让头发变顺滑","author":"沉浸式开箱","likes":142000,"comments":4800,"shares":8500,"tag":"热门","tags":["开箱","护发","好物"],"match":"91%","style":"沉浸式+真实开箱","videoUrl": "https://www.douyin.com/search/%E6%B2%89%E6%B5%B8%E5%BC%8F%E5%BC%80%E7%AE%B1%EF%BC%81%E6%8A%A4%E5%8F%91%E5%A5%BD%E7%89%A9%E8%AE%A9%E5%A4%B4%E5%8F%91%E5%8F%98%E9%A1%BA%E6%BB%91"},
    {"title":"被同事问了800遍的发型神器！沙发闭眼入","author":"办公室好物","likes":210000,"comments":5500,"shares":16000,"tag":"爆款","tags":["好物分享","护发","种草"],"match":"97%","style":"社交货币+闭眼入","videoUrl": "https://www.douyin.com/search/%E8%A2%AB%E5%90%8C%E4%BA%8B%E9%97%AE%E4%BA%86800%E9%81%8D%E7%9A%84%E5%8F%91%E5%9E%8B%E7%A5%9E%E5%99%A8%EF%BC%81%E6%B2%99%E5%8F%91%E9%97%AD%E7%9C%BC%E5%85%A5"},
    {"title":"真人出镜！我的护发Routine从炸毛到顺滑","author":"护发Routine","likes":168000,"comments":3900,"shares":11000,"tag":"热门","tags":["护发","真人出镜","好物"],"match":"95%","style":"Routine分享+全过程","videoUrl": "https://www.douyin.com/search/%E7%9C%9F%E4%BA%BA%E5%87%BA%E9%95%9C%EF%BC%81%E6%88%91%E7%9A%84%E6%8A%A4%E5%8F%91Routine%E4%BB%8E%E7%82%B8%E6%AF%9B%E5%88%B0%E9%A1%BA%E6%BB%91"},
    {"title":"买了就后悔没早买！10件生活好物太绝了","author":"好物清单","likes":320000,"comments":10200,"shares":28000,"tag":"爆款","tags":["好物分享","种草","清单体"],"match":"89%","style":"清单体+悬念结尾","videoUrl": "https://www.douyin.com/search/%E4%B9%B0%E4%BA%86%E5%B0%B1%E5%90%8E%E6%82%94%E6%B2%A1%E6%97%A9%E4%B9%B0%EF%BC%8110%E4%BB%B6%E7%94%9F%E6%B4%BB%E5%A5%BD%E7%89%A9%E5%A4%AA%E7%BB%9D%E4%BA%86"},
    # 18-30岁女生热点
    {"title":"打工人一周穿搭不重样！通勤ootd合集","author":"通勤穿搭日记","likes":420000,"comments":12800,"shares":35000,"tag":"爆款","tags":["穿搭","OOTD","通勤","女生"],"match":"92%","style":"场景化+合集+真实感","videoUrl": "https://www.douyin.com/search/%E6%89%93%E5%B7%A5%E4%BA%BA%E4%B8%80%E5%91%A8%E7%A9%BF%E6%90%AD%E4%B8%8D%E9%87%8D%E6%A0%B7%EF%BC%81%E9%80%9A%E5%8B%A4ootd%E5%90%88%E9%9B%86"},
    {"title":"独自生活的女生有多爽？治愈系vlog日常","author":"独居女孩日记","likes":380000,"comments":9500,"shares":28000,"tag":"爆款","tags":["vlog","独居","治愈","女生"],"match":"90%","style":"治愈系+生活方式","videoUrl": "https://www.douyin.com/search/%E7%8B%AC%E8%87%AA%E7%94%9F%E6%B4%BB%E7%9A%84%E5%A5%B3%E7%94%9F%E6%9C%89%E5%A4%9A%E7%88%BD%EF%BC%9F%E6%B2%BB%E6%84%88%E7%B3%BBvlog%E6%97%A5%E5%B8%B8"},
    {"title":"月薪5k和月薪5w女生的消费观差别有多大","author":"财商思维","likes":560000,"comments":18500,"shares":62000,"tag":"爆款","tags":["理财","消费观","女生","职场"],"match":"85%","style":"对比反差+话题性","videoUrl": "https://www.douyin.com/search/%E6%9C%88%E8%96%AA5k%E5%92%8C%E6%9C%88%E8%96%AA5w%E5%A5%B3%E7%94%9F%E7%9A%84%E6%B6%88%E8%B4%B9%E8%A7%82%E5%B7%AE%E5%88%AB%E6%9C%89%E5%A4%9A%E5%A4%A7"},
    {"title":"30岁之前一定要知道的10个道理！女生必看","author":"成长学姐","likes":290000,"comments":8200,"shares":19000,"tag":"热门","tags":["成长","女生","人生建议"],"match":"87%","style":"清单体+共鸣感","videoUrl": "https://www.douyin.com/search/30%E5%B2%81%E4%B9%8B%E5%89%8D%E4%B8%80%E5%AE%9A%E8%A6%81%E7%9F%A5%E9%81%93%E7%9A%8410%E4%B8%AA%E9%81%93%E7%90%86%EF%BC%81%E5%A5%B3%E7%94%9F%E5%BF%85%E7%9C%8B"},
    {"title":"周末一个人可以做的100件小事！治愈又快乐","author":"生活方式指南","likes":350000,"comments":7200,"shares":25000,"tag":"爆款","tags":["生活","治愈","清单","女生"],"match":"88%","style":"清单体+治愈系","videoUrl": "https://www.douyin.com/search/%E5%91%A8%E6%9C%AB%E4%B8%80%E4%B8%AA%E4%BA%BA%E5%8F%AF%E4%BB%A5%E5%81%9A%E7%9A%84100%E4%BB%B6%E5%B0%8F%E4%BA%8B%EF%BC%81%E6%B2%BB%E6%84%88%E5%8F%88%E5%BF%AB%E4%B9%90"},
    {"title":"从月薪3k到月入3w，我做对了什么","author":"搞钱女孩","likes":480000,"comments":15200,"shares":45000,"tag":"爆款","tags":["职场","搞钱","成长","女生"],"match":"86%","style":"故事+干货+共鸣","videoUrl": "https://www.douyin.com/search/%E4%BB%8E%E6%9C%88%E8%96%AA3k%E5%88%B0%E6%9C%88%E5%85%A53w%EF%BC%8C%E6%88%91%E5%81%9A%E5%AF%B9%E4%BA%86%E4%BB%80%E4%B9%88"},
    {"title":"女生一定要学会的情绪管理方法！内耗退退退","author":"心理学笔记","likes":260000,"comments":8900,"shares":22000,"tag":"热门","tags":["情绪","心理","内耗","女生"],"match":"91%","style":"痛点+方法论","videoUrl": "https://www.douyin.com/search/%E5%A5%B3%E7%94%9F%E4%B8%80%E5%AE%9A%E8%A6%81%E5%AD%A6%E4%BC%9A%E7%9A%84%E6%83%85%E7%BB%AA%E7%AE%A1%E7%90%86%E6%96%B9%E6%B3%95%EF%BC%81%E5%86%85%E8%80%97%E9%80%80%E9%80%80%E9%80%80"},
    {"title":"那些让人一眼心动的夏日穿搭！清凉又时髦","author":"穿搭灵感站","likes":330000,"comments":6800,"shares":18000,"tag":"爆款","tags":["穿搭","夏日","OOTD","女生"],"match":"89%","style":"季节感+美感+实用","videoUrl": "https://www.douyin.com/search/%E9%82%A3%E4%BA%9B%E8%AE%A9%E4%BA%BA%E4%B8%80%E7%9C%BC%E5%BF%83%E5%8A%A8%E7%9A%84%E5%A4%8F%E6%97%A5%E7%A9%BF%E6%90%AD%EF%BC%81%E6%B8%85%E5%87%89%E5%8F%88%E6%97%B6%E9%AB%A6"},
    {"title":"女孩们请记住：你不需要完美才值得被爱","author":"自我成长记","likes":410000,"comments":11300,"shares":38000,"tag":"爆款","tags":["自我成长","女生","治愈"],"match":"93%","style":"情感共鸣+正能量","videoUrl": "https://www.douyin.com/search/%E5%A5%B3%E5%AD%A9%E4%BB%AC%E8%AF%B7%E8%AE%B0%E4%BD%8F%EF%BC%9A%E4%BD%A0%E4%B8%8D%E9%9C%80%E8%A6%81%E5%AE%8C%E7%BE%8E%E6%89%8D%E5%80%BC%E5%BE%97%E8%A2%AB%E7%88%B1"},
    {"title":"2026年女生最值得做的副业合集！月入过万","author":"副业研究所","likes":520000,"comments":16800,"shares":58000,"tag":"爆款","tags":["副业","搞钱","女生","2026"],"match":"84%","style":"干货+清单+时效性","videoUrl": "https://www.douyin.com/search/2026%E5%B9%B4%E5%A5%B3%E7%94%9F%E6%9C%80%E5%80%BC%E5%BE%97%E5%81%9A%E7%9A%84%E5%89%AF%E4%B8%9A%E5%90%88%E9%9B%86%EF%BC%81%E6%9C%88%E5%85%A5%E8%BF%87%E4%B8%87"},
]

# ====== 每日鼓励语 ======
ENCOURAGE = [
    "今天的你比昨天更厉害 ✨",
    "慢慢来，比较快 🌱",
    "你已经很棒了，继续加油 💪",
    "别着急，好事都在路上 🌈",
    "每一个认真生活的你都闪闪发光 ⭐",
    "今天也是元气满满的一天！☀️",
    "不要和别人比，和昨天的自己比 🎯",
    "累了就休息，但不要放弃 🧘‍♀️",
    "你的努力，时间看得见 ⏰",
    "做自己的太阳，无需借谁的光 🔆",
    "今天迈出的每一步都算数 👣",
    "相信过程，相信你 🙌",
    "今天也要好好爱自己 💛",
    "小步快跑，持续前进 🏃‍♀️",
    "你值得所有美好的事物 🌸",
    "别内耗了，干就完了！⚡",
    "你比想象中更强大 🦁",
    "今天的汗水是明天的底气 💦",
    "允许自己偶尔慢下来 🍃",
    "你就是自己人生的主角 🎬",
]

# ====== 投资理财小知识 ======
INVEST_TIPS = [
    {"title":"什么是股票？","content":"股票是公司所有权的凭证。买入股票=成为公司的小股东，分享公司成长带来的收益。对于新手，建议从指数基金（如沪深300ETF）开始，分散风险。"},
    {"title":"基金vs股票怎么选？","content":"股票需要自己研究公司，风险高；基金由基金经理帮你选股，适合新手。建议小白先从定投指数基金开始，每月固定金额买入，平摊成本。"},
    {"title":"什么是定投？","content":"定期定额投资，比如每月1号固定买入1000元沪深300ETF。不管市场涨跌都买，长期来看能平摊成本。巴菲特说：普通人最好的投资方式就是定投指数基金。"},
    {"title":"市场风向：2026年关注什么？","content":"消费复苏、AI应用落地、新能源储能是当前热门赛道。但新手不要追热点！先建立自己的投资体系，了解自己的风险承受能力再入场。"},
    {"title":"新手必知：仓位管理","content":"永远不要满仓！建议留30%现金应对波动。分散投资：不同行业、不同类型的资产组合配置。记住：保住本金比赚钱更重要。"},
    {"title":"市盈率(PE)是什么？","content":"PE=股价÷每股收益。PE低=可能被低估，PE高=市场预期高。但不能只看PE，还要结合行业、成长性综合判断。消费类PE通常比科技类低。"},
]

# ====== 资讯文章 ======
NEWS_ARTICLES = [
    {"tag":"科技","title":"OpenAI发布GPT-5o模型，多模态能力大幅提升","summary":"OpenAI今日凌晨发布GPT-5o模型，在图像理解、语音交互和代码生成方面实现质的飞跃，响应速度提升3倍，成本降低60%。","source":"科技日报","time":"2小时前","link":"https://www.36kr.com"},
    {"tag":"科技","title":"苹果Vision Pro 2曝光：更轻更便宜，预计年底发布","summary":"据供应链消息，苹果第二代Vision Pro头显将大幅减重，价格有望降至1.5万元以内，同时配备更强大的M5芯片和改进的显示技术。","source":"钛媒体","time":"3小时前","link":"https://www.36kr.com"},
    {"tag":"科技","title":"国产大模型DeepSeek-V4发布，推理能力超越GPT-4o","summary":"深度求索发布DeepSeek-V4模型，在数学推理、代码生成等基准测试中超越GPT-4o，且开源免费，引发AI圈热议。","source":"量子位","time":"5小时前","link":"https://www.36kr.com"},
    {"tag":"电商","title":"抖音电商2026上半年GMV突破2万亿，直播带货持续增长","summary":"抖音电商公布上半年数据，GMV同比增长45%，直播带货贡献超60%份额，货架电商增速达78%，搜索电商成为新增长引擎。","source":"亿邦动力","time":"1小时前","link":"https://www.ebrun.com"},
    {"tag":"电商","title":"淘宝直播推出'AI虚拟主播'功能，24小时不间断带货","summary":"淘宝直播上线AI虚拟主播功能，商家可低成本生成虚拟主播全天候直播，单场成本降至真人主播的十分之一，中小商家纷纷尝鲜。","source":"电商在线","time":"4小时前","link":"https://www.ebrun.com"},
    {"tag":"电商","title":"拼多多海外版Temu进入全球50+国家，日活超亚马逊","summary":"拼多多旗下Temu已覆盖全球50多个国家和地区，日均活跃用户数超越亚马逊，成为中国出海电商增长最快的平台之一。","source":"36氪","time":"6小时前","link":"https://www.36kr.com"},
    {"tag":"趋势","title":"2026年Z世代消费报告：情绪价值成第一购买驱动力","summary":"最新调研显示，95后、00后消费者在购物决策中，情绪价值占比首次超过功能价值，治愈系、陪伴型产品销量增长超200%。","source":"CBNData","time":"3小时前","link":"https://www.cbndata.com"},
    {"tag":"趋势","title":"国货美妆出海加速，花西子、橘朵在东南亚月销破亿","summary":"国货美妆品牌加速出海步伐，花西子、橘朵、完美日记等品牌在东南亚市场表现亮眼，多个品牌单月海外销售额突破1亿元。","source":"青眼","time":"5小时前","link":"https://www.qingyan.com"},
    {"tag":"趋势","title":"AI+美妆成新风口，虚拟试妆用户突破5亿","summary":"得益于大模型技术突破，虚拟试妆体验大幅提升，全球虚拟试妆用户已突破5亿，欧莱雅、雅诗兰黛等巨头纷纷加码AI美妆赛道。","source":"美丽修行","time":"8小时前","link":"https://www.bevol.cn"},
    {"tag":"美妆","title":"夏日防晒新趋势：喷雾防晒销量暴涨300%，这些成分成焦点","summary":"入夏以来防晒喷雾销量暴涨300%，新型物化结合防晒成分如氧化锌+天兰苣提取物成为消费者关注焦点，温和不刺激成首选。","source":"美丽修行","time":"2小时前","link":"https://www.bevol.cn"},
    {"tag":"美妆","title":"护肤新成分'重组胶原蛋白'火了，国产品牌弯道超车","summary":"重组胶原蛋白成为2026年最火护肤成分，巨子生物、丸美等国产品牌在技术端实现突破，产品复购率远超国际大牌同类产品。","source":"青眼","time":"7小时前","link":"https://www.qingyan.com"},
    {"tag":"生活","title":"年轻人掀起'City Walk'热潮，城市漫游经济规模超500亿","summary":"2026年City Walk已成为年轻人最爱的休闲方式，带动城市漫游经济规模超500亿元，小红书相关笔记发布量同比增长320%。","source":"新榜","time":"4小时前","link":"https://www.newrank.cn"},
]

# ====== 播客列表 ======
PODCASTS = [
    {"title":"搞钱女孩","host":"小辉、阿楚","duration":"75分钟","episodes":"86期","category":"搞钱","desc":"两个90后女孩聊聊搞钱那些事，从副业、理财到创业，分享真实经历和踩坑经验，帮你找到适合自己的搞钱路径。"},
    {"title":"自习室","host":"乘以十","duration":"60分钟","episodes":"120期","category":"成长","desc":"一档关注自我成长的播客，每期围绕一个成长话题深入探讨，学习方法、时间管理、职业规划，陪你一起变得更好。"},
    {"title":"随机波动","host":"之琪、冷建国、张之琪","duration":"90分钟","episodes":"155期","category":"商业","desc":"三位女性视角的文化对谈播客，从社会热点到文化现象，用理性而温柔的声音解读当下，在随机中寻找确定性。"},
    {"title":"贤者时间","host":"小张、小王","duration":"70分钟","episodes":"92期","category":"情感","desc":"两个普通女孩的闲聊播客，聊爱情、聊友情、聊生活中的鸡毛蒜皮，不完美但真实，就像和闺蜜在咖啡馆的下午茶。"},
    {"title":"文化有限","host":"超哥、大一、朴鲁","duration":"80分钟","episodes":"180期","category":"成长","desc":"一档读书播客，三位主播每期推荐一本好书，从文学到社科，从经典到新书，用轻松的方式聊聊阅读这件事。"},
    {"title":"不合时宜","host":"王磬、若含、孟常","duration":"85分钟","episodes":"110期","category":"商业","desc":"关注全球议题的中文播客，从国际政治到社会文化，三位在不同国家生活的主播带来多元视角，理解世界的复杂性。"},
    {"title":"忽左忽右","host":"程衍樑、杨大壹","duration":"70分钟","episodes":"230期","category":"商业","desc":"一档深度对谈播客，话题涵盖历史、政治、商业和文化，邀请各领域专家深入聊透一个问题，在左右之间寻找平衡。"},
    {"title":"无人知晓","host":"孟岩","duration":"100分钟","episodes":"45期","category":"搞钱","desc":"有知有行创始人孟岩的个人播客，聊投资、聊理财、聊人生，在不确定的市场中寻找确定的成长，让投资回归常识。"},
    {"title":"知行小酒馆","host":"雨白、一知羊","duration":"65分钟","episodes":"78期","category":"搞钱","desc":"有知有行出品的投资播客，用大白话聊理财，从基金定投到资产配置，帮你建立适合自己的投资体系。"},
    {"title":"声动早咖啡","host":"声动活泼","duration":"15分钟","episodes":"365期","category":"商业","desc":"每日早间商业播客，15分钟了解全球商业大事，科技、金融、消费领域一网打尽，开启高效的一天。"},
    {"title":"三五环","host":"刘飞","duration":"80分钟","episodes":"95期","category":"商业","desc":"互联网产品人刘飞的对谈播客，聊产品、聊商业、聊互联网行业，邀请行业从业者分享真实经验和洞察。"},
    {"title":"大内密谈","host":"相征、杨樾","duration":"120分钟","episodes":"400期","category":"生活","desc":"中文播客届的老牌节目，聊音乐、聊文化、聊生活方式，三位老友天马行空地闲聊，总能在意外的地方收获惊喜。"},
]

# ====== 每日英语单词 ======
ENGLISH_WORDS = [
    {"word":"accomplish","phonetic":"/əˈkɒmplɪʃ/","pos":"v.","meaning":"完成，实现","sentence":"She worked hard to accomplish her goals.","translation":"她努力工作以实现自己的目标。"},
    {"word":"benefit","phonetic":"/ˈbenɪfɪt/","pos":"n.","meaning":"好处，益处","sentence":"Regular exercise has many benefits for your health.","translation":"规律运动对你的健康有很多好处。"},
    {"word":"confident","phonetic":"/ˈkɒnfɪdənt/","pos":"adj.","meaning":"自信的","sentence":"She felt confident about the job interview.","translation":"她对面试很有信心。"},
    {"word":"discover","phonetic":"/dɪˈskʌvə/","pos":"v.","meaning":"发现，找到","sentence":"I discovered a great new restaurant near my office.","translation":"我在办公室附近发现了一家很棒的新餐厅。"},
    {"word":"essential","phonetic":"/ɪˈsenʃl/","pos":"adj.","meaning":"必要的，重要的","sentence":"Water is essential for all living things.","translation":"水对所有生物都是必不可少的。"},
    {"word":"familiar","phonetic":"/fəˈmɪliə/","pos":"adj.","meaning":"熟悉的","sentence":"This song sounds very familiar to me.","translation":"这首歌听起来很熟悉。"},
    {"word":"generate","phonetic":"/ˈdʒenəreɪt/","pos":"v.","meaning":"产生，创造","sentence":"Solar panels generate electricity from sunlight.","translation":"太阳能电池板利用阳光发电。"},
    {"word":"hesitate","phonetic":"/ˈhezɪteɪt/","pos":"v.","meaning":"犹豫，迟疑","sentence":"Don't hesitate to ask if you need help.","translation":"如果需要帮助，不要犹豫。"},
    {"word":"improve","phonetic":"/ɪmˈpruːv/","pos":"v.","meaning":"改善，提高","sentence":"Reading every day can improve your vocabulary.","translation":"每天阅读可以提高你的词汇量。"},
    {"word":"journey","phonetic":"/ˈdʒɜːni/","pos":"n.","meaning":"旅程，旅行","sentence":"Life is a journey, not a destination.","translation":"生活是一场旅程，不是终点。"},
    {"word":"knowledge","phonetic":"/ˈnɒlɪdʒ/","pos":"n.","meaning":"知识，学识","sentence":"Knowledge is power, so never stop learning.","translation":"知识就是力量，所以永远不要停止学习。"},
    {"word":"launch","phonetic":"/lɔːntʃ/","pos":"v.","meaning":"发起，推出","sentence":"The company will launch a new product next month.","translation":"公司下个月将推出一款新产品。"},
    {"word":"manage","phonetic":"/ˈmænɪdʒ/","pos":"v.","meaning":"管理，应对","sentence":"She manages a team of twenty people.","translation":"她管理着一个二十人的团队。"},
    {"word":"negotiate","phonetic":"/nɪˈɡəʊʃieɪt/","pos":"v.","meaning":"谈判，协商","sentence":"We need to negotiate a better price with the supplier.","translation":"我们需要和供应商协商一个更好的价格。"},
    {"word":"opportunity","phonetic":"/ˌɒpəˈtjuːnɪti/","pos":"n.","meaning":"机会，时机","sentence":"This job offers a great opportunity for growth.","translation":"这份工作提供了很好的成长机会。"},
    {"word":"patient","phonetic":"/ˈpeɪʃnt/","pos":"adj.","meaning":"有耐心的","sentence":"Be patient, learning a language takes time.","translation":"要有耐心，学习一门语言需要时间。"},
    {"word":"quality","phonetic":"/ˈkwɒlɪti/","pos":"n.","meaning":"质量，品质","sentence":"We focus on quality rather than quantity.","translation":"我们注重质量而不是数量。"},
    {"word":"recognize","phonetic":"/ˈrekəɡnaɪz/","pos":"v.","meaning":"认出，识别","sentence":"I didn't recognize you with your new haircut.","translation":"你新剪了头发我都没认出来。"},
    {"word":"succeed","phonetic":"/səkˈsiːd/","pos":"v.","meaning":"成功，达到","sentence":"If you work hard, you will succeed in the end.","translation":"如果你努力，最终一定会成功。"},
    {"word":"trust","phonetic":"/trʌst/","pos":"n./v.","meaning":"信任，信赖","sentence":"Trust is the foundation of any good relationship.","translation":"信任是任何良好关系的基础。"},
    {"word":"unique","phonetic":"/juːˈniːk/","pos":"adj.","meaning":"独特的，唯一的","sentence":"Everyone has a unique perspective on life.","translation":"每个人对生活都有独特的看法。"},
    {"word":"valuable","phonetic":"/ˈvæljuəbl/","pos":"adj.","meaning":"有价值的，宝贵的","sentence":"Your experience is very valuable to our team.","translation":"你的经验对我们的团队非常宝贵。"},
    {"word":"wonder","phonetic":"/ˈwʌndə/","pos":"v.","meaning":"想知道，好奇","sentence":"I wonder what the weather will be like tomorrow.","translation":"我想知道明天天气会怎么样。"},
    {"word":"achieve","phonetic":"/əˈtʃiːv/","pos":"v.","meaning":"实现，达到","sentence":"You can achieve anything if you set your mind to it.","translation":"只要用心，你什么都能实现。"},
    {"word":"balance","phonetic":"/ˈbæləns/","pos":"n.","meaning":"平衡","sentence":"It's important to find a balance between work and life.","translation":"在工作和生活之间找到平衡很重要。"},
    {"word":"challenge","phonetic":"/ˈtʃælɪndʒ/","pos":"n.","meaning":"挑战","sentence":"Learning a new skill is always a challenge.","translation":"学习一项新技能总是一个挑战。"},
    {"word":"determine","phonetic":"/dɪˈtɜːmɪn/","pos":"v.","meaning":"决定，决心","sentence":"Your attitude determines your altitude.","translation":"你的态度决定了你的高度。"},
    {"word":"encourage","phonetic":"/ɪnˈkʌrɪdʒ/","pos":"v.","meaning":"鼓励，激励","sentence":"My parents always encourage me to follow my dreams.","translation":"我的父母总是鼓励我追求梦想。"},
    {"word":"focus","phonetic":"/ˈfəʊkəs/","pos":"v.","meaning":"集中，专注","sentence":"Stay focused on your goals and don't get distracted.","translation":"专注于你的目标，不要分心。"},
    {"word":"growth","phonetic":"/ɡrəʊθ/","pos":"n.","meaning":"成长，增长","sentence":"Personal growth comes from stepping out of your comfort zone.","translation":"个人成长来自于走出舒适区。"},
    {"word":"handle","phonetic":"/ˈhændl/","pos":"v.","meaning":"处理，应对","sentence":"She can handle any situation with calm and grace.","translation":"她能从容优雅地处理任何情况。"},
]

hot_cache = {"videos":[],"updateTime":"","ttl":0}

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path)
        if p.path == '/api/hot':
            self.api_hot()
            return
        if p.path == '/api/encourage':
            self.api_encourage()
            return
        if p.path == '/api/invest':
            self.api_invest()
            return
        if p.path == '/api/extract':
            self.api_extract(p)
            return
        if p.path == '/api/news':
            self.api_news()
            return
        if p.path == '/api/douyin':
            self.api_douyin()
            return
        if p.path == '/api/podcast':
            self.api_podcast()
            return
        if p.path == '/api/english':
            self.api_english()
            return
        if self.path in ('/',''):
            self.path = '/index.html'
        ct_map = {'.js':'application/javascript','.css':'text/css','.html':'text/html','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon'}
        ext = os.path.splitext(self.path)[1]
        ct = ct_map.get(ext,'application/octet-stream')
        try:
            fp = os.path.join(os.path.dirname(__file__), self.path.lstrip('/'))
            if not os.path.isfile(fp):
                self.send_error(404); return
            self.send_response(200)
            self.send_header('Content-Type', f'{ct}; charset=utf-8' if ext in ['.js','.css','.html','.json'] else ct)
            self.send_header('Cache-Control','no-cache,no-store,must-revalidate')
            self.end_headers()
            with open(fp,'rb') as f: self.wfile.write(f.read())
        except: self.send_error(500)

    def api_hot(self):
        global hot_cache
        now = time.time()
        if hot_cache['ttl'] > now and hot_cache['videos']:
            self.send_json(hot_cache); return
        vids = random.sample(HOT_VIDEOS, min(10,len(HOT_VIDEOS)))
        for v in vids:
            v = v.copy()
            v['likes'] += random.randint(-5000,15000)
            v['comments'] += random.randint(-200,500)
            v['shares'] += random.randint(-500,2000)
            v['likes'] = max(1000,v['likes'])
        hot_cache = {"videos":vids,"updateTime":datetime.now().strftime('%m月%d日 %H:%M'),"ttl":now+300}
        self.send_json(hot_cache)

    def api_encourage(self):
        tip = random.choice(ENCOURAGE)
        self.send_json({"text":tip,"date":datetime.now().strftime('%m月%d日')})

    def api_invest(self):
        tip = random.choice(INVEST_TIPS)
        self.send_json(tip)

    def api_extract(self, p):
        """模拟提取抖音视频文案"""
        qs = parse_qs(p.query)
        url = qs.get('url',[''])[0]
        # 模拟返回文案
        templates = [
            "【0-3秒】姐妹们！这个东西真的绝了！\n【3-8秒】先看效果，再看价格，真的惊到我了\n【8-15秒】详细展示使用过程，每一个细节都不放过\n【15-20秒】最后说价格，真的不贵！橱窗有同款",
            "【0-3秒】被问了800遍的XXX终于来了\n【3-8秒】为什么这么火？我帮你们测了\n【8-15秒】真实使用感受，优点缺点都说\n【15-20秒】值不值得买？我的建议是...",
            "【0-3秒】这个痛点你肯定也有！\n【3-8秒】直到我发现了这个宝藏\n【8-15秒】用了之后简直打开新世界\n【15-20秒】赶紧去试试，不好用来找我",
        ]
        self.send_json({"success":True,"title":"提取的视频文案","content":random.choice(templates),"source":url[:50]+"..." if url else "未知来源"})

    def api_news(self):
        """随机返回8条资讯文章"""
        articles = random.sample(NEWS_ARTICLES, min(8, len(NEWS_ARTICLES)))
        self.send_json({"articles": articles, "updateTime": "07月28日 12:00"})

    def api_douyin(self):
        """随机返回12条抖音热门，带rank字段"""
        trends = random.sample(HOT_VIDEOS, min(12, len(HOT_VIDEOS)))
        result = []
        for i, v in enumerate(trends):
            item = v.copy()
            item['rank'] = i + 1
            result.append(item)
        self.send_json({"trends": result, "updateTime": datetime.now().strftime('%m月%d日 %H:%M')})

    def api_podcast(self):
        """随机返回8条播客"""
        podcasts = random.sample(PODCASTS, min(8, len(PODCASTS)))
        self.send_json({"podcasts": podcasts})

    def api_english(self):
        """根据天数返回每日英语单词"""
        now = datetime.now()
        day_of_year = now.timetuple().tm_yday
        word = ENGLISH_WORDS[day_of_year % len(ENGLISH_WORDS)]
        self.send_json({"word": word, "date": now.strftime('%Y-%m-%d')})

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Cache-Control','no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data,ensure_ascii=False).encode('utf-8'))

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    srv = HTTPServer(('0.0.0.0',PORT), Handler)
    srv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f'🚀 王一然工作台 v2 已启动 http://0.0.0.0:{PORT}')
    try: srv.serve_forever()
    except KeyboardInterrupt: print('\n👋 关闭'); srv.shutdown()

if __name__ == '__main__': main()
