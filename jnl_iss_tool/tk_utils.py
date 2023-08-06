# coding: UTF-8
import tkinter as tk
from tkinter import filedialog as fd

def chg_file_path(target: tk.Entry, file_types: str):
    """
    ファイル選択ダイアログを開き
    選択したパスを指定のフォームに上書きする

    Parameters
    ----------
    target : tk.Entry
        テキストフォーム
    file_types : str
        拡張子

    Returns
    -------
    なし

    """

    path = fd.askopenfilename(filetypes=file_types)

    # ファイル未選択の場合は終了
    if len(path) == 0:
        return

    # 指定したパスに上書き
    target.delete(0, tk.END)
    target.insert(tk.END, path)
    return

def sub_window_close(sub_window: tk.Tk, parent_window: tk.Tk):
    """
    サブウィンドウをクローズして親ウィンドウを表示する

    Parameters
    ----------
    sub_window : tk.Tk
        サブウィンドウ
    parent_window : tk.Tk
        親ウィンドウ

    Returns
    -------
    なし

    """

    sub_window.destroy()

    if parent_window is None:
        return
    else:
        parent_window.deiconify()
    
    return