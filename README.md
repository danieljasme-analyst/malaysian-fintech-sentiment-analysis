# Malaysian Fintech Sentiment Analysis 🇲🇾

Multilingual sentiment analysis of **248,858 Google Play reviews** across 5 leading Malaysian e-wallet and digital banking apps, using rule-based VADER as baseline and a multilingual transformer (XLM-RoBERTa) for production-grade sentiment classification.

**Course**: ISP610 Business Data Analytics  
**Institution**: Universiti Teknologi MARA (UiTM)  
**Author**: Daniel — Final Year, Bachelor of Computer Science

---

## 🎯 Key Findings (so far)

- **4 out of 5** Malaysian fintech apps exhibit **net-negative user sentiment** when analysis includes Malay-language reviews
- The multilingual transformer (XLM-RoBERTa) detects **92.8%** of 1-star complaints as negative — vs only **51.2%** for English-only VADER
- **MAE by Maybank** ranks worst across **5 out of 9** aspect categories, with Login/Authentication scoring −0.71
- **Setel** is the only app with positive aspect sentiment, driven by its integration with Petronas Mesra Points

---

## 🧰 Tech Stack

- **Data**: `google-play-scraper`, pandas
- **NLP**: VADER, Hugging Face Transformers (XLM-RoBERTa), BERTopic
- **Language detection**: langdetect
- **Visualization**: matplotlib, seaborn, plotly
- **Environment**: Python 3.14, Jupyter, Google Colab (T4 GPU for transformer inference)

---

## 📁 Project Structure
.
 # Phases 1–3, 5: scrape, clean, VADER, ABSA
├── 01_data_exploration.ipynb  
# Phase 4: XLM-RoBERTa inference on Colab GPU
├── 02_transformer_sentiment.ipynb  
├── scrape_reviews.py               # Initial Play Store scraper
├── scrape_missing.py               # Top-up scraper for missing apps
├── phase3_vader_by_app.png         # Baseline sentiment per app
├── phase3_vader_distribution.png   # Sentiment label breakdown
├── phase5_aspect_heatmap.png       # ABSA heatmap (the main visual)
└── aspect_sentiment_pivot.csv      # Final aspect × app sentiment matrix

---

## 📊 Data Pipeline

1. **Phase 1** — Scraped 248,858 reviews from 5 apps in English + Malay (`google-play-scraper`)
2. **Phase 2** — Deduplicated (35% overlap due to lang filter), language-detected, filtered → 137,182 clean reviews
3. **Phase 3** — Established VADER baseline on English reviews (51% accuracy on 1-star)
4. **Phase 4** — Upgraded to XLM-RoBERTa multilingual transformer (92.8% accuracy on 1-star)
5. **Phase 5** — Aspect-Based Sentiment Analysis across 9 user-facing categories
6. **Phase 6** — BERTopic topic modeling (in progress)
7. **Phase 7** — Interactive dashboard + executive summary (in progress)

---

## 📈 Apps Analyzed

| App | Reviews | Avg Transformer Sentiment |
|---|---|---|
| Touch 'n Go eWallet | 59,361 | −0.226 |
| Boost | 32,036 | −0.213 |
| MAE by Maybank | 25,947 | **−0.467** (worst) |
| Setel | 17,294 | **+0.246** (best) |
| GXBank | 2,544 | −0.273 |

---

## ⚠️ Methodology Notes

- **Selection bias in aspect-tagged reviews**: users typically mention specific features only when problems occur. Interpretation focuses on **relative differences** between apps rather than absolute scores.
- **Language detection limits**: `langdetect` confuses Malay (ms) with Indonesian (id); both treated as Malay in this analysis.
- **Manglish (code-switching)**: ~9% of reviews use mixed English-Malay patterns that resist standard language detection.

---

## 📜 License

This is academic coursework. Review data belongs to the original reviewers and Google Play. Code is MIT licensed.
