import pyautogui
import time
import os
import csv
from datetime import datetime


# 配置参数
GAME_WINDOW_TITLE = "Minecraft: Java Edition"
DELAY_BETWEEN_COMMANDS = 0.5
INIT_DELAY = 5
BATTLE_DURATION = 100  # 战斗持续时间(秒)
LOG_PATH = "D:/TCLS/PCL最新正式版/.minecraft/versions/1.20.1-Forge_47.3.0/logs/debug.log" # 替换为本地debug.log地址
CONFIG_FILE = "output.csv"
RESULTS_FILE = "批量测试结果.md"

# 怪物数据（名称: (ID, 价格)）
MONSTER_DATA = {
    # BOSS级怪物
    "撼地斯拉": ("alexscaves:tremorzilla", 1000),
    "暝煌龙": ("alexscaves:luxtructosaurus", 800),
    "监守者": ("warden", 400),
    "骸骨斩首者": ("cataclysm:kobolediator", 250),
    "撼地龙": ("alexscaves:tremorsaurus", 200),
    "擎天龙": ("alexscaves:atlatitan", 200),
    "末影傀儡": ("cataclysm:ender_golem", 200),

    # 普通怪物
    "诡异蚊鬼": ("alexsmobs:warped_mosco", 180),
    "紫水晶巨蟹": ("cataclysm:amethyst_crab", 180),
    "炽燃遗魂": ("cataclysm:ignited_revenant", 180),
    "珊瑚巨兽": ("cataclysm:coralssus", 150),
    "瓦吉特": ("cataclysm:wadjet", 150),
    "霜冻巨兽": ("mowziesmobs:frostmaw", 150),
    "独眼巨人": ("iceandfire:cyclops", 150),
    "遗弃者": ("alexscaves:forsaken", 150),
    "雪怪首领": ("twilightforest:alpha_yeti", 150),
    "徘徊者": ("cataclysm:the_prowler", 140),
    "娜迦": ("twilightforest:naga", 120),
    "武装巨人": ("twilightforest:armored_giant", 120),
    "瞻远者": ("alexsmobs:farseer", 120),
    "太阳酋长": ("mowziesmobs:umvuthi", 120),
    "深潜者法师": ("alexscaves:deep_one_mage", 100),
    "冰雪女王": ("twilightforest:snow_queen", 100),
    "矿工巨人": ("twilightforest:giant_miner", 100),
    "核能苦力怕": ("alexscaves:nucleeper", 100),
    "铁傀儡": ("iron_golem", 100),
    "悚怖尸巫": ("iceandfire:dread_lich", 100),
    "珊瑚傀儡": ("cataclysm:coral_golem", 80),
    "现世遗魂": ("cataclysm:modern_remnant", 80),
    "大象": ("alexsmobs:elephant", 80),
    "劫掠者": ("pillager", 70),
    "渊灵蛮兵": ("cataclysm:deepling_brute", 60),
    "炽燃狂魂": ("cataclysm:ignited_berserker", 60),
    "食人妖": ("iceandfire:if_troll", 60),
    "遗迹恐手龙": ("alexscaves:relicheirus", 60),
    "渊灵术士": ("cataclysm:deepling_warlock", 50),
    "米诺菇": ("twilightforest:minoshroom", 50),
    "犀牛": ("alexsmobs:rhinoceros", 50),
    "唤魔者": ("evoker", 50),
    "灰熊": ("alexsmobs:grizzly_bear", 40),
    "老虎": ("alexsmobs:tiger", 40),
    "磁控机兵": ("alexscaves:magnetron", 40),
    "舐脑魔": ("alexscaves:brainiac", 40),
    "森蚺": ("alexsmobs:anaconda", 30),
    "獠牙兽": ("alexsmobs:tusklin", 30),
    "洞穴蜈蚣": ("alexsmobs:centipede_head", 30),
    "野牛": ("alexsmobs:bison", 30),
    "砷铅铁傀儡": ("twilightforest:tower_golem", 30),
    "渊灵祭司": ("cataclysm:deepling_priest", 35),
    "深潜者骑士": ("alexscaves:deep_one_knight", 35),
    "渊灵": ("cataclysm:deepling", 25),
    "轻语灵": ("alexsmobs:murmur", 25),
    "观测者": ("cataclysm:the_watcher", 25),
    "磁流灵": ("alexscaves:teleto", 25),
    "女巫": ("witch", 20),
    "卫道士": ("vindicator", 20),
    "跨座兽": ("alexsmobs:straddler", 20),
    "链锤哥布林": ("twilightforest:blockchain_goblin", 20),
    "鸡蛇": ("iceandfire:if_cockatrice", 20),
    "苦力怕": ("creeper", 20),
    "寒冬狼": ("twilightforest:winter_wolf", 16),
    "牛头人": ("twilightforest:minotaur", 16),
    "沙漠蛛蜂": ("alexsmobs:tarantula_hawk", 15),
    "铜羽泽鹗": ("iceandfire:stymphalianbird", 15),
    "骷髅狗头人": ("cataclysm:koboleton", 15),
    "迷雾狼": ("twilightforest:mist_wolf", 13),
    "国王蜘蛛": ("twilightforest:king_spider", 12),
    "粘液甲虫": ("twilightforest:slime_beetle", 12),
    "烈焰人": ("blaze", 10),
    "深潜者": ("alexscaves:deep_one", 10),
    "凋零骷髅": ("wither_skeleton", 8),
    "巨钳甲虫": ("twilightforest:pinch_beetle", 7),
    "流浪者": ("stray", 9),
    "阔鼻迅猛龙": ("alexscaves:vallumraptor", 8),
    "骷髅": ("skeleton", 8),
    "喷火甲虫": ("twilightforest:fire_beetle", 6),
    "死灵书": ("twilightforest:death_tome", 5),
    "骷髅德鲁伊": ("twilightforest:skeleton_druid", 5)
}


