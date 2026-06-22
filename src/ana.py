#!/usr/bin/env python3
"""
Ana — Wagashi Linux learning companion
For Ana Mamés (2002–2017)
"""

import sys
import os
import re
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QStackedWidget,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon

FONT_ANA     = "Klee One"
FONT_BODY    = "Literata"
FONT_BODY_JA = "Noto Serif CJK JP"

CONFIG_PATH = os.path.expanduser("~/.config/ana/config.json")
ICON_PATH = os.path.expanduser("~/Ana/assets/Ana_Notebook.png")

CARD_RADIUS = 18
INNER_RADIUS = 12

# ─── Themes ───────────────────────────────────────────────────────────────────

THEMES = {
    # Clannad · Dango Family — the softest one. Pastel, round, warm. Home.
    "light": {
        "app_bg": "#f0e6d2", "card": "#fffaf2", "card2": "#f5e8d5",
        "accent": "#d890a8", "accent2": "#a8c0d8",
        "text": "#3a2a0a", "text_muted": "#7a5c3a", "hover": "#f0ddc8",
        "highlight": "#d8d8a8",
    },
    # Clannad · Firefly — late night emotion, soft purple dark
    "dark": {
        "app_bg": "#000010", "card": "#10102c", "card2": "#181840",
        "accent": "#906090", "accent2": "#c0c0d8",
        "text": "#d8f0f0", "text_muted": "#9090b8", "hover": "#1c1c44",
        "highlight": "#d8a890",
    },
    # Sayuri — fixed monochrome + coral
    "sayuri": {
        "app_bg": "#000000", "card": "#0d0d0d", "card2": "#161616",
        "accent": "#e8a0a0", "accent2": "#e8a0a0",
        "text": "#e8e8e8", "text_muted": "#787878", "hover": "#1a1a1a",
        "highlight": "#e8a0a0",
    },
}

LANG_STRINGS = {
    "en": {
        "change_lang":  "Let's try another language",
        "reading_time": "Reading time: {} min",
        "not_written":  "This page hasn't been written yet.",
        "check_back":   "Check back soon.",
        "wagashi":      "Wagashi Linux",
        "welcome_sub":  "Relax.\nWe'll figure it out.",
    },
    "es": {
        "change_lang":  "Este idioma no me gusta",
        "reading_time": "Tiempo de lectura: {} min",
        "not_written":  "Esta página todavía no está escrita.",
        "check_back":   "Vuelve pronto.",
        "wagashi":      "Wagashi Linux",
        "welcome_sub":  "Tranquilidad.\nMente fría.\nVamos a resolverlo.",
    },
    "ja": {
        "change_lang":  "別の言語にしてみよう",
        "reading_time": "読む時間：{}分",
        "not_written":  "このページはまだ書かれていません。",
        "check_back":   "またね。",
        "wagashi":      "Wagashi Linux",
        "welcome_sub":  "大丈夫。\n一緒に考えよう。",
    },
}

