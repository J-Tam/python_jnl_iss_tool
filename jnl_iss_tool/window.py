# coding: UTF-8
import tkinter as tk
import json
import jnl_iss_tool.main_task as main_task
# import jnl_iss_tools.ui.jit01_exc_jnl.window as exc_jnl_ui
# import jnl_iss_tools.ui.jit02_svng_jnl.window as svng_jnl_ui
# import jnl_iss_tools.ui.jit03_stk_jnl.window as stk_jnl_ui
from jnl_iss_tool.main_bean import MainBean
import jnl_iss_tool.tk_utils as tk_utils
import jnl_iss_tool.const as const

import sys
sys.path.append("./jnl_iss_tools/")
# print(sys.path)

print(__name__, __package__)

# import subprocess
# subprocess.Popen('PAUSE', shell=True)

class ChkMkJnl():
    def __init__(self):
        # 作成仕訳
        self.val_xfr_exc = tk.BooleanVar(value=True)
        self.val_xfr_svng = tk.BooleanVar(value=True)
        self.val_intrst = tk.BooleanVar(value=True)
        self.val_pmt_tax = tk.BooleanVar(value=True)
        self.val_buy_asset = tk.BooleanVar(value=True)
        self.val_incm_gain = tk.BooleanVar(value=True)

class MainWindow():

    def __init__(self, main_window):

        # ** 関数定義 ** 参照ボタン（入出金明細（円））押下時処理
        def btn_ref_bnk_daw_jpy_click():
            tk_utils.chg_file_path(lfrm_bnk_jpy.children['txt_daw_jpy'], [("CSV", ".csv")])

        # ** 関数定義 ** 参照ボタン（入出金明細（米ドル））押下時処理
        def btnRefBnkDawUsd_click():
            tk_utils.chg_file_path(lfrm_bnk_usd.children['txt_daw_usd'], [("CSV", ".csv")])

        # ** 関数定義 ** 参照ボタン（入出金明細（外貨））押下時処理
        def btnRefStkDawFgn_click():
            tk_utils.chg_file_path(lfrm_stk_fgn.children['txt_daw_fgn'], [("CSV", ".csv")])

        # ** 関数定義 ** 参照ボタン（取引履歴）押下時処理
        def btn_ref_stk_tr_hist_click():
            tk_utils.chg_file_path(lfrm_stk_fgn.children['txt_stk_tr_hist'], [("CSV", ".csv")])

        # ** 関数定義 ** エクスポートファイル作成ボタン押下時処理
        def btn_exec_click():

            main_bean = MainBean(main_window, val_fmt, chk_mk_jnl)

            main_task.main(main_bean)

        # ** 関数定義 ** × ボタン押下時処理
        def btn_close_click():
            tk_utils.sub_window_close(main_window, None)

        def dummy():
            print(chk_mk_jnl.val_xfr_exc.get())
            print(chk_mk_jnl.val_xfr_svng.get())
            print(chk_mk_jnl.val_intrst.get())
            print(chk_mk_jnl.val_pmt_tax.get())
            print(chk_mk_jnl.val_buy_asset.get())
            print(chk_mk_jnl.val_incm_gain.get())
            print(val_fmt.get())


        # 初期処理
        main_window.title("証券口座取引仕訳作成ツール")
        main_window.geometry("560x660")
        
        # # × ボタンを定義
        main_window.protocol('WM_DELETE_WINDOW', btn_close_click)

        # 住信SBIネット銀行（円貨）
        lfrm_bnk_jpy = tk.LabelFrame(main_window, text='住信SBIネット銀行（円貨）', name='lfrm_bnk_jpy', width=150)
        lfrm_bnk_jpy.grid(row=1, column=1, padx=(25,0), pady=(20,0))
        lbl_bnk_daw_jpy = tk.Label(lfrm_bnk_jpy, name='lbl_daw_jpy', text='入出金明細').grid(row=1, column=1, sticky=tk.W, padx=(5,20), pady=(5,5))    
        txt_bnk_daw_jpy = tk.Entry(lfrm_bnk_jpy, width=60, name='txt_daw_jpy').grid(row=1, column=2, columnspan=3, sticky=tk.W)
        btn_ref_bnk_daw_jpy = tk.Button(lfrm_bnk_jpy, text='参照', command=btn_ref_bnk_daw_jpy_click).grid(row=1, column=5, padx=(5,8))
        lbl_bnk_bnk_nm_jpy = tk.Label(lfrm_bnk_jpy, name='lbl_bnk_nm_jpy', text='口座名').grid(row=2, column=1, sticky=tk.W, padx=(5,0), pady=(5,5))
        txt_bnk_bnk_nm_jpy = tk.Entry(lfrm_bnk_jpy, width=50, name='txt_bnk_nm_jpy').grid(row=2, column=2, columnspan=3, sticky=tk.W, pady=(5,5))

        # 住信SBIネット銀行（米ドル）
        lfrm_bnk_usd = tk.LabelFrame(main_window, text='住信SBIネット銀行（米ドル）', name='lfrm_bnk_usd', width=150)
        lfrm_bnk_usd.grid(row=2, column=1, padx=(25,0), pady=(10,0))
        lbl_bnk_daw_usd = tk.Label(lfrm_bnk_usd, name='lbl_daw_usd', text='入出金明細').grid(row=1, column=1, sticky=tk.W, padx=(5,20), pady=(5,5))    
        txt_bnk_daw_usd = tk.Entry(lfrm_bnk_usd, width=60, name='txt_daw_usd').grid(row=1, column=2, columnspan=3, sticky=tk.W)
        btn_ref_bnk_daw_usd = tk.Button(lfrm_bnk_usd, text='参照', command=btnRefBnkDawUsd_click).grid(row=1, column=5, padx=(5,8))
        lbl_bnk_bnk_nm_usd = tk.Label(lfrm_bnk_usd, name='lbl_bnk_nm_usd', text='口座名').grid(row=2, column=1, sticky=tk.W, padx=(5,0), pady=(5,5))
        txt_bnk_bnk_nm_usd = tk.Entry(lfrm_bnk_usd, width=50, name='txt_bnk_nm_usd').grid(row=2, column=2, columnspan=3, sticky=tk.W)
        lbl_blnc_usd = tk.Label(lfrm_bnk_usd, name='lbl_blnc_usd', text='現残高').grid(row=3, column=1, sticky=tk.W, padx=(5,2), pady=(5,5))    
        txt_blnc_usd = tk.Entry(lfrm_bnk_usd, width=20, name='txt_blnc_usd').grid(row=3, column=2, sticky=tk.W)
        lbl_dt_usd = tk.Label(lfrm_bnk_usd, name='lbl_eval_dt_usd', text='取得日').grid(row=3, column=3, sticky=tk.W, padx=(10,20), pady=(5,10)) 
        txt_dt_usd = tk.Entry(lfrm_bnk_usd, width=20, name='txt_eval_dt_usd').grid(row=3, column=4)

        # SBI証券（外貨）
        lfrm_stk_fgn = tk.LabelFrame(main_window, text='SBI証券（外貨）', name='lfrm_stk_fgn', width=150)
        lfrm_stk_fgn.grid(row=3, column=1, padx=(25,0), pady=(10,0))
        lbl_stk_daw_fgn = tk.Label(lfrm_stk_fgn, name='lbl_daw_fgn', text='入出金明細').grid(row=1, column=1, sticky=tk.W, padx=(5,20), pady=(5,5))    
        txt_stk_daw_fgn = tk.Entry(lfrm_stk_fgn, width=60, name='txt_daw_fgn').grid(row=1, column=2, columnspan=3, sticky=tk.W)
        btn_ref_stk_daw_fgn = tk.Button(lfrm_stk_fgn, text='参照', command=btnRefStkDawFgn_click).grid(row=1, column=5, padx=(5,8))
        lbl_stk_nm_fgn = tk.Label(lfrm_stk_fgn, name='lbl_stk_nm_fgn', text='口座名').grid(row=2, column=1, sticky=tk.W, padx=(5,0), pady=(5,5))
        txt_stk_nm_fgn = tk.Entry(lfrm_stk_fgn, width=50, name='txt_stk_nm_fgn').grid(row=2, column=2, columnspan=3, sticky=tk.W)
        lbl_blnc_fgn = tk.Label(lfrm_stk_fgn, name='lbl_blnc_fgn', text='現残高').grid(row=3, column=1, sticky=tk.W, padx=(5,2), pady=(5,5))    
        txt_blnc_fgn = tk.Entry(lfrm_stk_fgn, width=20, name='txt_blnc_fgn').grid(row=3, column=2, sticky=tk.W)
        lbl_eval_dt_fgn = tk.Label(lfrm_stk_fgn, name='lbl_eval_dt_fgn', text='取得日').grid(row=3, column=3, sticky=tk.W, padx=(10,20), pady=(5,10)) 
        txt_dt_fgn = tk.Entry(lfrm_stk_fgn, width=20, name='txt_eval_dt_fgn').grid(row=3, column=4)
        lbl_stk_tr_hist = tk.Label(lfrm_stk_fgn, name='lbl_tr_hist', text='取引履歴').grid(row=4, column=1, sticky=tk.W, padx=(5,20), pady=5)    
        txt_stk_tr_hist = tk.Entry(lfrm_stk_fgn, width=60, name='txt_tr_hist').grid(row=4, column=2, columnspan=3, sticky=tk.W)
        btn_ref_stk_tr_hist = tk.Button(lfrm_stk_fgn, text='参照', command=btn_ref_stk_tr_hist_click).grid(row=4, column=5, padx=(5,8), pady=(5,10))

        # 出力情報
        lfrm_out_conf = tk.LabelFrame(main_window, text='出力情報', name='lfrm_out_conf', width=150)
        lfrm_out_conf.grid(row=4, column=1, padx=(25,0), pady=(10,0), sticky=tk.W)
        # チェック変数
        val_fmt = tk.IntVar(value=const.SEL_YAYOI)
        lbl_fmt = tk.Label(lfrm_out_conf, name='lbl_fmt', text='出力フォーマット').grid(row=1, column=1, sticky=tk.W, padx=(5,0), pady=5)    
        rdo_fmt_mf = tk.Radiobutton( lfrm_out_conf, name='rdo_fmt_mf', variable=val_fmt, value=const.SEL_MF, text='マネーフォワード').grid(row=1, column=2, padx=(0,0), pady=(5,5))
        rdo_fmt_yayoi = tk.Radiobutton(lfrm_out_conf, variable=val_fmt, value=const.SEL_YAYOI, text='弥生会計').grid(row=1, column=3, padx=(5,20), pady=(5,0))
        lbl_rgstr_nm = tk.Label(lfrm_out_conf, name='lbl_rgstr_nm', text='作成者').grid(row=2, column=1, sticky=tk.W, padx=(5,20), pady=(5,5))    
        txt_rgstr_nm = tk.Entry(lfrm_out_conf, width=20, name='txt_rgstr_nm').grid(row=2, column=2, padx=(23,0), pady=(5,10))

        # 作成仕訳
        chk_mk_jnl = ChkMkJnl()
        lfrm_mk_jnl = tk.LabelFrame(main_window, text='作成仕訳', name='lfrm_mk_jnl', width=150)
        lfrm_mk_jnl.grid(row=5, column=1, padx=(25,0), pady=(10,0), sticky=tk.W)
        chk_jnl_xfr_exc = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_xfr_exc', text=const.JNL_NM_XFR_EXC, variable=chk_mk_jnl.val_xfr_exc).grid(row=1, column=1, padx=(5,0), pady=(5,5))
        chk_jnl_xfr_svng = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_xfr_svng', text=const.JNL_NM_XFR_SVNG, variable=chk_mk_jnl.val_xfr_svng).grid(row=1, column=2, padx=(5,0), pady=(5,5))
        chk_jnl_intrst = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_intrst', text=const.JNL_NM_INTRST, variable=chk_mk_jnl.val_intrst).grid(row=1, column=3, padx=(5,30), pady=(5,5))
        chk_jnl_tax = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_pmt_tax', text=const.JNL_NM_PMT_TAX, variable=chk_mk_jnl.val_pmt_tax).grid(row=2, column=1, sticky=tk.W, padx=(5,0), pady=(5,5))
        chk_jnl_buy_asset = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_buy_asset', text=const.JNL_NM_BUY_ASSET, variable=chk_mk_jnl.val_buy_asset).grid(row=2, column=2, sticky=tk.W, padx=(5,0), pady=(5,5))
        chk_jnl_incm_gain = tk.Checkbutton(lfrm_mk_jnl, name='chk_jnl_incm_gain', text=const.JNL_NM_INCM_GAIN, variable=chk_mk_jnl.val_incm_gain).grid(row=2, column=3, sticky=tk.W, padx=(5,0), pady=(5,5))
        btn_exec = tk.Button(main_window, text='エクスポートファイル作成', command=btn_exec_click).grid(row=6, column=1, padx=(50,0), pady=(15,5))

        # ** メインフォーム 初期値設定 **
        json_file = open('config/settings.json', 'r', encoding="utf-8_sig")
        json_data = json.load(json_file)

        lfrm_bnk_jpy.children['txt_daw_jpy'].insert(tk.END, json_data["common-input-info"]["住信SBI-入出金明細（円貨）パス"])
        lfrm_bnk_jpy.children['txt_bnk_nm_jpy'].insert(tk.END, json_data["common-input-info"]["住信SBI-円貨口座名"])
        lfrm_bnk_usd.children['txt_daw_usd'].insert(tk.END, json_data["common-input-info"]["住信SBI-入出金明細（米ドル）パス"])
        lfrm_bnk_usd.children['txt_bnk_nm_usd'].insert(tk.END, json_data["common-input-info"]["住信SBI-外貨口座名"])
        lfrm_stk_fgn.children['txt_daw_fgn'].insert(tk.END, json_data["common-input-info"]["SBI証券-入出金明細（米ドル）パス"])
        lfrm_stk_fgn.children['txt_stk_nm_fgn'].insert(tk.END, json_data["common-input-info"]["SBI証券-口座名"])
        lfrm_stk_fgn.children['txt_tr_hist'].insert(tk.END, json_data["common-input-info"]["SBI証券-取引履歴パス"])
        lfrm_out_conf.children['txt_rgstr_nm'].insert(tk.END, json_data["common-input-info"]["作成者"])

        return

def main():

    main_window = tk.Tk()
    app = MainWindow(main_window)
    main_window.mainloop()


if __name__ == "__main__":

    main()