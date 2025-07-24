import sys
from PyQt5.QtWidgets import  QWidget, QApplication
from tracker_app import TrackerApp
from programa import mywindow
import yappi
import faulthandler

def main():
    app = QApplication(sys.argv)
    form = TrackerApp()
    application = mywindow()
    form.show()
    application.show()
    app.exec_()


if __name__ == '__main__':
    #yappi.start()
    #with open("fault_handler.log", "w") as fobj:
    faulthandler.enable()    
    main()
    #cProfile.run('main()')
    # Getting all the stats
    #yappi.get_func_stats().print_all()
