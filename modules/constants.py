import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_PATH = os.path.join(BASE_DIR, 'dictionaries')

# A. KEYWORDS SPAM
SPAM_KEYWORDS = [
    'diskon', 'kode', 'voucher', 'klaim', 'daget', 'dana kaget', 
    'shopeefood', 'grabfood', 'sfood', 'shopeepay', 'gopay coins',
    'cashback', 'giveaway', 'gratis', 'free', 'biaya admin',
    'klik', 'link', 'check out', 'checkout', 'orderan', 
    'jasa', 'joki', 'open bo', 'cs', 'customer service',
    'zonauang', 'mutual', 'foll', 'follow', 'sub', 'subscribe',
    'turnitin', 'netflix', 'spotify', 'premium', 'jual', 'beli'
]

# B. STOPWORDS KHUSUS TOPIK
TOPIC_STOPWORDS = {
    # 1. Brand & Identity
    'gojek', 'gofood', 'gocar', 'gosend', 'grab', 'shopee', 'shopeefood',
    'tokopedia', 'sfood', 'goride', 'application', 'cs', 'user',
    'gojeknya', 'grabcar', 'bapaknya', 'beliau', 'nya', 'ibu',
    'maxim', 'indrive', 'mamang', 'mba', 'mas', 'kak', 'min', 'admin', 'gopay', 'ovo', 'dana', 'linkaja', 'mbak',
    
    # 2. Kata Kerja Umum
    'naik', 'pesen', 'order', 'makan', 'minta', 'beli', 'bayar', 'cari',
    'pake', 'pakai', 'jalan', 'bawa', 'kasih', 'dapet', 'liat', 'bilang',
    'kepikiran', 'ketemu', 'nyetir', 'mesen', 'ganti',
    'dikirim', 'milih', 'nemenin', 'kerumah',
    'pulang', 'tidur', 'bangun', 'buka', 'tutup', 'sampe', 'sampai', 'ampe', 'ketiduran', 'ngobrol', 'ditanya', 'nanya', 'jawab', 'tanya',
    'dateng', 'datang', 'tiba', 'balik', 'lewat', 'coba', 'cobain',
    'keluar', 'masuk', 'pilih', 'bikin', 'isi', 'mulai', 'chat',
    'tinggal', 'hidup', 'pernah', 'belum', 'punya', 'ambil',
    'ngirim', 'ngomong', 'masak', 'pergi', 'lupa', 'suka',
    'duduk', 'disuruh', 'foto', 'nyari', 'kena', 'sakit', 'pesan', 'pindah', 'nyicil', 'mati',
    'dikasih', 'make', 'main', 'lanjut', 'parkir', 'mikir', 'nangis',
    'bayangin', 'suruh', 'diminta', 'terima', 'kira', 'sengaja',
    
    # 3. Kata Sifat/Keterangan
    'biasanya', 'segitu', 'segini', 'hampir', 'habis', 'abis', 'sendiri', 'males', 'agak', 'jarang', 'selalu', 'setiap', 'ternyata', 'akhirnya',
    'pagi', 'siang', 'sore', 'malem', 'malam', 'tengah', 'bareng',
    'thanks', 'makasih', 'terimakasih', 'hadiah', 'gratis', 'promo', 'kota', 'bekasi', 'depok', 'jkt', 'jakarta', 'hotel', 'sandal', 'mie', 'jajan', 'kos', 'kost',
    'enak', 'lebih', 'baik', 'penting', 'makin', 'paling', 'kaya', 'kayak',
    'sendirian', 'sejam', 'menit', 'jam', 'hari', 'minggu', 'bulan', 'tahun',
    'panas', 'dingin', 'waktu', 'besok', 'kemarin', 'kemaren',
    'banyak', 'dikit', 'sedikit', 'gede', 'kecil', 'dekat',
    'salah', 'bener', 'betul', 'susah', 'gampang', 'mudah', 'ribet',
    'biasa', 'aneh', 'lucu', 'seru', 'asik', 'parah', 'gila', 'sial',
    'ngantuk', 'lancar', 'jelas', 'beda',
    'beneran', 'barang', 'jas', 'sedih', 'senang', 'senin', 'seharian',
    'kurang', 'terakhir', 'sering', 'selama', 'nomor', 'nama', 'alamat',
    'setengah', 'minimal', 'umum', 'kuat', 'alasan', 'cerita', 'kemana', 'ayam', 'kopi', 'sebagai', 'otw', 'rasanya',
    'opsi', 'giliran', 'bosen', 'mager', 'capek', 'cape', 'gabut', 'malu',
    'jaket', 'mirip', 'hati', 'good', 'halo', 'happy', 'dibanding',
    'selesai', 'diatas', 'menurut', 'nginep', 'sepanjang', 'ulang',
    
    # 4. Konteks Noise
    'indonesia', 'harusnya', 'makanan', 'minuman', 'resto', 'warung', 'jajanan',
    'the', 'of', 'in', 'and', 'to', 'for', 'amp', 
    'gabin', 'tape', 'ketan', 'surken', 'buatan', 'satunya', 'ribu', 
    'ubi', 'ungu', 'wisuda', 
    'via', 'dll', 'tak', 'tbtb', 'satu', 'dua', 'tiga', 'setelah',
    'sebelah', 'mulu', 'kadang', 'jujur', 'kali', 'kaki', 'tempat',
    'pakegojekpalinghemat', 
    
    # 5. Partikel & Slang
    'gue', 'gw', 'gua', 'aku', 'saya', 'lu', 'lo', 'kamu', 'anda', 'you',
    'dia', 'mereka', 'kita', 'kami', 'kalian', 'nder', 'sender', 'org', 'orang',
    'bgt', 'banget', 'bgtt', 'aja', 'saja', 'doang', 'gpp', 'gapapa',
    'ini', 'itu', 'dan', 'yang', 'yg', 'di', 'ke', 'dari',
    'mau', 'tapi', 'sama', 'ama', 'buat', 'kalo', 'kalau', 'klo',
    'ada', 'apa', 'bisa', 'udah', 'sudah', 'udh', 'lagi', 'kan', 'ya', 'yak', 'yaa', 'yaaa', 'iyaa',
    'sih', 'dong', 'mah', 'lah', 'kah', 'kok', 'kek', 'kyk', 'kayaknya',
    'gitu', 'gini', 'gmn', 'gtu', 'gni', 'tuh', 'nih', 'deh', 'dah',
    'gak', 'ga', 'nggak', 'ngga', 'enggak', 'kaga', 'kagak', 'gamau', 'gaada', 'gada', 'gabisa',
    'bukan', 'jangan', 'jgn', 'malah', 'padahal', 'terus', 'trs', 'trus', 'tpi', 'pdhl',
    'karna', 'karena', 'krn', 'gatau', 'tau', 'tahu', 'utk', 'untuk',
    'pasti', 'bakal', 'tiap', 'sini', 'disini', 'situ', 'sana', 'asli', 'luar', 'dalam',
    'baru', 'lama', 'dulu', 'sebelum', 'sesudah', 'kapan', 'nanti', 'nnti',
    'alias', 'si', 'mending', 'soalnya', 'mana', 'juga', 'atau', 'tanpa', 'asal', 'adalah',
    'cuma', 'cuman', 'hanya', 'pas', 'tadi', 'barusan', 'skrg', 'sekarang',
    'emang', 'emg', 'knp', 'kenapa', 'pgn', 'pengen', 'ingin',
    'wkwk', 'wkwkwk', 'haha', 'hehe', 'iya', 'tidak', 'temen', 'dpt', 'plg',
    'pls', 'please', 'plis', 'tolong', 'bantu', 'for', 'sama', 'sekali', 'gimana',
    'allah', 'yaallah', 'masa', 'kasus', 'ribet', 'kasian', 'nemu', 'apalagi', 'berapa',
    'drpd', 'daripada', 'pada', 'dengan', 'dgn', 'dr', 'anjir', 'ajg', 'njir', 'jir', 'gegara',
    'depan', 'belakang', 'samping', 'atas', 'bawah', 'kiri', 'kanan', 'yah',
    'langsung', 'lgsg', 'biar', 'masih', 'harus', 'boleh', 'maaf', 'semoga', 'pun', 'daerah',
    'kata', 'katanya', 'sambil', 'usah', 'lain', 'demi', 'pak', 'kakak', 'bang', 'guys',
    'sayang', 'anak', 'kemarin', 'semua', 'akan', 'jadi', 'otw', 'sebagai', 'diri', 'adek',
    'sumpah', 'sebenernya', 'blm', 'siapa', 'oleh', 'dapat', 'kemana',
    'atuh', 'makanya', 'gara', 'gbs', 'bet', 'loh', 'yowes', 'huhu', 'ayo', 'btw',
    'tdk', 'indo', 'yaudah', 'gajelas', 'gapernah', 'amat', 'semangat', 'always', 'ikut', 'ide', 'wkwkw', 'wkwk', 'wk', 'buset', 'samsek', 'belom', 'plisss',
    'dri', 'apakah', 'dipake', 'kaget', 'inget', 'baju', 'hamil', 'buset', 'anjir', 'anjrit',
    
    # Spam Manual
    'jual', 'beli', 'ready', 'stok', 'tersedia', 'minat', 'dm', 
    'wa', 'hubungi', 'cek', 'bio', 'link', 'shopee', 'tokped',
    'ragout', 'risol', 'pisang', 'coklat', 'keju', 'kue', 
    'bogor', 'jakarta', 'bandung', 'kirim', 'ongkir', 'cod',
    'scroll', 'bingung', 'izin', 'berkenan'
}
