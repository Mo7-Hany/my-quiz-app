import streamlit as st
import fitz
import pdfplumber  
import json
from google import genai
from google.genai import types
from image_mode import processing_image
from text_mode import processing_text 
st.markdown("""
    <style>
    /* تغيير خلفية التطبيق ولون الخط */
    .main {
        background-color: #f5f7f9;
    }
    
    /* تجميل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #0056b3;
        color: #ffffff;
        transform: scale(1.02);
    }

    /* تجميل الـ Sidebar */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(#2e3b4e, #1a242f);
        color: white;
    }
    
    /* العناوين */
    h1 {
        color: #1e3a5f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }

    /* تنسيق كروت الأسئلة */
    .stSelectbox {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("AI PDF Quiz Generator")
mode = st.sidebar.selectbox("Choose processing mode:", [None, "Image Mode (High Quality)", "Text Mode (Fast)"])


# حط الزرار في الجنب عشان ميزحمش الواجهة
with st.sidebar:
    st.divider() # خط فاصل
    if st.button("🔄 Reset Everything (نقطة الصفر)"):
        # 1. نمسح كل البيانات المتخزنة في الذاكرة
        st.session_state.clear()
        # 2. نجبر البرنامج إنه يعيد تحميل نفسه كأنه لسه مفتوح حالا
        st.rerun()
file =  st.file_uploader("Upload file", type=["pdf"]) 
# --- كود اختيار الصفحة (يوضع هنا) ---
page_selection_mode = None
selected_page = 1

if file:
    st.sidebar.divider()
    st.sidebar.subheader("إعدادات الصفحات")
    page_selection_mode = st.sidebar.radio(
        "اختر طريقة معالجة الصفحات:",
        [ "صفحة عشوائية","صفحة محددة يدويا"]
    )
    num_questions = st.slider("Number of questions", min_value=1, max_value=20, value=5)
    difficulty = st.selectbox("Difficulty level", ("easy", "medium", "hard"))
    st.markdown("---")
    if st.button("Refresh"):
        st.session_state.clear()


    if page_selection_mode == "صفحة محددة يدويًا" :
        
        selected_page = st.sidebar.number_input("ادخل رقم الصفحة", min_value=1, value=1)
    
        
    st.sidebar.divider()
if file:
    if mode == "Image Mode (High Quality)":
        with st.spinner("Processing using Image Mode...") :
          processing_image(file, page_selection_mode, selected_page,num_questions,difficulty)
    elif  mode ==  "Text Mode (Fast)" :
       with st.spinner("Processing using Text Mode..."):
         processing_text(file, page_selection_mode, selected_page,num_questions,difficulty)
    else :
      st.error("please select an mode from sidebar ")      

        







