# ============================================================
# gui.py — Tkinter Arayüzü (Mavi / Beyaz / Siyah Tema)
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================
# GEREKSİNİM 2: Tkinter + ttk widget'ları
# GEREKSİNİM 3: Varsayılan değerli giriş widget'ları
# GEREKSİNİM 7: Spotify tarzı düzen, Dinle butonları
# GEREKSİNİM 8: JSON + PNG olarak dışa aktarma
# GEREKSİNİM 9: Arka plan iş parçacığı + durum güncellemeleri
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import webbrowser
import json
import os

from config import (
    GENRES, ERAS,
    DEFAULT_GENRE, DEFAULT_ERA,
    DEFAULT_TRACK_COUNT, MIN_TRACK_COUNT, MAX_TRACK_COUNT,
)
from gemini_api import query_gemini
from lastfm_api import build_tracklist
from image_gen import generate_cover


# ──────────────────────────────────────────────────────────────
# Renk Paleti — Mavi / Beyaz / Siyah
# ──────────────────────────────────────────────────────────────
BLACK          = "#0A0A0A"
BLACK_LIGHT    = "#111111"
BLACK_CARD     = "#161616"
BLACK_FIELD    = "#1C1C1C"
BLACK_TRACK_A  = "#131313"
BLACK_TRACK_B  = "#1A1A1A"
BLACK_HOVER    = "#222222"

BLUE           = "#2E86DE"
BLUE_LIGHT     = "#54A0FF"
BLUE_BRIGHT    = "#74B9FF"
BLUE_DARK      = "#1B5FAD"
BLUE_DIM       = "#183D6E"

WHITE          = "#FFFFFF"
WHITE_SOFT     = "#F0F2F5"
WHITE_MID      = "#B8BEC8"
WHITE_DIM      = "#6C7380"
WHITE_FAINT    = "#3A3E48"

BORDER         = "#2A2D35"
ERROR_RED      = "#E74C3C"
AMBER          = "#F5A623"

TAG_COLORS = [
    ("#0D1A2E", "#54A0FF"),
    ("#0D2530", "#48DBFB"),
    ("#0D1F30", "#74B9FF"),
    ("#101D30", "#A3CBF1"),
    ("#0D2030", "#6BB5FF"),
    ("#0D2828", "#55D6C2"),
]


