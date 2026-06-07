#!/usr/bin/env python3
"""
Ana — Wagashi Linux learning companion
For Ana Mamés (2002–2017)
"""

import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QStackedWidget,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

FONT_ANA  = "Klee One"
FONT_BODY = "Literata"

THEME_LIGHT = {
    "name":       "light",
    "bg":         "#f0d8c0",
    "surface":    "#e8c8b0",
    "accent":     "#d890a8",
    "accent2":    "#a8c0d8",
    "text":       "#3a2a0a",
    "text_muted": "#7a5c3a",
    "border":     "#d4b898",
}

THEME_DARK = {
    "name":       "dark",
    "bg":         "#000030",
    "surface":    "#181848",
    "accent":     "#906090",
    "accent2":    "#c0c0d8",
    "text":       "#d8f0f0",
    "text_muted": "#8090a0",
    "border":     "#2a2a60",
}

BOOKS = [
    {
        "id": "basics",
        "icon": "📖",
        "title": "Basics",
        "subtitle": "Desktop and first steps",
        "chapters": [
            {"title": "The desktop",  "file": "basics/desktop.md",      "reading_time": 3, "music": ("Pumuky",        "Teoria de Cuerdas")},
            {"title": "Applications", "file": "basics/applications.md", "reading_time": 2, "music": ("Gorillaz",      "Feel Good Inc.")},
            {"title": "dango",        "file": "basics/dango.md",        "reading_time": 4, "music": ("Dorian",        "La Tormenta de Arena")},
            {"title": "Updates",      "file": "basics/updates.md",      "reading_time": 2, "music": ("Carlos Sadness","No Vuelvas a Japon")},
        ]
    },
    {
        "id": "troubleshooting",
        "icon": "🔧",
        "title": "When something isn't working",
        "subtitle": "Common problems and fixes",
        "chapters": [
            {"title": "Common problems",       "file": "troubleshooting/common.md",   "reading_time": 5, "music": ("Illenium",       "Crawl Outta Love")},
            {"title": "Recovery",              "file": "troubleshooting/recovery.md", "reading_time": 6, "music": ("Antonio Orozco",  "Soldado 229")},
            {"title": "When something breaks", "file": "troubleshooting/breaks.md",   "reading_time": 4, "music": ("ONE OK ROCK",     "Wherever You Are")},
        ]
    },
    {
        "id": "advanced",
        "icon": "📚",
        "title": "I want to learn more",
        "subtitle": "Terminal, config, customization",
        "chapters": [
            {"title": "The terminal",  "file": "advanced/terminal.md",      "reading_time": 7, "music": ("Pay Money To My Pain", "Already Gone")},
            {"title": "Configuration", "file": "advanced/config.md",        "reading_time": 5, "music": ("ODESZA",               "A Moment Apart")},
            {"title": "Customization", "file": "advanced/customization.md", "reading_time": 6, "music": ("Sufjan Stevens",       "Death With Dignity")},
        ]
    },
    {
        "id": "places",
        "icon": "🗺️",
        "title": "Places worth visiting",
        "subtitle": "Resources, links, community",
        "chapters": [
            {"title": "Arch Wiki",     "file": "places/archwiki.md",     "reading_time": 3, "music": ("Ivan Ferreiro",   "El Equilibrio es Imposible")},
            {"title": "Linux Journey", "file": "places/linuxjourney.md", "reading_time": 2, "music": ("The Peggies",     "Ashita mo")},
            {"title": "Community",     "file": "places/community.md",    "reading_time": 3, "music": ("Love of Lesbian", "Club de Fans de John Boy")},
        ]
    },
]


def ana_font(size=18):
    return QFont(FONT_ANA, size)


def body_font(size=13, bold=False, italic=False):
    f = QFont(FONT_BODY, size)
    if bold:
        f.setWeight(QFont.Weight.DemiBold)
    if italic:
        f.setItalic(True)
    return f


