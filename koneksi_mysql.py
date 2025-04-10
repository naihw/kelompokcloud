import pyodbc
import requests 

# Deteksi IP publik yang digunakan oleh script ini
try:
    my_ip = requests.get("https://api.ipify.org").text
    print("🌐 IP publik yang digunakan script ini:", my_ip)
except:
    print("⚠️ Tidak bisa mendeteksi IP publik")

# String koneksi
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=websederhana.database.windows.net;"
    "DATABASE=latihanDB;"
    "UID=sqladmin;"
    "PWD=nayaka_hilman0605;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Coba koneksi ke Azure SQL Server
try:
    conn = pyodbc.connect(conn_str)
    print("✅ Koneksi SQL Server berhasil!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases;")
    for row in cursor:
        print("📂", row)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Gagal koneksi:", e)
