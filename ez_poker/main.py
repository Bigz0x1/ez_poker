import tkinter as tk
from tkinter import ttk
from treys import Card, Evaluator
from itertools import product
import random

def init_window():
    window = tk.Tk()
    window.title("Poker Ripper")
    window.geometry("650x300")

    # Polices
    label_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    # Création du style
    style = ttk.Style()
    style.configure("Custom.TButton", font=button_font)

    # Créez un champ d'entrée pour la main de départ
    entry_frame = ttk.Frame(window)
    entry_frame.grid(column=0, row=0, sticky="EW")
    ttk.Label(entry_frame, text="Main de départ :", font=label_font).grid(row=0, column=0)
    entry = ttk.Entry(entry_frame)
    entry.grid(column=1, row=0)

    # Créez un bouton pour évaluer la main de départ
    bouton_evaluer = ttk.Button(window, text="Évaluer", command=lambda: evaluer_main_interface(entry, label_result), style="Custom.TButton")
    bouton_evaluer.grid(column=0, row=1, padx=5, pady=5)

    # Créez un label pour afficher le résultat
    label_result = ttk.Label(window, text="")
    label_result.grid(column=0, row=2)

    # Cartes en main
    hand_frame = ttk.Frame(window)
    hand_frame.grid(column=0, row=3, sticky="EW")
    ttk.Label(hand_frame, text="Cartes en main :", font=label_font).grid(row=3, column=0)
    hand_var = tk.StringVar()
    hand_entry = ttk.Entry(hand_frame, textvariable=hand_var)
    hand_entry.grid(row=3, column=1)

    # Cartes sur la table
    table_frame = ttk.Frame(window)
    table_frame.grid(column=0, row=4, sticky="EW")
    ttk.Label(table_frame, text="Cartes sur la table :", font=label_font).grid(row=4, column=0)
    table_cards_var = tk.StringVar()
    table_cards_entry = ttk.Entry(table_frame, textvariable=table_cards_var)
    table_cards_entry.grid(row=4, column=1)

    # Instructions
    create_instruction_label(window, "Rangs possibles : 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A", 5, 0)
    create_instruction_label(window, "Couleurs possibles : s (pique), h (coeur), d (carreau), c (trèfle)", 6, 0)

    # Bouton Calculer
    calculate_button = ttk.Button(window, text="Calculer", command=lambda: process_cards(window, hand_var.get(), table_cards_var.get()), style="Custom.TButton")
    calculate_button.grid(row=7, column=0, padx=5, pady=5)

    # Bouton Reset
    reset_button = ttk.Button(window, text="Reset", command=lambda: reset_entries(hand_entry, table_cards_entry, result_var, entry, label_result), style="Custom.TButton")
    reset_button.grid(row=9, column=0)

    # Résultat
    result_var = tk.StringVar()
    result_label = ttk.Label(window, textvariable=result_var)
    result_label.grid(row=8, column=0)

    return window

def evaluer_main_interface(entry, label_result):
    cartes = entry.get()
    carte1, carte2 = cartes.split(',')
    resultat = evaluer_main(carte1, carte2)
    label_result.config(text=resultat)

def evaluer_main(carte1, carte2):
    valeur_carte = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}

    # Récupérez la valeur et la couleur des cartes
    valeur1, couleur1 = carte1[0], carte1[1]
    valeur2, couleur2 = carte2[0], carte2[1]

    # Vérifiez si les cartes ont la même couleur
    suited = couleur1 == couleur2

    # Calculez la différence entre les valeurs des cartes
    diff = abs(valeur_carte[valeur1] - valeur_carte[valeur2])

    # Évaluez la force de la main
    if valeur_carte[valeur1] >= 10 and valeur_carte[valeur2] >= 10:
        return "Fort"
    elif suited and (diff == 1 or diff == 2):
        return "Moyen"
    else:
        return "Faible"

def create_instruction_label(parent, text, row, column):
    label = ttk.Label(parent, text=text, font=("Arial", 10, "italic"))
    label.grid(row=row, column=column, sticky="w")
    return label

def process_cards(window, hand, table_cards):
    hand_cards = [Card.new(f"{card.strip()[0].upper()}{card.strip()[1].lower()}") for card in hand.split(',')]
    table_cards_list = [Card.new(f"{card.strip()[0].upper()}{card.strip()[1].lower()}") for card in table_cards.split(',')]

    evaluator = Evaluator()
    score = evaluator.evaluate(hand_cards, table_cards_list)
    hand_strength = 1 - evaluator.get_five_card_rank_percentage(score)

    remaining_deck = get_full_deck()
    for card in hand_cards + table_cards_list:
        if card in remaining_deck:
            remaining_deck.remove(card)

    win_rate = simulate_hands(hand_cards, table_cards_list, remaining_deck, evaluator)

    advice = advise_player(hand_strength, win_rate)
    tk.Label(window, text=f"Force de la main : {hand_strength:.2%} | Taux de victoires : {win_rate:.2%} | Conseil : {advice}").grid(row=8, column=0)

def get_full_deck():
    ranks = "23456789TJQKA"
    suits = "shdc"
    return [Card.new(f"{rank}{suit}") for rank, suit in product(ranks, suits)]

def simulate_hands(hand_cards, table_cards, remaining_deck, evaluator):
    simulations = 10000
    wins = 0

    for _ in range(simulations):
        deck_copy = remaining_deck[:]
        random.shuffle(deck_copy)
        opponent_hand = deck_copy[:2]
        board = table_cards[:]

        while len(board) < 5:
            card = random.choice(deck_copy)
            deck_copy.remove(card)
            board.append(card)

        try:
            if evaluator.evaluate(hand_cards, board) < evaluator.evaluate(opponent_hand, board):
                wins += 1
        except KeyError:
            print(f"Error evaluating cards: {hand_cards} {board}")
            continue

    win_rate = wins / simulations
    return win_rate

def advise_player(hand_strength, win_rate):
    if hand_strength > 0.85 or win_rate > 0.6:
        return "Jouer"
    elif hand_strength > 0.65 or win_rate > 0.4:
        return "Ne pas miser"
    else:
        return "Passer"

def reset_entries(hand_entry, table_cards_entry, result_var, entry, label_result):
    hand_entry.delete(0, tk.END)
    table_cards_entry.delete(0, tk.END)
    result_var.set("")
    entry.delete(0, tk.END)
    label_result.config(text="")
    window.update_idletasks()
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) == 8 and widget.winfo_class() == "Label":
            widget.destroy()

if __name__ == "__main__":
    window = init_window()
    window.mainloop()