def md_to_html(text, theme):
    ct = theme["text"]
    cm = theme["text_muted"]
    ca = theme["accent"]
    out = []
    for line in text.split("\n"):
        if line.startswith("### "):
            out.append("<h3 style='font-family:" + FONT_BODY + ";color:" + ct + ";margin:20px 0 6px 0;font-size:15px;'>" + line[4:] + "</h3>")
        elif line.startswith("## "):
            out.append("<h2 style='font-family:" + FONT_BODY + ";color:" + ct + ";margin:28px 0 8px 0;font-size:17px;'>" + line[3:] + "</h2>")
        elif line.startswith("# "):
            pass
        elif line.startswith("> "):
            out.append("<blockquote style='border-left:3px solid " + ca + ";margin:16px 0;padding:8px 16px;color:" + cm + ";font-style:italic;font-family:" + FONT_BODY + ";'>" + line[2:] + "</blockquote>")
        elif line.strip() == "":
            out.append("<br>")
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"\*(.*?)\*", r"<i>\1</i>", line)
            line = re.sub(r"`(.*?)`", r"<code style='background:rgba(0,0,0,0.08);padding:2px 5px;border-radius:3px;font-family:monospace;font-size:12px;'>\1</code>", line)
            out.append("<p style='margin:0 0 14px 0;line-height:1.8;font-family:" + FONT_BODY + ";font-size:13px;color:" + ct + ";'>" + line + "</p>")
    return "".join(out)


