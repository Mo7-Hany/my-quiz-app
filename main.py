import streamlit as st
import fitz
import pdfplumber  
import json
from google import genai
from google.genai import types
from image_mode import processing_image
from text_mode import processing_text 

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
        [None,"كل الصفحات (Text Mode فقط)", "صفحة محددة يدويًا", "صفحة عشوائية 🎲"]
    )

    if page_selection_mode == "صفحة محددة يدويًا":
        # سنفترض أننا سنعرف عدد الصفحات داخل الدوال، لكن مبدئياً نضع رقماً
        selected_page = st.sidebar.number_input("أدخل رقم الصفحة:", min_value=1, value=1)
    
    st.sidebar.divider()
if file:
    if mode == "Image Mode (High Quality)":
        with st.spinner("Processing using Image Mode...") :
          processing_image(file, page_selection_mode, selected_page)
    elif  mode ==  "Text Mode (Fast)" :
       with st.spinner("Processing using Text Mode..."):
         processing_text(file, page_selection_mode, selected_page)
    else :
      st.write("please select an mode from sidebar ")      
        