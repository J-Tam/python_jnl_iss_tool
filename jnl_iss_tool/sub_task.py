# coding: UTF-8
import pandas as pd
from pandas import DataFrame
from pandas import Series
import datetime as dt
import numpy as np
import math
import jnl_iss_tool.df_utils as df_utils
from jnl_iss_tool.main_bean import MainBean
import jnl_iss_tool.jnl_fmt as jf
import jnl_iss_tool.const as const

def get_jnl_fmt(fmt_type: int) -> jf.JnlFmt:
    """
    指定のフォーマットに合わせたクラスを取得する

    Parameters
    ----------
    fmt_type : 
        フォーマット区分
        
    Returns
    -------
    jnl_fmt: jf.JnlFmt
        フォーマットクラス

    """

    if (fmt_type == const.SEL_MF):
        jnl_fmt = jf.MfJnlFmt()
    elif (fmt_type == const.SEL_YAYOI):
        jnl_fmt = jf.YayoiJnlFmt()
    else:
        jnl_fmt = None
    return jnl_fmt

def get_content(jnl_nm: str) -> str:

    if jnl_nm == const.JNL_NM_XFR_SVNG or jnl_nm == const.JNL_NM_BUY_ASSET:
        content = '振替　ＳＢＩ証券'
    elif jnl_nm == const.JNL_NM_PMT_TAX:
        content = '国税'

    return content    

def get_jpy_2_usd_rate_year(year: dt.datetime) -> DataFrame:
    """
    指定した年の円 ⇒ 米ドルレートを取得する

    Parameters
    ----------
    year : 
        年
        
    Returns
    -------
    df_jpy_2_usd_rate_year: DataFrame
        該当年のレート情報

        [列情報]
          日付: str
          当日レート: float

    """

    url = "https://www.77bank.co.jp/kawase/usd{1}.html".replace('{1}', str(year))

    df = pd.read_html(url)
    df_jpy_2_usd_rate_year = pd.DataFrame(index=[])

    # 1月~12月までループ
    for cnt in range(1,13):

        month = str(cnt) + '月'

        # 空のデータフレームを作成
        df_rate_tmp = pd.DataFrame(index=[])

        # 該当月の日付とレートを取得（['日 付', month] ⇒ [日付, レート]）
        df_rate_tmp = df[0].loc[:, ['日 付', month]]
        df_rate_tmp.rename(columns={'日 付' : '日付'}, inplace=True)
        df_rate_tmp.rename(columns={month : '当日レート'}, inplace=True)
        df_rate_tmp = df_rate_tmp[1:32]    # 1~31行目に絞り込み
        df_rate_tmp.dropna(subset=['当日レート'], inplace=True)
        df_rate_tmp['日付'] = str(year) + '/' + str(cnt).zfill(2) + '/' + df_rate_tmp['日付']

        df_jpy_2_usd_rate_year = pd.concat([df_jpy_2_usd_rate_year, df_rate_tmp])

    return df_jpy_2_usd_rate_year

def get_jpy_2_usd_rate(
          df_bnk_daw_jpy: DataFrame
        , df_bnk_daw_usd: DataFrame
        , df_stk_daw_fgn: DataFrame
        , df_stk_tr_hist: DataFrame
) -> DataFrame:
    """
    入力元の各CSVファイルの最も古い日付からシステム日付までの
    円 ⇒ 米ドルレートを取得する

    Parameters
    ----------
    df_bnk_daw_jpy : DataFrame
        住信SBIネット銀行-入出金明細（円貨）
    df_bnk_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    df_stk_daw_fgn : DataFrame
        SBI証券-入出金明細（外貨）
    df_stk_tr_hist : DataFrame
        SBI証券-取引履歴
        
    Returns
    -------
    df_rate : DataFrame
        レート情報

        [列情報]
          日付: str
          当日レート: float

    """

    min_date = get_min_date(df_bnk_daw_jpy, df_bnk_daw_usd, df_stk_daw_fgn, df_stk_tr_hist)

    df_rate = pd.DataFrame(index=[])

    for year in range(min_date.year, dt.date.today().year +1):

        df_rate = pd.concat([df_rate, get_jpy_2_usd_rate_year(year)])

    return df_rate

