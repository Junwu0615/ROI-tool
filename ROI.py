import sys
import os
from Hyper_parameters import hyper_parameters
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.font_manager


def strofsize(num, level):
    if level >= 2:
        return num, level
    elif num >= 10000:
        num /= 10000
        level += 1
        return strofsize(num, level)
    else:
        return num, level


def change(num):
    units = ['', '萬', '億']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 2), units[level])


def Interest(now_year):
    interest = now_year * (ROI * 0.01)  # 報酬
    return interest


def Now_year_ROI(now_year):
    now_year_ROI = now_year + Interest(now_year)  # 今年投資金+ROI
    return now_year_ROI


def png(year_type, value_1, value_2, value_3):
    plt.xlabel("歲數")
    plt.ylabel("萬")
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    plt.grid(True)
    if year_type == "工作年":
        plt.plot(df_1[year_type], df_1[value_1])
        plt.legend([value_1], loc="upper left")
    else:
        plt.plot(df_2[year_type], df_2[value_1])
        plt.plot(df_2[year_type], df_2[value_2])
        plt.legend([value_1, value_2], loc="upper left")
    plt.title(value_3)
    plt.savefig("result/"+ value_3 + ".png")
    plt.clf()


if __name__ == '__main__':

    work_year = hyper_parameters.work_year  # 只想要工作多久
    year = hyper_parameters.year  # 年齡
    dead = hyper_parameters.dead  # 想活到幾歲
    money_month = hyper_parameters.money_month  # 每月能投入股市資金
    ROI = hyper_parameters.ROI  # 投資報酬率
    object_num = hyper_parameters.object_num  # 預期想要達成金額
    money_once = hyper_parameters.money_once  # 一次性金額，如沒填0
    money_year = money_month * 12  # 每年要投入股市資金
    break_life = dead - (year + work_year)  # 退休還能活幾年

    isExists_file = os.path.exists('./result')
    if not isExists_file:
        os.makedirs('./result')
    result_txt = open('result/ROI_result.txt', 'a')
    result_txt.truncate(0)
    sys.stdout = result_txt

    print("==============================================")
    print("複利效應是你的好朋友")
    print("==============================================")
    print("投資報酬率: " + str(ROI) + "%")
    print("期望工作" + str(work_year) + "年後，就退休")
    print("每月能存多少，並投入股市資金: " + str(change(money_month)) + " (NTD)")
    print("到年底，總共要投入股市資金: " + str(change(money_year)) + " (NTD)")
    print("第一次投入股市，額外加碼: " + str(change(money_once)) + " (NTD)")
    print("預期活到: " + str(dead) + "歲")
    print(str(year) + "歲開始工作至老死，剩餘壽命尚有: " + str(dead - year) + "年")
    print("最終期望達成金額: " + str(change(object_num)) + " (NTD)")
    print()
    print("==============================================")

    now_year = money_year
    interest_each_year = []
    count_year = 1
    record_y_1_count = 0
    record_y_2_count = 0
    money_sum = money_year + money_once
    ALL_money_year = [money_sum]

    # 生成走勢圖
    data = [[], [], [], [], []]

    while count_year <= work_year + 1: # 複利滾的時間，之後退休

        if count_year == 1:
            money_sum = now_year + money_once
            now_year = money_sum

        now_year_ROI = Now_year_ROI(now_year)
        now_year_ROI = now_year_ROI + money_year
        interest = Interest(now_year)

        now_year = now_year_ROI
        # print(now_year_ROI)

        ALL_money_year.append(now_year_ROI)  # 歷年會賺到的錢
        # print(ALL_money_year) #歷年投入的本金&本金產生的利息之加總

        now_cost = (money_year * count_year) + money_once

        print("* 到目前為止投入成本有: %s" % change(now_cost))
        print("* 到目前為止獲得報酬有: %s" % change(ALL_money_year[-2] - now_cost))
        print("* 投資報酬率%s" % ROI + "%")

        if year == (year + work_year): # 退休年
            print("### 今年%s歲，退休年! ###" % year)
        else:
            print("* 今年%s歲" % year)
        print()

        data[0].append(year)

        if count_year == 1:
            money_sum = money_year + money_once
            print("  第" + str(count_year) + "年  投資金額有: %s" % change(money_sum))
            print()
            print("### 第一年投入尚無漲幅，需長期等待 ###")
            print("   -到目前為止，累積總資金約 %s" % change(money_sum))
            print()
        else:
            print("  第" + str(count_year) + "年  投資金額有: %s" % change(money_year))
            print()
            print("   -隔年，對比今年賺到差額: %s" % (change(Interest(ALL_money_year[-1]) - Interest(ALL_money_year[-2]))))
            print("   -今年，對比去年所賺到差額: %s" % (change(Interest(ALL_money_year[-2]) - Interest(ALL_money_year[-3]))))
            print()
            print("   -到目前為止，累積總資金約 %s" % change(ALL_money_year[-2]))
            print()
        year += 1
        data[2].append(ALL_money_year[-2])
        interest_each_year.append(interest)  # 每年利息報酬率，計入

        if now_cost < ALL_money_year[-2] - now_cost:  # 投入的本金在第幾年後回本
            record_y_1 = count_year
            record_y_1_count += 1

        if record_y_1_count == 1:
            print("### 第" + str(record_y_1) + "年，到目前為止獲得的報酬，已超過投入的本金 ###")

        if object_num < ALL_money_year[-2]:  # 第幾年後會達成當初設定的目標
            record_y_2 = count_year
            record_y_2_count += 1

        if record_y_2_count == 1:
            print("### 第" + str(record_y_2) + "年，達成當初所設立的目標金額: " + str(object_num) + " ###")

        count_year += 1
        print("==============================================")

    year -= 1  # 年齡數字校正

    # 當退休後，計算被動收入
    for b_life in range(1, break_life + 1):
        print("==============================================")

        if b_life == 1:
            now_year = ALL_money_year[-2]
        else:
            now_year = now_year * 1.15
            interest = Interest(now_year)
            ALL_money_year.append(now_year)
            interest_each_year.append(interest)

        print("* 今年%s歲" % year)
        print("資金運用之方案一: 被動收入")
        print("### 退休後，被動收入經換算後...每年 %s / 每月 %s / 每天 %s ###"
              % (change(interest_each_year[-2]), change(interest_each_year[-2] / 12),
                 change(interest_each_year[-2] / 12 / 30)))
        print("### 如果只領利息，不賣本，前提是ROI還是穩定維持下去 ###")
        print()
        print("資金運用之方案二: 提領出來")

        if b_life == 1:
            print("### 而一次提領約有: %s ###"
                  % (change(ALL_money_year[-2])))
            print("### 還能活%s年，換算...每年能花 %s元 / 每月能花 %s元 / 每日能花 %s元 ###"
                  % (change(break_life), change(ALL_money_year[-2] / break_life),
                     change(ALL_money_year[-2] / break_life / 12), change(ALL_money_year[-2] / break_life / 12 / 30)))

            data[3].append(interest_each_year[-2])
            data[4].append(ALL_money_year[-2])
        else:
            print("### 而一次提領約有: %s ###"
                  % (change(ALL_money_year[-1])))
            print("### 還能活%s年，換算...每年能花 %s元 / 每月能花 %s元 / 每日能花 %s元 ###"
                  % (change(break_life), change(ALL_money_year[-1] / break_life),
                     change(ALL_money_year[-1] / break_life / 12), change(ALL_money_year[-1] / break_life / 12 / 30)))

            data[3].append(interest_each_year[-2])
            data[4].append(ALL_money_year[-1])

        data[1].append(year)
        break_life -= 1
        year += 1
        print("==============================================")

    # 生成走勢圖
    df_1 = pd.DataFrame({"工作年": data[0], "累積總資金": data[2]})
    df_2 = pd.DataFrame({"休息年": data[1], "每年退休後被動收入": data[3], "提領出來": data[4]})
    # print(df_1)
    print(df_2)

    png("工作年", "累積總資金", "無", "工作年-每年定存再投入之總資金成長走勢")
    png("休息年", "提領出來", "每年退休後被動收入", "休息年-每年退休後被動收入&提領出來之成")
    #path = matplotlib.matplotlib_fname()
    #print(path)