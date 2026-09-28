import requests
import base64
import re

# 替换为你的原始订阅链接（例如每次变化或固定的源头链接）
SOURCE_SUB_URL = "https://example.com/api/your_raw_sub_link"

def decode_base64(data):
    """安全解码 Base64 字符串"""
    # 补全 Base64 填充等号
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Base64 解码异常: {e}")
        return data

def fetch_and_extract_nodes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        raw_text = response.text.strip()
        
        # 1. 尝试直接解码 Base64 文本
        decoded_text = decode_base64(raw_text)
        
        # 2. 使用正则表达式提取常见节点协议 (vmess, vless, ss, trojan, hy2 等)
        node_pattern = re.compile(r'((?:vmess|vless|ss|ssr|trojan|hysteria2|hy2)://[^\s]+)')
        nodes = node_pattern.findall(decoded_text)
        
        # 如果从解码文本中没找到，尝试直接从原始文本中匹配
        if not nodes:
            nodes = node_pattern.findall(raw_text)
            
        return nodes
    except Exception as e:
        print(f"获取订阅失败: {e}")
        return []

def main():
    nodes = fetch_and_extract_nodes(SOURCE_SUB_URL)
    
    if nodes:
        # 去重并以换行符分隔所有节点
        unique_nodes = list(dict.fromkeys(nodes))
        nodes_plain_text = "\n".join(unique_nodes)
        
        # 导出为明文节点文件
        with open("nodes_plain.txt", "w", encoding="utf-8") as f:
            f.write(nodes_plain_text)
            
        # 导出为标准 Base64 订阅文件 (小火箭/v2rayN 通用格式)
        base64_content = base64.b64encode(nodes_plain_text.encode('utf-8')).decode('utf-8')
        with open("sub_base64.txt", "w", encoding="utf-8") as f:
            f.write(base64_content)
            
        print(f"成功提取并保存了 {len(unique_nodes)} 个节点！")
    else:
        print("未提取到任何有效节点。")

if __name__ == "__main__":
    main()
