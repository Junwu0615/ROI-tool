import sys

##超參數
work_year = 34 #只想要工作多久
year = 26 #年齡
dead = 95 #想活到幾歲
money_month = 12 #每月能投入股市資金
ROI = 15 #投資報酬率
object_num = 30000000 #預期想要達成金額
money_once = 0 #一次性金額，如沒填0
##
run = work_year #複利滾的時間，之後退休
money_year = money_month*12 #每年要投入股市資金
alive = dead-year #還可以活多久
break_year = year + work_year #退休年
break_life = dead - (year + work_year) #退休還能活幾年

result_txt = open('result/ROI_result.txt','a')
result_txt.truncate(0)
sys.stdout = result_txt
print("==============================================")
print("複利效應是你的好朋友")
print("==============================================")

print("投資報酬率: " + str(ROI) + "%")
print("期望工作" + str(work_year)+ "年後，就退休")
print("每月能存多少，並投入股市資金: " + str(money_month)+ " (NTD)")
print("到年底，總共要投入股市資金: " + str(money_year)+ " (NTD)")
print("第一次投入股市，額外加碼: " + str(money_once)+ " (NTD)")
print("預期活到: " + str(dead)+ "歲")
print(str(year)+"歲開始工作至老死，剩餘壽命尚有: " + str(alive)+ "年")
print("最終期望達成金額: " + str(object_num)+ " (NTD)")
print("\n")
print("==============================================")

now_year = money_year
interest_each_year = []
record_num = []
count_year = 1
record_y_1_count = 0
record_y_2_count = 0
money_sum = money_year + money_once
ALL_money_year = [money_sum]

while count_year <= run+1:
    
    def Interest(now_year):
        interest = now_year * (ROI*0.01) #報酬
        return interest
    
    def Now_year_ROI(now_year):
        now_year_ROI = now_year + Interest(now_year) #今年投資金+ROI
        return now_year_ROI
    

    now_cost = money_year*count_year
    now_cost = now_cost + money_once
    
    ALL_money_sum = 0
    for before in ALL_money_year:
        ALL_money_sum = ALL_money_sum + before
    
    print("* 到目前為止投入成本有: %d" %now_cost)
    print("* 到目前為止獲得報酬有:  %d" %round(ALL_money_sum-now_cost,0))
    print("* 投資報酬率%d" %ROI+"%")
    if year == break_year:
        print("### 今年%d歲，退休年! ###" %year)
    else:
        print("* 今年%d歲" %year)
    print()
    if count_year == 1:
        money_sum = money_year + money_once
        print("  第"+str(count_year)+"年  投資金額有: %d" %round(money_sum,0))
        print()
    else:
        print("  第"+str(count_year)+"年  投資金額有: %d" %round(money_year,0))
        print()
    
    year += 1
    
    if count_year == 1:
        money_sum = now_year + money_once
        now_year_ROI = Now_year_ROI(money_sum)
        now_year_ROI = now_year_ROI + money_year
        interest = Interest(money_sum)
    else:
        now_year_ROI = Now_year_ROI(now_year)
        now_year_ROI = now_year_ROI + money_year
        interest = Interest(now_year)
        
    now_year = now_year_ROI
    
    if count_year == 1:
        record_num.append(Interest(ALL_money_sum))
        record_num_2 = record_num
        print("### 第一年投入尚無漲幅，需長期等待 ###")
    else:
        print("   -隔年，對比今年賺到差額: %d" %(round(Interest(ALL_money_sum)-record_num[-1],0)))
        if count_year > 2:
            print("   -今年，對比去年所賺到差額: %d" %(round(record_num[-1]-record_num[-2],0)))
        record_num.append(Interest(ALL_money_sum))
        print()
        
    print("   -到目前為止，累積總資金約 %s" %round(ALL_money_sum,0))
    print()
    
    ALL_money_year.append(now_year_ROI) #歷年會賺到的錢
    #print(ALL_money_year) #歷年投入的本金&本金產生的利息之加總
    interest_each_year.append(interest) #每年利息報酬率，計入
    #print(interest_each_year)

    #interest_sum = 0
    #for count in interest_each_year:
    #    interest_sum = interest_sum + count #目前為止報酬率加總
    #print(interest_sum)
    
    
    if now_cost < ALL_money_sum-now_cost: #投入的本金在第幾年後回本
        record_y_1 = count_year
        record_y_1_count += 1
    
    if record_y_1_count == 1:
        print("### 第"+str(record_y_1)+"年，到目前為止獲得的報酬，已超過投入的本金 ###")
    
    if object_num < ALL_money_sum: #第幾年後會達成當初設定的目標
        record_y_2 = count_year
        record_y_2_count += 1
    
    if record_y_2_count == 1:  
        print("### 第"+str(record_y_2)+"年，達成當初所設立的目標金額: "+str(object_num)+" ###")
    
    print("==============================================")
    count_year += 1
    
    
interest_end = interest_each_year[-2]    
year -= 1 #年齡數字校正
now_year = ALL_money_sum
#當退休後，計算被動收入
for b_life in range(1,break_life+1):
    print("==============================================")
    if b_life == 1:
        print("* 今年%d歲" %year)
        print("### 退休後，被動收入經換算後...每年 %d / 每月 %d / 每天 %d ###" 
              %(round(interest_end,0),round(interest_end/12,0),round(interest_end/12/30,0)))
        print("### 如果只領利息，不賣本，每年都還會繼續增幅，前提是ROI還是穩定維持下去 ###")
        print()
        print("### 一次提領約有: %d ###" 
              %(round(ALL_money_sum,0)))
        print("### 還能活%d年，換算...每年能花 %d元 / 每月能花 %d元 / 每日能花 %d元 ###" 
              %(round(break_life,0),round(ALL_money_sum/break_life,0),
                round(ALL_money_sum/break_life/12,0),round(ALL_money_sum/break_life/12/30,0)))
    else:
        print("* 今年%d歲" %year)
        print("### 退休後，被動收入經換算後...每年 %d / 每月 %d / 每天 %d ###" 
              %(round(interest_end,0),round(interest_end/12,0),round(interest_end/12/30,0)))
        print("### 如果只領利息，不賣本，每年都還會繼續增幅，前提是ROI還是穩定維持下去 ###")
        print()
        print("### 一次提領約有: %d ###" 
              %(round(ALL_money_sum,0)))
        print("### 還能活%d年，換算...每年能花 %d元 / 每月能花 %d元 / 每日能花 %d元 ###" 
              %(round(break_life,0),round(ALL_money_sum/break_life,0),
                round(ALL_money_sum/break_life/12,0),round(ALL_money_sum/break_life/12/30,0)))
        
    now_year = Now_year_ROI(now_year)
    interest = Interest(now_year)
    
    ALL_money_sum = 0
    for before in ALL_money_year:
        ALL_money_sum = ALL_money_sum + before
        
    interest_each_year.append(interest)
    interest_end = interest_each_year [-2]
    
    break_life -= 1
    year += 1
    print("==============================================")