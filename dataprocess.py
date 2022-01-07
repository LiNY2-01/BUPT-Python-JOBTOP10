# %% [markdown]
# ## 数据预处理

# %%
import pandas as pd
import numpy as np
XDUdf = pd.read_csv('./XIDIAN_ok.csv', sep=',',
                    header=0, encoding='utf-8')
BUPTdf = pd.read_csv('./BEIYOU_ok.csv', sep=',',
                    header=0, encoding='utf-8')
UESTCdf = pd.read_csv('./CHENGDIAN_ok.csv', sep=',',
                     header=0, encoding='utf-8')

def pre_handle(jobdf):
    for index, row in jobdf.iterrows():
        jobdf.loc[index, 'job_title'] = row['job_title'].strip(' \n\t-。.')
        #去除不必要字符
pre_handle(XDUdf)
pre_handle(BUPTdf)
pre_handle(UESTCdf)


# %% [markdown]
# ### 排序和去重

# %%
def del_repet(jobdf,school_cnt=False):
    jobdf=jobdf.sort_values(['job_title'], ascending=False)
    jobdf=jobdf.reset_index(drop=True)
    #排序，按名称排序，第二关键字是时间升序
    now_title=''
    now_index=-1
    for index, row in jobdf.iterrows():
        if row['job_title']!=now_title:
            now_index=index
            now_title=row['job_title']
        else:       
            jobdf.loc[now_index,'job_views'] += row['job_views']
            if school_cnt:
                jobdf.loc[now_index, 'school_cnt'] += row['school_cnt']
            jobdf.drop(index, inplace=True)
    return jobdf
    #去重算法，相同帖子访问量累加
XDUdf=del_repet(XDUdf)
BUPTdf=del_repet(BUPTdf)
UESTCdf=del_repet(UESTCdf)
mergeddf=pd.concat([XDUdf,BUPTdf.drop('job_nums',axis=1),UESTCdf],axis=0,ignore_index=True)
mergeddf.insert(3, 'school_cnt',1)
mergeddf=del_repet(mergeddf,school_cnt=True)


# %% [markdown]
# ## 数据合并

# %%

JOBmerged = pd.ExcelWriter('./JOBmerged.xlsx', engine="openpyxl")
workbook = JOBmerged.book
XDUdf.index.name = "序号"
BUPTdf.index.name = "序号"
UESTCdf.index.name = "序号"
mergeddf.index.name = "序号"
XDUdf.columns = ["招聘主题", "发布时间", "关注度（浏览次数）"]
BUPTdf.columns = ["招聘主题", "发布时间", "关注度（浏览次数）","职位个数"]
UESTCdf.columns = ["招聘主题", "发布时间", "关注度（浏览次数）"]
mergeddf.columns = ["招聘主题", "发布时间", "关注度（浏览次数）","学校计数"]

BUPTdf.to_excel(JOBmerged, sheet_name='北邮', encoding='GB2312')
XDUdf.to_excel(JOBmerged, sheet_name='西电', encoding='GB2312')

UESTCdf.to_excel(JOBmerged, sheet_name='成电', encoding='GB2312')
mergeddf.to_excel(JOBmerged, sheet_name='分类', encoding='GB2312')
JOBmerged.save()


# %% [markdown]
# ## 得出TOP榜单

# %%
JOBanalysis = pd.ExcelWriter('./JOBanalysis.xlsx', engine="openpyxl")

XDUdf = XDUdf.sort_values(['关注度（浏览次数）'], ascending=False).head(20)
UESTCdf=UESTCdf.sort_values(['关注度（浏览次数）'],ascending=False).head(20)
BUPT_TOP20viewdf = BUPTdf.sort_values(['关注度（浏览次数）'], ascending=False).head(20)
BUPT_TOP10numdf = BUPTdf.sort_values(['职位个数'], ascending=False).head(10)
mergeddf=mergeddf[mergeddf['学校计数'] == 3]

XDUdf = XDUdf.reset_index(drop=True)
BUPT_TOP20viewdf = BUPT_TOP20viewdf.reset_index(drop=True)
BUPT_TOP10numdf = BUPT_TOP10numdf.reset_index(drop=True)
UESTCdf = UESTCdf.reset_index(drop=True)
mergeddf = mergeddf.reset_index(drop=True)


workbook = JOBanalysis.book
BUPT_TOP20viewdf.to_excel(JOBanalysis, sheet_name='北邮0', encoding='GB2312')
BUPT_TOP10numdf.to_excel(JOBanalysis, sheet_name='北邮1', encoding='GB2312')
XDUdf.to_excel(JOBanalysis, sheet_name='西电', encoding='GB2312')
UESTCdf.to_excel(JOBanalysis, sheet_name='成电', encoding='GB2312')
mergeddf.to_excel(JOBanalysis, sheet_name='三校', encoding='GB2312')

XDUsheet = workbook['西电']
XDUsheet.insert_rows(1)
XDUsheet['A1'].value = "最受西电学生关注的招聘TOP20"
XDUsheet.merge_cells("A1:D1")

BUPT_TOP20viewsheet = workbook['北邮0']
BUPT_TOP20viewsheet.insert_rows(1)
BUPT_TOP20viewsheet['A1'].value = "最受北邮学生关注的招聘TOP20"
BUPT_TOP20viewsheet.merge_cells("A1:E1")


BUPT_TOP10numdfsheet = workbook['北邮1']
BUPT_TOP10numdfsheet.insert_rows(1)
BUPT_TOP10numdfsheet['A1'].value = "北邮招聘职位数量TOP10"
BUPT_TOP20viewsheet.merge_cells("A1:E1")


UESTCsheet = workbook['成电']
UESTCsheet.insert_rows(1)
UESTCsheet['A1'].value = "最受成电学生关注的招聘TOP20"
UESTCsheet.merge_cells("A1:D1")

mergedsheet = workbook['三校']
mergedsheet.insert_rows(1)
mergedsheet['A1'].value = "在三校均发布招聘信息的雇主"
mergedsheet.merge_cells("A1:E1")

JOBanalysis.save()