BOOKS = [
    {
        "id": "zero", "icon": "📖",
        "title": {"en": "Now what?", "es": "¿Y ahora qué?", "ja": "次は何しよう？"},
        "subtitle": {"en": "Before we start", "es": "Antes de empezar", "ja": "始める前に"},
        "chapters": [
            {"title": {"en": "Welcome", "es": "Bienvenida", "ja": "ようこそ"}, "file": "basics/welcome.md", "reading_time": 4, "music": ("Pumuky", "Teoria de Cuerdas")},
        ]
    },
    {
        "id": "basics", "icon": "📘",
        "title": {"en": "Basics", "es": "Básicos", "ja": "基本"},
        "subtitle": {"en": "Desktop and first steps", "es": "Escritorio y primeros pasos", "ja": "デスクトップと最初のステップ"},
        "chapters": [
            {"title": {"en": "The desktop",  "es": "El escritorio", "ja": "デスクトップ"},  "file": "basics/desktop.md",      "reading_time": 3, "music": ("Gorillaz",      "Feel Good Inc.")},
            {"title": {"en": "Applications", "es": "Aplicaciones",  "ja": "アプリ"},         "file": "basics/applications.md", "reading_time": 2, "music": ("Dorian",        "La Tormenta de Arena")},
            {"title": {"en": "dango",        "es": "dango",         "ja": "dango"},          "file": "basics/dango.md",        "reading_time": 4, "music": ("Carlos Sadness","No Vuelvas a Japon")},
            {"title": {"en": "Updates",      "es": "Actualizaciones","ja": "アップデート"},   "file": "basics/updates.md",      "reading_time": 2, "music": ("Illenium",      "Crawl Outta Love")},
        ]
    },
    {
        "id": "troubleshooting", "icon": "🔧",
        "title": {"en": "When something isn't working", "es": "Cuando algo no funciona", "ja": "うまくいかないとき"},
        "subtitle": {"en": "Common problems and fixes", "es": "Problemas comunes y soluciones", "ja": "よくある問題と解決方法"},
        "chapters": [
            {"title": {"en": "Common problems",       "es": "Problemas comunes",    "ja": "よくある問題"},      "file": "troubleshooting/common.md",   "reading_time": 5, "music": ("Antonio Orozco", "Soldado 229")},
            {"title": {"en": "Recovery",              "es": "Recuperación",         "ja": "復旧"},              "file": "troubleshooting/recovery.md", "reading_time": 6, "music": ("ONE OK ROCK",    "Wherever You Are")},
            {"title": {"en": "When something breaks", "es": "Cuando algo se rompe", "ja": "壊れてしまったら"},  "file": "troubleshooting/breaks.md",   "reading_time": 4, "music": ("ODESZA",         "A Moment Apart")},
        ]
    },
    {
        "id": "advanced", "icon": "📚",
        "title": {"en": "I want to learn more", "es": "Quiero aprender más", "ja": "もっと知りたい"},
        "subtitle": {"en": "Terminal, config, customization", "es": "Terminal, configuración, personalización", "ja": "ターミナル・設定・カスタマイズ"},
        "chapters": [
            {"title": {"en": "The terminal",  "es": "La terminal",       "ja": "ターミナル"},       "file": "advanced/terminal.md",      "reading_time": 7, "music": ("Pay Money To My Pain", "Already Gone")},
            {"title": {"en": "Configuration", "es": "Configuración",     "ja": "設定"},             "file": "advanced/config.md",        "reading_time": 5, "music": ("Sufjan Stevens",       "Death With Dignity")},
            {"title": {"en": "Customization", "es": "Personalización",   "ja": "カスタマイズ"},     "file": "advanced/customization.md", "reading_time": 6, "music": ("Love of Lesbian",      "Club de Fans de John Boy")},
        ]
    },
    {
        "id": "places", "icon": "🗺️",
        "title": {"en": "Places worth visiting", "es": "Sitios que merece la pena ver", "ja": "行く価値のある場所"},
        "subtitle": {"en": "Resources, links, community", "es": "Recursos, enlaces, comunidad", "ja": "リソース・リンク・コミュニティ"},
        "chapters": [
            {"title": {"en": "Arch Wiki",     "es": "Arch Wiki",     "ja": "Arch Wiki"},     "file": "places/archwiki.md",     "reading_time": 3, "music": ("Ivan Ferreiro",  "El Equilibrio es Imposible")},
            {"title": {"en": "Linux Journey", "es": "Linux Journey", "ja": "Linux Journey"}, "file": "places/linuxjourney.md", "reading_time": 2, "music": ("The Peggies",    "Ashita mo")},
            {"title": {"en": "Community",     "es": "Comunidad",     "ja": "コミュニティ"},   "file": "places/community.md",    "reading_time": 3, "music": ("Mago de Oz",      "Y Ahora Voy A Salir")},
        ]
    },
]

# ─── Config ───────────────────────────────────────────────────────────────────

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)

def detect_edition():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("VARIANT_ID="):
                    return line.strip().split("=", 1)[1].strip('"').lower()
    except Exception:
        pass
    return "ayu"

def get_theme_key(edition, dark):
    if edition == "sayuri":
        return "sayuri"
    return "dark" if dark else "light"

# ─── Fonts ────────────────────────────────────────────────────────────────────

