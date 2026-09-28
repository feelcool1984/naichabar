import base64
import re
import sys

# 不再使用 requests 请求网络，直接读取仓库里的本地文件
LOCAL_SUB_FILE = "raw_sub.txt" 

def decode_base64(data):
    data = data.strip().replace("\n", "").replace("\r", "")
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except Exception:
        return data

def fetch_and_extract_nodes_from_file(file_path):
    try:
        # 打开本地文件读取内容
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read().strip()
            
        decoded_text = decode_base64(raw_text)
        node_pattern = re.compile(r'((?:vmess|vless|ss|ssr|trojan|hysteria2|hy2)://[^\s]+)')
        nodes = node_pattern.findall(decoded_text)
        if not nodes:
            nodes = node_pattern.findall(raw_text)
            
        return nodes
    except Exception as e:
        print(f"读取本地订阅文件失败: {e}")
        return []

def main():
    # 改为从本地文件提取节点
    nodes = fetch_and_extract_nodes_from_file(LOCAL_SUB_FILE)
    
    if nodes:
        unique_nodes = list(dict.fromkeys(nodes))
        nodes_plain_text = "\n".join(unique_nodes)
        
        # 生成 base64 txt 文件
        base64_content = base64.b64encode(nodes_plain_text.encode('utf-8')).decode('utf-8')
        with open("kv4ynTKhcJWXZ3h.txt", "w", encoding="utf-8") as f:
            f.write(base64_content)
        print("已成功生成 kv4ynTKhcJWXZ3h.txt")

        # 生成 yaml 文件
        yaml_header = "port: 7890\nsocks-port: 7891\nallow-lan: false\nmode: rule\n"
        with open("kv4ynTKhcJWXZ3h.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_header)
        print("已成功生成 kv4ynTKhcJWXZ3h.yaml")
    else:
        print("未从本地文件中提取到有效节点！")
        sys.exit(1)

if __name__ == "__main__":
    main()
