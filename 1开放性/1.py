import pandas as pd
import datetime
import numpy as np




# 计算函数
# 读入用户的数据集
order_items = pd.read_csv("../inputdata/jdata_user_order.csv")
# 读取被选择的用户
action_data = pd.read_csv('../inputdata/jdata_user_action.csv')
action_data = action_data.dropna(axis=0)
items=pd.read_csv("../inputdata/jdata_sku_basic_info.csv")
action_items = pd.merge(action_data, items,how='left',on=['sku_id'])
order_items=pd.merge(order_items,items,how='left',on=['sku_id'])


starttime = datetime.datetime.now()
print('开始时间：',starttime)

# 用户所有购买会话的转移度
for uid,group in order_items.groupby('user_id'):
    print(uid)
    # 找到交互记录
    auid=action_items[action_items['user_id']==uid]
    # 首先找到用户的记录
    for date, group2 in group.groupby('date'):
        # 当天的所有浏览记录
        thisdateBro = auid[(auid['a_date']== date)] 
        # 总共浏览次数
        allBroswing = thisdateBro['a_num'].sum()
        # 今天购买的商品的所有种类   
        allCate = group2['cate'].unique() 
        # 记录用户当前会话会话购买的商品的浏览次数
        count = 0 
        # 总共浏览次数
        for cate in allCate: 
            count=count+thisdateBro[thisdateBro['cate'] == cate]['a_num'].sum()  # 购买商品的浏览次数
        temp=(count+1)/(allBroswing+1)
        order_items.loc[(order_items['user_id'] == uid)
                    & (order_items['date'] == date),'k1'] = temp
endtime = datetime.datetime.now()
print('结束时间：',endtime)
print('运行时间：',(endtime - starttime).seconds)
    
order_items.to_csv(path_or_buf="../outputdata/dataNaTemp.csv",header=True,index=False)  