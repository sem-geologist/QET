# -*- coding: utf-8 -*-
#
# Copyright 2016 Petras Jokubauskas
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with any project and source this library is coupled.
# If not, see <http://www.gnu.org/licenses/>.
#

from PyQt5 import QtCore, Qt
import re

# the periodic table possitions in gui:
# row, column:
pt_indexes = {'H': (0, 0), 'He': (0, 17), 'Li': (1, 0),
              'Be': (1, 1), 'B': (1, 12), 'C': (1, 13),
              'N': (1, 14), 'O': (1, 15), 'F': (1, 16),
              'Ne': (1, 17), 'Na': (2, 0), 'Mg': (2, 1),
              'Al': (2, 12), 'Si': (2, 13), 'P': (2, 14),
              'S': (2, 15), 'Cl': (2, 16), 'Ar': (2, 17),
              'K': (3, 0), 'Ca': (3, 1), 'Sc': (3, 2),
              'Ti': (3, 3), 'V': (3, 4), 'Cr': (3, 5),
              'Mn': (3, 6), 'Fe': (3, 7), 'Co': (3, 8),
              'Ni': (3, 9), 'Cu': (3, 10), 'Zn': (3, 11),
              'Ga': (3, 12), 'Ge': (3, 13), 'As': (3, 14),
              'Se': (3, 15), 'Br': (3, 16), 'Kr': (3, 17),
              'Rb': (4, 0), 'Sr': (4, 1), 'Y': (4, 2),
              'Zr': (4, 3), 'Nb': (4, 4), 'Mo': (4, 5),
              'Tc': (4, 6), 'Ru': (4, 7), 'Rh': (4, 8),
              'Pd': (4, 9), 'Ag': (4, 10), 'Cd': (4, 11),
              'In': (4, 12), 'Sn': (4, 13), 'Sb': (4, 14),
              'Te': (4, 15), 'I': (4, 16), 'Xe': (4, 17),
              'Cs': (5, 0), 'Ba': (5, 1), 'La': (7, 3),
              'Ce': (7, 4), 'Pr': (7, 5), 'Nd': (7, 6),
              'Pm': (7, 7), 'Sm': (7, 8), 'Eu': (7, 9),
              'Gd': (7, 10), 'Tb': (7, 11), 'Dy': (7, 12),
              'Ho': (7, 13), 'Er': (7, 14), 'Tm': (7, 15),
              'Yb': (7, 16), 'Lu': (7, 17), 'Hf': (5, 3),
              'Ta': (5, 4), 'W': (5, 5), 'Re': (5, 6),
              'Os': (5, 7), 'Ir': (5, 8), 'Pt': (5, 9),
              'Au': (5, 10), 'Hg': (5, 11), 'Tl': (5, 12),
              'Pb': (5, 13), 'Bi': (5, 14), 'Po': (5, 15),
              'At': (5, 16), 'Rn': (5, 17), 'Fr': (6, 0),
              'Ra': (6, 1), 'Ac': (8, 3), 'Th': (8, 4),
              'Pa': (8, 5), 'U': (8, 6), 'Np': (8, 7),
              'Pu': (8, 8)}

