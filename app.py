import pandas as pd
import plotly.express as px
import os
import streamlit as st
from datetime import datetime

from models.whisper_model import transcribe_audio
from models.semantic_model import calculate_similarity
from models.scoring import understanding_level

from audio.audio_features import extract_audio_features
from audio.waveform import plot_waveform
from audio.filler_detection import count_fillers

from reports.pdf_report import generate_pdf

from database.database import (
    create_database,
    insert_report,
    get_reports,
    get_dashboard_stats,
    get_similarity_history,
    delete_all_reports,
    get_top_students,
    get_topic_performance
)
from data.topics import TOPICS

# -----------------------------------
# Streamlit Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Voice-Based Concept Understanding Analyser",
    page_icon="🎤",
    layout="wide"
)
st.markdown("""
<style>

.metric-card{
    background:white;
    border-radius:22px;
    padding:14px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    text-align:center;
    margin-bottom:15px;
}

.metric-card:hover{
    transform:translateY(-5px);
    transition:0.3s;
    box-shadow:0 10px 20px rgba(0,0,0,.15);
}

.blue{
border-top:6px solid #2563eb;
}

.green{
border-top:6px solid #16a34a;
}

.orange{
border-top:6px solid #f59e0b;
}

.red{
border-top:6px solid #ef4444;
}

.metric-title{
font-size:20px;
font-weight:600;
color:#555;
}

.metric-value{
font-size:36px;
font-weight:bold;
color:#111827;
margin-top:15px;
}

.stApp{
    background:#f5f7fb;
}

</style>
""", unsafe_allow_html=True)


create_database()

st.title("🎤 Voice-Based Concept Understanding Analyser")

# ======================================================
# AI Platform Information
# ======================================================

st.markdown("""
<div style="
background:linear-gradient(135deg,#eef7ff,#ffffff);
padding:25px;
border-radius:18px;
border-left:6px solid #2563eb;
margin-bottom:25px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
">

<h2 style="color:#1d4ed8;">
🤖 AI-Powered Voice Analysis Platform
</h2>

<p style="font-size:17px;color:#444;">
This application evaluates a student's conceptual understanding
from spoken explanations using Artificial Intelligence and
Natural Language Processing.
</p>

<hr>

<h4>✨ Key Features</h4>

✅ Speech-to-Text using <b>OpenAI Whisper</b><br>
✅ Semantic Understanding using <b>Sentence-BERT</b><br>
✅ Audio Feature Analysis<br>
✅ AI Similarity Scoring<br>
✅ Automatic PDF Report Generation<br>
✅ Dashboard Analytics & Report History

</div>
""", unsafe_allow_html=True)

# ======================================================
# AI Workflow
# ======================================================

st.markdown("### ⚙️ AI Processing Workflow")

flow1, flow2, flow3, flow4, flow5, flow6 = st.columns(6)

flow1.markdown(
"""
<div style="text-align:center">
<h3>🎤</h3>
<b>Audio</b>
</div>
""",
unsafe_allow_html=True
)

flow2.markdown(
"""
<div style="text-align:center">
<h3>📝</h3>
<b>Speech to Text</b>
</div>
""",
unsafe_allow_html=True
)

flow3.markdown(
"""
<div style="text-align:center">
<h3>🧠</h3>
<b>Sentence-BERT</b>
</div>
""",
unsafe_allow_html=True
)

flow4.markdown(
"""
<div style="text-align:center">
<h3>📊</h3>
<b>Similarity</b>
</div>
""",
unsafe_allow_html=True
)

flow5.markdown(
"""
<div style="text-align:center">
<h3>🎵</h3>
<b>Audio Analysis</b>
</div>
""",
unsafe_allow_html=True
)

flow6.markdown(
"""
<div style="text-align:center">
<h3>📄</h3>
<b>PDF Report</b>
</div>
""",
unsafe_allow_html=True
)

st.divider()

# -----------------------------------
# Dashboard
# -----------------------------------

stats = get_dashboard_stats()



