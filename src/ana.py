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

FONT_ANA  = "Klee One"
FONT_BODY = "Literata"
FONT_BODY_JA = "Noto Serif CJK JP"

def get_body_font_family(lang="en"):
    return FONT_BODY_JA if lang == "ja" else FONT_BODY

CONFIG_PATH = os.path.expanduser("~/.config/ana/config.json")
ICON_PATH = os.path.expanduser("~/Ana/assets/Ana_Notebook.png")

THEME_LIGHT = {
    "name":       "light",
    "bg":         "#f0d8c0",
    "surface":    "#e8c8b0",
    "accent":     "#d890a8",
    "text":       "#3a2a0a",
    "text_muted": "#7a5c3a",
    "border":     "#d4b898",
}

THEME_DARK = {
    "name":       "dark",
    "bg":         "#000030",
    "surface":    "#181848",
    "accent":     "#906090",
    "text":       "#d8f0f0",
    "text_muted": "#8090a0",
    "border":     "#2a2a60",
}

LANG_STRINGS = {
    "en": {
        "change_lang":   "Let's try another language",
        "reading_time":  "Reading time: {} min",
        "not_written":   "This page hasn't been written yet.",
        "check_back":    "Check back soon.",
        "wagashi":       "Wagashi Linux",
        "welcome_sub":   "Relax.\nWe'll figure it out.",
    },
    "es": {
        "change_lang":   "Este idioma no me gusta",
        "reading_time":  "Tiempo de lectura: {} min",
        "not_written":   "Esta página todavía no está escrita.",
        "check_back":    "Vuelve pronto.",
        "wagashi":       "Wagashi Linux",
        "welcome_sub":   "Tranquilidad.\nMente fría.\nVamos a resolverlo.",
    },
    "ja": {
        "change_lang":   "別の言語にしてみよう",
        "reading_time":  "読む時間：{}分",
        "not_written":   "このページはまだ書かれていません。",
        "check_back":    "またね。",
        "wagashi":       "Wagashi Linux",
        "welcome_sub":   "大丈夫。\n一緒に考えよう。",
    },
}

BOOKS = [
    {
        "id": "zero",
        "icon": "📖",
        "title": {"en": "Now what?", "es": "¿Y ahora qué?", "ja": "次は何しよう？"},
        "subtitle": {"en": "Before we start", "es": "Antes de empezar", "ja": "始める前に"},
        "chapters": [
            {
                "title": {"en": "Welcome", "es": "Bienvenida", "ja": "ようこそ"},
                "file": "basics/welcome.md",
                "reading_time": 4,
                "music": ("Pumuky", "Teoria de Cuerdas"),
            },
        ]
    },
    {
        "id": "basics",
        "icon": "📘",
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
        "id": "troubleshooting",
        "icon": "🔧",
        "title": {"en": "When something isn't working", "es": "Cuando algo no funciona", "ja": "うまくいかないとき"},
        "subtitle": {"en": "Common problems and fixes", "es": "Problemas comunes y soluciones", "ja": "よくある問題と解決方法"},
        "chapters": [
            {"title": {"en": "Common problems",       "es": "Problemas comunes",    "ja": "よくある問題"},      "file": "troubleshooting/common.md",   "reading_time": 5, "music": ("Antonio Orozco", "Soldado 229")},
            {"title": {"en": "Recovery",              "es": "Recuperación",         "ja": "復旧"},              "file": "troubleshooting/recovery.md", "reading_time": 6, "music": ("ONE OK ROCK",    "Wherever You Are")},
            {"title": {"en": "When something breaks", "es": "Cuando algo se rompe", "ja": "壊れてしまったら"},  "file": "troubleshooting/breaks.md",   "reading_time": 4, "music": ("ODESZA",         "A Moment Apart")},
        ]
    },
    {
        "id": "advanced",
        "icon": "📚",
        "title": {"en": "I want to learn more", "es": "Quiero aprender más", "ja": "もっと知りたい"},
        "subtitle": {"en": "Terminal, config, customization", "es": "Terminal, configuración, personalización", "ja": "ターミナル・設定・カスタマイズ"},
        "chapters": [
            {"title": {"en": "The terminal",  "es": "La terminal",       "ja": "ターミナル"},       "file": "advanced/terminal.md",      "reading_time": 7, "music": ("Pay Money To My Pain", "Already Gone")},
            {"title": {"en": "Configuration", "es": "Configuración",     "ja": "設定"},             "file": "advanced/config.md",        "reading_time": 5, "music": ("Sufjan Stevens",       "Death With Dignity")},
            {"title": {"en": "Customization", "es": "Personalización",   "ja": "カスタマイズ"},     "file": "advanced/customization.md", "reading_time": 6, "music": ("Love of Lesbian",      "Club de Fans de John Boy")},
        ]
    },
    {
        "id": "places",
        "icon": "🗺️",
        "title": {"en": "Places worth visiting", "es": "Sitios que merece la pena ver", "ja": "行く価値のある場所"},
        "subtitle": {"en": "Resources, links, community", "es": "Recursos, enlaces, comunidad", "ja": "リソース・リンク・コミュニティ"},
        "chapters": [
            {"title": {"en": "Arch Wiki",     "es": "Arch Wiki",     "ja": "Arch Wiki"},     "file": "places/archwiki.md",     "reading_time": 3, "music": ("Ivan Ferreiro",  "El Equilibrio es Imposible")},
            {"title": {"en": "Linux Journey", "es": "Linux Journey", "ja": "Linux Journey"}, "file": "places/linuxjourney.md", "reading_time": 2, "music": ("The Peggies",    "Ashita mo")},
            {"title": {"en": "Community",     "es": "Comunidad",     "ja": "コミュニティ"},   "file": "places/community.md",    "reading_time": 3, "music": ("Gorillaz",       "Feel Good Inc.")},
        ]
    },
]

