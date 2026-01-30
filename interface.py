import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import math

# Fonction pour obtenir la connexion
def get_connection():
    return sqlite3.connect('gestion_materiel.db')

class GestionMaterielApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion du Matériel")
        self.root.geometry("900x600")
        
        # Créer les onglets
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet Equipements
        self.frame_equipements = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_equipements, text="Équipements")
        self.setup_equipements()
        
        # Onglet Techniciens
        self.frame_techniciens = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_techniciens, text="Techniciens")
        self.setup_techniciens()
        
        # Onglet Interventions
        self.frame_interventions = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_interventions, text="Interventions")
        self.setup_interventions()
        
        # Onglet Actions
        self.frame_actions = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_actions, text="Actions")
        self.setup_actions()
    
    def setup_equipements(self):
        # Formulaire
        frame_form = ttk.Frame(self.frame_equipements)
        frame_form.pack(padx=10, pady=10, fill=tk.X)
        
        ttk.Label(frame_form, text="Type d'équipement:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_type_eq = ttk.Entry(frame_form, width=30)
        self.entry_type_eq.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame_form, text="Ajouter", command=self.add_equipement).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame_form, text="Supprimer", command=self.delete_equipement).grid(row=0, column=3, padx=5, pady=5)
        
        # Tableau
        frame_table = ttk.Frame(self.frame_equipements)
        frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.tree_eq = ttk.Treeview(frame_table, columns=("ID", "Type"), height=15)
        self.tree_eq.column("#0", width=0, stretch=tk.NO)
        self.tree_eq.column("ID", anchor=tk.W, width=50)
        self.tree_eq.column("Type", anchor=tk.W, width=200)
        
        self.tree_eq.heading("#0", text="", anchor=tk.W)
        self.tree_eq.heading("ID", text="ID", anchor=tk.W)
        self.tree_eq.heading("Type", text="Type", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree_eq.yview)
        self.tree_eq.configure(yscroll=scrollbar.set)
        
        self.tree_eq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_equipements()
    
    def setup_techniciens(self):
        # Formulaire
        frame_form = ttk.Frame(self.frame_techniciens)
        frame_form.pack(padx=10, pady=10, fill=tk.X)
        
        ttk.Label(frame_form, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nom = ttk.Entry(frame_form, width=20)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Prénom:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_prenom = ttk.Entry(frame_form, width=20)
        self.entry_prenom.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_form, text="Ajouter", command=self.add_technicien).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_form, text="Supprimer", command=self.delete_technicien).grid(row=0, column=5, padx=5, pady=5)
        
        # Tableau
        frame_table = ttk.Frame(self.frame_techniciens)
        frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.tree_tech = ttk.Treeview(frame_table, columns=("ID", "Nom", "Prénom"), height=15)
        self.tree_tech.column("#0", width=0, stretch=tk.NO)
        self.tree_tech.column("ID", anchor=tk.W, width=50)
        self.tree_tech.column("Nom", anchor=tk.W, width=150)
        self.tree_tech.column("Prénom", anchor=tk.W, width=150)
        
        self.tree_tech.heading("#0", text="", anchor=tk.W)
        self.tree_tech.heading("ID", text="ID", anchor=tk.W)
        self.tree_tech.heading("Nom", text="Nom", anchor=tk.W)
        self.tree_tech.heading("Prénom", text="Prénom", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree_tech.yview)
        self.tree_tech.configure(yscroll=scrollbar.set)
        
        self.tree_tech.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_techniciens()
    
    def setup_interventions(self):
        # Formulaire
        frame_form = ttk.Frame(self.frame_interventions)
        frame_form.pack(padx=10, pady=10, fill=tk.X)
        
        ttk.Label(frame_form, text="Équipement:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_eq = ttk.Combobox(frame_form, width=15, state="readonly")
        self.combo_eq.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Technicien:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_tech = ttk.Combobox(frame_form, width=15, state="readonly")
        self.combo_tech.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_date = ttk.Entry(frame_form, width=15)
        self.entry_date.grid(row=1, column=1, padx=5, pady=5)
        self.entry_date.insert(0, "YYYY-MM-DD")
        
        ttk.Label(frame_form, text="Durée:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_duree = ttk.Entry(frame_form, width=15)
        self.entry_duree.grid(row=1, column=3, padx=5, pady=5)
        self.entry_duree.insert(0, "HH:MM:SS")
        
        ttk.Label(frame_form, text="Type:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_type_int = ttk.Entry(frame_form, width=20)
        self.entry_type_int.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Coût:").grid(row=2, column=2, padx=5, pady=5)
        self.entry_cout = ttk.Entry(frame_form, width=15)
        self.entry_cout.grid(row=2, column=3, padx=5, pady=5)
        
        ttk.Button(frame_form, text="Ajouter", command=self.add_intervention).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(frame_form, text="Supprimer", command=self.delete_intervention).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(frame_form, text="Rafraîchir", command=self.refresh_interventions).grid(row=3, column=2, padx=5, pady=5)
        
        # Tableau
        frame_table = ttk.Frame(self.frame_interventions)
        frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.tree_int = ttk.Treeview(frame_table, columns=("ID", "Équipement", "Technicien", "Date", "Durée", "Type", "Coût"), height=10)
        self.tree_int.column("#0", width=0, stretch=tk.NO)
        self.tree_int.column("ID", anchor=tk.W, width=40)
        self.tree_int.column("Équipement", anchor=tk.W, width=100)
        self.tree_int.column("Technicien", anchor=tk.W, width=100)
        self.tree_int.column("Date", anchor=tk.W, width=100)
        self.tree_int.column("Durée", anchor=tk.W, width=80)
        self.tree_int.column("Type", anchor=tk.W, width=100)
        self.tree_int.column("Coût", anchor=tk.W, width=80)
        
        self.tree_int.heading("#0", text="", anchor=tk.W)
        self.tree_int.heading("ID", text="ID", anchor=tk.W)
        self.tree_int.heading("Équipement", text="Équipement", anchor=tk.W)
        self.tree_int.heading("Technicien", text="Technicien", anchor=tk.W)
        self.tree_int.heading("Date", text="Date", anchor=tk.W)
        self.tree_int.heading("Durée", text="Durée", anchor=tk.W)
        self.tree_int.heading("Type", text="Type", anchor=tk.W)
        self.tree_int.heading("Coût", text="Coût", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree_int.yview)
        self.tree_int.configure(yscroll=scrollbar.set)
        
        self.tree_int.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_interventions()
    
    def setup_actions(self):
        # Titre
        title_frame = ttk.Frame(self.frame_actions)
        title_frame.pack(pady=20)
        ttk.Label(title_frame, text="Actions Rapides", font=("Arial", 16, "bold")).pack()
        
        # Section Statistiques
        stats_frame = ttk.LabelFrame(self.frame_actions, text="Statistiques", padding=20)
        stats_frame.pack(padx=20, pady=10, fill=tk.X)
        
        ttk.Button(stats_frame, text="Afficher la fréquence des interventions", 
                   command=self.show_frequence_interventions, width=40).pack(pady=5)
        ttk.Button(stats_frame, text="Afficher le temps moyen d'un intervention", 
                   command=self.show_AVG_time, width=40).pack(pady=5)
        ttk.Button(stats_frame, text="Afficher l'equipement le plus socilité en interventions", 
                   command=self.show_equipement_solicite, width=40).pack(pady=5)
        ttk.Button(stats_frame, text="Afficher le coût moyen", 
                   command=self.show_AVG_cost, width=40).pack(pady=5)
        
    
    def add_equipement(self):
        type_eq = self.entry_type_eq.get()
        if not type_eq:
            messagebox.showwarning("Erreur", "Veuillez entrer un type d'équipement")
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO equipement(type) VALUES(?)", (type_eq,))
        conn.commit()
        conn.close()
        
        self.entry_type_eq.delete(0, tk.END)
        self.refresh_equipements()
        messagebox.showinfo("Succès", "Équipement ajouté")
    
    def delete_equipement(self):
        selected = self.tree_eq.selection()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez un équipement")
            return
        
        item = self.tree_eq.item(selected[0])
        eq_id = item['values'][0]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipement WHERE id_equipement=?", (eq_id,))
        conn.commit()
        conn.close()
        
        self.refresh_equipements()
        messagebox.showinfo("Succès", "Équipement supprimé")
    
    def refresh_equipements(self):
        for item in self.tree_eq.get_children():
            self.tree_eq.delete(item)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipement")
        for row in cursor.fetchall():
            self.tree_eq.insert("", tk.END, values=row)
        conn.close()
    
    def add_technicien(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        if not nom or not prenom:
            messagebox.showwarning("Erreur", "Veuillez entrer le nom et prénom")
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO technicien(nom, prenom) VALUES(?, ?)", (nom, prenom))
        conn.commit()
        conn.close()
        
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.refresh_techniciens()
        self.update_combos()
        messagebox.showinfo("Succès", "Technicien ajouté")
    
    def delete_technicien(self):
        selected = self.tree_tech.selection()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez un technicien")
            return
        
        item = self.tree_tech.item(selected[0])
        tech_id = item['values'][0]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM technicien WHERE id_technicien=?", (tech_id,))
        conn.commit()
        conn.close()
        
        self.refresh_techniciens()
        self.update_combos()
        messagebox.showinfo("Succès", "Technicien supprimé")
    
    def refresh_techniciens(self):
        for item in self.tree_tech.get_children():
            self.tree_tech.delete(item)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM technicien")
        for row in cursor.fetchall():
            self.tree_tech.insert("", tk.END, values=row)
        conn.close()
    
    def add_intervention(self):
        eq_id = self.combo_eq.get()
        tech_id = self.combo_tech.get()
        date = self.entry_date.get()
        duree = self.entry_duree.get()
        type_int = self.entry_type_int.get()
        cout = self.entry_cout.get()
        
        if not all([eq_id, tech_id, date, duree, type_int, cout]):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Validation du coût (règle métier)
        try:
            cout_valide = float(cout)
            if cout_valide < 0:
                messagebox.showerror("Erreur de validation", "Le coût ne peut pas être négatif (doit être >= 0)")
                return
        except ValueError:
            messagebox.showerror("Erreur de validation", "Le coût doit être un nombre valide")
            return
        
        # Extraire l'ID du combo
        eq_id = eq_id.split(" - ")[0]
        tech_id = tech_id.split(" - ")[0]
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO intervention(id_equipement, id_technicien, date, duree, type, cout) VALUES(?, ?, ?, ?, ?, ?)",
                (eq_id, tech_id, date, duree, type_int, cout_valide)
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.close()
            messagebox.showerror("Erreur d'intégrité", f"Erreur lors de l'insertion : {str(e)}")
            return
        except Exception as e:
            conn.close()
            messagebox.showerror("Erreur", f"Erreur inattendue : {str(e)}")
            return
        finally:
            conn.close()
        
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, "YYYY-MM-DD")
        self.entry_duree.delete(0, tk.END)
        self.entry_duree.insert(0, "HH:MM:SS")
        self.entry_type_int.delete(0, tk.END)
        self.entry_cout.delete(0, tk.END)
        
        self.refresh_interventions()
        messagebox.showinfo("Succès", "Intervention ajoutée")
    
    def delete_intervention(self):
        selected = self.tree_int.selection()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez une intervention")
            return
        
        item = self.tree_int.item(selected[0])
        int_id = item['values'][0]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM intervention WHERE id_intervention=?", (int_id,))
        conn.commit()
        conn.close()
        
        self.refresh_interventions()
        messagebox.showinfo("Succès", "Intervention supprimée")
    
    def refresh_interventions(self):
        for item in self.tree_int.get_children():
            self.tree_int.delete(item)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_intervention, e.type, t.nom || ' ' || t.prenom, i.date, i.duree, i.type, i.cout
            FROM intervention i
            JOIN equipement e ON i.id_equipement = e.id_equipement
            JOIN technicien t ON i.id_technicien = t.id_technicien
        """)
        for row in cursor.fetchall():
            self.tree_int.insert("", tk.END, values=row)
        conn.close()
        
        self.update_combos()
    
    def update_combos(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id_equipement, type FROM equipement")
        eq_list = [(row[0], row[1]) for row in cursor.fetchall()]
        self.combo_eq['values'] = [f"{e[0]} - {e[1]}" for e in eq_list]
        
        cursor.execute("SELECT id_technicien, nom, prenom FROM technicien")
        tech_list = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
        self.combo_tech['values'] = [f"{t[0]} - {t[1]} {t[2]}" for t in tech_list]
        
        conn.close()

    def show_frequence_interventions(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Option 1: Nombre total d'interventions
        cursor.execute("SELECT COUNT(*) FROM intervention")
        total_interventions = cursor.fetchone()[0]
        
        # Option 2: Nombre d'équipements
        cursor.execute("SELECT COUNT(*) FROM equipement")
        total_equipements = cursor.fetchone()[0]
        
        # Option 3: Fréquence moyenne (interventions par équipement)
        if total_equipements > 0:
            frequence_moyenne = total_interventions / total_equipements
        else:
            frequence_moyenne = 0

        conn.close()
        
        info = f"Fréquence des interventions:\n\n"
        info += f"Total d'interventions: {total_interventions}\n"
        info += f"Total d'équipements: {total_equipements}\n"
        info += f"Fréquence moyenne: {frequence_moyenne:.2f} interventions/équipement"
        
        messagebox.showinfo("Statistiques", info)
    
    def show_AVG_time(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(duree) FROM intervention")
        duree = cursor.fetchone()[0]
        conn.close()
        messagebox.showinfo("Statistiques", f"Durée moyenne d'une intervention: {round(duree)}h")
    
    def show_equipement_solicite(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.type, COUNT(i.id_intervention) as nb_interventions
            FROM equipement e
            LEFT JOIN intervention i ON i.id_equipement = e.id_equipement
            GROUP BY e.id_equipement
            ORDER BY nb_interventions DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            messagebox.showinfo("Statistiques", f"Équipement le plus sollicité: {result[0]} ({result[1]} interventions)")
        else:
            messagebox.showinfo("Statistiques", "Aucune donnée disponible")
    
    def show_AVG_cost(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(cout) FROM intervention")
        moyenne = cursor.fetchone()[0]
        conn.close()
        if moyenne is None:
            moyenne = 0
        messagebox.showinfo("Statistiques", f"Coût moyen des interventions: {moyenne} €")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionMaterielApp(root)
    root.mainloop()