st.markdown("## 📊 Dashboard")

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-title">📄 Total Reports</div>
        <div class="metric-value">{stats['total_reports']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-title">📈 Average Similarity</div>
        <div class="metric-value">{stats['average_similarity']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:

    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-title">🏆 Best Similarity</div>
        <div class="metric-value">{stats['best_similarity']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-title">⏱ Average Duration</div>
        <div class="metric-value">{stats['average_duration']:.2f} sec</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
# -----------------------------------
# Similarity History Chart
# -----------------------------------

history = get_similarity_history()

if history:

    df = pd.DataFrame(
        history,
        columns=["Report ID", "Similarity"]
    )

    fig = px.line(
        df,
        x="Report ID",
        y="Similarity",
        markers=True,
        title="📈 Similarity Score History"
    )

    fig.update_traces(
       line=dict(width=4),
       marker=dict(size=10)
    )

    fig.update_layout(
        title_font_size=22,
        title_x=0.5,
        xaxis_title="Report Number",
        yaxis_title="Similarity (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        hovermode="x unified"
    )

    fig.update_xaxes(
       showgrid=False,
       zeroline=False
    )

    fig.update_yaxes(
       showgrid=True,
       gridcolor="lightgray",
       zeroline=False
    )

    st.plotly_chart(fig, use_container_width=True)
    # -----------------------------------
    # Topic-wise Performance
    # -----------------------------------

    topic_data = get_topic_performance()

    if topic_data:

        topic_df = pd.DataFrame(
            topic_data,
            columns=["Topic", "Average Similarity"]
        )

        st.markdown("## 📊 Topic-wise Performance")

        fig = px.bar(
           topic_df,
           x="Average Similarity",
           y="Topic",
           orientation="h",
           text="Average Similarity",
           color="Average Similarity",
           color_continuous_scale="Blues",
           title="📚 Topic-wise Performance"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_layout(
            title_x=0.5,
            title_font_size=22,
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=350,
            coloraxis_showscale=False,
            xaxis_title="Average Similarity (%)",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)
st.markdown("""          
            
Upload an audio explanation of a concept.

This application will:
- 🎙 Convert Speech to Text (Whisper)
- 🧠 Evaluate Concept Understanding (Sentence-BERT)
- ⭐ Calculate Understanding Score
- 🎵 Analyse Audio Features
""")

# -----------------------------------
# Student Details
# -----------------------------------

st.subheader("👤 Student Details")

st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
border-left:6px solid #2563eb;
margin-bottom:20px;
">

<h3 style="margin-bottom:10px;">📝 Student Information</h3>

<p style="font-size:16px;color:#555;">
Please enter the student's details below and upload a voice explanation.
The AI system will transcribe the speech, evaluate conceptual understanding,
analyze audio quality, and generate a detailed PDF report.
</p>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input(
        "👤 Student Name",
        placeholder="Enter student name"
    )

with col2:
    roll_number = st.text_input(
        "🆔 Roll Number",
        placeholder="Enter roll number"
    )

st.markdown("### 📚 Select Concept Topic")

topic = st.selectbox(
    "",
    list(TOPICS.keys()),
    label_visibility="collapsed"
)

# -----------------------------------
# Reference Concept
# -----------------------------------
reference_text = TOPICS[topic]

# -----------------------------------
# Upload Audio
# -----------------------------------
st.markdown("### 🎤 Upload Audio Explanation")

uploaded_file = st.file_uploader(
    "",
    type=[
        "wav",
        "mp3",
        "m4a",
        "mpeg",
        "aac",
        "ogg",
        "flac",
        "mp4"
    ]
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    audio_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Audio uploaded successfully!")

    st.audio(audio_path)

    if st.button(
    "🚀 Analyze Voice Explanation",
    use_container_width=True
    ):

        # -----------------------------
        # Whisper
        # -----------------------------
        with st.spinner("Transcribing audio..."):

            transcript = transcribe_audio(audio_path)
        
        st.divider()
        st.markdown("## 📝 Transcript")

        st.info(transcript)

        # -----------------------------
        # Semantic Similarity
        # -----------------------------
        similarity = calculate_similarity(
            reference_text,
            transcript
        )

        st.markdown("## 📊 Analysis Summary")
        st.progress(float(similarity))

        level = understanding_level(similarity)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
               "📈 Similarity Score",
               f"{similarity*100:.2f}%"
            )

            st.progress(similarity)

        with col2:

            if level.lower() == "excellent":
               st.success("🟢 Excellent")

            elif level.lower() == "good":
               st.info("🔵 Good")

            elif level.lower() == "average":
               st.warning("🟡 Average")

            else:
               st.error("🔴 Needs Improvement")
        # -----------------------------
        # Audio Analysis
        # -----------------------------
        st.markdown("## 🎵 Audio Statistics")

        features = extract_audio_features(audio_path)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Duration",
                f"{features['duration']} sec"
            )

        with col2:
            st.metric(
                "RMS Energy",
                features["rms_energy"]
            )

        # -----------------------------
        # Filler Words
        # -----------------------------
        fillers = count_fillers(transcript)

        st.metric(
            "Filler Words",
            fillers
        )

        # -----------------------------
        # Waveform
        # -----------------------------
        st.subheader("📈 Waveform")

        figure = plot_waveform(audio_path)

        st.pyplot(figure)
        
        # -----------------------------------
        # AI Feedback
        # -----------------------------------

        st.markdown("---")
        st.markdown("## 🤖 AI Feedback")

        if similarity >= 0.90:

           st.success("""
        ### 🌟 Excellent Performance

        ✅ Outstanding conceptual understanding.

        ✅ Your explanation closely matches the reference concept.

        ✅ Excellent use of technical terminology.

        💡 Recommendation:
        Keep maintaining this level of explanation.
        """)

        elif similarity >= 0.75:

           st.info("""
        ### 👍 Good Performance

        ✅ Good conceptual understanding.

        ✅ Most important concepts were explained correctly.

        💡 Recommendation:
        Include more examples and technical keywords for a higher score.
        """)

        elif similarity >= 0.50:

           st.warning("""
        ### 📚 Average Performance

        ✅ Basic understanding detected.

        ⚠ Some important concepts are missing.

        💡 Recommendation:
        Revise the topic and explain it with more details.
        """)

        else:

           st.error("""
        ### ❌ Needs Improvement

        ⚠ Low semantic similarity detected.

        ⚠ The explanation does not sufficiently cover the reference concept.

        💡 Recommendation:
        Study the topic again and provide a more complete explanation using key concepts.
        """)
        
        st.markdown("## 🕒 Report Information")

        col1, col2 = st.columns(2)

        with col1:
            st.info("📅 Date\n\n" + datetime.now().strftime("%d-%m-%Y"))

        with col2:
            st.info("🕒 Time\n\n" + datetime.now().strftime("%I:%M %p")) 
        # -----------------------------------
        # Performance Summary
        # -----------------------------------

        st.markdown("---")
        st.markdown("## 📋 Performance Summary")

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        ">

        <b>👤 Student Name:</b> {student_name}<br><br>

        <b>🆔 Roll Number:</b> {roll_number}<br><br>

        <b>📚 Topic:</b> {topic}<br><br>

        <b>📈 Similarity Score:</b> {similarity*100:.2f}%<br><br>

        <b>⭐ Understanding Level:</b> {level}<br><br>

        <b>🎵 Audio Duration:</b> {features['duration']} sec<br><br>

        <b>💬 Filler Words:</b> {fillers}

        </div>
        """, unsafe_allow_html=True) 
        
        st.markdown("### 🎯 Overall Result")

        if similarity >= 0.90:
           st.success("Excellent understanding of the selected concept.")

        elif similarity >= 0.75:
           st.info("Good understanding of the selected concept.")

        elif similarity >= 0.50:
           st.warning("Average understanding. More detailed explanation is recommended.")

        else:
           st.error("Needs improvement. Review the topic and explain it again.")  
           
           
        # -----------------------------
        # Generate PDF Report
        # -----------------------------

        pdf_path = generate_pdf(
            filename="report.pdf",
            student_name=student_name,
            roll_number=roll_number,
            topic=topic,
            transcript=transcript,
            similarity=similarity * 100,
            level=level,
            duration=features["duration"],
            rms=features["rms_energy"],
            fillers=fillers
            )

        

        with open(pdf_path, "rb") as pdf_file:
          st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="Voice_Report.pdf",
            mime="application/pdf"
          )
          
        insert_report(
           student_name=student_name,
           topic=topic,
           transcript=transcript,
           similarity=similarity * 100,
           level=level,
           duration=features["duration"],
           rms=features["rms_energy"],
           fillers=fillers
        )

        st.success("""
        ## 🎉 Voice Analysis Completed Successfully!

        ✅ Speech Transcribed

        ✅ Semantic Similarity Calculated

        ✅ Audio Features Extracted

        ✅ AI Feedback Generated

        ✅ PDF Report Generated

        ✅ Report Saved to Database
        """)
        
        # -----------------------------------
        # Previous Reports
        # -----------------------------------

        st.divider()
        
        # -----------------------------------
        # Student Leaderboard
        # -----------------------------------

        st.markdown("---")
        st.header("🏆 Top Performing Students")

        leaders = get_top_students()

        if leaders:

            for i, student in enumerate(leaders, start=1):

                if i == 1:
                    medal = "🥇"
                    color = "#FFD700"
                elif i == 2:
                    medal = "🥈"
                    color = "#C0C0C0"
                elif i == 3:
                    medal = "🥉"
                    color = "#CD7F32"
                else:
                    medal = "🏅"
                    color = "#2563EB"

                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:12px;
                    padding:15px;
                    margin-bottom:12px;
                    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
                    border-left:6px solid {color};
                ">

                <h4>{medal} {student[0]}</h4>

                <p style="font-size:18px;">
                    📊 Similarity Score:
                    <b style="color:{color};">{student[1]:.2f}%</b>
                </p>

                </div>
                """, unsafe_allow_html=True)

        else:

            st.info("No student records available.")

        st.header("📜 Previous Reports")
        
        search = st.text_input(
           "🔍 Search Student",
           placeholder="Enter student name..."
        )

        reports = get_reports()

        # Remove this after testing
        # st.write(reports)

        if reports:

            for report in reports:

                if search and search.lower() not in report[1].lower():
                    continue

                with st.expander(f"📄 Report #{report[0]}"):

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**👤 Student Name**")
                        st.write(report[1])

                        st.markdown("**📚 Topic**")
                        st.write(report[2])

                        st.markdown("**🧠 Understanding**")
                        st.success(report[5])

                    with col2:
                        st.metric("📊 Similarity", f"{report[4]:.2f}%")
                        st.metric("⏱ Duration", f"{report[6]:.2f} sec")
                        st.metric("💬 Filler Words", report[8])

                    st.markdown("### 📝 Transcript")
                    st.info(report[3])

                    st.markdown("### 🔊 RMS Energy")
                    st.code(str(report[7]))
        else:

            st.info("No reports found.")
        # -----------------------------------
        # Delete All Reports
        # -----------------------------------

        if st.button("🗑 Delete All Reports"):

            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):

            st.warning("⚠️ This will permanently delete all reports.")

            if st.checkbox("I understand. Delete all reports."):

               if st.button("✅ Confirm Delete"):

                  delete_all_reports()

                  st.success("All reports deleted successfully!")

                  st.session_state["confirm_delete"] = False

                  st.rerun()
            
st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:25px;
background:#f8f9fa;
border-radius:12px;
margin-top:20px;
">

<h3 style="color:#2563EB;">
🎤 Voice-Based Concept Understanding Analyser
</h3>

<p style="font-size:16px;color:#555;">
AI-Powered Student Performance Evaluation System
</p>

<p style="color:#666;">
🐍 Python &nbsp; • &nbsp;
⚡ Streamlit &nbsp; • &nbsp;
🎙 Whisper AI &nbsp; • &nbsp;
🧠 Sentence-BERT &nbsp; • &nbsp;
🗄 SQLite
</p>

<hr style="margin-top:15px;">

<p style="font-size:14px;color:gray;">
© 2026 Internship Project 
</p>

</div>
""", unsafe_allow_html=True)                   