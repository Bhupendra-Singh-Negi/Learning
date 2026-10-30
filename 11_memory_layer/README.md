# Types of Memory

### Short-term memory (STM)
- Active only during the current session
- Holds context while a task is being performed

### Long-term memory (LTM)
- Persists across sessions
- Types:
  - **Factual:** user details (name, age, preferences)
  - **Episodic:** past experiences and interactions with the user
  - **Semantic:** general knowledge and facts

## Embedding dimensions
 represent the number of numerical values used to represent text as a vector. These vectors help identify semantic similarities and relationships between sentences.

- **768 dimensions:** Lower storage and computation; suitable for lightweight applications.
- **1,536 dimensions:** Balances storage, speed, and representation capacity; suitable for RAG systems and chatbots.
- **3,072 dimensions:** Higher representation capacity, potentially helping recognize more complex semantic relationships, but requiring more storage and computation.

**Remember:** Generally, higher dimensions can represent more information, but do not guarantee better recognition or search results. The embedding model also matters. Dimensions must match your Qdrant collection's configuration.