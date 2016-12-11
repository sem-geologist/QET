import sys
from PyQt5.QtWidgets import QApplication, QWidget
 
import element_table_Qt5


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
    pet = element_table_Qt5.ElementTableGUI(preenabled=['La','Si','Al'])
    pet.disableElement.connect(toggled_off)
    pet.enableElement.connect(toggled_on)
    pet.elementHoveredOver.connect(hovered_over)
    pet.elementHoveredOff.connect(hovered_off)
    pet.someButtonRightClicked.connect(button_right_clicked)
    pet.allElementsCleared.connect(cleared_everything)
    pet.show()
    
    sys.exit(app.exec_())
