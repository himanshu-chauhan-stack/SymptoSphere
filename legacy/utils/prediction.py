import numpy as np

def predict_top3(model, encoder, input_array):
    probs = model.predict_proba(input_array)[0]
    classes = encoder.inverse_transform(range(len(probs)))

    top3_idx = probs.argsort()[-3:][::-1]

    results = []
    for i in top3_idx:
        results.append((classes[i], probs[i]*100))

    return results