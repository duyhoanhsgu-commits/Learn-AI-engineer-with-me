# Semantic Search: How Computers Search by Meaning

## Introduction

Every day, people use search systems to find information. We search on Google, look for products on shopping websites, find videos, or ask AI systems questions.

In the past, most search systems mainly looked for **keywords**. If the words in the user's question were also in a document, the system considered that document important.

However, people do not always use the same words to express the same idea.

For example, a user may search:

> "How can I reduce my electricity bill?"

But a document may contain:

> "Ways to save energy at home."

The two sentences use different words, but their meanings are very similar.

This is the main problem that **semantic search** tries to solve.

---

## 1. What Is Semantic Search?

Semantic search is a search method that tries to understand the **meaning** of a query instead of only matching words.

The word **semantic** is related to meaning.

A traditional search system may ask:

> "Do these sentences contain the same words?"

A semantic search system asks:

> "Do these sentences have similar meanings?"

For example:

**Query:**
"How can I learn English faster?"

**Document:**
"Tips for improving your English skills quickly."

There are not many exact words in common. However, both sentences talk about improving English in a short time.

A semantic search system can understand this relationship and return the document.

---

## 2. Traditional Keyword Search

Before semantic search became popular, many systems used **keyword search**, also called **lexical search**.

The basic idea is simple.

Imagine a user searches for:

> "cheap hotel near the beach"

The search system looks for documents that contain words such as:

* cheap
* hotel
* beach

If a document contains many of these words, it may receive a higher score.

Methods such as **TF-IDF** and **BM25** are commonly used for this type of search.

Keyword search is useful because it is fast and works very well when users know the exact words they need.

However, it has an important weakness: it does not fully understand meaning.

For example:

**Query:**
"How do I fix my laptop?"

**Document:**
"Steps to repair a computer."

A keyword system may not see a strong connection between **fix** and **repair**, or between **laptop** and **computer**.

A human can easily understand that these words are related.

This is why semantic search is useful.

---

## 3. Embeddings: Turning Meaning into Numbers

Computers cannot understand language in exactly the same way humans do. They work with numbers.

To help computers work with meaning, semantic search often uses **embeddings**.

An embedding is a numerical representation of text.

For example, the sentence:

> "I love learning English."

can be changed into a list of numbers:

> [0.12, -0.34, 0.78, 0.21, ...]

This list of numbers is called a **vector**.

In real systems, a vector can contain hundreds or even thousands of numbers.

The important idea is that texts with similar meanings usually have vectors that are close to each other.

For example:

> "I enjoy studying English."

and

> "I like learning English."

should have similar vectors because their meanings are similar.

However:

> "My car needs more fuel."

should have a very different vector because it talks about another topic.

---

## 4. How Semantic Search Works

A basic semantic search system usually has several steps.

### Step 1: Prepare the Documents

First, the system collects documents.

These documents can be:

* PDF files
* websites
* books
* company documents
* product information
* questions and answers

Large documents are often divided into smaller pieces called **chunks**.

For example, a 50-page PDF may be divided into many small text chunks.

This makes searching easier and more accurate.

### Step 2: Create Embeddings

Next, an embedding model converts every chunk into a vector.

For example:

> Document → Chunk → Embedding Model → Vector

The system now has a numerical representation of each piece of information.

### Step 3: Store the Vectors

The vectors are usually stored in a **vector database**.

Popular vector databases include Qdrant, Pinecone, Weaviate, Milvus, and Chroma.

A vector database is designed to store vectors and quickly find similar vectors.

### Step 4: Convert the User's Question

When a user asks:

> "How can I improve my English speaking?"

the system sends this question to the same embedding model.

The model creates a vector for the question.

So now we have:

> User Query → Embedding Model → Query Vector

### Step 5: Compare the Vectors

The system compares the query vector with the document vectors.

It tries to find the vectors that are closest to the query vector.

One common method is **cosine similarity**.

It measures how similar two vectors are.

A higher similarity score usually means that the two texts have more similar meanings.

### Step 6: Return the Best Results

Finally, the system chooses the most relevant chunks.

For example:

> User Query
> ↓
> Query Embedding
> ↓
> Vector Search
> ↓
> Top Similar Documents
> ↓
> Search Results

The system may return the top 3, top 5, or top 10 most similar results.

This process is called **retrieval**.

---

## 5. Semantic Search and RAG

Semantic search is also an important part of many modern AI systems.

