import streamlit as st        
import pdfplumber
import re 
import json
from google import genai
from google.genai import types 
import random   
pattern = r"[ـ&^#ـ]"  

def clean (text) :
      global pattern    
      return(re.sub(pattern,"",text)) 

def processing_text (file, mode_selection, manual_page_num,num_questions,difficulty):
      
      client = genai.Client(api_key=api_key)
      all_text = ""      
      if file is not None :
         with pdfplumber.open(file) as pdf:
          total_pages = len(pdf.pages)
        
        # منطق اختيار النص بناءً على طلبك
          if mode_selection == "صفحة عشوائية":
            target = random.randint(0, total_pages - 1)
            pages_to_process = [pdf.pages[target]]
            st.info(f"تم اختيار الصفحة رقم {target + 1} عشوائياً")
          elif mode_selection == "صفحة محددة يدويًا":
            target = min(manual_page_num, total_pages) - 1
            pages_to_process = [pdf.pages[target]]
            st.info(f"يتم الآن معالجة الصفحة رقم {target + 1}")
          else:
            pages_to_process = pdf.pages # كل الصفحات
            st.info("يتم معالجة المستند بالكامل...")
         

         my_prompt = f"""أنت مدرس خبير ومبرمج متخصص في معالجة البيانات. 
المهمة: استخرج {num_questions} أسئلة اختيار من متعدد (MCQ) بناءً على النص الموجود بين العلامات التاليه [START] و [END].
مستوى صعوبة الاسئلة {difficulty}
الشروط الصارمة:
1. يجب أن يكون الرد بصيغة JSON نقي فقط (Strict JSON).
2. لا تكتب أي مقدمات أو خاتمة (مثل: "تفضل الأسئلة").
3. تأكد أن كل سؤال له 4 خيارات، وخيار واحد صحيح.
4. استخدم التنسيق التالي تماماً:
[
  {{
    "question": "نص السؤال هنا",
    "options": ["اختيار 1", "اختيار 2", "اختيار 3", "اختيار 4"],
    "answer": "الاختيار الصحيح (يجب أن يكون مطابقاً تماماً لواحد من الخيارات)"
  }}
]

النص المراد تحليله:
{all_text}
"""
        
         if "quiz_data1" not in st.session_state:
            with st.spinner("جاري توليد الأسئلة من جيميني..."):
              try :
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", 
                    contents=[
                        my_prompt,
                        
                    ],
                    config={"response_mime_type": "application/json"}
                )
              except:
                st.error("تأكد من اتصالك بالانترنت ")   
              try :  
                st.session_state["quiz_data1"] = json.loads(response.text)
              except:
                 st.error("يبدوا ان الاسئلة لم تكن صحيحة حاول مرة اخرى")   

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
            if actual_score == len((st.session_state["quiz_data1"])):
              st.balloons()
              st.success("عبقري! إجابة كاملة 🌟")
            elif actual_score >= len((st.session_state["quiz_data1"])) / 2:
              st.success("أداء جيد جداً! 👍")
            else:
              st.warning("محاولة جيدة، حاول مرة أخرى لتحسين درجتك. 💪")











