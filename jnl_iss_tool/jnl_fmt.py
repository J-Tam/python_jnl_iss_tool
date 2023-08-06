# coding: UTF-8
import pandas as pd
from pandas import DataFrame
from pandas import Series
import math
import datetime as dt
import numpy as np
from tkinter import filedialog as fd

from jnl_iss_tool.main_bean import MainBean
import jnl_iss_tool.const as const

class JnlFmt():
    def __init__(self):
        self.df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': []})
        self.path_save = fd.askdirectory(title='保存先を選択')
        self.rgstr_dt = dt.date.today()

    def get_path_save_jnl(self, jnl_nm) -> str:
        path_save_jnl = self.path_save + '/' + jnl_nm + '_' + self.rgstr_dt.strftime('%Y-%m-%d') + '.csv'
        return path_save_jnl

    def mk_jnl(
              self
            , main_bean: MainBean
            , df_jnl_xfr_exc: DataFrame
            , path_save: str
    ):
        return

class YayoiJnlFmt(JnlFmt):
    def __init__(self):
        super().__init__()
        self.df_tmpl = pd.DataFrame({'*識別フラグ(4)': [], '伝票No.(6)': [], '決算(4)': [], '*取引日付(10)': [], '*借方勘定科目(24)': [], '借方補助科目(24)': [], '借方部門(24)': [], '*借方税区分(-)': [], '*借方金額(11)': [], '借方税金額(11)': [], '*貸方勘定科目(24)': [], '貸方補助科目(24)': [], '貸方部門(24)': [], '*貸方税区分(-)': [], '*貸方金額(11)': [], '貸方税金額(11)': [], '摘要(64)': [], '番号(10)': [], '期日(10)': [], '*タイプ(1)': [], '生成元(4)': [], '仕訳メモ(180)': [], '付箋1(1)': [], '付箋2(1)': [], '*調整()': []})

    def get_id_flg(self, row: Series):
        
        id_flg = '0'
        
        if row['本仕訳フラグ'] == True:

            if row['為替差損益'] == 0:
                id_flg = '2111'
            
            else:
                id_flg = '2110'
        
        else:
            id_flg = '2101'

        return id_flg

    def mk_jnl(
              self
            , main_bean: MainBean
            , df_jnl_xfr_exc: DataFrame
            , path_save: str
    ):

        df_dst = self.df_tmpl.copy()

        for index, row in df_jnl_xfr_exc.iterrows():
        
            if row['借方金額'] == 0 and row['貸方金額'] == 0:
                continue 

            df_tmp = pd.DataFrame(
                {
                  '*識別フラグ(4)': [self.get_id_flg(row)]
                , '伝票No.(6)': [row['seq']]
                # , '決算(4)': []
                , '*取引日付(10)': [row['日付']]
                , '*借方勘定科目(24)': [row['借方勘定科目']]
                , '借方補助科目(24)': [row['借方補助科目']]
                # , '借方部門(24)': []
                , '*借方税区分(-)': [const.TAX_TYPE_TAISHOGAI]
                , '*借方金額(11)': [row['借方金額']]
                , '借方税金額(11)': [0]
                , '*貸方勘定科目(24)': [row['貸方勘定科目']]
                , '貸方補助科目(24)': [row['貸方補助科目']]
                # , '貸方部門(24)': []
                , '*貸方税区分(-)': [const.TAX_TYPE_TAISHOGAI]
                , '*貸方金額(11)': [row['貸方金額']]
                , '貸方税金額(11)': [0]
                , '摘要(64)': [row['摘要']]
                # , '番号(10)': []
                # , '期日(10)': []
                , '*タイプ(1)': [0]
                # , '生成元(4)': []
                # , '仕訳メモ(180)': []
                # , '付箋1(1)': []
                # , '付箋2(1)': []
                , '*調整()': ['no']
                }
            )

            df_dst = pd.concat([df_dst, df_tmp], axis=0)

        df_dst.to_csv(path_or_buf=path_save, index=False, header=False, encoding='shift_jis')

        return



