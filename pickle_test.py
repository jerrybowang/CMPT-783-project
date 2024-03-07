import pickle


summary_set = {}
try:
    with open("imm_result/summary.pickle", "rb") as f:
        summary_set = pickle.load(f)
except FileNotFoundError:
    pass

print(summary_set)