# element groups:
# TODO: this could go to json and configs
geo_groups = {'LITHOPHILE': ['Na', 'K', 'Si', 'Al', 'Ti', 'Mg', 'Ca'],
              'SIDEROPHILE': ['Fe', 'Co', 'Ni', 'Pt', 'Re', 'Os'],
              'CHALCOPHILE': ['Cu', 'Ag', 'Zn', 'Pb', 'S'],
              'LILE': ['K', 'Rb', 'Cs', 'Ba'],
              'HFSE': ['Zr', 'Nb', 'Th', 'U'],
              'MAJOR': ['O', 'Na', 'K', 'Si', 'Al', 'Ti', 'Mg',
                        'Ca', 'Fe'],
              'HALOGENS': ['F', 'Cl', 'Br'],
              'REE': ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm',
                      'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
                      'Tm', 'Yb', 'Lu'],
              'LREE': ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm'],
              'HREE': ['Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
                       'Tm', 'Yb', 'Lu'],
              'COMMON': ['O', 'Na', 'K', 'Si', 'Al', 'Ti', 'Mg', 'Ca',
                         'Cr', 'Mn', 'Fe'],
              'ALL': ['He', 'Se', 'Sb', 'Pt', 'Ar', 'Ba', 'As', 'Pa',
                      'Au', 'Dy', 'Bi', 'U', 'Ne', 'Re', 'Al', 'Sc',
                      'Mn', 'Ra', 'In', 'O', 'P', 'Mo', 'Tb', 'V',
                      'Na', 'Ta', 'Hg', 'Ca', 'Hf', 'Ac', 'Eu', 'Nd',
                      'Br', 'Ag', 'Kr', 'W', 'K', 'S', 'Ga', 'At',
                      'Co', 'Sr', 'C', 'Ce', 'Be', 'I', 'Ni', 'Er',
                      'Cu', 'Cr', 'Ho', 'B', 'Li', 'Nb', 'Ru', 'Si',
                      'H', 'Rn', 'Zn', 'Yb', 'Pm', 'Te', 'Ti', 'F',
                      'Pu', 'Lu', 'La', 'Ge', 'Ir', 'Mg', 'Po', 'Pd',
                      'Y', 'Sn', 'Sm', 'Np', 'Zr', 'Cl', 'Tl', 'Xe',
                      'Gd', 'Os', 'Fe', 'Pb', 'Tm', 'Cd', 'N', 'Tc',
                      'Cs', 'Pr', 'Th', 'Rb', 'Fr', 'Rh']}

element_regex = r"C[laroudse]?|Os?|N[eaibdps]?|S[icernbm]?|" +\
        r"H[eofga]?|A[lrsgutcm]|B[erai]?|Dy|E[ur]|F[er]?|G[aed]|" +\
        r"I[nr]?|Kr?|L[iau]|M[gno]|R[buhena]|T[icebmalh]|" +\
        r"U|V|W|Xe|Yb?|Z[nr]|P[drmtboau]?"

geo_regex = '(?:%s)' % '|'.join(geo_groups.keys())


def separate_text(ptext):
    "Sparate text into positive and negative (with '-' sign)"
    if '-' in ptext:
        first_level = re.findall(r"[-]|[A-Z a-z,;]*", ptext)
        if first_level.index('-') == 0:
            positive_text = ''
            negative_text = first_level[1]
        else:
            positive_text = first_level[0]
            negative_text = first_level[first_level.index('-') + 1]
    else:
        positive_text = ptext
        negative_text = ''
    return positive_text, negative_text


def parse_elements(text):
        parsed = []
        geo_list = re.findall(geo_regex, text)
        for i in geo_list:
            parsed.extend(geo_groups[i])
            text = text.replace(i, '')
        parsed.extend(re.findall(element_regex, text))
        return set(parsed)


class HoverableButton(Qt.QPushButton):
    hoverChanged = QtCore.pyqtSignal()
    gainedFocus = QtCore.pyqtSignal()
    lostFocus = QtCore.pyqtSignal()

    def __init__(self, name, partly_disabled=True):
        Qt.QAbstractButton.__init__(self)
        self.partly_disabled = partly_disabled
        self.setMouseTracking(1)
        self.setText(name)
        self.setCheckable(True)
        self.hoverState = False
        self.orig_size = self.geometry()

    def focusInEvent(self, event):
        self.gainedFocus.emit()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.lostFocus.emit()
        super().focusOutEvent(event)

    def enterEvent(self, event):
        if self.isEnabled() or self.partly_disabled:
            self.hoverState = True
            self.hoverChanged.emit()
            self.orig_size = self.geometry()
            # some fancy graphic effects (inspired by KDE kalzium):
            self.setGeometry(self.orig_size.x() - self.orig_size.width() / 5,
                             self.orig_size.y() - self.orig_size.height() / 5,
                             self.orig_size.width() * 1.4,
                             self.orig_size.height() * 1.4)
            self.raise_()

    def leaveEvent(self, event):
        if self.isEnabled() or self.partly_disabled:
            self.hoverState = False
            self.hoverChanged.emit()
            self.setGeometry(self.orig_size)