class BookItem(QWidget):
    def __init__(self, book, theme, on_click, parent=None):
        super().__init__(parent)
        self.book = book
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

        self.t_lbl = QLabel(self.book["icon"] + "  " + self.book["title"])
        self.t_lbl.setFont(body_font(11, bold=True))
        self.t_lbl.setWordWrap(True)
        self.t_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.s_lbl = QLabel(self.book["subtitle"])
        self.s_lbl.setFont(body_font(9))
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
    def __init__(self, chapter, book, theme, on_click, parent=None):
        super().__init__(parent)
        self.chapter = chapter
        self.book = book
        self.theme = theme
        self.on_click = on_click
        self._active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(32)
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(36, 0, 16, 0)
        self.lbl = QLabel(self.chapter["title"])
        self.lbl.setFont(body_font(10))
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
    def __init__(self, theme, on_chapter, on_toggle, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.on_chapter = on_chapter
        self.on_toggle = on_toggle
        self.book_items = []
        self.chapter_items = []
        self.active_book = None
        self.active_chapter = None
        self.setFixedWidth(260)
        self._build()

    def _build(self):
        t = self.theme
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
        self.tog.clicked.connect(self.on_toggle)

        hl.addWidget(name)
        hl.addStretch()
        hl.addWidget(self.tog)
        self._lay.addWidget(hdr)

        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background:" + t["border"] + ";")
        self._lay.addWidget(div)

        # Scrollable list
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
            bi = BookItem(book, self.theme, self._book_clicked)
            self._inner_lay.addWidget(bi)
            self.book_items.append(bi)

        self._inner_lay.addStretch()
        self._scroll.setWidget(self._inner)
        self._lay.addWidget(self._scroll)

        # Footer
        ftr = QWidget()
        ftr.setFixedHeight(36)
        ftr.setStyleSheet("background:transparent;")
        fl = QHBoxLayout(ftr)
        fl.setContentsMargins(20, 0, 16, 0)
        wl = QLabel("Wagashi Linux")
        wl.setFont(body_font(8))
        wl.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")
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
                    ci = ChapterItem(ch, book, self.theme, self._chapter_clicked)
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


class WelcomeScreen(QWidget):
    def __init__(self, theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet("background:" + theme["bg"] + ";")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(12)

        icon = QLabel("📖")
        icon.setFont(QFont("Noto Color Emoji", 52))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("background:transparent;")

        title = QLabel("Ana")
        title.setFont(ana_font(42))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color:" + theme["text"] + ";background:transparent;")

        # Voz de Ana — fuente Ana
        sub = QLabel("Relax. We'll figure it out.")
        sub.setFont(ana_font(16))
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;")

        lay.addStretch()
        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addStretch()


class ContentView(QWidget):
    def __init__(self, theme, parent=None):
        super().__init__(parent)
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

        # Reading time — Literata italic
        self.time_lbl = QLabel("")
        self.time_lbl.setFont(body_font(9, italic=True))
        self.time_lbl.setStyleSheet("color:" + theme["text_muted"] + ";background:transparent;")

        # Music — Literata (tiene tildes)
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

        crumb = QLabel(book["icon"] + "  " + book["title"])
        crumb.setFont(body_font(9))
        crumb.setStyleSheet("color:" + t["text_muted"] + ";background:transparent;")

        # Título — Literata, no Ana
        title = QLabel(chapter["title"])
        title.setFont(body_font(28, bold=True))
        title.setWordWrap(True)
        title.setStyleSheet("color:" + t["text"] + ";background:transparent;margin-top:8px;margin-bottom:4px;")

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:" + t["border"] + ";margin:12px 0 20px 0;")

        raw = self._load(chapter)
        body = QLabel(raw)
        body.setFont(body_font(13))
        body.setWordWrap(True)
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        body.setStyleSheet("color:" + t["text"] + ";background:transparent;")
        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.page_lay.addWidget(crumb)
        self.page_lay.addWidget(title)
        self.page_lay.addWidget(sep)
        self.page_lay.addWidget(body)
        self.page_lay.addStretch()

        self.time_lbl.setText("Reading time: " + str(chapter["reading_time"]) + " min")
        artist, song = chapter["music"]
        self.music_lbl.setText("🎵  " + artist + " — " + song)
        self.scroll.verticalScrollBar().setValue(0)

    def _load(self, chapter):
        t = self.theme
        path = os.path.join("/usr/share/ana", chapter["file"])
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return md_to_html(f.read(), t)
        # Placeholder — "Check back soon." es voz de Ana pero sin tildes, ok
        return (
            "<p style='font-family:" + FONT_BODY + ";font-size:13px;color:" + t["text"] + ";line-height:1.8;margin-bottom:14px;'>"
            "This page hasn't been written yet.</p>"
            "<p style='font-family:" + FONT_ANA + ";font-size:15px;color:" + t["text_muted"] + ";'>"
            "Check back soon.</p>"
        )


class AnaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = THEME_LIGHT
        self._build()

    def _build(self):
        self.setWindowTitle("Ana")
        self.setMinimumSize(960, 620)
        self.resize(1140, 720)
        self.setStyleSheet("background:" + self.theme["bg"] + ";")

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(self.theme, self._on_chapter, self._toggle)
        root.addWidget(self.sidebar)

        div = QFrame()
        div.setFixedWidth(1)
        div.setStyleSheet("background:" + self.theme["border"] + ";")
        root.addWidget(div)

        self.stack = QStackedWidget()
        self.welcome = WelcomeScreen(self.theme)
        self.content = ContentView(self.theme)
        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.content)
        self.stack.setCurrentWidget(self.welcome)
        root.addWidget(self.stack)

    def _on_chapter(self, chapter, book):
        self.stack.setCurrentWidget(self.content)
        self.content.load_chapter(chapter, book)

    def _toggle(self):
        self.theme = THEME_DARK if self.theme["name"] == "light" else THEME_LIGHT
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(self.theme, self._on_chapter, self._toggle)
        root.addWidget(self.sidebar)

        div = QFrame()
        div.setFixedWidth(1)
        div.setStyleSheet("background:" + self.theme["border"] + ";")
        root.addWidget(div)

        self.stack = QStackedWidget()
        self.welcome = WelcomeScreen(self.theme)
        self.content = ContentView(self.theme)
        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.content)
        self.stack.setCurrentWidget(self.welcome)
        root.addWidget(self.stack)

        self.setStyleSheet("background:" + self.theme["bg"] + ";")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ana")
    app.setOrganizationName("Wagashi Linux")
    w = AnaWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