def get_min_date(
          df_bnk_daw_jpy: DataFrame
        , df_bnk_daw_usd: DataFrame
        , df_stk_daw_fgn: DataFrame
        , df_stk_tr_hist: DataFrame
) -> dt.datetime:
    """
    全ての入力ファイル内の最も古い日付を取得する

    Parameters
    ----------
    df_bnk_daw_jpy : DataFrame
        住信SBIネット銀行-入出金明細（円貨）
    df_bnk_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    df_stk_daw_fgn : DataFrame
        SBI証券-入出金明細（外貨）
    df_stk_tr_hist : DataFrame
        SBI証券-取引履歴
        
    Returns
    -------
    min_date : dt.datetime
        最小日付

    """

    # 住信SBIネット銀行-入出金明細（円貨）の最小日付を取得
    min_date_bnk_daw_jpy = df_utils.get_min_dt_fr_series(df_bnk_daw_jpy['日付'])

    min_date_bnk_daw_usd = df_utils.get_min_dt_fr_series(df_bnk_daw_usd['日付'])

    min_date_stk_daw_fgn = df_utils.get_min_dt_fr_series(df_stk_daw_fgn['入出金日'])

    df_stk_tr_hist['国内約定日'] = df_stk_tr_hist['国内約定日'].str.replace('年','/').str.replace('月','/').str.replace('日', '')
    min_date_stk_tr_hist = df_utils.get_min_dt_fr_series(df_stk_tr_hist['国内約定日'])

    tmp_min_date = min_date_bnk_daw_jpy

    if (min_date_bnk_daw_usd < tmp_min_date):
        tmp_min_date = min_date_bnk_daw_usd

    if (min_date_stk_daw_fgn < tmp_min_date):
        tmp_min_date = min_date_stk_daw_fgn

    if (min_date_stk_tr_hist < tmp_min_date):
        tmp_min_date = min_date_stk_tr_hist

    min_date = tmp_min_date

    return min_date

def get_jpy_dtl_jpy_2_usd(df_daw_jpy: DataFrame) -> DataFrame:
    """
    住信SBIネット銀行の入出金明細（円貨）から
    円貨_通貨振替明細（円 ⇒ 米ドル）を取得する

    Parameters
    ----------
    df_daw_jpy : DataFrame
        住信SBIネット銀行-入出金明細（円貨）

    Returns
    -------
    df_jpy_dtl_jpy_2_usd : DataFrame
        円貨_通貨振替明細（円 ⇒ 米ドル） 

        [列情報]
          日付: Date
          出金金額(円): int
    
    """

    # 内容列に"米ドル　代表口座"を含む行に絞り込み
    df = df_daw_jpy[df_daw_jpy['内容'].str.contains('米ドル　代表口座')].copy()

    # 出金金額(円)の型を数値型に変換
    df['出金金額(円)'] = df_utils.cnv_amt_str_2_int(df['出金金額(円)'])

    # 日付、出金金額(円)でソート（昇順）
    df = df.sort_values(['日付','出金金額(円)'])

    # インデックスの再採番
    df.reset_index(inplace=True)

    # 不要な列を除去
    df.drop(['index','内容','入金金額(円)','残高(円)','メモ'], axis=1, inplace=True)

    # 戻り値をセット
    df_jpy_dtl_jpy_2_usd = df.copy()
    return df_jpy_dtl_jpy_2_usd