#     def mk_jnl_bnk_usd(
#               self
#             , main_bean: MainBean
#             , df_bnk_daw_usd: DataFrame
#             , df_rate: DataFrame
#             , jnl_nm: str
#     ):

#      # 入金明細gain
#         df_dep_usd = common_service.get_df_dep_usd(main_bean, df_bnk_daw_usd, df_rate)

#         # 出金明細を取得
#         df_wit_usd = common_service.get_df_wit_usd(df_bnk_daw_usd, df_rate, content)

#         df_dst = self.df_tmpl.copy()

#         for index, row_wit in df_wit_usd.iterrows():

#             df_dep_calc_tgt = common_service.get_df_dep_calc_tgt(row_wit, df_dep_usd)
            
#             df_calc_bnk_2_stk = common_service.get_df_xfr_bnk_2_stk(row_wit, df_dep_calc_tgt)

#             print(df_calc_bnk_2_stk)

#             exc_diff_bean = common_bean.ExcDiffBean()
#             exc_diff_bean.getExcDiff(df_calc_bnk_2_stk.at[0,'為替差損益'])

#             acct_bean = common_bean.AcctBeanBnkUsd()
#             acct_bean.set_acct_nm(df_calc_bnk_2_stk.at[0,'内容'])

#             seq = index + 1

#             df_tmp = pd.DataFrame(
#                 {
#                 '*識別フラグ(4)': ['2110', '2101']
#                 , '伝票No.(6)': [seq, seq]
#                 # , '決算(4)': []
#                 , '*取引日付(10)': [str(row_wit['日付']).replace('/', ''), str(row_wit['日付']).replace('/', '')]
#                 , '*借方勘定科目(24)': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
#                 , '借方補助科目(24)': [main_bean.bnk_usd.bnk_nm.value,'']
#                 # , '借方部門(24)': []
#                 , '*借方税区分(-)': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '*借方金額(11)': [df_calc_bnk_2_stk.at[0, '出金金額(円)_当日レート基準'], exc_diff_bean.loss_amt]
#                 , '借方税金額(11)': [0, 0]
#                 , '*貸方勘定科目(24)': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
#                 , '貸方補助科目(24)': [main_bean.bnk_jpy.bnk_nm.value, '']
#                 # , '貸方部門(24)': []
#                 , '*貸方税区分(-)': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '*貸方金額(11)': [df_calc_bnk_2_stk.at[0, '入金金額(円)_当日レート基準'], exc_diff_bean.profit_amt]
#                 , '貸方税金額(11)': [0, 0]
#                 , '摘要(64)': ['', '']
#                 # , '番号(10)': []
#                 # , '期日(10)': []
#                 , '*タイプ(1)': [0, 0]
#                 # , '生成元(4)': []
#                 # , '仕訳メモ(180)': []
#                 # , '付箋1(1)': []
#                 # , '付箋2(1)': []
#                 , '*調整()': ['no', 'no']
#                 }
#             , index=['main', 'pol']
#             )

#             # 為替差損益 = 0 の場合は為替差損益明細を削除
#             if int(df_calc_bnk_2_stk.at[0,'為替差損益']) == 0:
#                 df_tmp.drop('pol', axis=0, inplace=True)

#             df_dst = pd.concat([df_dst, df_tmp], axis=0)

#         df_dst = df_dst.sort_index().sort_values(['取引日'])
#         df_dst = df_dst.reset_index(drop=True)        

#         df_dst.to_csv(path_or_buf=jnl_save_path, index=False, header=False, encoding='shift_jis')

#     def mk_jnl_buy_asset(
#               self
#             , main_bean: MainBean
#             , df_bnk_daw_usd: DataFrame
#             , df_stk_daw_fgn: DataFrame
#             , df_stk_tr_hist: DataFrame
#             , df_rate: DataFrame
#     ):
        
#         df_dst = self.df_tmpl.copy()
        
#         content = '振替　ＳＢＩ証券'

#         df_bnk_wit_usd = common_service.get_df_wit_usd(df_bnk_daw_usd, df_rate, content)
#         df_bnk_wit_usd = df_bnk_wit_usd.sort_values(['日付', '出金金額(USD)'])
#         df_bnk_wit_usd = df_bnk_wit_usd.reset_index(drop=True)

