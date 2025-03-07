# 📚 Personalized AI Tutor

**Personalized AI Tutor** is an intelligent educational assistant designed to retrieve course materials, explain concepts, and generate quizzes using Retrieval-Augmented Generation (RAG). It leverages **FAISS** for fast search, **Ollama** for AI-powered responses, and **Streamlit** for an interactive UI.

---

## 🚀 Features

✅ **Question & Answer System** 📖  
Retrieve relevant learning materials and get AI-generated explanations.

✅ **Quiz Generation** 🎯  
Generate multiple-choice quizzes with explanations based on selected topics.

✅ **Subject Support** 🏫  
Covers **Mathematics, Physics, Computer Science, Biology, Chemistry, Engineering, Economics, and Psychology**.

✅ **Efficient Search** 🔍  
Uses **FAISS** for fast semantic search on indexed educational data.

✅ **Streamlit UI** 🎨  
Provides an easy-to-use web interface for interaction.

---

## 🏗️ Tech Stack

- **Data Collection:** Web scraping using `BeautifulSoup` ([document_collection.py](document_collection.py))  
- **Indexing & Search:** FAISS with `SentenceTransformers` ([faiss_indexing.py](faiss_indexing.py))  
- **RAG Pipeline:** Retrieval and AI-generated responses using `Ollama` ([rag_pipeline.py](rag_pipeline.py))  
- **Quiz Generation:** AI-driven quiz questions using `Ollama` ([quiz_assessment.py](quiz_assessment.py))  
- **User Interface:** Built with `Streamlit` ([UI.py](UI.py))  

---

## 🛠 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/personalized-ai-tutor.git
cd personalized-ai-tutor
