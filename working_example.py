import sys
from PyQt5.QtWidgets import QApplication, QWidget
 
import element_table


#some dummy printing functions to demonstrate the signals emitted:
def toggled_on(thingy):
    print('toggled on ' + thingy)
    
def toggled_off(thingy):
    print('toggled off ' + thingy)

def hovered_over(thingy):
    print('hovered over ' + thingy)
    
def hovered_off(thingy):
    print('hovered off ' + thingy)

def button_right_clicked(thingy):
    print('right clicked ' + thingy)   

def cleared_everything():
    print('all_cleared')

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    pet = element_table.ElementTableGUI(preenabled=['La','Si','Al'],
                                            disabled=['H','He'])
    pet.elementUnchecked.connect(toggled_off)
    pet.elementChecked.connect(toggled_on)
    pet.elementConsidered.connect(hovered_over)
    pet.elementUnconsidered.connect(hovered_off)
    pet.elementRightClicked.connect(button_right_clicked)
    pet.allElementsCleared.connect(cleared_everything)
    pet.show()
    
    sys.exit(app.exec_())
