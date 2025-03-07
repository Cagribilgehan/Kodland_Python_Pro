from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Üretimde rastgele bir anahtar kullanın, örneğin: import secrets; app.secret_key = secrets.token_hex(16)

# Veritabanı bağlantısı
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Veritabanı Modelleri
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()

# Ana sayfa (quiz)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Kullanıcı adını al ve sanitizasyon yap
        user_name = request.form.get('user_name', 'Anonim').strip()
        if not user_name:  # Eğer boşsa Anonim yap
            user_name = 'Anonim'
        session['user_name'] = user_name
        session['user_id'] = user_name
        app.logger.info(f"Kullanıcı oturumu başlatıldı: {user_name}")
        return redirect('/quiz')
    return render_template('index.html')

# Quiz sayfası
@app.route('/quiz')
def quiz():
    if 'user_name' not in session:
        app.logger.warning("Kullanıcı oturumu bulunamadı, ana sayfaya yönlendiriliyor.")
        return redirect('/')

    try:
        questions = Question.query.all()
        global_high_score = db.session.query(db.func.max(Score.score)).scalar() or 0
        user_high_score = db.session.query(db.func.max(Score.score)).filter_by(user_id=session['user_id']).scalar() or 0
        app.logger.info(f"Quiz sayfası yüklendi. Soru sayısı: {len(questions)}, Global En Yüksek: {global_high_score}, Kullanıcı En Yüksek: {user_high_score}")
        return render_template('quiz.html', questions=questions, global_high_score=global_high_score, user_high_score=user_high_score, user_name=session['user_name'])
    except Exception as e:
        app.logger.error(f"Veritabanı hatası (quiz yüklenirken): {e}")
        return render_template('error.html', message="Bir hata oluştu, lütfen tekrar deneyin."), 500

# Sınav sonucu gönderme
@app.route('/submit', methods=['POST'])
def submit():
    if 'user_name' not in session:
        app.logger.warning("Kullanıcı oturumu bulunamadı, ana sayfaya yönlendiriliyor.")
        return redirect('/')

    try:
        questions = Question.query.all()
        if not questions:
            app.logger.error("Veritabanında hiç soru bulunamadı.")
            return render_template('error.html', message="Hiç soru bulunamadı."), 400

        score = 0
        total_questions = len(questions)
        for question in questions:
            user_answer = request.form.get(f"q{question.id}")
            correct_answer = question.correct_answer
            app.logger.debug(f"Soru ID: {question.id}, Kullanıcı Cevabı: {user_answer}, Doğru Cevap: {correct_answer}")
            if user_answer and user_answer.upper() == correct_answer.upper():
                score += 1
            else:
                app.logger.warning(f"Soru ID: {question.id} için yanlış cevap. Kullanıcı: {user_answer}, Doğru: {correct_answer}")

        # Skoru kaydet
        new_score = Score(user_id=session['user_id'], user_name=session['user_name'], score=score)
        db.session.add(new_score)
        db.session.commit()

        # En yüksek skorları güncelle
        global_high_score = db.session.query(db.func.max(Score.score)).scalar() or 0
        user_high_score = db.session.query(db.func.max(Score.score)).filter_by(user_id=session['user_id']).scalar() or 0

        app.logger.info(f"Kullanıcı: {session['user_name']}, Skor: {score}/{total_questions}, Global En Yüksek: {global_high_score}, Kullanıcı En Yüksek: {user_high_score}")
        return render_template('result.html', score=score, total_questions=total_questions, global_high_score=global_high_score, user_high_score=user_high_score, user_name=session['user_name'])
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Veritabanı hatası (sonuç işlenirken): {e}")
        return render_template('error.html', message="Sonuçlar işlenirken bir hata oluştu."), 500

# En yüksek puanı sıfırla
@app.route('/reset', methods=['POST'])
def reset_highest_score():
    try:
        db.session.query(Score).delete()
        db.session.commit()
        # Session'ı temizle
        session.pop('user_name', None)
        session.pop('user_id', None)
        app.logger.info("Skorlar sıfırlandı ve oturum temizlendi.")
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Veritabanı hatası (skor sıfırlanırken): {e}")
        return render_template('error.html', message="Puan sıfırlama sırasında bir hata oluştu."), 500

if __name__ == '__main__':
    app.run(debug=True)