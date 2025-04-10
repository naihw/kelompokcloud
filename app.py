from flask import Flask, request, jsonify, render_template, redirect
from extensions import db
from model import Mahasiswa
import os
import requests

app = Flask(__name__)

# Konfigurasi koneksi ke Azure SQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pymssql://sqladmin:nayaka_hilman0605@websederhana.database.windows.net:1433/latihanDB'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Buat tabel jika belum ada
with app.app_context():
    db.create_all()

# -----------------------
# ROUTE MAHASISWA
# -----------------------

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/tambah', methods=['POST'])
def tambah():
    data = request.get_json()
    mahasiswa = Mahasiswa(nama=data['nama'], nim=data['nim'])
    db.session.add(mahasiswa)
    db.session.commit()
    return jsonify({'message': 'Data berhasil ditambahkan'})

@app.route('/list')
def list_mahasiswa():
    mahasiswa = Mahasiswa.query.all()
    return jsonify([{'id': m.id, 'nama': m.nama, 'nim': m.nim} for m in mahasiswa])

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        mahasiswa = Mahasiswa(nama=nama, nim=nim)
        db.session.add(mahasiswa)
        db.session.commit()
        return redirect('/form')
    return render_template('form.html')

# -----------------------
# ROUTE BERITA (NewsAPI)
# -----------------------

@app.route('/berita')
def berita():
    kategori = request.args.get('kategori', 'general')
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        return jsonify({'error': 'API Key belum dikonfigurasi'}), 500

    url = f'https://newsapi.org/v2/top-headlines?country=id&category={kategori}&apiKey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'Gagal mengambil data dari NewsAPI'}), 500

@app.route('/cari-berita')
def cari_berita():
    keyword = request.args.get('q')  # contoh: /cari-berita?q=teknologi
    api_key = os.getenv('NEWS_API_KEY')

    if not api_key:
        return jsonify({'error': 'API Key belum dikonfigurasi'}), 500
    if not keyword:
        return jsonify({'error': 'Parameter q (query) wajib diisi'}), 400

    url = f'https://newsapi.org/v2/everything?q={keyword}&language=id&apiKey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return render_template('berita.html', articles=data['articles'], keyword=keyword)
    else:
        return jsonify({'error': 'Gagal mengambil data dari NewsAPI'}), 500

# -----------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
