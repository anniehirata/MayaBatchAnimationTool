# Maya Batch Animation Tool
UI tool for Maya to apply and save animations to a given character
![alt text](./BatchAnimationsUI.png?raw=true "Batch Animations UI")

Code to run the UI

    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    dialog = BatchAnimationsDialog()
    dialog.show()