#         df_stk_daw_usd_edit = common_service.get_df_stk_daw_usd_edit(main_bean, df_bnk_wit_usd, df_stk_daw_fgn, df_rate)

#         df_tr_hist = common_service.get_df_tr_hist(df_stk_tr_hist, df_rate)

#         df_buy_asset = common_service.get_df_buy_asset(df_stk_daw_usd_edit, df_tr_hist)

#         acct_bean = common_bean.AcctBeanStk()
#         acct_bean.set_acct_nm(main_bean.out_jnl.chk_jnl_buy_stk.title)

#         seq = 0

#         for index, row in df_buy_asset.iterrows():

#             seq += 1

#             exc_diff_bean = common_bean.ExcDiffBean()
#             exc_diff_bean.getExcDiff(row['為替差損益'])

#             df_tmp = pd.DataFrame(
#                 {
#                 '*識別フラグ(4)': ['2110', '2101']
#                 , '伝票No.(6)': [seq, seq]
#                 # , '決算(4)': []
#                 , '*取引日付(10)': [str(row['日付']).replace('/', ''), str(row['日付']).replace('/', '')]
#                 , '*借方勘定科目(24)': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
#                 , '借方補助科目(24)': [acct_bean.dr_sub_acct_nm, '']
#                 # , '借方部門(24)': []
#                 , '*借方税区分(-)': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '*借方金額(11)': [row['受渡金額(円)'], exc_diff_bean.loss_amt]
#                 , '借方税金額(11)': [0, 0]
#                 , '*貸方勘定科目(24)': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
#                 , '貸方補助科目(24)': [acct_bean.cr_sub_acct_nm, '']
#                 # , '貸方部門(24)': []
#                 , '*貸方税区分(-)': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '*貸方金額(11)': [row['出金金額(円)'], exc_diff_bean.profit_amt]
#                 , '貸方税金額(11)': [0, 0]
#                 , '摘要(64)': [row['摘要'], '']
#                 # , '番号(10)': []
#                 # , '期日(10)': []
#                 , '*タイプ(1)': [0, 0]
#                 # , '生成元(4)': []
#                 # , '仕訳メモ(180)': []
#                 # , '付箋1(1)': []
#                 # , '付箋2(1)': []
#                 , '*調整()': ['no', 'no']
#                 }
#             , index=['main', 'pol']
#             )

#             # 為替差損益 = 0 の場合は為替差損益明細を削除
#             if int(row['為替差損益']) == 0:
#                 df_tmp.drop('pol', axis=0, inplace=True)

#             df_dst = pd.concat([df_dst, df_tmp], axis=0)

#         df_dst = df_dst.sort_index().sort_values(['伝票No.(6)', '*識別フラグ(4)'], ascending=[True, False])
#         df_dst = df_dst.reset_index(drop=True)        

#         df_dst.to_csv(path_or_buf=self.asset_jnl_path, index=False, header=False, encoding='shift_jis')


