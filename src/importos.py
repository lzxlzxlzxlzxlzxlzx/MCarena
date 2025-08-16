import requests
import json
import csv

# 替换为你的 DeepSeek API Key
API_KEY = "sk-230dec004557436fbced6a2c5760f595"
# DeepSeek API 的请求地址，根据实际情况确认
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 怪物数据（扩展为完整属性）
MONSTER_DATA = {
    "撼地斯拉": {
        "price": "1000",
        "description": "boss，地面，范围攻击，超能射线，辐照",
        "health": "500",
        "attack": "30",
        "armor": "10",
        "unit_id": "alexscaves:tremorzilla"
    },
    "暝煌龙": {
        "price": "800",
        "description": "boss,地面，范围攻击，陨石雨",
        "health": "600",
        "attack": "12",
        "armor": "20",
        "unit_id": "alexscaves:luxtructosaurus"
    },
    "远古遗魂": {
        "price": "700",
        "description": "boss，地面，范围攻击，沙暴，甩尾",
        "health": "420",
        "attack": "11至34",
        "armor": "12",
        "unit_id": "cataclysm:ancient_remnant"
    },
    "先驱者": {
        "price": "600",
        "description": "boss，飞行，激光射击，导弹攻击",
        "health": "390",
        "attack": "5至27.5",
        "armor": "12",
        "unit_id": "cataclysm:the_harbinger"
    },
    "监守者": {
        "price": "400",
        "description": "地面，高速，单体近战高攻击，远程声波",
        "health": "500",
        "attack": "30（远程10）",
        "armor": "0",
        "unit_id": "warden"
    },
    "骸骨斩首者": {
        "price": "250",
        "description": "地面，范围攻击，冲锋斩击，格挡远程攻击",
        "health": "180",
        "attack": "14至17.5",
        "armor": "10",
        "unit_id": "cataclysm:kobolediator"
    },
    "撼地龙": {
        "price": "200",
        "description": "地面，单体高攻击，范围恐吓怒吼，咬住小型敌人",
        "health": "150",
        "attack": "14",
        "armor": "8",
        "unit_id": "alexscaves:tremorsaurus"
    },
    "擎天龙": {
        "price": "200",
        "description": "地面，高生命，范围攻击",
        "health": "400",
        "attack": "8",
        "armor": "0",
        "unit_id": "alexscaves:atlatitan"
    },
    "末影傀儡": {
        "price": "200",
        "description": "地面，超大范围攻击",
        "health": "120",
        "attack": "10至16",
        "armor": "12",
        "unit_id": "cataclysm:ender_golem"
    },
    "诡异蚊鬼": {
        "price": "180",
        "description": "飞行，近战攻击，吸血，20%血以下变为高机动远程攻击",
        "health": "100",
        "attack": "10（远程7）",
        "armor": "10",
        "unit_id": "alexsmobs:warped_mosco"
    }
}

# 读取测试结果文件内容
def read_test_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 A 队阵容
    a_team_start = content.find("### A队阵容\n") + len("### A队阵容\n")
    a_team_end = content.find("\n\n", a_team_start)
    a_team = content[a_team_start:a_team_end]
    
    # 提取 B 队阵容
    b_team_start = content.find("### B队阵容\n") + len("### B队阵容\n")
    b_team_end = content.find("\n\n", b_team_start)
    b_team = content[b_team_start:b_team_end]
    
    # 提取战斗结果
    a_alive_start = content.find("- A队存活: ") + len("- A队存活: ")
    a_alive_end = content.find("\n", a_alive_start)
    a_alive = content[a_alive_start:a_alive_end] == "True"
    
    b_alive_start = content.find("- B队存活: ") + len("- B队存活: ")
    b_alive_end = content.find("\n", b_alive_start)
    b_alive = content[b_alive_start:b_alive_end] == "True"
    
    return a_team, b_team, a_alive, b_alive

# 调用 DeepSeek API 进行分析和生成
def analyze_and_generate(a_team, b_team, a_alive, b_alive):
    # 构建怪物数据字符串，包含完整属性
    monster_data_str = "怪物数据信息：\n"
    for name, data in MONSTER_DATA.items():
        monster_data_str += (f"怪物: {name}, 价格: {data['price']}, 生命: {data['health']}, "
                            f"攻击力: {data['attack']}, 护甲: {data['armor']}, "
                            f"描述: {data['description']}\n")
    
    # 明确告知 DeepSeek 返回的格式要求，使用半角标点
    prompt = f'''请严格按照以下格式生成下一次的测试内容，不要输出任何额外的说明、分析或注释。注意双方的价格都不超过1000元，同时总价值尽量高（最好1000元整），生成不少于10个测试内容，尽量用更多种类的单位：
测试ID,A队阵容,B队阵容,测试备注
例如：
1,"铁傀儡:4,卫道士:20","炽燃遗魂:1,紫水晶巨蟹:1,铁傀儡:3,烈焰人:34",基础平衡测试

当前信息如下：
A 队阵容: {a_team}
B 队阵容: {b_team}
A 队存活: {a_alive}
B 队存活: {b_alive}
总预算: 1000 元

{monster_data_str}'''

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None

# 将结果写入 CSV 文件
def write_to_csv(new_test_content, csv_file_path):
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(["测试ID", "A队阵容", "B队阵容", "测试备注"])
        
        lines = new_test_content.split('\n')
        for line in lines:
            reader = csv.reader([line], delimiter=',', quotechar='"')
            row = next(reader)
            writer.writerow(row)

# 主函数
def main():
    test_result_file_path = "docs/批量测试结果.md"  # 更新为新的文件路径
    csv_file_path = "tests/data/output.csv"  # 更新为新的文件路径
    
    a_team, b_team, a_alive, b_alive = read_test_results(test_result_file_path)
    new_test_content = analyze_and_generate(a_team, b_team, a_alive, b_alive)
    
    if new_test_content:
        print(f"生成的下一次测试内容: {new_test_content}")
        write_to_csv(new_test_content, csv_file_path)

if __name__ == "__main__":
    main()