def send_command(command):
    """发送游戏指令"""
    try:
        pyautogui.keyDown('/')
        pyautogui.keyUp('/')
        time.sleep(0.1)
        pyautogui.typewrite(command, interval=0.01)
        pyautogui.press('enter')
        print(f"发送指令: {command[:50]}...")
        time.sleep(DELAY_BETWEEN_COMMANDS)
        return True
    except Exception as e:
        print(f"发送指令失败: {str(e)}")
        return False


def parse_lineup(lineup_str, is_team_a=True):
    """解析阵容字符串为召唤指令列表"""
    commands = []
    if not lineup_str:
        return commands

    for monster in lineup_str.split(','):
        try:
            clean_str = monster.strip().replace('：', ':')  # 将全角冒号统一为半角
            name, count = clean_str.split(':', maxsplit=1)  # 用半角冒号分割
            count = int(count)
            mob_id, _ = MONSTER_DATA.get(name, (None, None))

            if not mob_id:
                print(f"警告: 未知怪物 '{name}'，跳过")
                continue

            # 生成召唤指令，分配不同坐标避免重叠
            for i in range(count):
                x = -55 if is_team_a else -75
                z = -15 + (i % 10)
                y = 201 + (i // 10)
                commands.append(f"summon {mob_id} {x} {y} {z}")

        except Exception as e:
            print(f"解析阵容错误: {str(e)}，格式应为'怪物名称:数量'")

    return commands


def load_test_cases():
    """加载测试阵容配置文件"""
    test_cases = []
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8-sig') as f:  # 使用utf-8-sig避免BOM问题
            reader = csv.DictReader(f)
            for row in reader:
                test_cases.append({
                    "id": row["测试ID"],
                    "a_team": row["A队阵容"],
                    "b_team": row["B队阵容"],
                    "note": row["测试备注"]
                })
        print(f"成功加载 {len(test_cases)} 个测试用例")
        return test_cases
    except Exception as e:
        print(f"加载配置文件失败: {str(e)}")
        return []


def monitor_log():
    """监控日志文件获取战斗结果"""
    results = {"a_alive": False, "b_alive": False}
    start_time = time.time()

    try:
        with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, os.SEEK_END)  # 移动到文件末尾

            while time.time() - start_time < 20:  # 监控60秒
                line = f.readline()
                if line:
                    if "AAAA" in line:
                        results["a_alive"] = True
                    if "BBBB" in line:
                        results["b_alive"] = True
                time.sleep(0.1)

        return results
    except Exception as e:
        print(f"监控日志失败: {str(e)}")
        return results


