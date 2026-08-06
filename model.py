from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate(student_answer, model_answer):

    emb1 = model.encode(student_answer, convert_to_tensor=True)
    emb2 = model.encode(model_answer, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2)

    score = float(similarity[0][0]) * 10

    if score < 0:
        score = 0

    return round(score,2)