class MfJnlFmt(JnlFmt):
    def __init__(self):
        super().__init__()
        self.df_tmpl = pd.DataFrame({'取引No': [], '取引日': [], '借方勘定科目': [], '借方補助科目': [], '借方税区分': [], '借方部門': [], '借方金額(円)': [], '借方税額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方税区分': [], '貸方部門': [], '貸方金額(円)': [], '貸方税額': [], '摘要': [], '仕訳メモ': [], 'タグ': [], 'MF仕訳タイプ': [], '決算整理仕訳': [], '作成日時': [], '作成者': [], '最終更新日時': [], '最終更新者': []})

    def mk_jnl(
              self
            , main_bean: MainBean
            , df_jnl_xfr_exc: DataFrame
            , path_save: str
    ):

        df_dst = self.df_tmpl.copy()

        for index, row in df_jnl_xfr_exc.iterrows():
        
            if row['借方金額'] == 0 and row['貸方金額'] == 0:
                next

            df_tmp = pd.DataFrame(
                {
                  '取引No': [row['seq']]
                , '取引日': [row['日付']]
                , '借方勘定科目': [row['借方勘定科目']]
                , '借方補助科目': [row['借方補助科目']]
                , '借方税区分': [const.TAX_TYPE_TAISHOGAI]
                , '借方金額(円)': [row['借方金額']]
                , '借方税額': [0]
                , '貸方勘定科目': [row['貸方勘定科目']]
                , '貸方補助科目': [row['貸方補助科目']]
                , '貸方税区分': [const.TAX_TYPE_TAISHOGAI]
                , '貸方金額(円)': [row['貸方金額']]
                , '貸方税額': [0]
                , '摘要': [row['摘要']]
                , '作成日時': [self.rgstr_dt]
                , '作成者': [main_bean.out_conf_rgstr_nm.value]
                , '最終更新日時': [self.rgstr_dt]
                , '最終更新者': [main_bean.out_conf_rgstr_nm.value]
                }
            )

            df_dst = pd.concat([df_dst, df_tmp], axis=0)

        df_dst.to_csv(path_or_buf=path_save, index=False, header=False, encoding='shift_jis')

        return

#     def mk_jnl_bnk_usd(
#               self
#             , main_bean: MainBean
#             , df_bnk_daw_usd: DataFrame
#             , df_rate: DataFrame
#             , jnl_nm: str
#     ):

#         if jnl_nm == '預け金振替（外貨預金 ⇒ 証券）':
#             content = '振替　ＳＢＩ証券'
#             jnl_save_path = self.xfr_svng_path
#         elif jnl_nm == '外貨':
#             content = ''

#      # 入金明細gain
#         df_dep_usd = common_service.get_df_dep_usd(main_bean, df_bnk_daw_usd, df_rate)

#         # 出金明細を取得
#         df_wit_usd = common_service.get_df_wit_usd(df_bnk_daw_usd, df_rate, content)

#         df_dst = self.df_tmpl.copy()

#         for index, row_wit in df_wit_usd.iterrows():

#             df_dep_calc_tgt = common_service.get_df_dep_calc_tgt(row_wit, df_dep_usd)
            
#             df_calc_bnk_2_stk = common_service.get_df_xfr_bnk_2_stk(row_wit, df_dep_calc_tgt)

#             print(df_calc_bnk_2_stk)

#             exc_diff_bean = common_bean.ExcDiffBean()
#             exc_diff_bean.getExcDiff(df_calc_bnk_2_stk.at[0,'為替差損益'])

#             acct_bean = common_bean.AcctBeanBnkUsd()
#             acct_bean.set_acct_nm(df_calc_bnk_2_stk.at[0,'内容'])

#             seq = index + 1

#             df_tmp = pd.DataFrame(
#                 {
#                   '取引No': [seq, seq]
#                 , '取引日': [row_wit['日付'], row_wit['日付']]
#                 , '借方勘定科目': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
#                 , '借方補助科目': [acct_bean.dr_sub_acct_nm, '']
#                 , '借方税区分': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '借方金額(円)': [df_calc_bnk_2_stk.at[0, '出金金額(円)_当日レート基準'], exc_diff_bean.loss_amt]
#                 , '借方税額': [0, 0]
#                 , '貸方勘定科目': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
#                 , '貸方補助科目': [acct_bean.cr_sub_acct_nm, '']
#                 , '貸方税区分': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '貸方金額(円)': [df_calc_bnk_2_stk.at[0, '入金金額(円)_当日レート基準'], exc_diff_bean.profit_amt]
#                 , '貸方税額': [0, 0]
#                 , '摘要': [df_calc_bnk_2_stk.at[0, '内容'], '']
#                 , '作成日時': [self.rgstr_dt, self.rgstr_dt]
#                 , '作成者': [main_bean.out_conf.rgstr_nm.value, main_bean.out_conf.rgstr_nm.value]
#                 , '最終更新日時': [self.rgstr_dt, self.rgstr_dt]
#                 , '最終更新者': [main_bean.out_conf.rgstr_nm.value, main_bean.out_conf.rgstr_nm.value]
#                 }
#             , index=['main', 'pol']
#             )

