import streamlit as st

import pandas as pd
import numpy as np
import altair as alt

import joblib

model = joblib.load(open("model/emotional_compass.pkl", "rb"))

emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}


def predict_emotions(docx):
    results = model.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = model.predict_proba([docx])
    return results


def main():
    st.title("Emotional Compass 🧭")
    st.subheader("Emotionally aware, emotionally empowered")

    with st.form(key='my_form'):
        raw_text = st.text_area("Share your feelings...")
        submit_text = st.form_submit_button(label='Submit')

    if submit_text:
        col1, col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("Original Text")
            st.write(raw_text)

            st.success("Prediction")
            emoji_icon = emotions_emoji_dict[prediction]
            st.write("{}:{}".format(prediction, emoji_icon))
            st.write("Confidence:{}".format(np.max(probability)))

        with col2:
            st.success("Prediction Probability")
            proba_df = pd.DataFrame(probability, columns=model.classes_)
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()