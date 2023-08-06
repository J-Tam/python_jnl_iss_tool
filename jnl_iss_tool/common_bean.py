# # coding: UTF-8
# from jnl_iss_tools.const.jit99_common.const import Const

# class Item():
#     def __init__(self, title, val):
#         self.title = title
#         self.value = val
#         return

# class ExcDiffBean():
#     def __init__(self):
#         self.dr_acct_nm = ''
#         self.cr_acct_nm = ''
#         self.profit_amt = 0
#         self.loss_amt = 0
#         return

#     def getExcDiff(self, diff_amt: int):
#         """
#         為替差損益を判定して仕訳情報を取得する

#         Parameters
#         ----------
#         self : 
            
#         diff_amt : int
#             為替差損益

#         Returns
#         -------
#         なし

#         """
#         if diff_amt < 0:
#             self.dr_acct_nm = ''
#             self.cr_acct_nm = Const.ACCT_NM_KAWASESAEKI
#             self.profit_amt = -1 * diff_amt
#             self.loss_amt = 0
#         else:
#             self.dr_acct_nm = Const.ACCT_NM_KAWASESASON
#             self.cr_acct_nm = ''
#             self.profit_amt = 0
#             self.loss_amt = diff_amt
        
#         return

# class AcctBean():
#     def __init__(self):
#         self.dr_acct_nm = ''
#         self.dr_sub_acct_nm = ''
#         self.cr_acct_nm = ''
#         self.cr_sub_acct_nm = ''
#         return

#     def set_acct_nm(self, content):
#         return

# class AcctBeanBnkJpy(AcctBean):
#     def __init__(self):
#         super().__init__()

#     def set_acct_nm(self, content):
#         if '積立　米ドル' in content:
#             self.dr_acct_nm = Const.ACCT_NM_GAIKAYOKIN
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_BNK_USD
#             self.dr_acct_nm = Const.ACCT_NM_FUSTUYOKIN
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_BNK_JPY

# class AcctBeanBnkUsd(AcctBean):
#     def __init__(self):
#         super().__init__()

#     def set_acct_nm(self, content):
#         if '振替　ＳＢＩ証券' in content:
#             self.dr_acct_nm = Const.ACCT_NM_AZUKEKIN
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_STK
#             self.cr_acct_nm = Const.ACCT_NM_GAIKAYOKIN
#             self.cr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_BNK_USD

#         elif '国税' in content:
#             self.dr_acct_nm = Const.ACCT_NM_SOZEIKOKA
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_BLANK
#             self.cr_acct_nm = Const.ACCT_NM_GAIKAYOKIN
#             self.cr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_BNK_USD

#         return

# class AcctBeanStk(AcctBean):
#     def __init__(self):
#         super().__init__()

#     def set_acct_nm(self, content):
#         if '分配金' in content:
#             self.dr_acct_nm = Const.ACCT_NM_AZUKEKIN
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_STK
#             self.cr_acct_nm = Const.ACCT_NM_UKETORIHAITO
#             self.cr_sub_acct_nm = Const.SUB_ACCT_NM_BLANK

#         if '有価証券購入' in content:
#             self.dr_acct_nm = Const.ACCT_NM_YUKASHOKEN
#             self.dr_sub_acct_nm = Const.SUB_ACCT_NM_BLANK
#             self.cr_acct_nm = Const.ACCT_NM_AZUKEKIN
#             self.cr_sub_acct_nm = Const.SUB_ACCT_NM_SBI_STK
