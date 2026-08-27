from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Tải pre-trained model embedding (model nhỏ nhẹ, chạy nhanh)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Danh sách các câu dữ liệu mẫu
documents = [
    "Tôi thích ăn phở bò Hà Nội.",
    "Bún chả là món ăn rất ngon.",
    "Tôi không yêu Việt Nam",
    "Python là ngôn ngữ lập trình phổ biến."
]

# 3. Tạo Embedding Vectors cho danh sách câu
# Kích thước đầu ra của mỗi câu là một vectơ 384 chiều (float32)
embeddings = model.encode(documents)

print(f"Số lượng văn bản: {len(embeddings)}")
print(f"Kích thước 1 vector embedding: {embeddings[0].shape}")

# 4. Giả sử người dùng nhập 1 câu truy vấn (Query)
query = "tôi yêu việt nam"
query_embedding = model.encode([query])

# 5. Tính độ tương đồng Cosine Similarity giữa Query và các Document
similarities = cosine_similarity(query_embedding, embeddings)[0]

# 6. In kết quả độ tương đồng
print(f"\nQuery: '{query}'\n")
for doc, score in zip(documents, similarities):
    print(f"Score: {score:.4f} | Document: {doc}")
