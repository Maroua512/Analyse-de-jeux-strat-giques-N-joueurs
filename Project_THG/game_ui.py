import tkinter as tk
from itertools import product
from tkinter import Button, Label, Toplevel, messagebox
from tkinter.scrolledtext import ScrolledText

from ttkbootstrap import Style

import game_analysis


class GameTheoryApp:
    # Initialise la fenêtre, les données de l'application et les composants graphiques.
    def __init__(self, root):
        self.root = root
        self.root.title("Game Theory Analyzer")
        self.root.geometry("900x700")
        self.style = Style("flatly")
        self.num_players = 0
        self.strategy_entries = []
        self.entries = {}
        self.profiles = []
        self.strategies_per_player = []
        self.build_ui()

    # Construit les champs et les boutons permanents de l'interface.
    def build_ui(self):
        Label(self.root, text="Game Theory Analysis Tool", font=("Helvetica", 20, "bold")).pack(pady=20)
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        Label(self.input_frame, text="Nombre de joueurs :", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.num_players_entry = tk.Entry(self.input_frame, width=5)
        self.num_players_entry.grid(row=0, column=1, padx=5)
        tk.Button(self.input_frame, text="Valider", command=self.create_strategy_fields, bg="#0275d8", fg="white").grid(row=0, column=2, padx=5)
        self.dynamic_frame = tk.Frame(self.root)
        self.dynamic_frame.pack(pady=20)
        self.matrix_frame = tk.Frame(self.root)
        self.matrix_frame.pack(pady=10)
        self.calc_button = tk.Button(self.root, text="Analyser", command=self.show_analysis, bg="#f0ad4e", fg="white")
        self.result_label = Label(self.root, text="", justify="left", font=("Arial", 9))

    # Demande le nombre de joueurs et crée un champ pour leurs stratégies.
    def create_strategy_fields(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.strategy_entries.clear()
        try:
            self.num_players = int(self.num_players_entry.get())
            if self.num_players < 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Entrez un nombre valide de joueurs (>=2).")
            return
        Label(self.dynamic_frame, text="Nombre de stratégies par joueur :", font=("Helvetica", 12)).pack(pady=5)
        for player in range(self.num_players):
            frame = tk.Frame(self.dynamic_frame)
            frame.pack(pady=3)
            Label(frame, text=f"Joueur {player + 1} :", width=12).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.strategy_entries.append(entry)
        tk.Button(self.dynamic_frame, text="Valider stratégies", command=self.create_matrix_inputs, bg="#5cb85c", fg="white").pack(pady=10)

    # Crée la matrice de saisie des gains pour tous les profils de stratégies.
    def create_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
        try:
            self.strategies_per_player = [int(entry.get()) for entry in self.strategy_entries]
            if not all(count > 0 for count in self.strategies_per_player):
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les stratégies.")
            return
        self.entries = {}
        self.profiles = list(product(*[range(count) for count in self.strategies_per_player]))
        Label(self.matrix_frame, text="Remplissez les paiements pour chaque profil :").pack()
        grid = tk.Frame(self.matrix_frame)
        grid.pack()
        for row, profile in enumerate(self.profiles):
            Label(grid, text=f"{profile}").grid(row=row, column=0, sticky="e")
            self.entries[profile] = []
            for player in range(self.num_players):
                entry = tk.Entry(grid, width=5)
                entry.grid(row=row, column=player + 1)
                self.entries[profile].append(entry)
        self.calc_button.pack(pady=10)
        self.result_label.pack(pady=5)

    # Convertit les gains saisis dans l'interface en données numériques.
    def get_payoffs(self):
        payoffs = {}
        for profile, entry_list in self.entries.items():
            try:
                payoffs[profile] = tuple(float(entry.get()) for entry in entry_list)
            except ValueError:
                messagebox.showerror("Erreur", f"Entrée invalide pour le profil {profile}")
                return None
        return payoffs

    # Lance les analyses et affiche leurs résultats dans une nouvelle fenêtre.
    def show_analysis(self):
        payoffs = self.get_payoffs()
        if payoffs is None:
            return
        arguments = (self.num_players, self.strategies_per_player, self.profiles, payoffs)
        result = "🔹 Stratégies Strictement Dominantes\n" + game_analysis.calculate_dominant_strategies(*arguments)
        result += "\n\n🔹 Stratégies Faiblement Dominantes\n" + game_analysis.calculate_weakly_dominant_strategies(*arguments)
        result += "\n\n🔹 Équilibres de Nash\n" + game_analysis.calculate_nash_equilibria(*arguments)
        result += "\n\n🔹 Optima de Pareto\n" + game_analysis.calculate_pareto_optima(self.num_players, self.profiles, payoffs)
        result += "\n\n🔹 Niveaux de sécurité\n" + game_analysis.calculate_security_levels(*arguments)
        result += "\n\n🔹 Élimination itérative\n" + game_analysis.calculate_iterated_elimination(*arguments)
        result_window = Toplevel(self.root)
        result_window.title("Résultats de l'analyse")
        result_window.geometry("700x600")
        Label(result_window, text="Analyse du jeu", font=("Helvetica", 16, "bold")).pack(pady=10)
        text_area = ScrolledText(result_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill="both")
        text_area.insert(tk.END, result)
        text_area.config(state=tk.DISABLED)
        Button(result_window, text="Fermer", command=result_window.destroy, bg="#d9534f", fg="white").pack(pady=10)