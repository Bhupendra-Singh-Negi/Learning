import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text ="Hello there! How are you doing today? I hope you're having a great day."
tokens = enc.encode(text)

print("Original Text:", text)
print("Tokenized Output:", tokens)
print("Number of Tokens:", enc.decode([13225, 1354, 0, 3253, 553, 481, 5306, 4044, 30, 357, 5498, 7163, 4566, 261, 2212, 2163, 13]))