def ana_font(size=18):
    return QFont(FONT_ANA, size)

def body_font(size=13, bold=False, italic=False, lang="en"):
    family = FONT_BODY_JA if lang == "ja" else FONT_BODY
    f = QFont(family, size)
    if bold:
        f.setWeight(QFont.Weight.DemiBold)
    if italic:
        f.setItalic(True)
    return f

def get_body_font_family(lang="en"):
    return FONT_BODY_JA if lang == "ja" else FONT_BODY

# ─── Markdown ─────────────────────────────────────────────────────────────────

def md_to_html(text, theme, lang="en"):
    ct = theme["text"]
    cm = theme["text_muted"]
    ca = theme["accent"]
    font_stack = get_body_font_family(lang)
    out = []
    for line in text.split("\n"):
        if line.startswith("### "):
            out.append("<h3 style='font-family:" + font_stack + ";color:" + ct + ";margin:20px 0 6px 0;font-size:15px;'>" + line[4:] + "</h3>")
        elif line.startswith("## "):
            out.append("<h2 style='font-family:" + font_stack + ";color:" + ct + ";margin:28px 0 8px 0;font-size:17px;'>" + line[3:] + "</h2>")
        elif line.startswith("# "):
            pass
        elif line.startswith("> "):
            out.append("<blockquote style='border-left:3px solid " + ca + ";margin:16px 0;padding:8px 16px;color:" + cm + ";font-style:italic;font-family:" + font_stack + ";'>" + line[2:] + "</blockquote>")
        elif line.strip() == "":
            out.append("<p style='margin:0 0 4px 0;'></p>")
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"\*(.*?)\*", r"<i>\1</i>", line)
            line = re.sub(r"`(.*?)`", r"<code style='background:rgba(0,0,0,0.08);padding:2px 5px;border-radius:3px;font-family:monospace;font-size:12px;'>\1</code>", line)
            out.append("<p style='margin:0 0 6px 0;line-height:1.5;font-family:" + font_stack + ";font-size:15px;color:" + ct + ";'>" + line + "</p>")
    return "".join(out)

# ─── Floating card base ───────────────────────────────────────────────────────

class Card(QFrame):
    def __init__(self, theme, radius=CARD_RADIUS, parent=None):
        super().__init__(parent)
        t = theme
        self.setStyleSheet(f"QFrame{{background:{t['card']}; border:none; border-radius:{radius}px;}}")

# ─── Language Selector ────────────────────────────────────────────────────────

class LangButton(QFrame):
    def __init__(self, flag, line1, line2, lang_code, theme, on_select, parent=None):
        super().__init__(parent)
        self.lang_code = lang_code
        self.on_select = on_select
        self.theme = theme
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(96)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        t = theme
        self.setStyleSheet(
            f"QFrame{{background:{t['card2']}; border:none; border-radius:{INNER_RADIUS}px;}}"
            f"QFrame:hover{{background:{t['hover']};}}"
        )

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 16, 24, 16)
        lay.setSpacing(4)

        l1 = QLabel(flag + "  " + line1)
        l1.setFont(ana_font(15))
        l1.setStyleSheet(f"color:{t['text']}; background:transparent; border:none;")
        l1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        l2 = QLabel(line2)
        l2.setFont(body_font(10, italic=True))
        l2.setStyleSheet(f"color:{t['text_muted']}; background:transparent; border:none;")
        l2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        lay.addWidget(l1)
        lay.addWidget(l2)

    def mousePressEvent(self, e):
        self.on_select(self.lang_code)


