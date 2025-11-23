import pandas as pd
import re
import streamlit as st
import os
from transformers import pipeline

# --- 1. CONFIG PATH ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_PATH = os.path.join(BASE_DIR, 'dictionaries')

# --- 2. KEYWORDS SPAM ---
SPAM_KEYWORDS = [
    'diskon', 'kode', 'voucher', 'klaim', 'daget', 'dana kaget', 
    'shopeefood', 'grabfood', 'sfood', 'shopeepay', 'gopay coins',
    'cashback', 'giveaway', 'gratis', 'free', 'biaya admin',
    'klik', 'link', 'check out', 'checkout', 'orderan', 
    'jasa', 'joki', 'open bo', 'cs', 'customer service',
    'zonauang', 'mutual', 'foll', 'follow', 'sub', 'subscribe',
    'turnitin', 'netflix', 'spotify', 'premium', 'jual', 'beli'
]

# --- 3. LOAD RESOURCES ---
@st.cache_resource
def load_stopwords():
    try:
        stop_df = pd.read_csv(os.path.join(DICT_PATH, 'stopwords.csv'))
        stop_set = set(stop_df['word'].str.strip().str.lower())
    except Exception:
        stop_set = set()
    return stop_set

STOP_SET = load_stopwords()

@st.cache_resource
def load_sentiment_model():
    # Model Indo-RoBERTa
    classifier = pipeline(
        "sentiment-analysis", 
        model="w11wo/indonesian-roberta-base-sentiment-classifier",
        tokenizer="w11wo/indonesian-roberta-base-sentiment-classifier"
    )
    return classifier

sentiment_pipeline = load_sentiment_model()

# --- 4. FUNGSI DETEKSI SPAM ---
def is_spam(text):
    """Mengembalikan True jika teks terindikasi spam/promo"""
    if not isinstance(text, str): return False
    text_lower = text.lower()
    
    # Cek Keywords
    for keyword in SPAM_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
            return True
            
    # Cek Link tanpa konteks
    words = text_lower.split()
    if len(words) < 5 and 'http' in text_lower:
        return True
        
    return False

# ... (kode atas tetap sama)

# TAMBAHAN: STOPWORD KHUSUS TOPIK (Brand & Kata Umum)
# ... (kode atas sama)

# UPDATE DAFTAR KATA "HARAM" BUAT TOPIK
TOPIC_STOPWORDS = {
    # 1. Brand & Identity (Termasuk variasi imbuhan -nya)
    'gojek', 'gofood', 'gocar', 'gosend', 'grab', 'shopee', 'shopeefood',
    'tokopedia', 'sfood', 'goride', 'application', 'aplikasi', 'driver', 'abang',
    'ojol', 'ojek', 'motor', 'mobil', 'cs', 'drivernya', 'user',
    'gojeknya', 'grabcar', 'bapaknya', 'beliau', 'nya',
    
    # 2. Kata Ganti & Sapaan
    'gue', 'gw', 'gua', 'aku', 'saya', 'lu', 'lo', 'kamu', 'anda', 'you',
    'dia', 'mereka', 'kita', 'kami', 'kalian', 'nder', 'sender', 'org', 'orang',
    'mas', 'mbak', 'kak', 'pak', 'bu', 'bapak', 'ibu', 'bang', 'bg', 'kang',
    'guys', 'gan', 'sis', 'kakak', 'min', 'admin', 'anak', 'bocah', 'diri',
    
    # 3. Kata Kerja Umum (HAPUS INI BIAR TOPIK LEBIH SPESIFIK)
    'naik', 'pesen', 'order', 'makan', 'minta', 'beli', 'bayar', 'cari',
    'pake', 'pakai', 'jalan', 'bawa', 'kasih', 'dapet', 'liat', 'bilang',
    'kepikiran', 'ketemu', 'nunggu', 'laper', 'nyetir', 'mesen',
    
    # 4. Partikel Percakapan (Noise)
    'bgt', 'banget', 'bgtt', 'aja', 'saja', 'doang', 'gpp', 'gapapa',
    'ini', 'itu', 'dan', 'yang', 'yg', 'di', 'ke', 'dari',
    'mau', 'tapi', 'sama', 'ama', 'buat', 'kalo', 'kalau',
    'ada', 'apa', 'bisa', 'udah', 'sudah', 'udh', 'lagi', 'kan', 'ya', 'yak', 'yaa',
    'sih', 'dong', 'mah', 'lah', 'kah', 'kok', 'kek', 'kayak', 'kyk',
    'gitu', 'gini', 'gtu', 'gni', 'tuh', 'nih', 'deh', 'dah',
    'gak', 'ga', 'nggak', 'ngga', 'enggak', 'kaga', 'kagak', 'gamau', 'gaada', 'gada',
    'bukan', 'jangan', 'malah', 'padahal', 'terus', 'trs', 'tpi',
    'karna', 'karena', 'krn', 'gatau', 'tau', 'tahu', 'utk', 'untuk',
    'pasti', 'bakal', 'tiap', 'sini', 'situ', 'sana', 'asli', 'luar', 'dalam',
    'baru', 'lama', 'dulu', 'sebelum', 'sesudah', 'kapan', 'sampe', 'sampai',
    'segini', 'segitu', 'wkwk', 'alias', 'si', 'biasanya', 'mending', 'hampir',
    'soalnya', 'agak', 'mana', 'juga', 'atau', 'tanpa', 'asal', 'adalah', 'yaitu',
    
    # 5. Emosi Kasar (Opsional, buang biar fokus ke konteks)
    'anjing', 'anjir', 'ajg', 'jir', 'bjir', 'njir', 'gila', 'sial', 'parah',
    
    # 6. Waktu & Umum
    'hari', 'jam', 'tadi', 'nanti', 'besok', 'sekarang', 'skrg',
    'kemarin', 'minggu', 'bulan', 'tahun', 'terakhir', 'pernah',
    'mohon', 'tolong', 'pls', 'please', 'bantu', 'kenapa', 'knp',
    'langsung', 'cuma', 'hanya', 'pas', 'saat', 'waktu',
    'jadi', 'jd', 'sebab', 'biar', 'mungkin',
    'paling', 'lebih', 'kurang', 'banyak', 'dikit', 'sedikit',
    'masuk', 'keluar', 'pulang', 'pergi', 'balik', 'lewat',
    'bener', 'jujur', 'klo', 'dr', 'emang', 'bahkan',
    
    # 7. Spam Manual
    'jual', 'beli', 'ready', 'stok', 'tersedia', 'minat', 'dm', 
    'wa', 'hubungi', 'cek', 'bio', 'link', 'shopee', 'tokped',
    'ragout', 'risol', 'pisang', 'coklat', 'keju', 'kue', 
    'bogor', 'jakarta', 'bandung', 'kirim', 'ongkir', 'cod',
    'scroll', 'bingung', 'izin', 'berkenan', 'thanks'
}