# ─── Config ───────────────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)

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

# ─── Language Selector ────────────────────────────────────────────────────────

class LangButton(QWidget):
    def __init__(self, flag, line1, line2, lang_code, theme, on_select, parent=None):
        super().__init__(parent)
        self.lang_code = lang_code
        self.on_select = on_select
        self.theme = theme
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 16, 24, 16)
        lay.setSpacing(4)

        l1 = QLabel(flag + "  " + line1)
        l1.setFont(ana_font(15))
        l1.setStyleSheet("color:" + theme["text"] + ";background:transparent;")
        l1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        l2 = QLabel(line2)
        l2.setFont(body_font(10, italic=True))
        l2.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;")
        l2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        lay.addWidget(l1)
        lay.addWidget(l2)

        self.setStyleSheet(
            "QWidget{background:transparent;border:1px solid " + theme["border"] + ";border-radius:10px;}"
            "QWidget:hover{background:" + theme["surface"] + ";}"
        )

    def mousePressEvent(self, e):
        self.on_select(self.lang_code)


class LanguageScreen(QWidget):
    def __init__(self, theme, on_select, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.on_select = on_select
        self.setStyleSheet("background:" + theme["bg"] + ";")
        self._build()

    def _build(self):
        t = self.theme
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(0, 0, 0, 0)

        inner = QWidget()
        inner.setFixedWidth(420)
        inner.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(inner)
        lay.setSpacing(12)
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

class BookItem(QWidget):
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
        lay.setContentsMargins(20, 10, 16, 10)
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
        self.t_lbl.setStyleSheet("color:" + t["text"] + ";background:transparent;")
        self.s_lbl.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")
        if self._active:
            self.setStyleSheet("QWidget{background:" + t["surface"] + ";border-left:3px solid " + t["accent"] + ";}")
        else:
            self.setStyleSheet("QWidget{background:transparent;border-left:3px solid transparent;}QWidget:hover{background:" + t["surface"] + ";}")

    def mousePressEvent(self, e):
        self.on_click(self.book, self)


class ChapterItem(QWidget):
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
        lay.setContentsMargins(36, 0, 16, 0)
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
            self.lbl.setStyleSheet("color:" + t["accent"] + ";background:transparent;font-weight:600;")
        else:
            self.lbl.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")
        self.setStyleSheet("QWidget{background:transparent;border-radius:4px;}QWidget:hover{background:" + t["surface"] + ";}")

    def mousePressEvent(self, e):
        self.on_click(self.chapter, self.book, self)


class Sidebar(QWidget):
    def __init__(self, lang, theme, on_chapter, on_toggle_theme, on_change_lang, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
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
        s = LANG_STRINGS[self.lang]
        self.setStyleSheet("background:" + t["surface"] + ";")
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setFixedHeight(56)
        hdr.setStyleSheet("background:transparent;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20, 0, 16, 0)

        name = QLabel("Ana")
        name.setFont(ana_font(22))
        name.setStyleSheet("color:" + t["text"] + ";background:transparent;")

        self.tog = QPushButton("◐")
        self.tog.setFixedSize(30, 30)
        self.tog.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tog.setFont(body_font(13))
        self.tog.setStyleSheet(
            "QPushButton{background:transparent;border:1px solid " + t["border"] + ";border-radius:15px;color:" + t["text_muted"] + ";}"
            "QPushButton:hover{background:" + t["bg"] + ";}"
        )
        self.tog.clicked.connect(self.on_toggle_theme)

        hl.addWidget(name)
        hl.addStretch()
        hl.addWidget(self.tog)
        self._lay.addWidget(hdr)

        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background:" + t["border"] + ";")
        self._lay.addWidget(div)

        # Book list
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("background:transparent;border:none;")

        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        self._inner_lay = QVBoxLayout(self._inner)
        self._inner_lay.setContentsMargins(0, 8, 0, 8)
        self._inner_lay.setSpacing(0)

        self.book_items = []
        for book in BOOKS:
            bi = BookItem(book, self.lang, self.theme, self._book_clicked)
            self._inner_lay.addWidget(bi)
            self.book_items.append(bi)

        self._inner_lay.addStretch()
        self._scroll.setWidget(self._inner)
        self._lay.addWidget(self._scroll)

        # Footer
        ftr = QWidget()
        ftr.setStyleSheet("background:transparent;")
        fl = QVBoxLayout(ftr)
        fl.setContentsMargins(16, 8, 16, 12)
        fl.setSpacing(6)

        # Change language button
        lang_btn = QPushButton(s["change_lang"])
        lang_btn.setFont(body_font(9))
        lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lang_btn.setFixedHeight(28)
        lang_btn.setStyleSheet(
            "QPushButton{background:transparent;border:1px solid " + t["border"] + ";border-radius:6px;color:" + t["text_muted"] + ";padding:0 8px;text-align:center;}"
            "QPushButton:hover{background:" + t["bg"] + ";color:" + t["accent"] + ";border-color:" + t["accent"] + ";}"
        )
        lang_btn.clicked.connect(self.on_change_lang)

        wl = QLabel(s["wagashi"])
        wl.setFont(body_font(8))
        wl.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")

        fl.addWidget(lang_btn)
        fl.addWidget(wl)
        self._lay.addWidget(ftr)

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
        self.setStyleSheet("background:" + theme["bg"] + ";")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(12)

        icon = QLabel()
        if os.path.exists(ICON_PATH):
            pix = QPixmap(ICON_PATH).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon.setPixmap(pix)
        else:
            icon.setText("📖")
            icon.setFont(QFont("Noto Color Emoji", 52))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("background:transparent;")

        title = QLabel("Ana")
        title.setFont(ana_font(42))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color:" + theme["text"] + ";background:transparent;")

        sub_text = LANG_STRINGS[lang]["welcome_sub"].replace("\n", "<br>")
        sub = QLabel(sub_text)
        sub.setFont(ana_font(16))
        sub.setTextFormat(Qt.TextFormat.RichText)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;text-align:center;")

        lay.addStretch()
        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addStretch()


class ContentView(QWidget):
    def __init__(self, lang, theme, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        self.setStyleSheet("background:" + theme["bg"] + ";")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background:" + theme["bg"] + ";border:none;")

        self.page = QWidget()
        self.page.setStyleSheet("background:" + theme["bg"] + ";")
        self.page_lay = QVBoxLayout(self.page)
        self.page_lay.setContentsMargins(72, 52, 72, 40)
        self.page_lay.setSpacing(0)
        self.page_lay.addStretch()
        self.scroll.setWidget(self.page)

        self.footer = QWidget()
        self.footer.setFixedHeight(44)
        self.footer.setStyleSheet(
            "background:" + theme["surface"] + ";"
            "border-top:1px solid " + theme["border"] + ";"
        )
        fl = QHBoxLayout(self.footer)
        fl.setContentsMargins(72, 0, 72, 0)

        self.time_lbl = QLabel("")
        self.time_lbl.setFont(body_font(9, italic=True))
        self.time_lbl.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;")

        self.music_lbl = QLabel("")
        self.music_lbl.setFont(body_font(10))
        self.music_lbl.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;")
        self.music_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        fl.addWidget(self.time_lbl)
        fl.addStretch()
        fl.addWidget(self.music_lbl)

        lay.addWidget(self.scroll)
        lay.addWidget(self.footer)

    def _clear(self):
        for i in reversed(range(self.page_lay.count())):
            item = self.page_lay.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

    def load_chapter(self, chapter, book):
        self._clear()
        t = self.theme
        s = LANG_STRINGS[self.lang]

        crumb = QLabel(book["icon"] + "  " + book["title"][self.lang])
        crumb.setFont(body_font(9))
        crumb.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")

        title = QLabel(chapter["title"][self.lang])
        title.setFont(body_font(28, bold=True, lang=self.lang))
        title.setWordWrap(True)
        title.setStyleSheet("color:" + t["text"] + ";background:transparent;margin-top:8px;margin-bottom:4px;")

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:" + t["border"] + ";margin:12px 0 20px 0;")

        raw = self._load(chapter)
        body = QLabel(raw)
        body.setFont(body_font(15, lang=self.lang))
        body.setWordWrap(True)
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        body.setStyleSheet("color:" + t["text"] + ";background:transparent;")
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
        # Content path: ~/Ana/content/{lang}/{file}
        base = os.path.expanduser("~/Ana/content")
        path = os.path.join(base, self.lang, chapter["file"])
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return md_to_html(f.read(), t, self.lang)
        return (
            "<p style='font-family:" + FONT_BODY + ";font-size:13px;color:" + t["text"] + ";line-height:1.8;margin-bottom:14px;'>"
            + s["not_written"] + "</p>"
            "<p style='font-family:" + FONT_ANA + ";font-size:15px;color:" + t["text_muted"] + ";'>"
            + s["check_back"] + "</p>"
        )


# ─── Main Window ──────────────────────────────────────────────────────────────

class AnaWindow(QMainWindow):
    def __init__(self, lang, theme):
        super().__init__()
        self.lang = lang
        self.theme = theme
        self._build()

    def _build(self):
        self.setWindowTitle("Ana")
        self.setMinimumSize(960, 620)
        self.resize(1140, 720)
        self.setStyleSheet("background:" + self.theme["bg"] + ";")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(
            self.lang, self.theme,
            on_chapter=self._on_chapter,
            on_toggle_theme=self._toggle_theme,
            on_change_lang=self._change_lang,
        )
        root.addWidget(self.sidebar)

        div = QFrame()
        div.setFixedWidth(1)
        div.setStyleSheet("background:" + self.theme["border"] + ";")
        root.addWidget(div)

        self.stack = QStackedWidget()
        self.welcome = WelcomeScreen(self.lang, self.theme)
        self.content = ContentView(self.lang, self.theme)
        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.content)
        self.stack.setCurrentWidget(self.welcome)
        root.addWidget(self.stack)

    def _on_chapter(self, chapter, book):
        self.stack.setCurrentWidget(self.content)
        self.content.load_chapter(chapter, book)

    def _toggle_theme(self):
        self.theme = THEME_DARK if self.theme["name"] == "light" else THEME_LIGHT
        self._rebuild()

    def _change_lang(self):
        # Save lang as empty to force selector next time, then restart
        cfg = load_config()
        cfg.pop("lang", None)
        save_config(cfg)
        # Show lang selector overlay
        self.close()
        show_lang_selector(self.theme)

    def _rebuild(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(
            self.lang, self.theme,
            on_chapter=self._on_chapter,
            on_toggle_theme=self._toggle_theme,
            on_change_lang=self._change_lang,
        )
        root.addWidget(self.sidebar)

        div = QFrame()
        div.setFixedWidth(1)
        div.setStyleSheet("background:" + self.theme["border"] + ";")
        root.addWidget(div)

        self.stack = QStackedWidget()
        self.welcome = WelcomeScreen(self.lang, self.theme)
        self.content = ContentView(self.lang, self.theme)
        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.content)
        self.stack.setCurrentWidget(self.welcome)
        root.addWidget(self.stack)

        self.setStyleSheet("background:" + self.theme["bg"] + ";")


class LangSelectorWindow(QMainWindow):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.setWindowTitle("Ana")
        self.setMinimumSize(500, 400)
        self.resize(600, 480)
        self.setStyleSheet("background:" + theme["bg"] + ";")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        central = LanguageScreen(theme, self._on_select)
        self.setCentralWidget(central)

    def _on_select(self, lang):
        cfg = load_config()
        cfg["lang"] = lang
        save_config(cfg)
        self.close()
        win = AnaWindow(lang, self.theme)
        win.show()
        self._main_win = win


def show_lang_selector(theme=None):
    if theme is None:
        theme = THEME_LIGHT
    win = LangSelectorWindow(theme)
    win.show()
    return win


# ─── Entry ────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ana")
    app.setOrganizationName("Wagashi Linux")

    cfg = load_config()
    lang = cfg.get("lang")
    theme = THEME_LIGHT

    if lang and lang in ("en", "es", "ja"):
        win = AnaWindow(lang, theme)
        win.show()
    else:
        win = show_lang_selector(theme)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
