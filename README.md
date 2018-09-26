# 笨笨聊小说模块说明

## 环境配置

1. Python版本：Python 3.5.4

2. 相关库：

   ```
   numpy 1.14.2
   jieba *
   opennmt-py https://github.com/OpenNMT/OpenNMT-py latest
   pytorch 0.4.0
   threadpool *
   BeautifulSoup *
   requests *
   json *
   rstr *
   ```

注：*表示对版本不作要求

## 使用说明

模型初始化比较耗时，加载完成后调用`npc.query(question, person)`即可