import streamlit as st
from thefuzz import fuzz
from thefuzz import process

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบตรวจสอบชื่อคล้าย", layout="wide")
st.title("🔍 เครื่องมือเทียบชื่อ (Name Matching Tool)")
st.write("เปรียบเทียบรายชื่อจากสองช่องทางเพื่อหาข้อมูลที่ใกล้เคียงกัน")

# 2. ส่วนการกรอกข้อมูล
col1, col2 = st.columns(2)

with col1:
    st.subheader("ช่องทาง A (รายชื่อตั้งต้น)")
    input_a = st.text_area("ใส่รายชื่อ A (1 ชื่อต่อ 1 บรรทัด)", height=200)

with col2:
    st.subheader("ช่องทาง B (รายชื่อที่ต้องการตรวจสอบ)")
    input_b = st.text_area("ใส่รายชื่อ B (1 ชื่อต่อ 1 บรรทัด)", height=200)

# 3. ส่วนการประมวลผล
threshold = st.slider("ระดับความคล้ายที่ต้องการ (%)", 0, 100, 80)

if st.button("เริ่มการตรวจสอบ"):
    list_a = [name.strip() for name in input_a.split('\n') if name.strip()]
    list_b = [name.strip() for name in input_b.split('\n') if name.strip()]
    
    if not list_a or not list_b:
        st.error("กรุณากรอกข้อมูลทั้งสองช่องทางครับ")
    else:
        results = []
        
        for name_b in list_b:
            # หาชื่อใน List A ที่คล้ายกับ name_b มากที่สุด
            match, score = process.extractOne(name_b, list_a, scorer=fuzz.token_sort_ratio)
            
            if score >= threshold:
                results.append({
                    "ชื่อจาก B": name_b,
                    "ชื่อที่คล้ายใน A": match,
                    "คะแนนความคล้าย (%)": score
                })
        
        # 4. แสดงผลลัพธ์
        if results:
            st.success(f"พบรายชื่อที่คล้ายกันทั้งหมด {len(results)} รายการ")
            st.table(results)
        else:
            st.warning("ไม่พบชื่อที่มีความคล้ายคลึงตามเกณฑ์ที่กำหนด")