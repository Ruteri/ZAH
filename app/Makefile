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

ui/ui_aboutdialog.py: ui/aboutdialog.ui
	pyuic5 -o ui/ui_aboutdialog.py ui/aboutdialog.ui

ui/ui_citiesmapdialog.py: ui/citiesmapdialog.ui
	pyuic5 -o ui/ui_citiesmapdialog.py ui/citiesmapdialog.ui

ui/ui_inputdatadialog.py: ui/inputdatadialog.ui
	pyuic5 -o ui/ui_inputdatadialog.py ui/inputdatadialog.ui

rc/images_rc.py: rc/images.qrc
	pyrcc5 -o rc/images_rc.py rc/images.qrc

all:ui/ui_mainwindow.py \
	ui/ui_resultsdialog.py \
	ui/ui_aboutdialog.py \
	ui/ui_citiesmapdialog.py \
	ui/ui_inputdatadialog.py \
	rc/images_rc.py

.PHONY: clean
clean:
	rm -rf ui/ui_mainwindow.py ui/ui_resultsdialog.py ui/ui_aboutdialog.py rc/images_rc.py