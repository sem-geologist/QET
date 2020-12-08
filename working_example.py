import sys
from PyQt5.QtWidgets import QApplication, QWidget
import element_table


# some dummy printing functions to demonstrate the signals emitted:

def triggered(thingy):
    print('triggered ' + thingy)

def toggled_on(thingy):
    print('toggled on ' + thingy)


def toggled_off(thingy):
    print('toggled off ' + thingy)


def hovered_over(thingy):
    print('element {} considered'.format(thingy))


def hovered_off(thingy):
    print('element {} unconsidered'.format(thingy))


def button_right_clicked(thingy):
    print('right clicked ' + thingy)


def cleared_everything():
    print('all_cleared')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = element_table.ElementTableGUI(prechecked=['La', 'Si', 'Al'],
                                        state_list=['H', 'He'])
    pet.elementUnchecked.connect(toggled_off)
    pet.elementChecked.connect(toggled_on)
    pet.elementConsidered.connect(hovered_over)
    pet.elementUnconsidered.connect(hovered_off)
    pet.elementRightClicked.connect(button_right_clicked)
    pet.allElementsCleared.connect(cleared_everything)
    pet.elementTriggered.connect(triggered)
    pet.show()
    # second example using more options
    pet2 = element_table.ElementTableGUI(prechecked=['La', 'Si', 'Al', 'Ar'],
                                         state_list="REE,MAJOR",
                                         state_list_enables=True,
                                         silent_disabled=True,
                                         disable_fancy=True,
                                         buttons_auto_depress=True)

    pet2.elementUnchecked.connect(toggled_off)
    pet2.elementChecked.connect(toggled_on)
    pet2.elementConsidered.connect(hovered_over)
    pet2.elementUnconsidered.connect(hovered_off)
    pet2.elementRightClicked.connect(button_right_clicked)
    pet2.elementTriggered.connect(triggered)
    pet2.allElementsCleared.connect(cleared_everything)
    pet2.show()

    sys.exit(app.exec_())