def get_usd_dtl_content(df_daw_usd: DataFrame, content: str) -> DataFrame:
    """
    住信SBIネット銀行の入出金明細（米ドル）から
    指定の明細をを取得する

    Parameters
    ----------
    df_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    content : str
        内容
        
    Returns
    -------
    df_usd_dtl_jpy_2_usd : DataFrame
        米ドル_通貨振替明細（円 ⇒ 米ドル） 

        [列情報]
          日付: Date
          入金金額(USD): float

    """

    # 内容列に"円　代表口座"を含む行に絞り込み
    df = df_daw_usd[df_daw_usd['内容'].str.contains(content)].copy()

    # 入金金額(USD)の型を数値型に変換
    df['入金金額(USD)'] = df_utils.cnv_amt_str_2_float(df['入金金額(USD)'])
    # df['入金金額(USD)'] = df['入金金額(USD)'].str.replace(',','')
    # df['入金金額(USD)'] = df['入金金額(USD)'].astype('float')

    df['日付'] = df_utils.cnv_date_str_zfill(df['日付'])

    # 日付、入金金額(USD)でソート（昇順）
    df = df.sort_values(['日付','入金金額(USD)'])

    # インデックスの再採番
    df.reset_index(inplace=True)

    # 不要な列を除去
    df.drop(['内容','出金金額(USD)','残高(USD)','メモ'], axis=1, inplace=True)

    # 戻り値をセット
    df_usd_dtl_jpy_2_usd = df.copy()
    return df_usd_dtl_jpy_2_usd

def get_dtl_jpy_2_usd(
        df_bnk_daw_jpy: DataFrame
      , df_bnk_daw_usd: DataFrame
      , df_rate: DataFrame
) -> DataFrame:
    """
    住信SBIネット銀行の入出金明細（円貨）と入出金明細（米ドル）から
    通貨振替明細（円 ⇒ 米ドル）を取得する

    Parameters
    ----------
    df_bnk_daw_jpy : DataFrame
        住信SBIネット銀行-入出金明細（円貨）
    df_bnk_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    df_rate : DataFrame
        レート情報（円⇒米ドル）

    Returns
    -------
    df_dtl_jpy_2_usd : DataFrame
        通貨振替明細（円 ⇒ 米ドル）

        [列情報]
          日付: Date
          出金金額(円): int
          入金金額(USD): float
          当日レート: float
          入金金額(円): int
          為替差損益: int

    """

    # 円貨_通貨振替明細（円 ⇒ 米ドル）を取得
    df_dtl_jpy = get_jpy_dtl_jpy_2_usd(df_bnk_daw_jpy)

    # 米ドル_通貨振替明細（円 ⇒ 米ドル）を取得
    df_dtl_usd = get_usd_dtl_content(df_bnk_daw_usd, '円　代表口座')

    # 不要な列を除去
    df_dtl_usd.drop(['日付'], axis=1, inplace=True)

    # 円貨と米ドルの明細をマージ
    df_tmp = pd.merge(df_dtl_jpy, df_dtl_usd, left_index=True, right_index=True)

    # レート情報をマージ
    df_tmp = pd.merge(df_tmp, df_rate, how='left', on='日付')

    # 列を追加
    df_tmp['入金金額(円)'] = (df_tmp['入金金額(USD)'] * df_tmp['当日レート']).agg(np.floor)
    df_tmp['為替差損益'] = df_tmp['入金金額(円)'] - df_tmp['出金金額(円)']

    df_dtl_jpy_2_usd = df_tmp
    return df_dtl_jpy_2_usd

