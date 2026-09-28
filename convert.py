import base64
import requests
import sys
import urllib.parse

LOCAL_SUB_FILE = "raw_sub.txt" # 你存放在仓库里的原始订阅文件路径

def main():
    try:
        # 1. 读取本地的原始订阅/明文节点文件
        with open(LOCAL_SUB_FILE, "r", encoding="utf-8") as f:
            raw_content = f.read().strip()
            
        if not raw_content:
            print("错误：原始订阅文件内容为空！")
            sys.exit(1)

        # 2. 如果文件是明文节点，将其编码为 Base64（subconverter API 识别 Base64 更稳定）
        if "://" in raw_content:
            sub_base64 = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
        else:
            sub_base64 = raw_content

        # 保存明文/格式化的 TXT 节点订阅
        # (如果是明文直接写入，如果是 base64 则解码写入)
        try:
            plain_nodes = base64.b64decode(sub_base64).decode("utf-8", errors="ignore")
        except Exception:
            plain_nodes = raw_content

        with open("kv4ynTKhcJWXZ3h.txt", "w", encoding="utf-8") as f:
            f.write(plain_nodes)
        print("已成功更新明文节点文件 kv4ynTKhcJWXZ3h.txt")

        # 3. 将 Base64 内容转化为 data URI 形式，调用 Subconverter API 转成 Clash yaml
        data_url = f"data:text/plain;base64,{sub_base64}"
        encoded_data_url = urllib.parse.quote(data_url, safe="")
        
        # 使用公共的 subconverter 转换接口
        api_url = f"https://api.v1.mk/sub?target=clash&url={encoded_data_url}&insert=false"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print("正在请求转换服务生成 Clash YAML...")
        response = requests.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()
        clash_yaml = response.text

        # 检查转换出来的 YAML 是否包含代理节点
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
