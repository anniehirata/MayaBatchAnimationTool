# MayaBatchAnimationTool
UI tool for Maya to apply and save animations to a given character


Code to run the UI

    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    dialog = BatchAnimationsDialog()
    dialog.show()
