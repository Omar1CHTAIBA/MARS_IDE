from PyQt6.Qsci import QsciScintilla, QsciLexerHTML, QsciAPIs, QsciLexerJavaScript, QsciLexerCSS
from PyQt6.QtGui import QColor, QFont


class Lexers:
    def MainLexer(self):
        editor = QsciScintilla()
        editor.setUtf8(True)
        window_font = QFont('Consolas', 10)
        editor.setFont(window_font)
        editor.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setIndentationGuides(True)
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)

        editor.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        editor.setAutoCompletionThreshold(1)
        editor.setAutoCompletionCaseSensitivity(False)
        editor.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)

        editor.setCaretLineVisible(True)
        editor.setCaretWidth(2)

        editor.setEolMode(QsciScintilla.EolMode.EolWindows)
        editor.setEolVisibility(False)

        # lexer for HTML
        html_lexer = QsciLexerHTML()
        html_lexer.setDefaultFont(window_font)

        # api for HTML
        html_api = QsciAPIs(html_lexer)
        html_keywords_and_attributes = [
            "html", "head", "body", "title", "base", "meta", "link", "script", "style", "div", "span", "p", "a", "img",
            "form",
            "input", "button", "select", "option", "textarea", "label", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5",
            "h6",
            "table", "tr", "td", "th", "thead", "tbody", "tfoot", "caption", "footer", "header", "section", "article",
            "aside",
            "main", "nav", "blockquote", "code", "pre", "q", "abbr", "address", "cite", "dfn", "time", "var", "kbd",
            "samp",
            "progress", "meter", "details", "summary", "mark", "ins", "del", "svg", "canvas", "video", "audio",
            "iframe",
            "object", "embed", "picture", "source", "track", "iframe", "noscript", "b", "i", "u", "strong", "em",
            "small",
            "sub", "sup", "bdi", "bdo", "wbr", "br", "hr", "legend", "fieldset", "datalist", "keygen", "output", "area",
            "map", "col", "colgroup", "thead", "tfoot", "caption", "progress", "meter", "template", "slot", "basefont",
            "class", "id", "style", "src", "href", "alt", "title", "width", "height", "target", "rel", "type", "name",
            "value", "placeholder", "readonly", "disabled", "checked", "selected", "autofocus", "action", "method",
            "enctype",
            "novalidate", "form", "accept-charset", "charset", "cols", "rows", "for", "label", "max", "min", "step",
            "maxlength", "pattern", "accept", "multiple", "required", "contenteditable", "draggable", "spellcheck",
            "hidden", "accesskey", "tabindex", "lang", "dir", "media", "sizes", "crossorigin", "download", "type",
            "crossorigin", "async", "defer", "integrity", "referrerpolicy", "autoplay", "controls", "loop", "muted",
            "poster"]
        for keyword_attribute in html_keywords_and_attributes:
            html_api.add(keyword_attribute)

        html_api.prepare()

        editor.setLexer(html_lexer)

        # Line numbers
        editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        editor.setMarginWidth(0, "00000")
        editor.setMarginsForegroundColor(QColor("#A9B7C6"))  # PyCharm line number color
        editor.setMarginsBackgroundColor(QColor("#2b2b2b"))
        editor.setMarginsFont(window_font)

        # Set colors for editor
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_DEFAULT, QColor("#A9B7C6"))
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.Tag, QColor("#FFA500"))  # Tags
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.Attribute, QColor("#666699"))  # Attributes
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.HTMLDoubleQuotedString, QColor("#6A8759"))  # Double-quoted strings
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.HTMLComment, QColor("#808080"))  # Comments
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.HTMLNumber, QColor("#FF0000"))  # Numbers - Red\

        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.HTMLSingleQuotedString, QColor("#98C379"))  # Embedded content - single-quoted strings
        # editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.keywords, QColor("#C678DD"))  # Embedded content - keywords
                  
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerHTML.JavaScriptKeyword, QColor("#C678DD"))  

        editor.setCaretForegroundColor(QColor("#FFFFFF"))

        # Set the selection color
        editor.setSelectionBackgroundColor(QColor("#214283"))

        return editor
