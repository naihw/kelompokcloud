from flask import Flask, request, jsonify, render_template, redirect
from extensions import db
from model import Mahasiswa

app = Flask(__name__)

# Ganti sesuai user/password dan nama database MySQL kamu
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sqladmin:nayaka_hilman0605@websederhana.database.windows.net/latihanDB'
    '?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "✅ API Mahasiswa - Flask + MySQL (Azure)"

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

if __name__ == '__main__':
    app.run(debug=True)