import pandas as pd
import re
import streamlit as st
import os
from transformers import pipeline
from modules.constants import SPAM_KEYWORDS, TOPIC_STOPWORDS, DICT_PATH

class DataEngine:
    @staticmethod
    @st.cache_resource
    def load_resources():
        """Load stopwords dan Model AI"""
        try:
            stop_df = pd.read_csv(os.path.join(DICT_PATH, 'stopwords.csv'))
            csv_stop_set = set(stop_df['word'].str.strip().str.lower())
        except Exception:
            csv_stop_set = set()
        
        final_stop_set = csv_stop_set.union(TOPIC_STOPWORDS)
        
        try:
            classifier = pipeline(
                "sentiment-analysis", 
                model="w11wo/indonesian-roberta-base-sentiment-classifier",
                tokenizer="w11wo/indonesian-roberta-base-sentiment-classifier"
            )
        except Exception:
            classifier = None
        
        return final_stop_set, classifier

    @staticmethod
    def is_spam(text):
        if not isinstance(text, str): return False
        text_lower = text.lower()
        for keyword in SPAM_KEYWORDS:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                return True
        words = text_lower.split()
        if len(words) < 5 and 'http' in text_lower:
            return True
        return False

    @staticmethod
    def clean_text_for_topic(text, stop_set):
        if not isinstance(text, str): return ""
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'@[A-Za-z0-9_]+', '', text)
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        words = text.split()
        clean_words = []
        for w in words:
            if w in stop_set: continue
            if len(w) < 3: continue
            clean_words.append(w)
        return " ".join(clean_words)

    @staticmethod
    @st.cache_data
    def process_dataset(file_source):
        try:
            # 1. Load Resources
            final_stop_set, sentiment_pipeline = DataEngine.load_resources()

            # 2. Read Data
            df = pd.read_csv(file_source, dtype={'id_str': str, 'user_id_str': str})
            df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y', errors='coerce')
            df.sort_values(by='created_at', inplace=True)
            df['date_only'] = df['created_at'].dt.date
            df.drop_duplicates(subset=['full_text'], inplace=True)

            clean_texts, sent_labels, sent_scores, is_promo = [], [], [], []
            texts = df['full_text'].astype(str).tolist()
            total = len(df)
            
            bar = st.progress(0)

            for i, text in enumerate(texts):
                # SPAM CHECK
                if DataEngine.is_spam(text):
                    is_promo.append(True)
                    sent_labels.append('Promo')
                    sent_scores.append(0)
                    clean_texts.append("")
                else:
                    # ORGANIC PROCESS
                    is_promo.append(False)
                    clean_texts.append(DataEngine.clean_text_for_topic(text, final_stop_set))
                    
                    # SENTIMENT
                    fl, fs = 'Netral', 0
                    if sentiment_pipeline:
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
                            pass
                    
                    sent_labels.append(fl)
                    sent_scores.append(fs)
                
                if i % 10 == 0: bar.progress((i+1)/total)
            
            bar.empty()

            df['clean_text'] = clean_texts
            df['sentiment'] = sent_labels
            df['sentiment_score'] = sent_scores
            df['is_promo'] = is_promo
            
            # Engagement Calculation
            fav = df['favorite_count'] if 'favorite_count' in df.columns else 0
            rt = df['retweet_count'] if 'retweet_count' in df.columns else 0
            rep = df['reply_count'] if 'reply_count' in df.columns else 0
            df['engagement_score'] = fav + (2 * rt) + (1.5 * rep)
            
            if 'username' in df.columns:
                df['username'] = df['username'].fillna('User ' + df['user_id_str'].fillna(''))
            else:
                df['username'] = 'User ' + df['user_id_str'].fillna('')
                
            return df
        except Exception as e:
            st.error(f"Error: {e}")
            return None

