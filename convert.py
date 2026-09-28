import requests
import base64
import re
import sys

SOURCE_SUB_URL = "https://express-free.868382.xyz/vgk-kujio/y-jic-yt/uv-yw-ae-p-ws-dc/77f9a9f48b66f63d3376aa60270c650c" # 你的订阅链接

def decode_base64(data):
    # 去除可能存在的换行符和空格
    data = data.strip().replace("\n", "").replace("\r", "")
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Base64 解码失败，尝试直接使用原文: {e}")
        return data

def fetch_and_extract_nodes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    try:
        # verify=False 忽略证书校验，timeout 设置为 20 秒
        response = requests.get(url, headers=headers, timeout=20, verify=False)
        response.raise_for_status()
        raw_text = response.text.strip()
        
        decoded_text = decode_base64(raw_text)
        node_pattern = re.compile(r'((?:vmess|vless|ss|ssr|trojan|hysteria2|hy2)://[^\s]+)')
        nodes = node_pattern.findall(decoded_text)
        if not nodes:
            nodes = node_pattern.findall(raw_text)
            
        return nodes
    except Exception as e:
        print(f"获取订阅失败: {e}")
        return []

def generate_clash_yaml(nodes):
    yaml_header = """port: 7890
socks-port: 7891
allow-lan: false
mode: rule
log-level: info
external-controller: 127.0.0.1:9090
"""
    return yaml_header

def main():
    nodes = fetch_and_extract_nodes(SOURCE_SUB_URL)
    
    if nodes:
        unique_nodes = list(dict.fromkeys(nodes))
        nodes_plain_text = "\n".join(unique_nodes)
        
        # 1. 生成 base64 文本
        base64_content = base64.b64encode(nodes_plain_text.encode('utf-8')).decode('utf-8')
        with open("kv4ynTKhcJWXZ3h.txt", "w", encoding="utf-8") as f:
            f.write(base64_content)
        print("已成功生成 kv4ynTKhcJWXZ3h.txt")

        # 2. 生成 clash.yaml
        clash_content = generate_clash_yaml(unique_nodes)
        with open("kv4ynTKhcJWXZ3h.yaml", "w", encoding="utf-8") as f:
            f.write(clash_content)
        print("已成功生成 kv4ynTKhcJWXZ3h.yaml")
        
    else:
        print("错误：未提取到任何有效节点，请检查订阅链接是否可用或已被墙！")
        # 让脚本抛出非零退出码，阻断后续的 Git 操作
        sys.exit(1)

if __name__ == "__main__":
    main()
