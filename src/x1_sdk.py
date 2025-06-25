from openai import OpenAI


api_key = "uGEaTkszqGmfxdRcYSOx:JnpSOlLWspUXIIsLxPKu"  # 请替换为您的 APIpassword,获取地址：https://console.xfyun.cn/services/bmx1
api_base = "https://spark-api-open.xf-yun.com/v2/"

# 请求模型，并将结果输出
def get_answer(message):
    #初始化client对象
    client = OpenAI(api_key=api_key, base_url=api_base)
    tool = [
        {
            "type": "web_search",
            "web_search": {
                "enable": True,
            	"search_mode":"deep"
            }
        }]
    try:
        # 发出请求
        response = client.chat.completions.create(
            model="x1",             #请求模型
            messages= message,      #对话历史
            stream=True,            #是否流式返回
            temperature= 1.2,       #温度控制参数：(0,2]
            max_tokens= 32768 ,      #输出最大长度限制，取值范围：[1,32768]
            tools= tool

        )

        full_response = ""          # 存储返回结果
        isFirstContent= True           # 首帧标识
        for chunk in response:
            #打印返回的每帧内容
            # print(chunk)
            # 只对支持深度思考的模型才有此字段
            if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[
                0].delta.reasoning_content is not None:
                reasoning_content = chunk.choices[0].delta.reasoning_content
                print(reasoning_content, end="", flush=True)  # 实时打印思考模型输出的思考过程每个片段

            #判断content是否存在，且不为空
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                #判断是否首帧结果
                if(isFirstContent):
                    print("\n*******************以上为思维链内容，模型回复内容如下********************\n")
                    isFirstContent = False
                print(content, end="", flush=True)  # 实时打印每个片段
                full_response += content

        # print("\n\n ------完整响应：", full_response)
        return full_response
    except Exception as e:
        print(f"Error: {e}")

# 管理对话历史，按序编为列表
def getText(text,role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

# 获取对话中的所有角色的content长度
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

# 判断长度是否超长，当前限制8K tokens
def checklen(text):
    while (getlength(text) > 11000):
        del text[0]
    return text


#主程序入口
if __name__ =='__main__':

    #对话历史存储列表
    chatHistory = []
    #循环对话轮次
    while (1):
        # 等待控制台输入
        Input = input("\n" + "我:")
        question = checklen(getText(chatHistory,"user", Input))
        # 开始输出模型内容
        print("星火:", end="")
        getText(chatHistory,"assistant", get_answer(question))


