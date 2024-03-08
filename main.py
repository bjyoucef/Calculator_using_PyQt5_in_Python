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


class Calculator():
    def __init__(self, ui):
        self.ui = ui
        self.first_number = ''
        self.second_number = ''
        self.result = ''
        self.operator_selected = False
        self.equation_completed = False
        self.ui.calcLabel.setText('')

        # Connect number buttons dynamically
        for i in range(10):
            button = getattr(self.ui, f"btn{i}")
            button.clicked.connect(lambda _, num=str(i): self.func_button_num(num))

        self.ui.btnAdd.clicked.connect(lambda: self.func_button_flag('+'))
        self.ui.btnMultiply.clicked.connect(lambda: self.func_button_flag('*'))
        self.ui.btnDivide.clicked.connect(lambda: self.func_button_flag('/'))

        self.ui.btnSubtract.clicked.connect(self.func_button_subtract)
        self.ui.btnPoint.clicked.connect(self.func_button_dot)
        self.ui.btnC.clicked.connect(self.func_button_cls)
        self.ui.btnEvaluate.clicked.connect(self.evaluate_expression)

    def func_calcLabel(self):
        self.ui.calcLabel.setText(f"{self.first_number} {self.operator} {self.second_number}")

    def func_button_num(self, num):
        if not self.equation_completed:
            if not self.operator_selected:
                self.first_number += num
                self.ui.calcLabel.setText(self.first_number.lstrip('0') or '0')
            else:
                self.second_number += num
                self.func_calcLabel()
        else:
            if not self.operator_selected:
                self.first_number += num
                self.ui.calcLabel.setText(self.first_number.lstrip('0') or '0')
                self.equation_completed = False

    def func_button_dot(self):
        if not self.equation_completed:
            if not self.operator_selected and "." not in self.first_number:
                self.first_number += "." if self.first_number else "0."
                self.ui.calcLabel.setText(self.first_number)
            elif "." not in self.second_number:
                self.second_number += "." if self.second_number else "0."
                self.func_calcLabel()
        else:
            if not self.operator_selected and "." not in self.first_number:
                self.first_number += "." if self.first_number else "0."
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

    def evaluate_expression(self):
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