#             # 為替差損益 = 0 の場合は為替差損益明細を削除
#             if int(df_calc_bnk_2_stk.at[0,'為替差損益']) == 0:
#                 df_tmp.drop('pol', axis=0, inplace=True)

#             df_dst = pd.concat([df_dst, df_tmp], axis=0)

#         df_dst = df_dst.sort_index().sort_values(['取引日'])
#         df_dst = df_dst.reset_index(drop=True)        

#         df_dst.to_csv(path_or_buf=jnl_save_path, index=False, header=False, encoding='shift_jis')

#     def mk_jnl_buy_asset(
#               self
#             , main_bean: MainBean
#             , df_bnk_daw_usd: DataFrame
#             , df_stk_daw_fgn: DataFrame
#             , df_stk_tr_hist: DataFrame
#             , df_rate: DataFrame
#     ):
        
#         df_dst = self.df_tmpl.copy()
        
#         content = '振替　ＳＢＩ証券'

#         df_bnk_wit_usd = common_service.get_df_wit_usd(df_bnk_daw_usd, df_rate, content)
#         df_bnk_wit_usd = df_bnk_wit_usd.sort_values(['日付', '出金金額(USD)'])
#         df_bnk_wit_usd = df_bnk_wit_usd.reset_index(drop=True)

#         df_stk_daw_usd_edit = common_service.get_df_stk_daw_usd_edit(main_bean, df_bnk_wit_usd, df_stk_daw_fgn, df_rate)

#         df_tr_hist = common_service.get_df_tr_hist(df_stk_tr_hist, df_rate)

#         df_buy_asset = common_service.get_df_buy_asset(df_stk_daw_usd_edit, df_tr_hist)

#         acct_bean = common_bean.AcctBeanStk()
#         acct_bean.set_acct_nm(main_bean.out_jnl.chk_jnl_buy_stk.title)

#         for index, row in df_buy_asset.iterrows():

#             seq = index + 1

#             exc_diff_bean = common_bean.ExcDiffBean()
#             exc_diff_bean.getExcDiff(row['為替差損益'])

#             df_tmp = pd.DataFrame(
#                 {
#                 '取引No': [seq, seq]
#                 , '取引日': [row['日付'], row['日付']]
#                 , '借方勘定科目': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
#                 , '借方補助科目': [acct_bean.dr_sub_acct_nm, '']
#                 , '借方税区分': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '借方金額(円)': [row['受渡金額(円)'], exc_diff_bean.loss_amt]
#                 , '借方税額': [0, 0]
#                 , '貸方勘定科目': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
#                 , '貸方補助科目': [acct_bean.cr_sub_acct_nm, '']
#                 , '貸方税区分': [const.TAX_TYPE_TAISHOGAI, const.TAX_TYPE_TAISHOGAI]
#                 , '貸方金額(円)': [row['出金金額(円)'], exc_diff_bean.profit_amt]
#                 , '貸方税額': [0, 0]
#                 , '摘要': [row['摘要'], '']
#                 , '作成日時': [self.rgstr_dt, self.rgstr_dt]
#                 , '作成者': [main_bean.out_conf.rgstr_nm.value, main_bean.out_conf.rgstr_nm.value]
#                 , '最終更新日時': [self.rgstr_dt, self.rgstr_dt]
#                 , '最終更新者': [main_bean.out_conf.rgstr_nm.value, main_bean.out_conf.rgstr_nm.value]
#                 }
#             , index=['main', 'pol']
#             )

#             # 為替差損益 = 0 の場合は為替差損益明細を削除
#             if int(row['為替差損益']) == 0:
#                 df_tmp.drop('pol', axis=0, inplace=True)

#             df_dst = pd.concat([df_dst, df_tmp], axis=0)

#         df_dst = df_dst.sort_index().sort_values(['取引日'])
#         df_dst = df_dst.reset_index(drop=True)        

#         df_dst.to_csv(path_or_buf=self.asset_jnl_path, index=False, header=False, encoding='shift_jis')
