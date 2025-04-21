@echo off
pyside6-lupdate src\MainWindow.py ^
  src\controllers\DiscreteModeController.py ^
  src\controllers\ExerciseController.py ^
  src\controllers\PlotController.py ^
  src\controllers\ScenarioController.py ^
  ui\fake.ui -ts resources\translations\main_en.ts
pyside6-lrelease resources\translations\main_en.ts -qm resources\translations\main_en.qm