# coding: UTF-8
import pandas as pd
from pandas import DataFrame
from tkinter import filedialog as fd
import numpy as np

from jnl_iss_tool.main_bean import MainBean
import jnl_iss_tool.sub_task as sub_task
import jnl_iss_tool.jnl_fmt as jf
import jnl_iss_tool.const as const
import jnl_iss_tool.jnl_bean as jb


def main(main_bean: MainBean):
    """
    メイン処理

    Parameters
    ----------
    main_bean : MainBean
        メイン画面Bean

    Returns
    -------
        なし

    """

    # 出力フォーマットを取得
    jnl_fmt = sub_task.get_jnl_fmt(main_bean.out_conf_fmt.value)
    if jnl_fmt == None:
         return

    # 各入力ファイルをDataFrame形式で取得
    df_bnk_daw_jpy = pd.read_csv(main_bean.bnk_jpy_daw_path.value, encoding='shift_jis')                   # 住信SBIネット銀行-入出金明細（円貨）
    df_bnk_daw_usd = pd.read_csv(main_bean.bnk_usd_daw_path.value, encoding='shift_jis')                   # 住信SBIネット銀行-入出金明細（米ドル）
    df_stk_daw_fgn = pd.read_csv(main_bean.stk_fgn_daw_path.value, encoding='shift_jis', header=3)         # SBI証券-入出金明細（外貨）を取得
    df_stk_tr_hist = pd.read_csv(main_bean.stk_fgn_tr_hist_path.value, encoding='shift_jis', header=2)     # SBI証券-取引履歴を取得
    df_rate = sub_task.get_jpy_2_usd_rate(df_bnk_daw_jpy, df_bnk_daw_usd, df_stk_daw_fgn, df_stk_tr_hist)  # レート情報

    # 通貨振替（円 ⇒ 米ドル）
    if (main_bean.mk_jnl_xfr_exc.value == True):

        df_jnl_xfr_exc = get_df_jnl_xfr_exc(main_bean, df_bnk_daw_jpy, df_bnk_daw_usd, df_rate)
        jnl_fmt.mk_jnl(main_bean, df_jnl_xfr_exc, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_xfr_exc.title))

    # 預け金振替（外貨預金 ⇒ 証券）
    if (main_bean.mk_jnl_xfr_svng.value == True):
        df_jnl_xfr_svng = get_df_jnl_wit_bnk_usd(main_bean, df_bnk_daw_usd, df_rate, main_bean.mk_jnl_xfr_svng.title)
        jnl_fmt.mk_jnl(main_bean, df_jnl_xfr_svng, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_xfr_svng.title))

    # 国税支払
    if (main_bean.mk_jnl_pmt_tax.value == True):
        df_jnl_pmt_tax = get_df_jnl_wit_bnk_usd(main_bean, df_bnk_daw_usd, df_rate, main_bean.mk_jnl_pmt_tax.title)
        jnl_fmt.mk_jnl(main_bean, df_jnl_pmt_tax, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_pmt_tax.title))

    # 受取利息
    if (main_bean.mk_jnl_intrst.value == True):
        df_jnl_intrst = get_df_jnl_intrst(main_bean, df_bnk_daw_usd, df_rate)
        jnl_fmt.mk_jnl(main_bean, df_jnl_intrst, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_intrst.title))

    # 有価証券購入
    if (main_bean.mk_jnl_buy_asset.value == True):
        df_jnl_buy_asset = get_df_jnl_buy_asset(main_bean, df_bnk_daw_usd, df_stk_daw_fgn, df_stk_tr_hist, df_rate)
        jnl_fmt.mk_jnl(main_bean, df_jnl_buy_asset, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_buy_asset.title))

    # 分配金
    if (main_bean.mk_jnl_incm_gain.value == True):
        df_jnl_incm_gain = get_df_jnl_incm_gain(main_bean, df_stk_daw_fgn, df_rate)
        jnl_fmt.mk_jnl(main_bean, df_jnl_incm_gain, jnl_fmt.get_path_save_jnl(main_bean.mk_jnl_incm_gain.title))

