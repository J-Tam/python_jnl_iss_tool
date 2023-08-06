# coding: UTF-8
import tkinter as tk
# import jnl_iss_tool.const as const

def get_text_item(main_window: tk.Tk, parent_nm: str, self_base_nm: str): 

    parent = main_window.children[parent_nm].cget('text')
    title = main_window.children[parent_nm].children['lbl_' + self_base_nm].cget('text')
    value = main_window.children[parent_nm].children['txt_' + self_base_nm].get()

    item = Item(parent, title, value)
    return item

def get_rdo_item(main_window: tk.Tk, parent_nm: str, self_base_nm: str, self_rdo_value: tk.IntVar): 

    parent = main_window.children[parent_nm].cget('text')
    title = main_window.children[parent_nm].children['lbl_' + self_base_nm].cget('text')
    value = self_rdo_value.get()

    item = Item(parent, title, value)
    return item

def get_chk_item(main_window: tk.Tk, parent_nm: str, self_base_nm: str, self_chk_value: tk.BooleanVar): 

    parent = main_window.children[parent_nm].cget('text')
    title = main_window.children[parent_nm].children['chk_' + self_base_nm].cget('text')
    value = self_chk_value.get()

    item = Item(parent, title, value)
    return item

class Item():
    def __init__(self, parent: str, title: str, value: str):
        self.parent = parent
        self.title = title
        self.value = value
        return

# class LfrmBnkJpyBean():
#     def __init__(self, lfrm_bnk_jpy):
#         self.title = lfrm_bnk_jpy.cget('text')
#         self.daw_path = common_bean.Item(lfrm_bnk_jpy.children['lbl_daw_jpy'].cget('text'), lfrm_bnk_jpy.children['txt_daw_jpy'].get())
#         self.bnk_nm = common_bean.Item(lfrm_bnk_jpy.children['lbl_bnk_nm_jpy'].cget('text'), lfrm_bnk_jpy.children['txt_bnk_nm_jpy'].get())

# class LfrmBnkUsdBean():
#     def __init__(self, lfrm_bnk_usd):
#         self.title = lfrm_bnk_usd.cget('text')
#         self.daw_path = common_bean.Item(lfrm_bnk_usd.children['lbl_daw_usd'].cget('text'), lfrm_bnk_usd.children['txt_daw_usd'].get())
#         self.bnk_nm = common_bean.Item(lfrm_bnk_usd.children['lbl_bnk_nm_usd'].cget('text'), lfrm_bnk_usd.children['txt_bnk_nm_usd'].get())
#         self.blnc = common_bean.Item(lfrm_bnk_usd.children['lbl_blnc_usd'].cget('text'), lfrm_bnk_usd.children['txt_blnc_usd'].get())
#         self.eval_dt = common_bean.Item(lfrm_bnk_usd.children['txt_eval_dt_usd'].cget('text'), lfrm_bnk_usd.children['txt_eval_dt_usd'].get())

# class LfrmStkFgnBean():
#     def __init__(self, lfrm_stk_fgn):

#         self.title = lfrm_stk_fgn.cget('text')
#         self.daw_path = common_bean.Item(lfrm_stk_fgn.children['lbl_daw_fgn'].cget('text'), lfrm_stk_fgn.children['txt_daw_fgn'].get())
#         self.stk_nm = common_bean.Item(lfrm_stk_fgn.children['lbl_stk_nm_fgn'].cget('text'), lfrm_stk_fgn.children['txt_stk_nm_fgn'].get())
#         self.blnc = common_bean.Item(lfrm_stk_fgn.children['lbl_blnc_fgn'].cget('text'), lfrm_stk_fgn.children['txt_blnc_fgn'].get())
#         self.eval_dt = common_bean.Item(lfrm_stk_fgn.children['lbl_eval_dt_fgn'].cget('text'), lfrm_stk_fgn.children['txt_eval_dt_fgn'].get())
#         self.tr_hist_path = common_bean.Item(lfrm_stk_fgn.children['lbl_tr_hist'].cget('text'), lfrm_stk_fgn.children['txt_tr_hist'].get())

# class LfrmOutConfBean():
#     def __init__(self, lfrm_out_conf, val_fmt: tk.IntVar):

#         self.title = lfrm_out_conf.cget('text')
#         self.jnl_fmt = common_bean.Item(lfrm_out_conf.children['lbl_fmt'].cget('text'), val_fmt.get())
#         self.rgstr_nm = common_bean.Item(lfrm_out_conf.children['lbl_rgstr_nm'].cget('text'), lfrm_out_conf.children['txt_rgstr_nm'].get())

