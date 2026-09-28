import requests
import base64
import re

SOURCE_SUB_URL = "https://express-free.868382.xyz/vgk-kujio/y-jic-yt/uv-yw-ae-p-ws-dc/77f9a9f48b66f63d3376aa60270c650c" # 替换为你的原始订阅链接

def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except Exception as e:
        return data

def fetch_and_extract_nodes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
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
    """简单的 Clash 配置模板生成逻辑"""
    # 基础的 Clash 配置头
    yaml_header = """port: 7890
socks-port: 7891
allow-lan: false
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

# 节点配置（此处直接导入原始链接节点，若需要完整的解析需使用 pyyaml）
# 注意：Clash 官方原生格式需要将节点解析为 key-value 字典。
# 如果直接包含代理节点，标准转换更推荐结合第三方库或将节点节点串写为节点列表。
"""
    # 这里演示生成包含节点的配置骨架
    # 在实际使用中，如果只是简单输出，可以直接把节点以文本方式或代理组形式写入
    return yaml_header

def main():
    nodes = fetch_and_extract_nodes(SOURCE_SUB_URL)
    
    if nodes:
        unique_nodes = list(dict.fromkeys(nodes))
        nodes_plain_text = "\n".join(unique_nodes)
        
        # 1. 生成 Shadowrocket / 通用客户端需要的 sub_base64.txt
        base64_content = base64.b64encode(nodes_plain_text.encode('utf-8')).decode('utf-8')
        with open("kv4ynTKhcJWXZ3h.txt", "w", encoding="utf-8") as f:
            f.write(base64_content)
        print("已成功生成 kv4ynTKhcJWXZ3h.txt")

        # 2. 生成 Clash 客户端需要的 clash.yaml
        # 注意：如果原始节点已经是完整的 Clash 配置 YAML，直接写入即可；
        # 如果是 Base64 节点，建议直接将 YAML 内容覆盖写入 clash.yaml
        clash_content = generate_clash_yaml(unique_nodes)
        with open("kv4ynTKhcJWXZ3h.yaml", "w", encoding="utf-8") as f:
            f.write(clash_content)
        print("已成功生成 kv4ynTKhcJWXZ3h.yaml")
        
    else:
        print("未提取到任何有效节点。")

if __name__ == "__main__":
    main()