def get_df_jnl_xfr_exc(
          main_bean: MainBean
        , df_bnk_daw_jpy: DataFrame
        , df_bnk_daw_usd: DataFrame
        , df_rate: DataFrame
):

    df_dtl_jpy_2_usd = sub_task.get_dtl_jpy_2_usd(df_bnk_daw_jpy, df_bnk_daw_usd, df_rate)

    acct_bean = jb.AcctBean(main_bean.mk_jnl_xfr_exc.title)

    df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': [], '本仕訳フラグ': [], '為替差損益': []})

    for index, row in df_dtl_jpy_2_usd.iterrows():
    
        seq = index + 1

        exc_diff_bean = jb.ExcDiffBean(row['為替差損益'])

        df_tmp = pd.DataFrame(
            {
                  'seq':[seq, seq]
                , '日付': [str(row['日付']).replace('/', ''), str(row['日付']).replace('/', '')]
                , '借方勘定科目': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
                , '借方補助科目': [acct_bean.dr_sub_acct_nm, exc_diff_bean.dr_sub_acct_nm]
                , '借方金額': [row['入金金額(円)'], exc_diff_bean.loss_amt]
                , '貸方勘定科目': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
                , '貸方補助科目': [acct_bean.cr_sub_acct_nm, exc_diff_bean.cr_sub_acct_nm]
                , '貸方金額': [row['出金金額(円)'], exc_diff_bean.profit_amt]
                , '摘要': ['', '']
                , '本仕訳フラグ': [True, False]
                , '為替差損益': [row['為替差損益'], 0]
            }
        )

        df_base = pd.concat([df_base, df_tmp], axis=0)

    df_base['seq'] = df_base['seq'].astype('int')
    df_base['借方金額'] = df_base['借方金額'].astype('int')
    df_base['貸方金額'] = df_base['貸方金額'].astype('int')

    return df_base

def get_df_jnl_wit_bnk_usd(
          main_bean: MainBean
        , df_bnk_daw_usd: DataFrame
        , df_rate: DataFrame
        , jnl_nm: str
):

    # 入金明細を取得
    df_dep_usd = sub_task.get_df_dep_usd(main_bean, df_bnk_daw_usd, df_rate)

    # 出金明細を取得
    df_wit_usd = sub_task.get_df_wit_usd(df_bnk_daw_usd, df_rate, jnl_nm)

    acct_bean = jb.AcctBean(jnl_nm)

    df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': [], '本仕訳フラグ': [], '為替差損益': []})

    seq = 0

    for index, row_wit in df_wit_usd.iterrows():

        df_dep_calc_tgt = sub_task.get_df_dep_calc_tgt(row_wit, df_dep_usd)
        
        df_calc_bnk_2_stk = sub_task.get_df_xfr_bnk_2_stk(row_wit, df_dep_calc_tgt)

        exc_diff_bean = jb.ExcDiffBean(df_calc_bnk_2_stk.at[0,'為替差損益'])

        seq += 1

        df_tmp = pd.DataFrame(
            {
                  'seq':[seq, seq]
                , '日付': [str(row_wit['日付']).replace('/', ''), str(row_wit['日付']).replace('/', '')]
                , '借方勘定科目': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
                , '借方補助科目': [acct_bean.dr_sub_acct_nm, exc_diff_bean.dr_sub_acct_nm]
                , '借方金額': [df_calc_bnk_2_stk.at[0, '預け金額(円)'], exc_diff_bean.loss_amt]
                , '貸方勘定科目': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
                , '貸方補助科目': [acct_bean.cr_sub_acct_nm, exc_diff_bean.cr_sub_acct_nm]
                , '貸方金額': [df_calc_bnk_2_stk.at[0, '出金元金額(円)'], exc_diff_bean.profit_amt]
                , '摘要': ['', '']
                , '本仕訳フラグ': [True, False]
                , '為替差損益': [df_calc_bnk_2_stk.at[0,'為替差損益'], 0]
            }
        )

        df_base = pd.concat([df_base, df_tmp], axis=0)

    df_base = df_base.sort_index().sort_values(['seq', '本仕訳フラグ'], ascending=[False, False])
    df_base = df_base.reset_index(drop=True)        

    return df_base

def get_df_jnl_intrst(
          main_bean: MainBean
        , df_bnk_daw_usd: DataFrame
        , df_rate: DataFrame
):

    # 入金明細を取得
    df_dtl_intrst = sub_task.get_usd_dtl_content(df_bnk_daw_usd, '利息')

    df_dtl_intrst = pd.merge(df_dtl_intrst, df_rate, how='left', on='日付')

    df_dtl_intrst['入金金額(円)'] = (df_dtl_intrst['入金金額(USD)'] * df_dtl_intrst['当日レート']).agg(np.floor)

    acct_bean = jb.AcctBean(main_bean.mk_jnl_intrst.title)

    df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': [], '本仕訳フラグ': [], '為替差損益': []})

    seq = 0

    for index, row_intrst in df_dtl_intrst.iterrows():

        seq += 1

        df_tmp = pd.DataFrame(
            {
                  'seq':[seq]
                , '日付': [str(row_intrst['日付']).replace('/', '')]
                , '借方勘定科目': [acct_bean.dr_acct_nm]
                , '借方補助科目': [acct_bean.dr_sub_acct_nm]
                , '借方金額': [row_intrst['入金金額(円)']]
                , '貸方勘定科目': [acct_bean.cr_acct_nm]
                , '貸方補助科目': [acct_bean.cr_sub_acct_nm]
                , '貸方金額': [row_intrst['入金金額(円)']]
                , '摘要': ['']
                , '本仕訳フラグ': [True]
                , '為替差損益': [0]
            }
        )    
    
        df_base = pd.concat([df_base, df_tmp], axis=0)

    return df_base

