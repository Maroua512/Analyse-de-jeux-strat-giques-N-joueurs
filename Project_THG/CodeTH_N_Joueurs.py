import tkinter as tk

from game_ui import GameTheoryApp


# Lance l'application graphique lorsque ce fichier est exécuté directement.
if __name__ == "__main__":
    root = tk.Tk()
    GameTheoryApp(root)
    root.mainloop()
