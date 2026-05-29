# ============================================================
# main.py — Uygulama Giriş Noktası
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================

import tkinter as tk
from gui import AlbumGeneratorApp


def main():
    """Ana pencereyi oluşturur ve uygulamayı başlatır."""
    root = tk.Tk()

    # Uygulama simgesini ayarla (isteğe bağlı, yoksa hata vermez)
    try:
        root.iconbitmap(default="")
    except tk.TclError:
        pass

    # Uygulamayı oluştur ve çalıştır
    app = AlbumGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


