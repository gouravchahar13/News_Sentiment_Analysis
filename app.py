import streamlit as st
from news import fetch_news
from utils import get_sentiment, extract_keywords, text_to_speech, comparison_impact, summarize_text
from googletrans import Translator

# Initialize Google Translator
translator = Translator()

# Streamlit App Title
st.title("📢 News Sentiment & Keyword Analyzer with Hindi Speech & Comparison")

# User Input for Company Name
company_name = st.text_input("Enter Company Name:",placeholder="Google Tesla Apple etc")

if st.button("Fetch News & Analyze"):
    st.write(f"Fetching latest news about **{company_name}**...")

    # Fetch News Articles
    news_data = fetch_news(company=company_name, limit=10)

    if news_data:
        sentiment_results = []  # Store Sentiment Results
        summarized_text = ""  # Combined summary for TTS
        previous_article = None  # Store the previous article for comparison

        for article in news_data:
            title = article["title"]
            snippet = article["snippet"]
            link = article["link"]

            # Summarize title + snippet
            summary = summarize_text(title + " " + snippet)

            # Analyze Sentiment
            sentiment = get_sentiment(summary)

            # Extract Keywords
            keywords = extract_keywords(summary)
            keywords_display = ", ".join(keywords) if isinstance(keywords, list) else "No keywords extracted"

            # Display Summarized Article with Sentiment and Keywords
            st.subheader(title)
            st.write(f"📰 **Summary:** {summary}")
            st.write(f"🔗 [Read More]({link})")
            st.write(f"🧠 **Sentiment:** {sentiment}")
            st.write(f"🔑 **Keywords:** {keywords_display}")

            # Compare with previous article
            if previous_article:
                comparison_result = comparison_impact(previous_article, summary)
                st.write("📊 **Comparison Impact with Previous Article:**")
                st.write(comparison_result["Impact Analysis"])
            
            # Store current summary as previous for next iteration
            previous_article = summary

            sentiment_results.append((title, sentiment))
            summarized_text += summary + " "  # Append for TTS

        # Translate Summary to Hindi
        translated_summary = translator.translate(summarized_text, src="en", dest="hi").text

        # Automatically Generate and Play Hindi Speech
        st.write("🔊 **Generating Hindi Audio...**")
        text_to_speech(translated_summary)

        # Display Audio Output
        st.audio("output.wav", format="audio/wav")
    
    else:
        st.error("❌ No news articles found! Try another company.")
