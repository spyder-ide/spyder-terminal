
from qtpy.QtCore import Slot
from qtpy.QtWidgets import (QGridLayout, QHBoxLayout, QLabel,
                            QSizePolicy, QWidget)

from spyder.utils.misc import regexp_error_msg
from spyder.widgets.findreplace import FindReplace


class FindTerminal(FindReplace):
    """Find in terminal widget."""

    def __init__(self, parent):
        super().__init__(parent, enable_replace=False)
        self.parent = parent

    def show(self, hide_replace=False):
        """Overrides Qt Method"""
        QWidget.show(self)
        self.visibility_changed.emit(True)
        self.search_text.setFocus()

    @Slot()
    def hide(self):
        """Overrides Qt Method"""
        QWidget.hide(self)
        self.visibility_changed.emit(False)

    @Slot(bool)
    def toggle_highlighting(self, state):
        """Override the method from FindReplace widget."""
        pass

    def highlight_matches(self):
        """Override the method from FindReplace widget."""
        pass

    def clear_matches(self):
        """Override the method from FindReplace widget."""
        pass

    def find(self, changed=True, forward=True, rehighlight=False,
             start_highlight_timer=False, multiline_replace_check=False):
        """Call the find function"""
        text = self.search_text.currentText()
        if len(text) == 0:
            self.search_text.lineEdit().setStyleSheet("")
            return None
        else:
            case = self.case_button.isChecked()
            word = self.words_button.isChecked()
            regexp = self.re_button.isChecked()
            if forward:
                found = self.parent.search_next(text, case=case,
                                                regex=regexp, word=word)
            else:
                found = self.parent.search_previous(text, case=case,
                                                    regex=regexp, word=word)

            found = False if found == -1 else True
            stylesheet = self.STYLE[found]
            tooltip = self.TOOLTIP[found]
            if not found and regexp:
                error_msg = regexp_error_msg(text)
                if error_msg:  # special styling for regexp errors
                    stylesheet = self.STYLE['regexp_error']
                    tooltip = self.TOOLTIP['regexp_error'] + ': ' + error_msg
            self.search_text.lineEdit().setStyleSheet(stylesheet)
            self.search_text.setToolTip(tooltip)
            return found
