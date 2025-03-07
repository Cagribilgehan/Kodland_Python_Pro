from app import db, Question, app

# Flask uygulama bağlamını kullanarak işlemleri gerçekleştir
with app.app_context():
    db.drop_all()  # Önce eski veritabanını temizle
    db.create_all()  # Yeni tabloları oluştur

    # 📌 Soruları ekleyelim
    new_questions = [
        # Python ile sohbet botu otomasyonu (Discord.py) - 2 soru
        Question(text="Discord botunda bir komutun çalışmasını sağlamak için hangi decorator kullanılır?", 
                 option_a="@bot.command", 
                 option_b="@bot.event", 
                 option_c="@bot.listen", 
                 option_d="@bot.run", 
                 correct_answer="A"),  # Doğru cevap A
        
        Question(text="Discord.py ile bir botun sunucuya katılması nasıl kontrol edilir?", 
                 option_a="on_ready()", 
                 option_b="on_join()", 
                 option_c="on_start()", 
                 option_d="on_connect()", 
                 correct_answer="B"),  # Doğru cevap B
        
        # Python ile web geliştirme (Flask) - 2 soru
        Question(text="Flask'te bir şablonu render etmek için hangi fonksiyon kullanılır?", 
                 option_a="render_template()", 
                 option_b="load_template()", 
                 option_c="display_template()", 
                 option_d="render_page()", 
                 correct_answer="A"),  # Doğru cevap A
        
        Question(text="Flask uygulamasında bir route için HTTP GET metodunu tanımlamak için ne kullanılır?", 
                 option_a="@app.route('/', methods=['GET'])", 
                 option_b="@app.get('/')", 
                 option_c="@app.request('GET')", 
                 option_d="@app.method('GET')", 
                 correct_answer="B"),  # Doğru cevap B
        
        # Python ile yapay zeka geliştirme - 2 soru
        Question(text="Yapay zeka modellerinde kayıp fonksiyonunu optimize etmek için hangi yöntem kullanılır?", 
                 option_a="Gradient Descent", 
                 option_b="Linear Regression", 
                 option_c="Decision Tree", 
                 option_d="K-Means", 
                 correct_answer="A"),  # Doğru cevap A
        
        Question(text="TensorFlow’da bir modelin katmanlarını eklemek için hangi API kullanılır?", 
                 option_a="tf.keras.layers", 
                 option_b="tf.model.layers", 
                 option_c="tf.network.add", 
                 option_d="tf.structure.build", 
                 correct_answer="C"),  # Doğru cevap C
        
        # Bilgisayar görüşü (Computer Vision - TensorFlow, ImageAI) - 2 soru
        Question(text="ImageAI ile görüntü tanımada hangi dosya formatı genellikle kullanılır?", 
                 option_a="JPEG", 
                 option_b="TXT", 
                 option_c="CSV", 
                 option_d="MP4", 
                 correct_answer="A"),  # Doğru cevap A
        
        Question(text="TensorFlow’da bir görüntüyü ön işlemek için hangi fonksiyon tercih edilir?", 
                 option_a="tf.image.resize", 
                 option_b="tf.image.crop", 
                 option_c="tf.image.transform", 
                 option_d="tf.image.convert", 
                 correct_answer="D"),  # Doğru cevap D
        
        # Doğal Dil İşleme (Natural Language Processing - BeautifulSoup, NLTK) - 2 soru
        Question(text="BeautifulSoup ile bir HTML sayfasından belirli bir etiketi seçmek için hangi metod kullanılır?", 
                 option_a="find()", 
                 option_b="select_one()", 
                 option_c="get_tag()", 
                 option_d="extract()", 
                 correct_answer="A"),  # Doğru cevap A
        
        Question(text="NLTK ile bir metnin kelime tokenizasyonunu yapmak için hangi fonksiyon kullanılır?", 
                 option_a="word_tokenize()", 
                 option_b="tokenize_words()", 
                 option_c="split_text()", 
                 option_d="nltk_parse()", 
                 correct_answer="A"),  # Doğru cevap A
    ]

    # 🔹 Soruları veritabanına ekle
    db.session.add_all(new_questions)
    db.session.commit()

    print("✅ Veritabanı oluşturuldu ve 4 seçenekli soruların doğru cevapları dağıtıldı!")