def get_df_dep_usd(
        main_window_bean: MainBean
      , df_bnk_daw_usd: DataFrame
      , df_rate: DataFrame
):
    """
    住信SBIネット銀行の入出金明細（米ドル）から
    入金明細のみを取得する

    Parameters
    ----------
    main_window_bean : MainBean
        メイン画面Bean
    df_bnk_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    df_rate : DataFrame
        レート情報（円 ⇒ 米ドル）

    Returns
    -------
    df_dep_usd : DataFrame
        入金明細（米ドル） 

        [列情報]
        日付: Date
        入金金額(USD): float
        当日レート: float
        入金金額(円): int

    """

    df_init = pd.DataFrame(
        {
          '日付': [main_window_bean.bnk_usd_eval_dt.value]
        , '入金金額(USD)': [main_window_bean.bnk_usd_blnc.value]
        }
    , index=['init']
    )

    # 不要な列を削除
    df_dep_usd = df_bnk_daw_usd.copy()
    df_dep_usd = df_dep_usd.drop(['内容', '出金金額(USD)', '残高(USD)', 'メモ'], axis=1)
    df_dep_usd = df_dep_usd[~df_dep_usd['入金金額(USD)'].isna()]

    if not len(df_init.at['init', '日付']) == 0:
        df_dep_usd = pd.concat([df_init, df_dep_usd])

    df_dep_usd = df_dep_usd.sort_values(['日付','入金金額(USD)'])

    # カンマを除去して型変換
    df_dep_usd['入金金額(USD)'] = df_utils.cnv_amt_str_2_float(df_dep_usd['入金金額(USD)'])

    df_dep_usd['日付'] = df_utils.cnv_date_str_zfill(df_dep_usd['日付'])

    # 入金明細を日付単位で集計
    df_dep_usd = df_dep_usd[['日付', '入金金額(USD)']].groupby('日付').sum()

    df_dep_usd = pd.merge(df_dep_usd, df_rate, how='left', on='日付')
    df_dep_usd['入金金額(円)'] = (df_dep_usd['入金金額(USD)'] * df_dep_usd['当日レート']).agg(np.floor)

    df_dep_usd = df_dep_usd.reset_index(drop=True)

    return df_dep_usd

def get_df_wit_usd(
        df_bnk_daw_usd: DataFrame
      , df_rate: DataFrame
      , jnl_nm: str
) -> DataFrame:
    """
    住信SBIネット銀行の入出金明細（米ドル）から
    出金明細のみを取得する

    Parameters
    ----------
    df_bnk_daw_usd : DataFrame
        住信SBIネット銀行-入出金明細（米ドル）
    df_rate : DataFrame
        レート情報（円 ⇒ 米ドル）
    jnl_nm : str
        仕訳名

    Returns
    -------
    df_dep_usd : DataFrame
        出金明細（米ドル） 

        [列情報]
        日付: Date
        内容: str
        出金金額(USD): float
        残高(USD): float
        当日レート: float
        出金金額(円): int

    """
    
    # 不要な列を削除
    df_wit_usd = df_bnk_daw_usd.copy()
    df_wit_usd = df_wit_usd.drop(['入金金額(USD)', 'メモ'], axis=1)

    df_wit_usd = df_wit_usd[~df_wit_usd['出金金額(USD)'].isna()]
    df_wit_usd = df_wit_usd[df_wit_usd['内容'].str.contains(get_content(jnl_nm))]
    
    df_wit_usd['出金金額(USD)'] = df_utils.cnv_amt_str_2_float(df_wit_usd['出金金額(USD)'])
    df_wit_usd['残高(USD)'] = df_utils.cnv_amt_str_2_float(df_wit_usd['残高(USD)'])

    df_wit_usd['日付'] = df_utils.cnv_date_str_zfill(df_wit_usd['日付'])

    df_wit_usd = pd.merge(df_wit_usd, df_rate, how='left', on='日付')
    df_wit_usd['出金金額(円)'] = (df_wit_usd['出金金額(USD)'] * df_wit_usd['当日レート']).agg(np.floor)

    return df_wit_usd

