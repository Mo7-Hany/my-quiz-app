import fitz
import streamlit as st 
from google import genai
import json
from google.genai import types 
import random

def processing_image(file,mode_selection, manual_page_num):
    api_key =st.secrets["GEMINI_API_KEY"]# 1. إعداد العميل (تأكد من استخدام مفتاحك الصحيح)
    client = genai.Client(api_key=api_key)

    if file is not None:
        # قراءة الملف وتحويله لصور (كما في كودك)
        file_bytes = file.read()
        file.seek(0)
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
          total_pages = len(pdf)
        
        # 1. حدد الصفحة المطلوبة أولاً
          if mode_selection == "صفحة عشوائية 🎲":
            target = random.randint(0, total_pages - 1)
          elif mode_selection == "صفحة محددة يدويًا":
            target = min(manual_page_num, total_pages) - 1
          else:
            target = 0
            
        # 2. الآن استخرج "كائن الصفحة" ثم حوله لصور (هنا الحل)
          page_obj = pdf[target] 
          pix = page_obj.get_pixmap(matrix=fitz.Matrix(2, 2))
          image_bytes = pix.tobytes("png")
        
          st.info(f"📸 جاري معالجة الصفحة رقم {target + 1}")
    my_prompt = f"""
أنت مدرس خبير ومبرمج متخصص في معالجة البيانات.
المهمة: استخرج {num_questions} أسئلة اختيار من متعدد (MCQ) بناءً على النص الموجود في الصورة المرفقة.

الشروط الصارمة:
1. الرد يجب أن يكون بصيغة (Strict JSON) فقط.
2. لا تكتب أي مقدمات أو خاتمة (مثل: "تفضل الأسئلة").
3. تأكد أن كل سؤال له 4 خيارات، وخيار واحد صحيح فقط.
4. الإجابة الصحيحة (answer) يجب أن تكون مطابقة تماماً لواحد من الخيارات الأربعة.
5.مستوى صعوبة الاسئلة {difficulty}
5. استخدم التنسيق التالي تماماً:

[
  {{
    "question": "نص السؤال هنا",
    "options": ["اختيار 1", "اختيار 2", "اختيار 3", "اختيار 4"],
    "answer": "الاختيار الصحيح (يجب أن يكون مطابقاً تماماً لواحد من الخيارات)"
  }}
]

استخرج هذه الأسئلة باللغة العربية من الصورة المرفقة.
"""

        
        
    if "quiz_data1" not in st.session_state:
            with st.spinner("جاري توليد الأسئلة من جيميني..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", 
                    contents=[
                        my_prompt,
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ],
                    config={"response_mime_type": "application/json"}
                )
                # تخزين الأسئلة في الذاكرة للأبد
                st.session_state["quiz_data1"] = json.loads(response.text)

        # ---------------------------------------------------------
        # عرض الفورم (باستخدام اسم فريد لتجنب الـ Duplicate Error)
        # ---------------------------------------------------------
    with st.form("final_quiz_form"):
            st.write("### 📝 Solve the Quiz")
            
            # بنعرض من الذاكرة المحفوظة
            for i, word in enumerate(st.session_state["quiz_data1"]):
                st.write(f"**Q{i+1}:** {word['question']}")
                # استخدام مفتاح فريد لكل سؤال هو اللي بيحفظ الإجابة
                st.selectbox(
                    "Choose the correct answer:", 
                    word["options"], 
                    index=None, 
                    key=f"user_q_{i}" # مفتاح فريد لكل سؤال
                )
            
            # ار الإرسال داخل الفورم بمحاذاة اللو
            submitted = st.form_submit_button("Submit My Answers")

        
    
    if submitted:
            actual_score = 0
            for i, word in enumerate(st.session_state["quiz_data1"]):
                #  الإجابة من الدرج الخاص بيها باستخدام الـ key
                student_answer = st.session_state.get(f"user_q_{i}")
                if student_answer == word["answer"]:
                    actual_score += 1
            st.success(f"Excellent! Your score is {actual_score} / {len(st.session_state['quiz_data1'])}")
            if actual_score == 5:
              st.balloons()
              st.success("عبقري! إجابة كاملة 🌟")
            elif actual_score >= 5 / 2:
              st.success("أداء جيد جداً! 👍")
            else:
              st.warning("محاولة جيدة، حاول مرة أخرى لتحسين درجتك. 💪")