class ElementTableGUI(Qt.QWidget):
    """Create the periodic element gui with toggleble buttons
    for element selection and preview signal triggered with
    mouse hover events and right click for optional menu/ window.

    Initialisation can take python list with elements
    for which buttons is pre-toggled:
    -----------
    args:
    preenabled -- python list with elements (abbrevations), the
    buttons which should be initially pushed.
    disabled = python list with elements (abbrevations) for buttons
    which should be disabled.
    -----------

    additionally to native QtGui.QTableWidget provides
    such signals:

    elementConsidered -- signal which emits element abbrevation
        when mouse hovers over the button, or the coresponding
        button gets focus, or is emitted by text input interface.
    elementUnconsidered -- emits element abrevation at moment mouse
        leaves the button area
    elementChecked -- emits the element abbrevation when button
        changes to checked possition.
    elementUnchecked -- emits the element abbrevation when button
        changes to unchecked possition.

    elementRightClicked -- emits the element abbrevation when
        button gets right clicked.

    allElementsCleared -- emits, when the clear all button clicked.
        Alternatively the element by element could be dissabled,
        however this signal can be much faster.
    """

    # preview slots:
    elementConsidered = QtCore.pyqtSignal(str)
    elementUnconsidered = QtCore.pyqtSignal(str)
    # button press slots:
    elementChecked = QtCore.pyqtSignal(str)
    elementUnchecked = QtCore.pyqtSignal(str)
    # right_mouse_button_press_slot:
    elementRightClicked = QtCore.pyqtSignal(str)
    allElementsCleared = QtCore.pyqtSignal()

    def __init__(self, parent=None,
                 preenabled=[], disabled=[]):
        super().__init__()
        self.setWindowTitle('Element Table')
        layout = Qt.QGridLayout(self)
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(4, 4, 4, 4)
        self._setup_table(preenabled, disabled)
        self._setup_text_interface()
        self.resize(400, 250)
        self._setup_clear_all()

    def _setup_clear_all(self):
        self.clear_all_button = Qt.QPushButton('Clear all')
        self.layout().addWidget(self.clear_all_button, 7, 0, 2, 3)
        self.clear_all_button.pressed.connect(self.clear_all)
        self.clear_all_button.setMinimumSize(32, 32)
        self.clear_all_button.setMaximumSize(512, 512)

    def _setup_text_interface(self):
        self.textInterface = Qt.QLineEdit()
        self.textInterface.setMinimumSize(16, 16)
        self.layout().addWidget(self.textInterface, 8, 9, 1, 9)
        self.textInterface.returnPressed.connect(self.toggle_elements)
        self.textInterface.textChanged.connect(self.consider_element)
        self.textInterface.setToolTip(
            "text interface.\n"
            "Input abbrevations of elements:\n"
            "    without any space:\n"
            "        AlSiNaK\n"
            "    with any separators like comma/space:\n"
            "        Al;Br K,La\n"
            "abbrevations of element groups:\n"
            "    HFSE, REE, REE_SEM, LILE, major\n"
            "Use '-' (minus) sign to switch all elements after it:\n"
            "    -AlCa, K; P -> toggles off Al, Ca, K, P\n"
            "HFSE - Nb -> toggles on HFSE elements, but switches off Nb")
        completer = Qt.QCompleter(list(pt_indexes.keys()) +
                                  list(geo_groups.keys()))
        self.textInterface.setCompleter(completer)
        self.textInterface.setMaximumSize(512, 1024)

    def getButton(self, index):
        """index - tuple"""
        item = self.layout().itemAtPosition(*index)
        return item.widget()

    def toggle_elements(self):
        ptext = self.textInterface.text()
        positive_text, negative_text = separate_text(ptext)
        # clear text interface:
        self.textInterface.clear()
        # parse what to add first:
        positive_list = parse_elements(positive_text)
        self.toggle_on(positive_list)
        # parse what to remove:
        negative_list = parse_elements(negative_text)
        self.toggle_off(negative_list)

    def consider_element(self, text):
        positive_text = separate_text(text)[0]
        positive_list = parse_elements(positive_text)
        self.elementUnconsidered.emit('')
        for i in positive_list:
            self.elementConsidered.emit(i)

    def toggle_on(self, toggle_list):
        for i in toggle_list:
            button = self.getButton(pt_indexes[i])
            if button.isEnabled():
                button.setChecked(True)
                button.setStyleSheet("""font: bold;""")

    def toggle_off(self, toggle_list):
        for i in toggle_list:
            button = self.getButton(pt_indexes[i])
            if button.isEnabled():
                button.setChecked(False)
                button.setStyleSheet("""font: normal;""")

    def clear_all(self):
        self.blockSignals(True)
        self.toggle_off(geo_groups['ALL'])
        self.blockSignals(False)
        self.allElementsCleared.emit()

    def _setup_table(self, enabled_elements, disabled_elements):
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[Qt.QWidget].connect(self.previewToggler)
        self.signalMapper2 = QtCore.QSignalMapper(self)
        self.signalMapper2.mapped[Qt.QWidget].connect(self.elementToggler)
        self.signalMapper3 = QtCore.QSignalMapper(self)
        self.signalMapper3.mapped[Qt.QWidget].connect(self.emit_right_clicked)
        self.signalMapper4 = QtCore.QSignalMapper(self)
        self.signalMapper4.mapped[Qt.QWidget].connect(self.focus_on_toggler)
        self.signalMapper5 = QtCore.QSignalMapper(self)
        self.signalMapper5.mapped[Qt.QWidget].connect(self.focus_off_toggler)
        for i in pt_indexes:
            pt_button = HoverableButton(i)
            pt_button.setMinimumSize(16, 16)
            pt_button.setMaximumSize(512, 512)
            if i in enabled_elements:
                pt_button.setChecked(True)
            self.layout().addWidget(pt_button,
                                    pt_indexes[i][0],
                                    pt_indexes[i][1])
            pt_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            pt_button.hoverChanged.connect(self.signalMapper.map)
            pt_button.toggled.connect(self.signalMapper2.map)
            pt_button.customContextMenuRequested.connect(
                self.signalMapper3.map)
            pt_button.gainedFocus.connect(self.signalMapper4.map)
            pt_button.lostFocus.connect(self.signalMapper5.map)
            self.signalMapper.setMapping(pt_button, pt_button)
            self.signalMapper2.setMapping(pt_button, pt_button)
            self.signalMapper3.setMapping(pt_button, pt_button)
            self.signalMapper4.setMapping(pt_button, pt_button)
            self.signalMapper5.setMapping(pt_button, pt_button)
        line = Qt.QFrame()
        line.setFrameShape(Qt.QFrame.HLine)
        line.setFrameShadow(Qt.QFrame.Sunken)
        line.setSizePolicy(Qt.QSizePolicy.Preferred, Qt.QSizePolicy.Preferred)
        self.layout().addWidget(line, 6, 3, 1, 15)
        # dissable inert gasses and H, He and Li:
        for i in disabled_elements:
            self.getButton(pt_indexes[i]).setEnabled(False)
        lant_text = Qt.QLabel('Lan')
        act_text = Qt.QLabel('Act')
        lant_text.setAlignment(QtCore.Qt.AlignCenter)
        act_text.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().addWidget(lant_text, 5, 2)
        self.layout().addWidget(act_text, 6, 2)
        lant_text.setEnabled(False)
        act_text.setEnabled(False)

    def keyPressEvent(self, event):
        """Jump to text interface at shift key press"""
        if event.key() == QtCore.Qt.Key_Shift:
            self.textInterface.setFocus()

    # @QtCore.pyqtSlot(QtCore.QObject)  # NOTE decorators are commented out
    # as pyQt5.7 made regression with using QObject or QWidget in signals
    # or is it the problem with mapping of signals?
    def previewToggler(self, button):
        # if button.isEnabled():
        if button.hoverState:
            self.elementConsidered.emit(button.text())
        else:
            self.elementUnconsidered.emit(button.text())

    def focus_on_toggler(self, button):
        """this is for sending same signal as with hovering, but by
        "Tab" jumping through buttons"""
        self.elementConsidered.emit(button.text())

    def focus_off_toggler(self, button):
        """this is for sending same signal as with hovering, but by
        "Tab" jumping through buttons"""
        self.elementUnconsidered.emit(button.text())

    # @QtCore.pyqtSlot(QtCore.QObject)
    def elementToggler(self, button):
        if button.isChecked():
            self.elementChecked.emit(button.text())
            if button.hoverState:
                button.setGeometry(button.orig_size)
                button.setStyleSheet("""font: bold;""")
        else:
            self.elementUnchecked.emit(button.text())
            button.setStyleSheet("""font: normal;""")

    # @QtCore.pyqtSlot(QtCore.QObject)
    def emit_right_clicked(self,  button):
        self.elementRightClicked.emit(button.text())

    def toggle_buttons_wo_trigger(self, elements):
        self.signalMapper2.blockSignals(True)
        for i in elements:
            self.layout().itemAtPosition(pt_indexes[i][0],
                                         pt_indexes[i][1]).widget().toggle()
        self.signalMapper2.blockSignals(False)
