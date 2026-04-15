# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built using **Python, Streamlit, and Machine Learning**.

This application recommends similar movies based on **genre, director, and cast** using **CountVectorizer** and **Cosine Similarity**.

---

## 🚀 Features

- 🎯 Recommend top **9 similar movies**
- 🔍 Handle **misspelled movie names** using fuzzy matching
- 🎥 Fetch and display **movie posters using TMDB API**
- 🕘 Show **recent search history**
- ⚡ Fast recommendations using cosine similarity
- 📱 Clean and responsive **Streamlit UI**

---

## ⚠️ Important Note

This project uses the **IMDb Top 1000 Movies Dataset**, so:

- Recommendations are limited to **only these 1000 movies**
- It does **NOT include all movies from IMDb or the internet**

---

## 📊 Dataset Information

The dataset contains **top 1000 highest-rated movies from IMDb**.

### Columns Used:
- `Series_Title`
- `Genre`
- `Director`
- `Star1`
- `Star2`
- `Star3`

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Scikit-learn**
- **Requests**
- **TMDB API**

---

## 🧠 How It Works

### 1️⃣ Data Preprocessing

Important features are combined into a single **tag column**:

```python
tag = Genre + Director + Star1 + Star2 + Star3
```

---

### 2️⃣ Text Vectorization

Text data is converted into numerical vectors:

```python
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
vectors = cv.fit_transform(tags)
```

---

### 3️⃣ Similarity Calculation

Cosine similarity is used to find similar movies:

```python
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)
```

---

### 4️⃣ Fuzzy Search

Handles incorrect spellings:

```
avngers → avengers
```

---

## 📂 Project Structure

```
movie-recommendation-system-streamlit/
│
├── app.py
├── data.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/krishna-srivastava/movie-recommendation-system-streamlit.git
cd movie-recommendation-system-streamlit
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the application

```bash
streamlit run app.py
```

---

## 🔑 TMDB API Setup

Get your API key from TMDB and add:

```python
TMDB_API_KEY = "your_api_key_here"
```

---

## 📸 Preview

```markdown
![App Screenshot](https://raw.githubusercontent.com/krishna-srivastava/movie-recommendation-system-streamlit/main/screenshot.png)
```

---

## 🎯 Future Improvements

- 📖 Add movie overview / plot
- ⭐ Include IMDb ratings
- 🎭 Genre-based filtering
- 🤖 Improve recommendation accuracy
- ☁️ Deploy on Streamlit Cloud
- 📚 Expand dataset beyond top 1000 movies

---

## 👨‍💻 Author

Made with ❤️ by **Krishna**
