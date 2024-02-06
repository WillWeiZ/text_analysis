import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import altair as alt
from collections import Counter

def plot_wordcloud(docx):
    mywordcloud = WordCloud().generate(docx)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(mywordcloud,interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)


def plot_word_freequncy(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    x,y = zip(*most_common_tokens)
    fig = plt.figure(figsize=(20,10))
    plt.bar(x,y)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_word_freq_with_altair(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    x,y = zip(*most_common_tokens)
    data = pd.DataFrame({'tokens':x,'counts':y})
    fig = alt.Chart(data).mark_bar().encode(
        x='tokens',
        y='counts',
        opacity=alt.value(0.7)
    )
    st.altair_chart(fig,use_container_width=True)


import neattext.functions as nfx

def main():
    st.subheader("Text Analysis App")

    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        # text area
        raw_text = st.text_area("Your Text","Enter Text Here")

        if st.button("Sumbit"):
            if len(raw_text) > 2:
                st.write("Success")

            elif len(raw_text) == 1:
                st.warning("Minimum 2 Characters for Analysis")

            else:
                st.write("Enter Text for Analysis")

        # layout, 2 coloumns
        col1, col2 = st.columns(2)
        processed_text = nfx.remove_stopwords(raw_text)
        # col1
        with col1:
            with st.expander("Original Text"):
                st.write(raw_text)
            
            with st.expander("PoS Tagged Text"):
                plot_word_freq_with_altair(processed_text)
            
            with st.expander("Plot Word Frequency"):
                plot_word_freequncy(processed_text)
        
        with col2:
            with st.expander("Processed Text"):
                
                st.write(processed_text)

            with st.expander("Plot wordcloud"):
                plot_wordcloud(processed_text)
            
            with st.expander("Plot Stylometry Curve"):
                st.success("Medelhall Curve")




    if choice == "About":
        pass



if __name__ == '__main__':
    main()
