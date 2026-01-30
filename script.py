import tkinter
import sqlite3

# Initialisation de la base de données SQLite
def init_database():
    
    # Connexion à la base de données (créée si elle n'existe pas)
    conn = sqlite3.connect('gestion_materiel.db')
    cursor = conn.cursor()
    

    cursor.executescript("""         
        CREATE TABLE IF NOT EXISTS equipement(
            id_equipement INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS technicien(
            id_technicien INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(255),
            prenom VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS intervention(
            id_intervention INTEGER PRIMARY KEY AUTOINCREMENT,
            id_equipement INTEGER,
            id_technicien INTEGER,
            date DATE,
            duree TIME,
            type VARCHAR(255),
            cout INT,
            FOREIGN KEY (id_equipement) REFERENCES equipements(id_equipement),
            FOREIGN KEY (id_technicien) REFERENCES technicien(id_technicien)
        );

                                    
        INSERT INTO intervention(id_equipement, id_technicien, date, duree, type, cout) VALUES("2","1", "2026-01-30", "01:30:00", "injection SQL", "10000");
        INSERT INTO intervention(id_equipement, id_technicien, date, duree, type, cout) VALUES("1","2", "2026-02-14", "5:30:00", "incendie", "50000");
        INSERT INTO intervention(id_equipement, id_technicien, date, duree, type, cout) VALUES("3", "1", "2026-02-14", "7:00:00", "van dijk", "15000000");

        
        INSERT INTO equipement(type) VALUES("ordinateur");
        INSERT INTO equipement(type) VALUES("Serveur");
        INSERT INTO equipement(type) VALUES("equipement technique");
                         
        INSERT INTO technicien(nom, prenom) VALUES("COURAULT", "Edouard");
        INSERT INTO technicien(nom, prenom) VALUES("MEURIEL", "Hugo");
                         
    """)
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès!")

# Initialiser la base de données au démarrage
init_database()
