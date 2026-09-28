import base64
import requests
import sys
import urllib.parse

LOCAL_SUB_FILE = "raw_sub.txt" # 你存放在仓库里的原始订阅文件路径

def main():
    try:
        # 1. 读取本地的原始订阅文件
        with open(LOCAL_SUB_FILE, "r", encoding="utf-8") as f:
            raw_content = f.read().strip()
            
        if not raw_content:
            print("错误：原始订阅文件内容为空！")
            sys.exit(1)

        # 2. 判断内容是明文节点还是已经 Base64 编码
        if "://" in raw_content:
            # 如果是明文节点链接（vless:// 等），将其统一转为 Base64 编码
            sub_base64 = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
        else:
            # 如果本身已经是 Base64 字符串，直接保留
            sub_base64 = raw_content

        # 3. 写入 kv4ynTKhcJWXZ3h.txt （输出标准 Base64 编码格式，不解码为明文）
        with open("kv4ynTKhcJWXZ3h.txt", "w", encoding="utf-8") as f:
            f.write(sub_base64)
        print("已成功更新 Base64 订阅文件 kv4ynTKhcJWXZ3h.txt")

        # 4. 调用 Subconverter API 将该 Base64 节点转换为 Clash YAML
        data_url = f"data:text/plain;base64,{sub_base64}"
        encoded_data_url = urllib.parse.quote(data_url, safe="")
        
        api_url = f"https://api.v1.mk/sub?target=clash&url={encoded_data_url}&insert=false"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print("正在请求转换服务生成 Clash YAML...")
        response = requests.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()
        clash_yaml = response.text

        # 检查转换出的 YAML 是否有效
        if "proxies:" in clash_yaml or "proxy-groups:" in clash_yaml:
            with open("kv4ynTKhcJWXZ3h.yaml", "w", encoding="utf-8") as f:
                f.write(clash_yaml)
            print("已成功生成包含完整节点的 kv4ynTKhcJWXZ3h.yaml")
        else:
            print("警告：转换出的 YAML 中没有找到 proxies 节点，请检查原始节点格式！")
            sys.exit(1)

    except Exception as e:
        print(f"运行发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