# class LfrmOutJnlBean():
#     def __init__(self, lfrm_mk_jnl, chk_mk_jnl: ChkMkJnl):
#         self.title = lfrm_mk_jnl.cget('text')
#         self.chk_jnl_xfr_exc = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_xfr_exc'].cget('text'), chk_mk_jnl.val_xfr_exc.get())
#         self.chk_jnl_svng = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_svng'].cget('text'), chk_mk_jnl.val_svng.get())
#         self.chk_jnl_intrst = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_intrst'].cget('text'), chk_mk_jnl.val_intrst.get())
#         self.chk_jnl_tax = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_tax'].cget('text'), chk_mk_jnl.val_tax.get())
#         self.chk_jnl_buy_stk = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_buy_stk'].cget('text'), chk_mk_jnl.val_buy_stk.get())
#         self.chk_jnl_incm = common_bean.Item(lfrm_mk_jnl.children['chk_jnl_incm'].cget('text'), chk_mk_jnl.val_incm.get())

class MainBean():
    def __init__(self, main_window, val_fmt, chk_mk_jnl):

        self.bnk_jpy_daw_path = get_text_item(main_window, 'lfrm_bnk_jpy', 'daw_jpy')
        self.bnk_jpy_bnk_nm = get_text_item(main_window, 'lfrm_bnk_jpy', 'bnk_nm_jpy')

        self.bnk_usd_daw_path = get_text_item(main_window, 'lfrm_bnk_usd', 'daw_usd')
        self.bnk_usd_bnk_nm = get_text_item(main_window, 'lfrm_bnk_usd', 'bnk_nm_usd')
        self.bnk_usd_blnc = get_text_item(main_window, 'lfrm_bnk_usd', 'blnc_usd')
        self.bnk_usd_eval_dt = get_text_item(main_window, 'lfrm_bnk_usd', 'eval_dt_usd')

        self.stk_fgn_daw_path = get_text_item(main_window, 'lfrm_stk_fgn', 'daw_fgn')
        self.stk_fgn_stk_nm = get_text_item(main_window, 'lfrm_stk_fgn', 'stk_nm_fgn')
        self.stk_fgn_blnc = get_text_item(main_window, 'lfrm_stk_fgn', 'blnc_fgn')
        self.stk_fgn_eval_dt = get_text_item(main_window, 'lfrm_stk_fgn', 'eval_dt_fgn')
        self.stk_fgn_tr_hist_path = get_text_item(main_window, 'lfrm_stk_fgn', 'tr_hist')

        self.out_conf_fmt = get_rdo_item(main_window, 'lfrm_out_conf', 'fmt', val_fmt)
        self.out_conf_rgstr_nm = get_text_item(main_window, 'lfrm_out_conf', 'rgstr_nm')

        self.mk_jnl_xfr_exc = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_xfr_exc', chk_mk_jnl.val_xfr_exc)
        self.mk_jnl_xfr_svng = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_xfr_svng', chk_mk_jnl.val_xfr_svng)
        self.mk_jnl_intrst = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_intrst', chk_mk_jnl.val_intrst)
        self.mk_jnl_pmt_tax = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_pmt_tax', chk_mk_jnl.val_pmt_tax)
        self.mk_jnl_buy_asset = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_buy_asset', chk_mk_jnl.val_buy_asset)
        self.mk_jnl_incm_gain = get_chk_item(main_window, 'lfrm_mk_jnl', 'jnl_incm_gain', chk_mk_jnl.val_incm_gain)

        # # 住信SBIネット銀行（円貨）
        # self.bnk_jpy = LfrmBnkJpyBean(main_window.children['lfrm_bnk_jpy'])

        # # 住信SBIネット銀行（米ドル）
        # self.bnk_usd = LfrmBnkUsdBean(main_window.children['lfrm_bnk_usd'])

        # # SBI証券
        # self.stk_fgn = LfrmStkFgnBean(main_window.children['lfrm_stk_fgn'])

        # # 出力情報
        # self.out_conf = LfrmOutConfBean(main_window.children['lfrm_out_conf'], val_fmt)
        
        # # 作成仕訳
        # self.out_jnl = LfrmOutJnlBean(main_window.children['lfrm_mk_jnl'], chk_mk_jnl)