def get_df_dep_reduce_blnc(df_dep: DataFrame, blnc: float) -> DataFrame:
    """
    出金明細の残高を元に
    出金前最新の入金明細から残高分を除外した結果を取得

    [例_入出金明細（米ドル）] 
    日付        内容               出金金額(USD)  入金金額(USD)  残高(USD) 
    2023/2/2	振替  ＳＢＩ証券	1,540.42                    1,000.00
    2023/1/27	積立  円  代表口座	              1,540.35      2,540.42
    2023/1/22	国税	           0.01		                   1,000.07
    2023/1/22	利息		                     0.08	       1,000.08
    2022/12/27	積立  円  代表口座		          1,506.70	    2,506.73
    ・・・以下省略
    
    この場合、出金前最新の入金明細から残高分を除外した結果は下記の通り
    2023/1/27	積立  円  代表口座                540.35
    2023/1/22	利息		                     0.08
    2022/12/27	積立  円  代表口座		          1,506.70
    ・・・以下省略

    Parameters
    ----------
    df_dep : DataFrame
        入金明細（米ドル）
    blnc : float
        残高

    Returns
    -------
    df_dep_reduce_blnc : DataFrame
        入金明細（米ドル）_残高減算後

        [列情報]
        日付: Date
        入金金額(USD): float
        当日レート: float
        入金金額(円): int

    """

    df_tmp = df_dep.copy()
    tmp_blnc = blnc

    for index, row_dep in df_dep.iterrows():

        # 差額許容内で一致の場合
        if abs(row_dep['入金金額(USD)'] - tmp_blnc) < 1e-9:
            df_tmp.drop(index)
            break

        # 入金金額が残高より小さい場合
        elif (row_dep['入金金額(USD)'] < tmp_blnc):
            tmp_blnc = tmp_blnc - row_dep['入金金額(USD)'] 
            df_tmp.drop(index)
        
        else:
            df_tmp.at[index,'入金金額(USD)'] = df_tmp.at[index,'入金金額(USD)'] - tmp_blnc
            df_tmp.at[index,'入金金額(円)'] = math.floor((df_tmp.at[index,'入金金額(円)'] - tmp_blnc * df_tmp.at[index,'当日レート']))

            if df_tmp.at[index,'入金金額(円)'] == 0:
                df_tmp.at[index,'入金金額(円)'] = 1

            break

    df_tmp['入金金額(円)'] = df_tmp['入金金額(円)'].astype('int')
    df_dep_reduce_blnc = df_tmp.copy()

    return df_dep_reduce_blnc

def get_df_dep_calc_tgt(
        row_df_wit: Series
      , df_dep_usd: DataFrame
) -> DataFrame:
    """
    出金明細に対して、出金に用いられた入金明細を取得する

    [例_入出金明細（米ドル）]
    日付        内容               出金金額(USD)  入金金額(USD)  残高(USD)
    2023/2/2	振替  ＳＢＩ証券	1,540.42                    1,000.00
    2023/1/27	積立  円  代表口座	              1,540.35      2,540.42
    2023/1/22	国税	           0.01		                   1,000.07
    2023/1/22	利息		                     0.08	       1,000.08
    2022/12/27	積立  円  代表口座		          1,506.70	    2,506.73
    ・・・以下省略
    
    この場合、出金(2023/2/2_振替  ＳＢＩ証券)に用いられた入金明細は下記の通り
    2023/1/27	積立  円  代表口座                540.35
    2023/1/22	利息		                     0.08
    2022/12/27	積立  円  代表口座		          999.99
                合計                             1,540.42
    
    Parameters
    ----------
    row_df_wit : Series
        出金明細（米ドル）_1行
    df_dep_usd : DataFrame
        入金明細（米ドル）

    Returns
    -------
    df_dep_calc_tgt : DataFrame
        入金明細（米ドル）_計算対象

        [列情報]
        日付: Date
        入金金額(USD): float
        当日レート: float
        入金金額(円): int

    """

    # 出金明細以前の入金明細を取得し、日付の降順でソート
    df_dep = df_dep_usd[df_dep_usd['日付'] <= row_df_wit['日付']]
    df_dep = df_dep.sort_values(['日付'], ascending=[False])
    df_dep = df_dep.reset_index(drop=True)

    # 出金明細の残高(USD)を最新の入金明細から減算
    df_dep_reduce_blnc = get_df_dep_reduce_blnc(df_dep, row_df_wit['残高(USD)'])

    df_tmp = pd.DataFrame({'日付': [], '入金金額(USD)': [], '当日レート': [], '入金金額(円)': []})

    wit_tmp = row_df_wit['出金金額(USD)']

    for index, row_dep in df_dep_reduce_blnc.iterrows():

        # 差額許容内で一致の場合
        if abs(row_dep['入金金額(USD)'] - wit_tmp) < 1e-9:

            # 当該行の入金明細を計算対象に加える
            df_tmp = pd.concat([df_tmp, df_dep_reduce_blnc.iloc[[index]]], axis=0)
            break

        # 入金金額が出金金額以下の場合
        elif (row_dep['入金金額(USD)'] < wit_tmp):

            # 当該行の入金明細を計算対象に加える
            df_tmp = pd.concat([df_tmp, df_dep_reduce_blnc.iloc[[index]]], axis=0)
            wit_tmp = wit_tmp - row_dep['入金金額(USD)']

        # 入金金額が出金金額より大きい場合
        else:

            # 当該行の入金明細の入金金額を出金金額に置き換えて計算対象に加える
            df_dep_reduce_blnc.at[index, '入金金額(USD)'] = wit_tmp
            df_dep_reduce_blnc.at[index, '入金金額(円)'] = math.floor(wit_tmp * df_dep_reduce_blnc.at[index, '当日レート'])

            if df_dep_reduce_blnc.at[index,'入金金額(円)'] == 0:
                df_dep_reduce_blnc.at[index,'入金金額(円)'] = 1

            df_tmp = pd.concat([df_tmp, df_dep_reduce_blnc.iloc[[index]]], axis=0)
            break

    df_tmp['入金金額(円)'] = df_tmp['入金金額(円)'].astype('int')
    df_dep_calc_tgt = df_tmp.copy()

    return df_dep_calc_tgt

