import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Remote Python Jobs", layout="wide")

# ---------- HEADER ----------
st.markdown("<h1 style='font-size: 42px;'>💼 Remote Python Job Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px;'>Explore remote Python job listings scraped from RemoteOK. Use filters to customize your view.</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- ABOUT THE PROJECT ----------
with st.expander("ℹ️ About this project"):
    st.write("""
        This dashboard shows live remote Python job listings scraped from [RemoteOK](https://remoteok.com).
        It is built using **Python**, **BeautifulSoup**, **pandas**, **Plotly**, and **Streamlit**.
        
        ✅ Features:
        - Real-time job filtering by company, location, and keyword  
        - Interactive bar chart and word cloud  
        - CSV download of filtered results  
        
        📌 Useful for job seekers, analysts, and recruiters.
    """)


# ---------- LOAD DATA ----------
df = pd.read_csv("jobs.csv")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filter Jobs")
selected_company = st.sidebar.multiselect("Company", options=sorted(df["Company"].unique()))
selected_location = st.sidebar.multiselect("Location", options=sorted(df["Location"].unique()))

# ---------- APPLY FILTERS ----------
filtered_df = df.copy()

if selected_company:
    filtered_df = filtered_df[filtered_df["Company"].isin(selected_company)]

if selected_location:
    filtered_df = filtered_df[filtered_df["Location"].isin(selected_location)]

# ---------- KPI BOX ----------
st.markdown(
    f"""
    <div style="
        background-color: #262730; 
        color: #FAFAFA; 
        padding: 15px; 
        border-radius: 10px; 
        font-size: 18px; 
        margin-bottom: 20px; 
        border-left: 5px solid #1f77b4;">
        ✅ <strong>Total Jobs Found:</strong> {len(filtered_df)}
    </div>
    """,
    unsafe_allow_html=True
)


import plotly.express as px

# ---------- BAR CHART: Top 5 Hiring Companies ----------
top_companies = filtered_df["Company"].value_counts().nlargest(5).reset_index()
top_companies.columns = ["Company", "Job Count"]

if not top_companies.empty:
    st.subheader("📊 Top 5 Companies Hiring")
    fig = px.bar(
        top_companies,
        x="Company",
        y="Job Count",
        color="Company",
        color_discrete_sequence=px.colors.sequential.Blues,
        text="Job Count"
    )
    fig.update_layout(xaxis_title="", yaxis_title="Number of Jobs", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available to show the chart.")


from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.subheader("🔠 Most Common Job Titles")

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_df['Job Title']))

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)


# ---------- SEARCH BAR ----------
st.subheader("🔎 Search by Keyword")
keyword = st.text_input("Type a keyword to filter job titles")

if keyword:
    filtered_df = filtered_df[filtered_df["Job Title"].str.contains(keyword, case=False)]


st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_jobs.csv",
    mime="text/csv"
)

job_types = filtered_df["Job Title"].str.extract(r"(Intern|Contract|Senior|Junior)", expand=False).fillna("Other")
pie_df = job_types.value_counts().reset_index()
pie_df.columns = ["Job Type", "Count"]


# ---------- DATAFRAME ----------
st.dataframe(filtered_df, use_container_width=True)


st.markdown("📢 Share this app: [Copy this link](https://sarthxk20-remotejobs.streamlit.app)")


# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<p style='font-size: 14px; text-align: center;'>Made with ❤️ using Streamlit | Data source: RemoteOK</p>", unsafe_allow_html=True)