class AlbumGeneratorApp:
    """PDA-226 Kurgusal Albüm Oluşturucu ana uygulama sınıfı."""

    def __init__(self, root):
        self.root = root
        self.root.title("PDA-226 • Album Cover Studio")
        self.root.geometry("1200x740")
        self.root.minsize(1050, 650)
        self.root.configure(bg=BLACK)

        # Uygulama durumu
        self.album_data = None
        self.tracklist = None
        self.cover_image = None
        self.cover_photo = None
        self.is_generating = False
        self._photo_refs = []

        self._setup_style()
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    # Tema ve Stil
    # ──────────────────────────────────────────────────────────
    def _setup_style(self):
        """ttk stillerini yapılandır — mavi/beyaz/siyah."""
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("Panel.TFrame", background=BLACK_LIGHT)
        s.configure("Deep.TFrame",  background=BLACK)

        # Açılır kutu (Combobox)
        s.configure("Accent.TCombobox",
                     fieldbackground=BLACK_FIELD, background=BLACK_FIELD,
                     foreground=WHITE, arrowcolor=BLUE_LIGHT,
                     borderwidth=1, relief="flat", padding=6)
        s.map("Accent.TCombobox",
              fieldbackground=[("readonly", BLACK_FIELD)],
              foreground=[("readonly", WHITE)],
              selectbackground=[("readonly", BLACK_FIELD)],
              selectforeground=[("readonly", WHITE)])

        # Sayı kutusu (Spinbox)
        s.configure("Accent.TSpinbox",
                     fieldbackground=BLACK_FIELD, background=BLACK_FIELD,
                     foreground=WHITE, arrowcolor=BLUE_LIGHT,
                     borderwidth=1, padding=4)

        # Oluştur butonu — düz mavi
        s.configure("Generate.TButton",
                     background=BLUE, foreground=WHITE,
                     font=("Segoe UI", 11, "bold"),
                     borderwidth=0, padding=(20, 13))
        s.map("Generate.TButton",
              background=[("active", BLUE_LIGHT), ("disabled", WHITE_FAINT)])

        # Kaydet butonu — koyu mavi
        s.configure("Save.TButton",
                     background=BLUE_DARK, foreground=WHITE,
                     font=("Segoe UI", 10, "bold"),
                     borderwidth=0, padding=(16, 11))
        s.map("Save.TButton",
              background=[("active", BLUE), ("disabled", WHITE_FAINT)])

    # ──────────────────────────────────────────────────────────
    # Arayüz Oluşturma
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        wrapper = ttk.Frame(self.root, style="Deep.TFrame")
        wrapper.pack(fill=tk.BOTH, expand=True)

        self._build_left(wrapper)
        tk.Frame(wrapper, width=1, bg=BORDER).pack(side=tk.LEFT, fill=tk.Y)
        self._build_right(wrapper)

    # ──────────────────────────────────────────────────────────
    # Sol Panel
    # ──────────────────────────────────────────────────────────
    def _build_left(self, parent):
        left = ttk.Frame(parent, style="Panel.TFrame", width=380)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        pad = tk.Frame(left, bg=BLACK_LIGHT)
        pad.pack(fill=tk.BOTH, expand=True, padx=26, pady=26)

        # ── Başlık ──
        row = tk.Frame(pad, bg=BLACK_LIGHT)
        row.pack(anchor="w", fill=tk.X)
        tk.Label(row, text="♪", bg=BLACK_LIGHT, fg=BLUE_LIGHT,
                 font=("Segoe UI", 22)).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(row, text="Album Cover Studio", bg=BLACK_LIGHT,
                 fg=WHITE, font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)

        tk.Label(pad, text="Describe your mood, enjoy the generated tracklist.",
                 bg=BLACK_LIGHT, fg=WHITE_MID,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 20))

        # Mavi vurgu çizgisi
        tk.Frame(pad, height=3, bg=BLUE).pack(fill=tk.X, pady=(0, 22))

        # ── Ruh Hali ──
        self._label(pad, "Your Mood (English or Turkish)")

        self.journal_text = tk.Text(
            pad, height=6,
            bg=BLACK_FIELD, fg=WHITE_SOFT,
            insertbackground=BLUE_LIGHT,
            font=("Segoe UI", 10),
            relief=tk.FLAT, padx=12, pady=10,
            wrap=tk.WORD, borderwidth=0,
            highlightthickness=2,
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            selectbackground=BLUE_DIM,
            selectforeground=WHITE,
            spacing1=2, spacing3=2,
        )
        self.journal_text.pack(fill=tk.X, pady=(0, 18))
        self._set_ph()
        self.journal_text.bind("<FocusIn>", self._ph_in)
        self.journal_text.bind("<FocusOut>", self._ph_out)

        # ── Tür ──
        self._label(pad, "Genre")
        self.genre_var = tk.StringVar(value=DEFAULT_GENRE)
        ttk.Combobox(pad, textvariable=self.genre_var,
                     values=GENRES, state="readonly",
                     style="Accent.TCombobox",
                     font=("Segoe UI", 10)).pack(fill=tk.X, pady=(0, 14))

        # ── Dönem ──
        self._label(pad, "Era")
        self.era_var = tk.StringVar(value=DEFAULT_ERA)
        ttk.Combobox(pad, textvariable=self.era_var,
                     values=ERAS, state="readonly",
                     style="Accent.TCombobox",
                     font=("Segoe UI", 10)).pack(fill=tk.X, pady=(0, 14))

        # ── Parça Sayısı ──
        self._label(pad, "Track Count")
        self.track_count_var = tk.IntVar(value=DEFAULT_TRACK_COUNT)
        ttk.Spinbox(pad, from_=MIN_TRACK_COUNT, to=MAX_TRACK_COUNT,
                    textvariable=self.track_count_var,
                    state="readonly",
                    style="Accent.TSpinbox",
                    font=("Segoe UI", 10),
                    width=6).pack(anchor="w", pady=(0, 28))

        # ── Oluştur ──
        self.gen_btn = ttk.Button(pad, text="GENERATE ALBUM",
                                  style="Generate.TButton",
                                  command=self.generate_album)
        self.gen_btn.pack(fill=tk.X, pady=(0, 12))

        # ── Durum ──
        self.status_lbl = tk.Label(pad, text="Ready",
                                   bg=BLACK_LIGHT, fg=WHITE_DIM,
                                   font=("Segoe UI", 8, "italic"), anchor="w")
        self.status_lbl.pack(anchor="w", fill=tk.X)

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg=BLACK_LIGHT, fg=BLUE_LIGHT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))

    # ──────────────────────────────────────────────────────────
    # Sağ Panel
    # ──────────────────────────────────────────────────────────
    def _build_right(self, parent):
        self.right = ttk.Frame(parent, style="Deep.TFrame")
        self.right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Karşılama ekranı
        self.welcome = tk.Frame(self.right, bg=BLACK)
        self.welcome.pack(fill=tk.BOTH, expand=True)
        c = tk.Frame(self.welcome, bg=BLACK)
        c.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(c, text="🎧", bg=BLACK, font=("Segoe UI", 52)).pack()
        tk.Label(c, text="Generated tracklist will be shown here.",
                 bg=BLACK, fg=WHITE_MID,
                 font=("Segoe UI", 13)).pack(pady=(14, 4))
        tk.Label(c, text="Write your mood → choose parameters → Generate!",
                 bg=BLACK, fg=WHITE_DIM,
                 font=("Segoe UI", 9, "italic")).pack()

        # Albüm çerçevesi (gizli)
        self.album_frame = tk.Frame(self.right, bg=BLACK)
        self.r_canvas = tk.Canvas(self.album_frame, bg=BLACK,
                                   highlightthickness=0, bd=0)
        self.r_scroll = ttk.Scrollbar(self.album_frame, orient="vertical",
                                       command=self.r_canvas.yview)
        self.r_inner = tk.Frame(self.r_canvas, bg=BLACK)
        self.r_inner.bind("<Configure>",
                          lambda e: self.r_canvas.configure(
                              scrollregion=self.r_canvas.bbox("all")))
        self.r_canvas.create_window((0, 0), window=self.r_inner, anchor="nw")
        self.r_canvas.configure(yscrollcommand=self.r_scroll.set)
        self.r_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.r_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.r_canvas.bind("<Enter>", lambda e: self.r_canvas.bind_all(
            "<MouseWheel>", lambda ev: self.r_canvas.yview_scroll(
                int(-1 * (ev.delta / 120)), "units")))
        self.r_canvas.bind("<Leave>",
                           lambda e: self.r_canvas.unbind_all("<MouseWheel>"))

    # ──────────────────────────────────────────────────────────
    # Yer Tutucu Metin
    # ──────────────────────────────────────────────────────────
    _PH = "I was looking at the sea in Izmir. It was raining softly, and an old song was playing..."

    def _set_ph(self):
        self.journal_text.insert("1.0", self._PH)
        self.journal_text.config(fg=WHITE_DIM)

    def _ph_in(self, e):
        if self.journal_text.get("1.0", tk.END).strip() == self._PH:
            self.journal_text.delete("1.0", tk.END)
            self.journal_text.config(fg=WHITE_SOFT)

    def _ph_out(self, e):
        if not self.journal_text.get("1.0", tk.END).strip():
            self._set_ph()

    # ──────────────────────────────────────────────────────────
    # Oluştur (GEREKSİNİM 9)
    # ──────────────────────────────────────────────────────────
    def generate_album(self):
        """Arka plan iş parçacığında albüm oluşturmayı başlatır."""
        if self.is_generating:
            return
        journal = self.journal_text.get("1.0", tk.END).strip()
        if not journal or journal == self._PH:
            messagebox.showwarning("Input Required",
                                   "Please write a journal entry or mood description.")
            return
        genre = self.genre_var.get()
        era = self.era_var.get()
        try:
            tc = self.track_count_var.get()
        except tk.TclError:
            tc = DEFAULT_TRACK_COUNT
        # Güvenlik: değeri izin verilen aralığa sınırla
        tc = max(MIN_TRACK_COUNT, min(MAX_TRACK_COUNT, tc))

        self.is_generating = True
        self.gen_btn.config(state="disabled")
        self._status("✨ Gemini is thinking...", AMBER)

        threading.Thread(target=self._worker,
                         args=(journal, genre, era, tc),
                         daemon=True).start()

    def _worker(self, journal, genre, era, tc):
        try:
            self.root.after(0, self._status, "✨ Gemini is thinking...", AMBER)
            data = query_gemini(journal, genre, era, tc)

            self.root.after(0, self._status,
                           "🎵 Fetching tracks from Last.fm...", AMBER)
            tags = data.get("lastfm_tags", [])
            tracks = build_tracklist(tags, tc)

            self.root.after(0, self._status,
                           "🎨 Generating cover art...", AMBER)
            prompt = data.get("cover_prompt", "abstract album cover art")
            img = generate_cover(prompt, genre)

            self.root.after(0, self._done, data, tracks, img)
        except Exception as ex:
            self.root.after(0, self._error, str(ex))

    def _done(self, data, tracks, img):
        self.album_data, self.tracklist, self.cover_image = data, tracks, img
        self.is_generating = False
        self.gen_btn.config(state="normal")
        self._show_album(data, tracks, img)
        self._status(f"✓ {len(tracks)} real songs loaded", BLUE_LIGHT)

    def _error(self, msg):
        self.is_generating = False
        self.gen_btn.config(state="normal")
        self._status(f"✗ {msg}", ERROR_RED)
        messagebox.showerror("Error", msg)

    # ──────────────────────────────────────────────────────────
    # Albümü Göster (GEREKSİNİM 7)
    # ──────────────────────────────────────────────────────────
    def _show_album(self, data, tracks, img):
        self.welcome.pack_forget()
        self.album_frame.pack(fill=tk.BOTH, expand=True)

        for w in self.r_inner.winfo_children():
            w.destroy()
        self._photo_refs.clear()

        body = tk.Frame(self.r_inner, bg=BLACK)
        body.pack(fill=tk.BOTH, expand=True, padx=34, pady=24)

        # ═══════════ Başlık: Kapak + Bilgi ═══════════
        hdr = tk.Frame(body, bg=BLACK)
        hdr.pack(fill=tk.X, pady=(0, 18))

        # Mavi kenarlıklı kapak görseli
        sz = 210
        bordered = Image.new("RGB", (sz + 6, sz + 6), BLUE)
        resized = img.resize((sz, sz), Image.LANCZOS)
        bordered.paste(resized, (3, 3))
        self.cover_photo = ImageTk.PhotoImage(bordered)
        self._photo_refs.append(self.cover_photo)

        tk.Label(hdr, image=self.cover_photo, bg=BLACK, bd=0).pack(
            side=tk.LEFT, padx=(0, 28))

        info = tk.Frame(hdr, bg=BLACK)
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=6)

        # Rozet
        tk.Label(info, text="  CURATED PLAYLIST  ", bg=BLUE_DARK,
                 fg=WHITE, font=("Segoe UI", 7, "bold"),
                 padx=6, pady=2).pack(anchor="w")

        # Albüm adı — büyük beyaz kalın
        tk.Label(info, text=data.get("album_name", "Untitled"),
                 bg=BLACK, fg=WHITE,
                 font=("Segoe UI", 24, "bold"),
                 wraplength=420, justify="left").pack(anchor="w", pady=(10, 2))

        # Sanatçı — mavi
        tk.Label(info, text=data.get("artist_name", "Unknown Artist"),
                 bg=BLACK, fg=BLUE_LIGHT,
                 font=("Segoe UI", 13)).pack(anchor="w", pady=(0, 6))

        # Ruh hali — italik orta beyaz
        mood = data.get("mood_description", "")
        if mood:
            tk.Label(info, text=f'"{mood}"',
                     bg=BLACK, fg=WHITE_MID,
                     font=("Segoe UI", 9, "italic"),
                     wraplength=420, justify="left").pack(anchor="w", pady=(0, 8))

        # Meta bilgi satırı
        parts = []
        y = data.get("year", "")
        if y:
            parts.append(str(y))
        parts.append(f"{len(tracks)} songs")
        lbl = data.get("label", "")
        if lbl:
            parts.append(lbl)
        tk.Label(info, text="  ·  ".join(parts), bg=BLACK, fg=WHITE_DIM,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))

        # Etiketler — mavi tonları
        tags = data.get("lastfm_tags", [])
        if tags:
            tf = tk.Frame(info, bg=BLACK)
            tf.pack(anchor="w")
            for i, t in enumerate(tags):
                bg_c, fg_c = TAG_COLORS[i % len(TAG_COLORS)]
                tk.Label(tf, text=f" #{t} ", bg=bg_c, fg=fg_c,
                         font=("Segoe UI", 8, "bold"),
                         padx=6, pady=2).pack(side=tk.LEFT, padx=(0, 5), pady=2)

        # ═══════════ Ayırıcı ═══════════
        tk.Frame(body, height=1, bg=BORDER).pack(fill=tk.X, pady=(6, 0))

        # ═══════════ Parça Listesi Başlığı ═══════════
        th = tk.Frame(body, bg=BLACK)
        th.pack(fill=tk.X, pady=(12, 4))
        tk.Label(th, text="#", bg=BLACK, fg=WHITE_DIM,
                 font=("Segoe UI", 9, "bold"), width=4,
                 anchor="w").pack(side=tk.LEFT)
        tk.Label(th, text="TITLE", bg=BLACK, fg=WHITE_DIM,
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Label(th, text="", bg=BLACK, width=10).pack(side=tk.LEFT)
        tk.Frame(body, height=1, bg=BORDER).pack(fill=tk.X, pady=(0, 2))

        # ═══════════ Parça Satırları ═══════════
        for i, tr in enumerate(tracks):
            self._track_row(body, i + 1, tr,
                            BLACK_TRACK_A if i % 2 == 0 else BLACK_TRACK_B)

        # ═══════════ Kaydet Butonu ═══════════
        sf = tk.Frame(body, bg=BLACK)
        sf.pack(fill=tk.X, pady=(22, 8))
        ttk.Button(sf, text="SAVE ALBUM  (JSON + PNG)",
                   style="Save.TButton",
                   command=self.export_album).pack(fill=tk.X)

        self.r_canvas.yview_moveto(0)
        self.r_canvas.bind("<Configure>", self._fit)

    def _fit(self, e):
        items = self.r_canvas.find_all()
        if items:
            self.r_canvas.itemconfigure(items[0], width=e.width)

    # ──────────────────────────────────────────────────────────
    # Parça Satırı
    # ──────────────────────────────────────────────────────────
    def _track_row(self, parent, num, track, bg):
        row = tk.Frame(parent, bg=bg, padx=10, pady=9)
        row.pack(fill=tk.X, pady=(1, 0))

        n_lbl = tk.Label(row, text=str(num), bg=bg, fg=WHITE_DIM,
                         font=("Segoe UI", 10), width=4, anchor="w")
        n_lbl.pack(side=tk.LEFT)

        col = tk.Frame(row, bg=bg)
        col.pack(side=tk.LEFT, expand=True, fill=tk.X)

        t_lbl = tk.Label(col, text=track.get("title", "Unknown"),
                         bg=bg, fg=WHITE,
                         font=("Segoe UI", 10, "bold"), anchor="w")
        t_lbl.pack(anchor="w")

        a_lbl = tk.Label(col, text=track.get("artist", "Unknown"),
                         bg=bg, fg=WHITE_MID,
                         font=("Segoe UI", 9), anchor="w")
        a_lbl.pack(anchor="w")

        url = track.get("url", "")
        tk.Button(row, text="Listen ▶",
                  bg=BLUE, fg=WHITE,
                  font=("Segoe UI", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2",
                  activebackground=BLUE_LIGHT, activeforeground=WHITE,
                  padx=10, pady=3, bd=0,
                  command=lambda u=url: webbrowser.open(u) if u else None
                  ).pack(side=tk.RIGHT, padx=(10, 0))

        all_w = [n_lbl, t_lbl, a_lbl, col]

        def enter(e, r=row, ws=all_w):
            r.config(bg=BLACK_HOVER)
            for w in ws:
                w.config(bg=BLACK_HOVER)

        def leave(e, r=row, ws=all_w, b=bg):
            r.config(bg=b)
            for w in ws:
                w.config(bg=b)

        row.bind("<Enter>", enter)
        row.bind("<Leave>", leave)

    # ──────────────────────────────────────────────────────────
    # Dışa Aktarma (GEREKSİNİM 8)
    # ──────────────────────────────────────────────────────────
    def export_album(self):
        """Oluşturulan albümü JSON + PNG dosyaları olarak dışa aktarır."""
        if not self.album_data or not self.cover_image:
            messagebox.showwarning("No Album", "Generate an album first!")
            return
        export_dir = filedialog.askdirectory(title="Choose Export Folder")
        if not export_dir:
            return
        try:
            safe = "".join(c if c.isalnum() or c in " -_" else "_"
                           for c in self.album_data.get("album_name", "album")).strip()

            export_data = {
                "album_name":       self.album_data.get("album_name"),
                "artist_name":      self.album_data.get("artist_name"),
                "year":             self.album_data.get("year"),
                "label":            self.album_data.get("label"),
                "mood_description": self.album_data.get("mood_description"),
                "tracklist": [
                    {"number": i + 1, "title": t["title"],
                     "artist": t["artist"], "url": t["url"]}
                    for i, t in enumerate(self.tracklist)
                ]
            }
            json_path = os.path.join(export_dir, f"{safe}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            png_path = os.path.join(export_dir, f"{safe}.png")
            self.cover_image.save(png_path, "PNG")

            self._status(f"Exported to {export_dir}", BLUE_LIGHT)
            messagebox.showinfo("Export Successful",
                                f"Album exported!\n\n{safe}.json\n{safe}.png\n\n{export_dir}")
        except Exception as ex:
            messagebox.showerror("Export Error", f"Failed: {ex}")

    # ──────────────────────────────────────────────────────────
    # Durum
    # ──────────────────────────────────────────────────────────
    def _status(self, text, color=WHITE_DIM):
        self.status_lbl.config(text=text, fg=color)
