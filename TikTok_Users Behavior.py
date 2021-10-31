
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pandas import to_datetime

data = pd.read_csv('douyin_data.txt', names=['uid','user_city','item_id','author_id', 'item_city', 'channel','finish','like','music_id','source','time','duration_time'], skiprows=1, sep='\t')


data[data == -1] = np.nan
data.dropna(how='any',inplace=True)
#缺省值清洗

data = data.drop_duplicates()
#重复值处理

data.time = data.time.map(lambda x: str(x).lstrip('5'))
data.time = pd.to_datetime(data.time, unit='s')
#数据格式处理

data['viewcount'] = data.groupby('item_id')['item_id'].transform('count')
data['likerate'] = data.groupby('like')['like'].transform(lambda x: (100*x.sum()/x.count()))
data['finishrate'] = data.groupby('finish')['finish'].transform(lambda x: (100*x.sum()/x.count()))


data_time_finish_like = data.groupby('duration_time').mean()[['finish','like']].sort_index()
y_finish = data_time_finish_like.sort_index()['finish']
y_liked = data_time_finish_like.sort_index()['like']
x_f_l = data_time_finish_like.index
date_musicId = data.groupby('music_id').mean()[['finish','like']].sort_index()
x_musicid = date_musicId.index


fig,axl = plt.subplots(figsize=(12,6))
color = 'tab:red'
axl.set_title('Duration time VS Finished rate VS Liked Rate ')
axl.set_xlabel('duration time/s')
axl.set_ylabel('Finished rate',color = color)
axl.plot(x_f_l,y_finish,color = color)
axl.tick_params(axis = 'y',labelcolor = color)

ax2 = axl.twinx()
color  = 'tab:blue'
ax2.set_ylabel('Liked Rate',color = color)
ax2.plot(x_f_l,y_liked,color = color)
ax2.tick_params(axis = 'y',labelcolor = color)
fig.tight_layout()
plt.show()
#作品时长和完播率，点赞率的关系



data_dailyviewcount = data.groupby('time').count()['item_id']
x = data_dailyviewcount.index
y = data_dailyviewcount.values
plt.plot(x,y)
plt.show()
#全平台每日总播放量变化

data_dailyuser = data.groupby('time').nunique()['uid']
x1 = data_dailyuser.index
y1 = data_dailyuser.values
plt.plot(x1,y1)
plt.show()
#全平台每日用户数变化

data_dailyproducer = data.groupby('time').nunique()['author_id']
x2 = data_dailyproducer.index
y2 = data_dailyproducer.values
plt.plot(x2,y2)
plt.show()
#全平台每日制作者变化


data_authrocontribute = data.groupby('author_id').count()['item_id']
x3 = data_authrocontribute.index
y3 = data_authrocontribute.values
plt.plot(x3,y3)
plt.show()
#各个作者为平台贡献的总播放数