def run_test_case(test_case):
    """运行单个测试用例"""
    print(f"\n======= 测试用例 {test_case['id']} =======")
    print(f"备注: {test_case['note']}")

    # 初始化竞技场
    send_command("fill -31 167 -20 -31 167 -20 minecraft:redstone_block")
    time.sleep(2)

    # 召唤A队
    a_commands = parse_lineup(test_case["a_team"], is_team_a=True)
    print(f"\n发送A队指令 ({len(a_commands)}个单位)")
    for cmd in a_commands:
        send_command(cmd)

    # 召唤B队
    b_commands = parse_lineup(test_case["b_team"], is_team_a=False)
    print(f"\n发送B队指令 ({len(b_commands)}个单位)")
    for cmd in b_commands:
        send_command(cmd)

    # 开始战斗
    send_command("fill -40 167 -27 -40 167 -27 minecraft:redstone_block")
    print(f"\n战斗开始，持续 {BATTLE_DURATION} 秒...")

    # 战斗倒计时
    for i in range(BATTLE_DURATION, 0, -1):
        mins, secs = divmod(i, 60)
        print(f"剩余时间: {mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)

    # 结束战斗并监控结果
    send_command("fill -42 167 -25 -42 167 -25 minecraft:redstone_block")
    print("\n战斗结束，监控结果...")
    results = monitor_log()

    # 记录结果
    result_str = f"## 测试用例 {test_case['id']} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    result_str += f"- 测试备注: {test_case['note']}\n"
    result_str += f"- A队阵容: {test_case['a_team']}\n"
    result_str += f"- B队阵容: {test_case['b_team']}\n"
    result_str += f"- A队存活: {results['a_alive']}\n"
    result_str += f"- B队存活: {results['b_alive']}\n"
    if results["a_alive"] and results["b_alive"]:
        result_str += "- 战斗结果: 平局\n"
    else:
        result_str += f"- 战斗结果: {'A队获胜' if results['a_alive'] else 'B队获胜'}\n"
    result_str += "\n"

    with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
        f.write(result_str)

    if results["a_alive"] and results["b_alive"]:
        print("\n测试结果: 平局")
    else:
        print(f"\n测试结果: {'A队存活' if results['a_alive'] else 'B队存活'}")
    return results


def main():
    print("=== 自动竞技场批量测试工具 ===")

    # 检查配置文件
    if not os.path.exists(CONFIG_FILE):
        print(f"错误: 配置文件 '{CONFIG_FILE}' 不存在")
        return

    # 加载测试用例
    test_cases = load_test_cases()
    if not test_cases:
        print("没有加载到测试用例")
        return

    # 初始化结果文件，使用追加模式
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# 竞技场批量测试结果\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"测试用例数量: {len(test_cases)}\n\n")
    else:
        with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"### 新的测试开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"测试用例数量: {len(test_cases)}\n\n")

    # 切换到游戏窗口
    print(f"\n请在 {INIT_DELAY} 秒内切换到游戏窗口...")
    for i in range(INIT_DELAY, 0, -1):
        print(f"倒计时: {i}秒", end="\r")
        time.sleep(1)

    # 解除暂停
    pyautogui.press('esc')
    time.sleep(1)

    # 执行所有测试用例
    for idx, case in enumerate(test_cases, 1):
        run_test_case(case)

    print("\n======= 测试完成 =======")
    print(f"结果已保存到: {os.path.abspath(RESULTS_FILE)}")


if __name__ == "__main__":
    try:
        import pyautogui
    except ImportError:
        print("错误: 未安装pyautogui，请执行: pip install pyautogui")
        input("按Enter键退出...")
        exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序错误: {str(e)}")
    finally:
        input("按Enter键退出...")