One common example is **Retrieval-Augmented Generation**, or **RAG**.

A normal Large Language Model, or LLM, generates answers using knowledge learned during training. However, the model may not know private company information or new information.

RAG solves part of this problem by adding a retrieval system.

A simple RAG pipeline looks like this:

> User Question
> ↓
> Semantic Search
> ↓
> Retrieve Relevant Documents
> ↓
> Send Documents + Question to the LLM
> ↓
> Generate an Answer

For example, imagine a hotel has hundreds of documents about rooms, services, rules, and facilities.

A guest asks:

> "Can I bring my pet to the hotel?"

Semantic search can find the part of the hotel document that talks about pets.

The system then gives this information to the LLM.

The LLM can use the retrieved information to answer the guest.

This makes the answer more connected to the real documents.

---

## 6. Semantic Search vs. Keyword Search

Semantic search is powerful, but this does not mean keyword search is useless.

Keyword search is often better when users search for exact information such as:

> "HTTP 404"

> "iPhone 15 Pro"

> "Order ID A12345"

In these cases, exact words are very important.

Semantic search is often better for natural questions such as:

> "Why can't I access this page?"

or:

> "Which phone has a good camera for travel?"

For this reason, many modern systems use both methods together.

This approach is called **hybrid search**.

Hybrid search combines:

> Keyword Search + Semantic Search

The system can use exact word matching and meaning at the same time.

This often produces better results than using only one method.

---

## 7. Reranking Search Results

Sometimes semantic search returns many possible documents.

The first search may be fast, but the order of the results may not be perfect.

A system can use another model to check these results again. This process is called **reranking**.

For example:

> User Query
> ↓
> Semantic Search
> ↓
> Top 20 Results
> ↓
> Reranker
> ↓
> Best 5 Results

The first search finds possible documents quickly.

Then, the reranker looks more carefully at the query and each document. It moves the most useful documents to the top.

This can improve the quality of a RAG system because the LLM receives better information.

---

## 8. Challenges of Semantic Search

Semantic search is useful, but it is not perfect.

One challenge is the **embedding model**.

Different embedding models understand language differently. A model that works well for English may not work as well for Vietnamese or other languages.

Another challenge is **chunking**.

If chunks are too large, they may contain too much unrelated information.

If chunks are too small, they may lose important context.

The quality of the documents is also important.

If the database contains incorrect or old information, semantic search may still retrieve it.

Finally, similar meaning does not always mean that a document is the correct answer.

Because of this, developers need to test and evaluate the retrieval system carefully.

---

## 9. How Can We Evaluate Semantic Search?

Developers need to know whether the search system is finding the correct information.

One simple method is to prepare a group of test questions with expected documents.

For each question, we can check whether the correct document appears in the top search results.

For example:

> Question → Expected Document → Search Results

If the expected document appears in the top 5 results, the retrieval is successful for that question.

Common evaluation ideas include **Precision**, **Recall**, **Hit Rate**, and **MRR**.

These measurements help developers compare different embedding models, chunk sizes, and search methods.

---

## 10. A Complete Semantic Search Pipeline

A simple production system can be divided into two main stages.

### Indexing

This stage happens before users search.

> Documents
> ↓
> Parse Text
> ↓
> Clean Text
> ↓
> Chunk Documents
> ↓
> Create Embeddings
> ↓
> Store Vectors and Metadata

### Retrieval

This stage happens when a user asks a question.

> User Query
> ↓
> Create Query Embedding
> ↓
> Search Vector Database
> ↓
> Find Similar Chunks
> ↓
> Optional Hybrid Search
> ↓
> Rerank Results
> ↓
> Return the Best Documents

If the system uses RAG, one more step is added:

> Best Documents + User Question
> ↓
> LLM
> ↓
> Final Answer

---

## Conclusion

Semantic search changes the way computers find information.

Traditional search mainly focuses on **words**, while semantic search focuses on **meaning**.

The main idea is simple:

> Text → Embedding → Vector → Similarity Search → Relevant Information

Embeddings allow computers to represent the meaning of text as numbers. Vector databases make it possible to search millions of these vectors quickly.

Semantic search is especially useful for natural-language questions and is an important part of modern RAG systems.

However, semantic search alone is not always enough. Good systems also need proper chunking, useful metadata, strong embedding models, evaluation, and sometimes keyword search and reranking.

The goal is not only to find documents that contain the same words as the user's question.

The real goal is to find information that **means what the user is looking for**.