class LanguageScreen(QWidget):
    def __init__(self, theme, on_select, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.on_select = on_select
        self.setStyleSheet(f"background:{theme['app_bg']};")
        self._build()

    def _build(self):
        t = self.theme
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(40, 40, 40, 40)

        inner = QWidget()
        inner.setFixedWidth(420)
        inner.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(inner)
        lay.setSpacing(14)
        lay.setContentsMargins(0, 0, 0, 0)

        es_btn = LangButton("🇪🇸", "Hola.", "Háblame en español", "es", t, self.on_select)
        en_btn = LangButton("🇬🇧", "Hi.", "Talk to me in English", "en", t, self.on_select)
        ja_btn = LangButton("🇯🇵", "こんにちは。", "日本語で話して", "ja", t, self.on_select)

        lay.addWidget(es_btn)
        lay.addWidget(en_btn)
        lay.addWidget(ja_btn)

        outer.addStretch()
        outer.addWidget(inner, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch()

# ─── Sidebar ──────────────────────────────────────────────────────────────────

class BookItem(QFrame):
    def __init__(self, book, lang, theme, on_click, parent=None):
        super().__init__(parent)
        self.book = book
        self.lang = lang
        self.theme = theme
        self.on_click = on_click
        self._active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 10, 14, 10)
        lay.setSpacing(3)

        title = self.book["icon"] + "  " + self.book["title"][self.lang]
        subtitle = self.book["subtitle"][self.lang]

        self.t_lbl = QLabel(title)
        self.t_lbl.setFont(body_font(11, bold=True, lang=self.lang))
        self.t_lbl.setWordWrap(True)
        self.t_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.s_lbl = QLabel(subtitle)
        self.s_lbl.setFont(body_font(9, lang=self.lang))
        self.s_lbl.setWordWrap(True)
        self.s_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        lay.addWidget(self.t_lbl)
        lay.addWidget(self.s_lbl)
        self._style()

    def set_active(self, v):
        self._active = v
        self._style()

    def _style(self):
        t = self.theme
        self.t_lbl.setStyleSheet(f"color:{t['text']}; background:transparent; border:none;")
        self.s_lbl.setStyleSheet(f"color:{t['text_muted']}; background:transparent; border:none;")
        radius = INNER_RADIUS
        if self._active:
            self.setStyleSheet(f"QFrame{{background:{t['accent']}; border:none; border-radius:{radius}px;}}")
            self.t_lbl.setStyleSheet(f"color:{t['card']}; background:transparent; border:none; font-weight:bold;")
            self.s_lbl.setStyleSheet(f"color:{t['card']}; background:transparent; border:none;")
        else:
            self.setStyleSheet(
                f"QFrame{{background:transparent; border:none; border-radius:{radius}px;}}"
                f"QFrame:hover{{background:{t['hover']};}}"
            )

    def mousePressEvent(self, e):
        self.on_click(self.book, self)


class ChapterItem(QFrame):
    def __init__(self, chapter, book, lang, theme, on_click, parent=None):
        super().__init__(parent)
        self.chapter = chapter
        self.book = book
        self.lang = lang
        self.theme = theme
        self.on_click = on_click
        self._active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(32)
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(32, 0, 14, 0)
        self.lbl = QLabel(self.chapter["title"][self.lang])
        self.lbl.setFont(body_font(10, lang=self.lang))
        self.lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        lay.addWidget(self.lbl)
        self._style()

    def set_active(self, v):
        self._active = v
        self._style()

    def _style(self):
        t = self.theme
        if self._active:
            self.lbl.setStyleSheet(f"color:{t['accent']}; background:transparent; border:none; font-weight:600;")
        else:
            self.lbl.setStyleSheet(f"color:{t['text_muted']}; background:transparent; border:none;")
        self.setStyleSheet(
            f"QFrame{{background:transparent; border:none; border-radius:{INNER_RADIUS-4}px;}}"
            f"QFrame:hover{{background:{t['hover']};}}"
        )

    def mousePressEvent(self, e):
        self.on_click(self.chapter, self.book, self)


class Sidebar(QFrame):
    def __init__(self, lang, theme, edition, on_chapter, on_toggle_theme, on_change_lang, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        self.edition = edition
        self.on_chapter = on_chapter
        self.on_toggle_theme = on_toggle_theme
        self.on_change_lang = on_change_lang
        self.book_items = []
        self.chapter_items = []
        self.active_book = None
        self.active_chapter = None
        self.setFixedWidth(260)
        self._build()

    def _build(self):
        t = self.theme
        self.setStyleSheet(f"QFrame{{background:{t['card']}; border:none; border-radius:{CARD_RADIUS}px;}}")
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(0)

        header = QFrame()
        header.setStyleSheet("background:transparent; border:none;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(18, 16, 14, 10)

        name = QLabel("Ana")
        name.setFont(ana_font(22))
        name.setStyleSheet(f"color:{t['text']}; background:transparent; border:none;")

        self.tog = QPushButton("◐")
        self.tog.setFixedSize(30, 30)
        self.tog.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tog.setFont(body_font(13, lang=self.lang))
        self.tog.setStyleSheet(
            f"QPushButton{{background:transparent;border:1.5px solid {t['hover']};border-radius:15px;color:{t['text_muted']};}}"
            f"QPushButton:hover{{background:{t['hover']};border-color:{t['accent']};color:{t['accent']};}}"
        )
        self.tog.clicked.connect(self.on_toggle_theme)
        if self.edition == "sayuri":
            self.tog.setVisible(False)

        hl.addWidget(name)
        hl.addStretch()
        hl.addWidget(self.tog)
        self._lay.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(
            "QScrollArea{background:transparent; border:none;}"
            "QScrollBar:vertical{background:transparent; width:6px; margin:2px;}"
            f"QScrollBar::handle:vertical{{background:{t['text_muted']}; border-radius:3px; min-height:20px;}}"
            f"QScrollBar::handle:vertical:hover{{background:{t['accent']};}}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{height:0px;}"
        )

        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        self._inner_lay = QVBoxLayout(self._inner)
        self._inner_lay.setContentsMargins(8, 4, 8, 8)
        self._inner_lay.setSpacing(2)

        self.book_items = []
        for book in BOOKS:
            bi = BookItem(book, self.lang, self.theme, self._book_clicked)
            self._inner_lay.addWidget(bi)
            self.book_items.append(bi)

        self._inner_lay.addStretch()
        scroll_area.setWidget(self._inner)
        self._lay.addWidget(scroll_area)

        footer = QFrame()
        footer.setStyleSheet("background:transparent; border:none;")
        fl = QVBoxLayout(footer)
        fl.setContentsMargins(18, 8, 14, 14)
        fl.setSpacing(6)

        s = LANG_STRINGS[self.lang]
        lang_btn = QPushButton(s["change_lang"])
        lang_btn.setFont(body_font(8, italic=True, lang=self.lang))
        lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lang_btn.setFixedHeight(26)
        lang_btn.setStyleSheet(
            f"QPushButton{{background:transparent;border:1px solid {t['hover']};border-radius:8px;color:{t['text_muted']};padding:0 8px;}}"
            f"QPushButton:hover{{background:{t['hover']};color:{t['accent']};border-color:{t['accent']};}}"
        )
        lang_btn.clicked.connect(self.on_change_lang)

        wl = QLabel(s["wagashi"])
        wl.setFont(body_font(8, lang=self.lang))
        wl.setStyleSheet(f"color:{t['text_muted']}; background:transparent; border:none;")

        fl.addWidget(lang_btn)
        fl.addWidget(wl)
        self._lay.addWidget(footer)

    def _book_clicked(self, book, item):
        if self.active_book:
            self.active_book.set_active(False)
        item.set_active(True)
        self.active_book = item

        for ci in self.chapter_items:
            ci.setParent(None)
        self.chapter_items = []
        self.active_chapter = None

        while self._inner_lay.count():
            self._inner_lay.takeAt(0)

        book_index = self.book_items.index(item)
        for idx, bi in enumerate(self.book_items):
            self._inner_lay.addWidget(bi)
            if idx == book_index:
                for ch in book["chapters"]:
                    ci = ChapterItem(ch, book, self.lang, self.theme, self._chapter_clicked)
                    self._inner_lay.addWidget(ci)
                    self.chapter_items.append(ci)

        self._inner_lay.addStretch()

        if self.chapter_items:
            self._chapter_clicked(book["chapters"][0], book, self.chapter_items[0])

    def _chapter_clicked(self, chapter, book, item):
        if self.active_chapter:
            self.active_chapter.set_active(False)
        item.set_active(True)
        self.active_chapter = item
        self.on_chapter(chapter, book)

# ─── Content ──────────────────────────────────────────────────────────────────

class WelcomeScreen(QWidget):
    def __init__(self, lang, theme, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(12)

        icon = QLabel()
        if os.path.exists(ICON_PATH):
            pix = QPixmap(ICON_PATH).scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon.setPixmap(pix)
        else:
            icon.setText("📖")
            icon.setFont(QFont("Noto Color Emoji", 52))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("background:transparent;")

        title = QLabel("Ana")
        title.setFont(ana_font(42))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color:{theme['text']}; background:transparent;")

        sub_text = LANG_STRINGS[lang]["welcome_sub"].replace("\n", "<br>")
        sub = QLabel(sub_text)
        sub.setFont(ana_font(16))
        sub.setTextFormat(Qt.TextFormat.RichText)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color:{theme['text_muted']}; background:transparent;")

        lay.addStretch()
        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addStretch()


class ContentView(QFrame):
    def __init__(self, lang, theme, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        t = theme
        self.setStyleSheet(f"QFrame{{background:{t['card']}; border:none; border-radius:{CARD_RADIUS}px;}}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background:transparent;")

        self.welcome = WelcomeScreen(lang, theme)
        self.stack.addWidget(self.welcome)

        # Scroll for chapter content
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(
            "QScrollArea{background:transparent; border:none;}"
            "QScrollBar:vertical{background:transparent; width:8px; margin:4px;}"
            f"QScrollBar::handle:vertical{{background:{t['text_muted']}; border-radius:4px; min-height:24px;}}"
            f"QScrollBar::handle:vertical:hover{{background:{t['accent']};}}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{height:0px;}"
        )

        self.page = QWidget()
        self.page.setStyleSheet("background:transparent;")
        self.page_lay = QVBoxLayout(self.page)
        self.page_lay.setContentsMargins(48, 40, 48, 32)
        self.page_lay.setSpacing(0)
        self.page_lay.addStretch()
        self.scroll.setWidget(self.page)
        self.stack.addWidget(self.scroll)

        self.stack.setCurrentWidget(self.welcome)
        lay.addWidget(self.stack)

        # Footer bar
        self.footer = QFrame()
        self.footer.setFixedHeight(44)
        self.footer.setStyleSheet(
            f"QFrame{{background:{t['card2']}; border:none; border-bottom-left-radius:{CARD_RADIUS}px; border-bottom-right-radius:{CARD_RADIUS}px;}}"
        )
        fl = QHBoxLayout(self.footer)
        fl.setContentsMargins(48, 0, 48, 0)

        self.time_lbl = QLabel("")
        self.time_lbl.setFont(body_font(9, italic=True, lang=lang))
        self.time_lbl.setStyleSheet(f"color:{t['text_muted']}; background:transparent;")

        self.music_lbl = QLabel("")
        self.music_lbl.setFont(body_font(10, lang=lang))
        self.music_lbl.setStyleSheet(f"color:{t['text_muted']}; background:transparent;")
        self.music_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        fl.addWidget(self.time_lbl)
        fl.addStretch()
        fl.addWidget(self.music_lbl)
        lay.addWidget(self.footer)
        self.footer.hide()

    def show_welcome(self):
        self.stack.setCurrentWidget(self.welcome)
        self.footer.hide()

    def _clear_page(self):
        for i in reversed(range(self.page_lay.count())):
            item = self.page_lay.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

    def load_chapter(self, chapter, book):
        self.stack.setCurrentWidget(self.scroll)
        self.footer.show()
        self._clear_page()
        t = self.theme
        s = LANG_STRINGS[self.lang]

        crumb = QLabel(book["icon"] + "  " + book["title"][self.lang])
        crumb.setFont(body_font(9, lang=self.lang))
        crumb.setStyleSheet(f"color:{t['text_muted']}; background:transparent;")

        title = QLabel(chapter["title"][self.lang])
        title.setFont(body_font(28, bold=True, lang=self.lang))
        title.setWordWrap(True)
        title.setStyleSheet(f"color:{t['text']}; background:transparent; margin-top:8px; margin-bottom:4px;")

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background:{t['hover']}; border:none; margin:12px 0 20px 0;")

        raw = self._load(chapter)
        body = QLabel(raw)
        body.setFont(body_font(15, lang=self.lang))
        body.setWordWrap(True)
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        body.setStyleSheet(f"color:{t['text']}; background:transparent;")
        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.page_lay.addWidget(crumb)
        self.page_lay.addWidget(title)
        self.page_lay.addWidget(sep)
        self.page_lay.addWidget(body)
        self.page_lay.addStretch()

        rt = s["reading_time"].format(chapter["reading_time"])
        self.time_lbl.setText(rt)
        artist, song = chapter["music"]
        self.music_lbl.setText("🎵  " + artist + " — " + song)
        self.scroll.verticalScrollBar().setValue(0)

    def _load(self, chapter):
        t = self.theme
        s = LANG_STRINGS[self.lang]
        base = os.path.expanduser("~/Ana/content")
        path = os.path.join(base, self.lang, chapter["file"])
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return md_to_html(f.read(), t, self.lang)
        return (
            "<p style='font-family:" + get_body_font_family(self.lang) + ";font-size:15px;color:" + t["text"] + ";line-height:1.8;margin-bottom:14px;'>"
            + s["not_written"] + "</p>"
            "<p style='font-family:" + FONT_ANA + ";font-size:15px;color:" + t["text_muted"] + ";'>"
            + s["check_back"] + "</p>"
        )

# ─── Main Window ──────────────────────────────────────────────────────────────

class AnaWindow(QMainWindow):
    def __init__(self, lang, dark, edition):
        super().__init__()
        self.lang = lang
        self.dark = dark
        self.edition = edition
        self.theme = THEMES[get_theme_key(edition, dark)]
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        self._build()

    def _build(self):
        self.setWindowTitle("Ana")
        self.setMinimumSize(960, 620)
        self.resize(1140, 720)
        central = QWidget()
        self.setCentralWidget(central)
        self._build_into(central)

    def _build_into(self, central):
        t = self.theme
        central.setStyleSheet(f"background:{t['app_bg']};")
        root = QHBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        self.sidebar = Sidebar(
            self.lang, self.theme, self.edition,
            on_chapter=self._on_chapter,
            on_toggle_theme=self._toggle_theme,
            on_change_lang=self._change_lang,
        )
        root.addWidget(self.sidebar)

        self.content = ContentView(self.lang, self.theme)
        root.addWidget(self.content)

    def _on_chapter(self, chapter, book):
        self.content.load_chapter(chapter, book)

    def _toggle_theme(self):
        if self.edition == "sayuri":
            return
        self.dark = not self.dark
        cfg = load_config()
        cfg["dark"] = self.dark
        save_config(cfg)
        self.theme = THEMES[get_theme_key(self.edition, self.dark)]
        central = QWidget()
        self.setCentralWidget(central)
        self._build_into(central)

    def _change_lang(self):
        cfg = load_config()
        cfg.pop("lang", None)
        save_config(cfg)
        self.close()
        show_lang_selector(self.theme, self.dark, self.edition)


class LangSelectorWindow(QMainWindow):
    def __init__(self, theme, dark, edition):
        super().__init__()
        self.theme = theme
        self.dark = dark
        self.edition = edition
        self.setWindowTitle("Ana")
        self.setMinimumSize(500, 400)
        self.resize(600, 480)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        central = LanguageScreen(theme, self._on_select)
        self.setCentralWidget(central)

    def _on_select(self, lang):
        cfg = load_config()
        cfg["lang"] = lang
        save_config(cfg)
        self.close()
        win = AnaWindow(lang, self.dark, self.edition)
        win.show()
        self._main_win = win


def show_lang_selector(theme, dark, edition):
    win = LangSelectorWindow(theme, dark, edition)
    win.show()
    return win

# ─── Entry ────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ana")
    app.setOrganizationName("Wagashi Linux")

    edition = detect_edition()
    cfg = load_config()
    lang = cfg.get("lang")
    dark = cfg.get("dark", edition == "sayuri")
    theme = THEMES[get_theme_key(edition, dark)]

    if lang and lang in ("en", "es", "ja"):
        win = AnaWindow(lang, dark, edition)
        win.show()
    else:
        win = show_lang_selector(theme, dark, edition)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