# Gabungkan dengan stopword dari CSV
FINAL_STOP_SET = STOP_SET.union(TOPIC_STOPWORDS)

# ... (lanjut ke fungsi clean_text_for_topic seperti sebelumnya)

# --- 5. PREPROCESSING (Topic) ---
def clean_text_for_topic(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text) # Hapus angka & simbol
    
    words = text.split()
    
    # LOGIKA FILTER BARU:
    clean_words = []
    for w in words:
        # 1. Cek apakah ada di STOPWORD
        if w in FINAL_STOP_SET:
            continue
        # 2. Cek panjang kata (hapus kata 1-2 huruf)
        if len(w) < 3:
            continue
        # 3. Normalisasi Slang dulu (opsional, biar 'bgt' jadi 'banget' lalu kebuang)
        # w = NORM_DICT.get(w, w) 
        
        clean_words.append(w)
        
    return " ".join(clean_words)

# ... (kode bawah tetap sama)

# ... (kode impor dan inisialisasi lainnya tetap sama)

# ... (import dan fungsi lain tetap sama)

# --- 6. MAIN LOADER ---
@st.cache_data
def load_dataset(file):
    try:
        # 1. Baca CSV
        df = pd.read_csv(file, dtype={'id_str': str, 'user_id_str': str})
        
        # 2. Parsing Tanggal (Full Timestamp)
        # Kita tetap butuh ini dulu supaya bisa ambil tanggalnya
        df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y', errors='coerce')
        
        # 3. Buat Kolom Tanggal Saja (DILAKUKAN DULUAN)
        df['date_only'] = df['created_at'].dt.date
        
        # 4. SORTING BERDASARKAN TANGGAL (SESUAI REQUEST KAMU)
        # Kita urutkan berdasarkan 'date_only' dulu.
        # Jika tanggalnya sama, baru urutkan berdasarkan jam ('created_at')
        df.sort_values(by=['date_only', 'created_at'], inplace=True)
        
        # 5. Hapus Duplikat & Data Error
        # Buang data yang tanggalnya gagal diparsing (NaT)
        df.dropna(subset=['created_at'], inplace=True)
        df.drop_duplicates(subset=['full_text'], inplace=True)

        # ... (Sisa kode ke bawah untuk proses Sentimen & Spam SAMA PERSIS) ...
        # ... (Copy paste bagian loop for i, text in enumerate(texts): sampai return df) ...
        
        # Container Hasil
        clean_texts = []
        sent_labels = []
        sent_scores = []
        is_promo = []

        texts = df['full_text'].astype(str).tolist()
        total = len(df)
        
        bar = st.progress(0)

        for i, text in enumerate(texts):
            if is_spam(text):
                is_promo.append(True)
                sent_labels.append('Promo')
                sent_scores.append(0)
                clean_texts.append("")
            else:
                is_promo.append(False)
                clean_texts.append(clean_text_for_topic(text))
                try:
                    res = sentiment_pipeline(text[:512])[0]
                    lbl, scr = res['label'], res['score']
                    if lbl == 'positive': fl = 'Positif'
                    elif lbl == 'negative': fl = 'Negatif'
                    else: fl = 'Netral'
                    
                    if fl == 'Negatif': fs = -scr
                    elif fl == 'Netral': fs = 0
                    else: fs = scr
                except:
                    fl = 'Netral'; fs = 0
                sent_labels.append(fl)
                sent_scores.append(fs)
            
            if i % 10 == 0: bar.progress((i+1)/total)
        
        bar.empty()

        df['clean_text'] = clean_texts
        df['sentiment'] = sent_labels
        df['sentiment_score'] = sent_scores
        df['is_promo'] = is_promo
        df['engagement_score'] = df['favorite_count'] + (2 * df['retweet_count']) + (1.5 * df['reply_count'])
        
        if 'username' in df.columns:
            df['username'] = df['username'].fillna('User ' + df['user_id_str'].fillna(''))
        else:
            df['username'] = 'User ' + df['user_id_str'].fillna('')
            
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None