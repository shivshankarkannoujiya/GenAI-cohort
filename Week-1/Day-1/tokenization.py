import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")
print("Vocab size: ", encoder.n_vocab)

text = "The cat sat on the mat"
token = encoder.encode(text)
print("Tokens: ", token)

my_tokens = [976, 9059, 10139, 402, 290, 2450]
decoded = encoder.decode(my_tokens)
print("decoded: ", decoded)