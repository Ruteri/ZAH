.PHONY: default
default: all

# UI_FILES = \
# 	ui/mainwindow.ui \
# 	ui/resultsdialog.ui \

# RC_FILES = \
# 	rc/images.qrc

ui/ui_mainwindow.py: ui/mainwindow.ui
	pyuic5 -o ui/ui_mainwindow.py ui/mainwindow.ui

ui/ui_resultsdialog.py: ui/resultsdialog.ui
	pyuic5 -o ui/ui_resultsdialog.py ui/resultsdialog.ui

rc/images_rc.py: rc/images.qrc
	pyrcc5 -o rc/images_rc.py rc/images.qrc

all: ui/ui_mainwindow.py ui/ui_resultsdialog.py rc/images_rc.py

.PHONY: clean
clean:
	rm -rf ui/ui_mainwindow.py ui/ui_resultsdialog.py rc/images_rc.py