def get_df_jnl_buy_asset(
          main_bean: MainBean
        , df_bnk_daw_usd: DataFrame
        , df_stk_daw_fgn: DataFrame
        , df_stk_tr_hist: DataFrame
        , df_rate: DataFrame
):

    df_bnk_wit_usd = sub_task.get_df_wit_usd(df_bnk_daw_usd, df_rate, main_bean.mk_jnl_buy_asset.title)
    df_bnk_wit_usd = df_bnk_wit_usd.sort_values(['日付', '出金金額(USD)'])
    df_bnk_wit_usd = df_bnk_wit_usd.reset_index(drop=True)

    df_stk_daw_usd_edit = sub_task.get_df_stk_daw_usd_edit(main_bean, df_bnk_wit_usd, df_stk_daw_fgn, df_rate)

    df_tr_hist = sub_task.get_df_tr_hist(df_stk_tr_hist, df_rate)

    df_buy_asset = sub_task.get_df_buy_asset(df_stk_daw_usd_edit, df_tr_hist)

    acct_bean = jb.AcctBean(main_bean.mk_jnl_buy_asset.title)

    df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': [], '本仕訳フラグ': [], '為替差損益': []})

    seq = 0

    for index, row_buy_asset in df_buy_asset.iterrows():

        exc_diff_bean = jb.ExcDiffBean(row_buy_asset['為替差損益'])

        seq += 1

        df_tmp = pd.DataFrame(
            {
                  'seq':[seq, seq]
                , '日付': [str(row_buy_asset['日付']).replace('/', ''), str(row_buy_asset['日付']).replace('/', '')]
                , '借方勘定科目': [acct_bean.dr_acct_nm, exc_diff_bean.dr_acct_nm]
                , '借方補助科目': [acct_bean.dr_sub_acct_nm, exc_diff_bean.dr_sub_acct_nm]
                , '借方金額': [row_buy_asset['受渡金額(円)'], exc_diff_bean.loss_amt]
                , '貸方勘定科目': [acct_bean.cr_acct_nm, exc_diff_bean.cr_acct_nm]
                , '貸方補助科目': [acct_bean.cr_sub_acct_nm, exc_diff_bean.cr_sub_acct_nm]
                , '貸方金額': [row_buy_asset['出金金額(円)'], exc_diff_bean.profit_amt]
                , '摘要': ['', '']
                , '本仕訳フラグ': [True, False]
                , '為替差損益': [0, 0]
            }
        )    
    
        df_base = pd.concat([df_base, df_tmp], axis=0)
    
    return df_base

def get_df_jnl_incm_gain(
          main_bean: MainBean
        , df_stk_daw_fgn: DataFrame
        , df_rate: DataFrame
):

    df_bnk_incm_gain = sub_task.get_df_incm_gain(df_stk_daw_fgn, df_rate)

    acct_bean = jb.AcctBean(main_bean.mk_jnl_incm_gain.title)

    df_base = pd.DataFrame({'seq': [], '日付': [], '借方勘定科目': [], '借方補助科目': [], '借方金額': [], '貸方勘定科目': [], '貸方補助科目': [], '貸方金額': [], '摘要': [], '本仕訳フラグ': [], '為替差損益': []})

    seq = 0

    for index, row_bnk_incm_gain in df_bnk_incm_gain.iterrows():

        seq += 1

        df_tmp = pd.DataFrame(
            {
                  'seq':[seq]
                , '日付': [str(row_bnk_incm_gain['日付']).replace('/', '')]
                , '借方勘定科目': [acct_bean.dr_acct_nm]
                , '借方補助科目': [acct_bean.dr_sub_acct_nm]
                , '借方金額': [row_bnk_incm_gain['入金金額(円)']]
                , '貸方勘定科目': [acct_bean.cr_acct_nm]
                , '貸方補助科目': [acct_bean.cr_sub_acct_nm]
                , '貸方金額': [row_bnk_incm_gain['入金金額(円)']]
                , '摘要': [row_bnk_incm_gain['摘要']]
                , '本仕訳フラグ': [True]
                , '為替差損益': [0]
            }
        )    
    
        df_base = pd.concat([df_base, df_tmp], axis=0)
    
    return df_base