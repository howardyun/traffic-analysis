import json

saveUrl = '../collectData/'


def extract_packet_info(json_file):
    """从 JSON 文件中提取每个数据包的时间、大小和进出方向信息"""
    # 读取 JSON 文件
    with open(json_file, 'r') as file:
        data = json.load(file)

    # 初始化数据包信息列表
    packet_info_list = []

    # 遍历 JSON 数据，提取信息
    for packet in data:
        # 获取时间戳
        timestamp = packet['_source']['layers']['frame']['frame.time_epoch']

        # 获取数据包大小
        packet_size = packet['_source']['layers']['frame']['frame.len']

        # 检查进出方向（假设存在某种方式区分，如IP地址或其他标识）
        # 这里我们简化处理，仅展示如何获取IP地址（发送者和接收者）
        src_ip = packet['_source']['layers']['ip']['ip.src']
        dst_ip = packet['_source']['layers']['ip']['ip.dst']

        # 添加到列表
        packet_info_list.append({
            'timestamp': timestamp,
            'size': packet_size,
            'src_ip': src_ip,
            'dst_ip': dst_ip
        })

    return packet_info_list


def main():
    # 调用函数并打印结果
    packets = extract_packet_info(saveUrl + 'capture.json')
    for packet in packets:
        print(
            f"Time: {packet['timestamp']}, Size: {packet['size']}, Src IP: {packet['src_ip']}, Dst IP: {packet['dst_ip']}")


if __name__ == '__main__':
    main()