def get_df_xfr_bnk_2_stk(
        row_df_wit: Series
      , df_dep_calc_tgt: DataFrame
) -> DataFrame:
    """
    出金明細とそれに対応する入金明細を突合せして
    振替明細を取得する

    例
    [出金明細（米ドル）_1行]
    日付        内容               出金金額(USD)  残高(USD)  当日レート  出金金額(円)
    2023/2/2	振替  ＳＢＩ証券	1,540.42      1,000.00   128.5      197,943

    [入金明細（米ドル）_計算対象]
    日付        入金金額(USD)      当日レート     入金金額(円)
    2023/1/27	540.35            129.59        70,023    
    2023/1/22	0.08              128.71        10
    2022/12/27	999.99            133.24        133,238

    [振替明細]
    日付        出金金額(USD)  当日レート  出金金額(円)  入金金額(USD)   入金金額(円)   為替差損益
                預け金額(USD)             預け金額(円)  出金元金額(USD) 出金元金額(円)
    2023/2/2	1,540.42      128.5      197,943       1,540.42       203,271        5,328

    Parameters
    ----------
    row_df_wit : Series
        出金明細（米ドル）_1行
    df_dep_calc_tgt : DataFrame
        入金明細（米ドル）_計算対象

    Returns
    -------
    df_xfr_bnk_2_stk : DataFrame
        仕訳情報（外貨預金 ⇒ 預け金）

        [列情報]
        日付: Date
        出金金額(USD): float
        当日レート: float
        出金金額(円): int
        入金金額(USD): float
        入金金額(円): int
        
    """

    # 入金明細（米ドル）_計算対象の入金金額を集計する
    df_dep_smy = df_dep_calc_tgt.copy()
    df_dep_smy = df_dep_smy.drop(['日付', '当日レート'], axis=1)
    df_dep_smy = pd.DataFrame(df_dep_smy.sum()).T
    df_dep_smy['key'] = 0

    df_row_df_wit = pd.DataFrame(row_df_wit).T
    df_row_df_wit['key'] = 0

    df_xfr_bnk_2_stk = pd.merge(df_row_df_wit, df_dep_smy, how='left', on='key')
    df_xfr_bnk_2_stk.drop(['残高(USD)', 'key'], axis=1, inplace=True)

    df_xfr_bnk_2_stk = df_xfr_bnk_2_stk.rename(columns={'出金金額(USD)': '預け金額(USD)', '出金金額(円)': '預け金額(円)', '入金金額(USD)': '出金元金額(USD)', '入金金額(円)': '出金元金額(円)'})

    df_xfr_bnk_2_stk['為替差損益'] = (df_xfr_bnk_2_stk['預け金額(円)'] - df_xfr_bnk_2_stk['出金元金額(円)']).agg(np.floor)

    return df_xfr_bnk_2_stk

