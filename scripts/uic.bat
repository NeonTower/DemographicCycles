@echo off
pyside6-uic ui\fake.ui -o src\autogen\fake.py
pyside6-uic ui\en_comp.ui -o src\autogen\en_comp.py --from-imports src\autogen
pyside6-uic ui\en_model.ui -o src\autogen\en_model.py --from-imports src\autogen
pyside6-uic ui\ru_comp.ui -o src\autogen\ru_comp.py --from-imports src\autogen
pyside6-uic ui\ru_model.ui -o src\autogen\ru_model.py --from-imports src\autogen