import json
import sqlite3
import os

db_path = 'database_gadai.db'
json_path = 'options.json'

def migrate():
    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create master_barang
    c.execute('DROP TABLE IF EXISTS master_barang')
    c.execute('''
        CREATE TABLE master_barang (
            id_barang INTEGER PRIMARY KEY AUTOINCREMENT,
            jenis_barang TEXT,
            tipe_barang TEXT
        )
    ''')
    
    # Insert data
    jenis_to_type = data.get('jenis_to_type', {})
    for jenis, types in jenis_to_type.items():
        for t in types:
            c.execute('INSERT INTO master_barang (jenis_barang, tipe_barang) VALUES (?, ?)', (jenis, t))
            
    # Recreate riwayat_prediksi
    c.execute('DROP TABLE IF EXISTS riwayat_prediksi')
    c.execute('''
        CREATE TABLE riwayat_prediksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_prediksi TEXT,
            id_barang INTEGER,
            tenor INTEGER,
            estimasi_nilai INTEGER,
            FOREIGN KEY(id_barang) REFERENCES master_barang(id_barang)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Migration successful")

if __name__ == "__main__":
    migrate()