def get_df_stk_daw_usd_edit(
        main_window_bean: MainBean
      , df_bnk_wit_usd: DataFrame
      , df_stk_daw_fgn: DataFrame
      , df_rate: DataFrame
    ):
    """
    SBI証券の入出金明細（外貨）を次のように編集した結果を取得する
    ・摘要が「住信SBIネット銀行から外貨入金」の場合、入手金日をSBIネット銀行側の日付に変換
    ・レート情報を結合
    
    Parameters
    ----------
    main_window_bean : MainBean
        メイン画面Bean
    df_bnk_wit_usd : DataFrame
        住信SBIネット銀行-出金明細（米ドル）
    df_stk_daw_fgn : DataFrame
        SBI証券-入出金明細（外貨）
    df_rate : DataFrame
        レート情報（円 ⇒ 米ドル）

    Returns
    -------
    df_stk_daw_usd_edit : DataFrame
        SBI証券の入出金明細（外貨）_編集後

        [列情報]
        日付: Date
        摘要: str
        入金額: float
        当日レート: float

    """

    df_init = pd.DataFrame(
        {
          '日付': [main_window_bean.bnk_usd_eval_dt.value]
        , '入金額': [main_window_bean.bnk_usd_blnc.value]
        }
    , index=['init']
    )

    df = df_stk_daw_fgn.copy()
    df = df.drop(['区分', '通貨', '出金額'], axis=1)

    df_xfr = df[df['摘要'].str.contains('住信SBIネット銀行から外貨入金')]
    df_xfr = df_xfr.sort_values(['入出金日', '入金額']) 
    df_xfr = df_xfr.reset_index(drop=True)

    df_xfr = pd.merge(df_bnk_wit_usd, df_xfr, left_index=True, right_index=True)
    df_xfr = df_xfr.drop(['内容', '残高(USD)', '当日レート', '出金金額(円)', '入出金日', '出金金額(USD)'], axis=1)

    df_incm = df[df['摘要'].str.contains('分配金')]
    df_incm = df_incm.rename(columns={'入出金日' : '日付'})
    df_incm = df_incm.sort_values(['日付', '入金額']) 

    df_stk_daw_fgn_edit = pd.concat([df_xfr, df_incm], axis=0)

    if not len(df_init.at['init','日付']) == 0:
        df_stk_daw_fgn_edit = pd.concat([df_init, df_stk_daw_fgn_edit])

    df_stk_daw_fgn_edit = df_stk_daw_fgn_edit.sort_values(['日付', '入金額'])

    df_stk_daw_fgn_edit = pd.merge(df_stk_daw_fgn_edit, df_rate, how='left', on='日付')

    return df_stk_daw_fgn_edit

