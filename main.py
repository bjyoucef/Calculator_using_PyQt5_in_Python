# pyuic5 -x interfaceCal.ui -o ui_interfaceCal.py
# pyrcc5 ressources.qrc -o ressources_rc.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Gui.ui_interfaceCal import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupCalculator()

    def setupCalculator(self):
        self.calculator = Calculator(self.ui)

        for i in range(10):
            button = getattr(self.ui, f"btn{i}")
            button.clicked.connect(lambda _, num=str(i): self.calculator.func_button_num(num))

        self.ui.btnAdd.clicked.connect(lambda: self.calculator.func_button_flag('+'))
        self.ui.btnMultiply.clicked.connect(lambda: self.calculator.func_button_flag('*'))
        self.ui.btnDivide.clicked.connect(lambda: self.calculator.func_button_flag('/'))
        self.ui.btnSubtract.clicked.connect(lambda: self.calculator.func_button_flag('-'))

        self.ui.btnPoint.clicked.connect(self.calculator.func_button_dot)
        self.ui.btnAC.clicked.connect(self.calculator.clear_all)
        self.ui.btnC.clicked.connect(self.calculator.clear)
        self.ui.btnEvaluate.clicked.connect(self.calculator.evaluate)


class Calculator:

    def __init__(self, ui):
        self.result = None
        self.operator_selected = None
        self.operator = None
        self.equation_completed = None
        self.first_number = None
        self.second_number = None
        self.ui = ui
        self.clear_all()

    def clear_all(self):
        self.equation_completed = False
        self.operator_selected = False
        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''
        self.ui.calcLabel.setText('')
        self.ui.textEdit_HC.clear()



    def clear(self):
        if self.equation_completed:
            return
        if self.second_number:
            self.second_number = self.second_number[:-1]
            self.func_calcLabel()
        elif self.operator_selected:
            self.operator_selected = False
            self.operator = ''
            self.func_calcLabel()
        elif self.first_number:
            self.first_number = self.first_number[:-1]
            self.ui.calcLabel.setText(self.first_number.lstrip('0') or '0')

    def func_calcLabel(self):
        self.ui.calcLabel.setText(f"{self.first_number} {self.operator} {self.second_number}")

    def func_button_num(self, num):
        if not self.equation_completed:
            if not self.operator_selected:
                if "." not in self.first_number:
                    self.first_number += num
                    self.first_number = self.first_number.lstrip('0')
                    self.ui.calcLabel.setText(self.first_number or '0')
                else:
                    self.first_number += num
                    self.ui.calcLabel.setText(self.first_number)

            else:
                if "." not in self.second_number:
                    self.second_number += num
                    self.second_number = self.second_number.lstrip('0')
                else:
                    self.second_number += num
                self.func_calcLabel()
        else:
            if not self.operator_selected:
                if "." not in self.first_number:
                    self.first_number += num
                    self.first_number = self.first_number.lstrip('0')
                    self.ui.calcLabel.setText(self.first_number or '0')
                else:
                    self.first_number += num
                    self.ui.calcLabel.setText(self.first_number)
                self.equation_completed = False

    def func_button_flag(self, operator):
        if not self.equation_completed and not self.operator_selected:
            self.operator = operator
            self.operator_selected = True
            self.func_calcLabel()

        elif self.equation_completed and not self.operator_selected:
            self.first_number = self.result
            self.second_number = ""
            self.operator = operator
            self.operator_selected = True
            self.func_calcLabel()

        elif self.operator_selected:
            self.second_number = ""

        self.operator = operator
        self.operator_selected = True
        self.func_calcLabel()
        self.equation_completed = False

    def func_button_dot(self):
        if not self.equation_completed:
            if not self.operator_selected:
                if "." not in self.first_number:
                    if self.first_number:
                        self.first_number += "."
                    else:
                        self.first_number = "0."
                    self.ui.calcLabel.setText(self.first_number)
            else:
                if "." not in self.second_number:
                    if self.second_number:
                        self.second_number += "."
                    else:
                        self.second_number = "0."
                    self.func_calcLabel()

        else:
            if not self.operator_selected:
                pass
            else:
                if "." not in self.second_number:
                    if self.second_number:
                        self.second_number += "."
                    else:
                        self.second_number = "0."
                    self.func_calcLabel()

    def func_button_subtract(self):
        if not self.equation_completed:
            if not self.operator_selected:
                self.first_number = "-" if self.first_number == "" else self.first_number
                self.operator_selected = True
                self.operator = "-"
                self.func_calcLabel()
            elif not self.second_number:
                self.second_number = "-"
                self.func_calcLabel()
        else:
            self.first_number = self.result
            if not self.operator_selected:
                self.first_number = "-" if self.first_number == "" else self.first_number
                self.operator_selected = True
                self.operator = "-"
                self.func_calcLabel()
            elif "-" in self.second_number:
                pass
            elif not self.second_number:
                self.second_number = "-"
                self.func_calcLabel()

    def evaluate(self):
        try:
            if self.operator_selected:
                self.result = str(eval(f"{self.first_number} {self.operator} {self.second_number}"))
                self.ui.calcLabel.setText(self.result)

                self.ui.textEdit_HC.append(f"{self.first_number} {self.operator} {self.second_number} = {self.result}")
                self.equation_completed = True
                self.operator_selected = False
                self.first_number = ""
                self.second_number = ""

        except ZeroDivisionError:
            self.ui.calcLabel.setText("Cannot divide by zero")
        except SyntaxError:
            self.ui.calcLabel.setText("Invalid expression")
        except Exception as e:
            self.ui.calcLabel.setText(f"An error occurred: {e}")

    def func_button_cls(self):
        self.first_number = ''
        self.second_number = ''
        self.result = ''
        self.operator_selected = False
        self.equation_completed = False
        self.ui.calcLabel.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    # window.showFullScreen()  # open the window in full-screen mode
    sys.exit(app.exec_())
