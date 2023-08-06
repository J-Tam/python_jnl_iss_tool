# coding: UTF-8
import jnl_iss_tool.const as const

class ExcDiffBean():
    def __init__(self, diff_amt: int):
        """
        為替差損益を判定して仕訳情報を取得する

        Parameters
        ----------
        self : 
            
        diff_amt : int
            為替差損益

        Returns
        -------
        なし

        """
        if diff_amt < 0:
            self.dr_acct_nm = const.ACCT_NM_KAWASESASON
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.cr_acct_nm = const.ACCT_NM_BLANK
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.profit_amt = 0
            self.loss_amt = -1 * diff_amt
        else:
            self.dr_acct_nm = const.ACCT_NM_BLANK
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.cr_acct_nm = const.ACCT_NM_KAWASESAEKI
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.profit_amt = diff_amt
            self.loss_amt = 0
        
        return

class AcctBean():
    def __init__(self, jnl_nm: str):
        """
        仕訳名に応じた勘定科目をセットする

        Parameters
        ----------
        self : 
            
        jnl_nm : str
            仕訳名

        Returns
        -------
        なし

        """        

        if jnl_nm == const.JNL_NM_XFR_EXC:

            self.dr_acct_nm = const.ACCT_NM_GAIKAYOKIN
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_SBI_BNK_USD
            self.cr_acct_nm = const.ACCT_NM_FUSTUYOKIN
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_SBI_BNK_JPY

        elif jnl_nm == const.JNL_NM_XFR_SVNG:

            self.dr_acct_nm = const.ACCT_NM_AZUKEKIN
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_SBI_STK
            self.cr_acct_nm = const.ACCT_NM_GAIKAYOKIN
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_SBI_BNK_USD

        elif jnl_nm == const.JNL_NM_PMT_TAX:

            self.dr_acct_nm = const.ACCT_NM_SOZEIKOKA
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.cr_acct_nm = const.ACCT_NM_GAIKAYOKIN
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_SBI_BNK_USD

        elif jnl_nm == const.JNL_NM_INTRST:

            self.dr_acct_nm = const.ACCT_NM_GAIKAYOKIN
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_SBI_BNK_USD
            self.cr_acct_nm = const.ACCT_NM_UKETORIRISOKU
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_BLANK

        elif jnl_nm == const.JNL_NM_BUY_ASSET:

            self.dr_acct_nm = const.ACCT_NM_YUKASHOKEN
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_BLANK
            self.cr_acct_nm = const.ACCT_NM_AZUKEKIN
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_SBI_STK

        elif jnl_nm == const.JNL_NM_INCM_GAIN:

            self.dr_acct_nm = const.ACCT_NM_AZUKEKIN
            self.dr_sub_acct_nm = const.SUB_ACCT_NM_SBI_STK
            self.cr_acct_nm = const.ACCT_NM_UKETORIHAITO
            self.cr_sub_acct_nm = const.SUB_ACCT_NM_BLANK

        return