def get_df_tr_hist(
        df_stk_tr_hist: DataFrame
      , df_rate: DataFrame
):
    """
    SBI証券の取引履歴（米ドル）を取得
    
    Parameters
    ----------
    df_stk_tr_hist : DataFrame
        SBI証券-取引履歴（外貨）
    df_rate : DataFrame
        レート情報（円 ⇒ 米ドル）

    Returns
    -------
    df_tr_hist : DataFrame
        SBI証券-取引履歴（米ドル）

        [列情報]
        日付: Date
        通貨: str
        受渡金額: float
        備考: str
        当日レート: float
        受渡金額(円): float

    """

    df = df_stk_tr_hist.copy()
    df = df[df['通貨'].str.contains('米国ドル')]

    df.rename(columns={'国内約定日' : '日付'}, inplace=True)
    # df['受渡金額'] = df['受渡金額'].str.replace('USD','')
    # df['受渡金額'] = df['受渡金額'].str.replace(',','')
    # df['受渡金額'] = df['受渡金額'].astype('float')
    
    df['日付'] = df['日付'].str.replace('年','/').str.replace('月','/').str.replace('日', '')

    df = df.sort_values(['日付', '受渡金額'])

    df['備考'] = df['銘柄名'] + ':' + df['約定単価'].astype('str') + '×' + df['約定数量'].astype('str')

    df = df.drop(['銘柄名', '取引', '預り区分', '約定数量', '約定単価', '国内受渡日'], axis=1)

    # レート情報をマージ
    df = pd.merge(df, df_rate, how='left', on='日付')
    df['受渡金額(円)'] = (df['受渡金額'] * df['当日レート']).agg(np.floor)

    df_tr_hist = df

    return df_tr_hist

def get_df_buy_asset(df_stk_daw_usd_edit: DataFrame, df_tr_hist: DataFrame):

    df_buy_asset = pd.DataFrame({'日付': [], '出金金額(円)': [], '受渡金額(円)': [], '為替差損益': [], '摘要': []})

    blnc_dep = 0
    row_idx_dep = 0

    for index, row_tr_hist in df_tr_hist.iterrows():

        exc_pos = 0

        blnc_tr_amt = row_tr_hist['受渡金額']
        rate_wit = row_tr_hist['当日レート']

        while row_idx_dep < len(df_stk_daw_usd_edit):

            # 入金金額(残額)が0以下の場合    
            if blnc_dep <= 0:

                blnc_dep = round(df_stk_daw_usd_edit.at[row_idx_dep,'入金額'], 3)
                rate_dep = df_stk_daw_usd_edit.at[row_idx_dep,'当日レート']

            # 入金金額(残額)が出金金額(残額)より小さい場合
            if blnc_dep - blnc_tr_amt < 0:

                # 入金金額(残額)から為替差損益を算出
                exc_pos += blnc_dep * rate_dep - blnc_dep * rate_wit

                # 出金金額(残額)から入金金額(残額)を減算
                blnc_tr_amt = round((blnc_tr_amt - blnc_dep), 3)

                blnc_dep = 0
                row_idx_dep += 1

            else:

                # 出金金額(残額)から為替差損益を算出
                exc_pos += blnc_tr_amt * rate_dep - blnc_tr_amt * rate_wit

                # 入金金額(残額)から出金金額(残額)を減算
                blnc_dep = round((blnc_dep - blnc_tr_amt), 3)

                break

        if blnc_dep <= 0:
            row_idx_dep += 1

        exc_pos = math.floor(exc_pos)

        df = pd.DataFrame({
              '日付': [str(row_tr_hist['日付']).replace('/', '')]
            , '出金金額(円)': [row_tr_hist['受渡金額(円)'] + exc_pos]
            , '受渡金額(円)': [row_tr_hist['受渡金額(円)']]
            , '為替差損益': [exc_pos *(-1)]
            , '摘要': [row_tr_hist['備考']]})

        df_buy_asset  = pd.concat([df_buy_asset, df], axis=0)

    return df_buy_asset

def get_df_incm_gain(df_stk_daw_usd: DataFrame, df_rate: DataFrame):

    df = df_stk_daw_usd.copy()
    df = df.drop(['区分', '通貨', '出金額'], axis=1)

    df = df[df['摘要'].str.contains('分配金')]
    df = df.sort_values(['入出金日', '入金額']) 
    df = df.reset_index(drop=True)

    df.rename(columns={'入出金日' : '日付'}, inplace=True)

    df = pd.merge(df, df_rate, how='left', on='日付')

    df['入金金額(円)'] = (df['入金額'] * df['当日レート']).agg(np.floor)

    return df