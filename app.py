import streamlit as st
import os
import pandas as pd

st.title("學生繳費表單")

with st.form(key='payment_form'):
    student_name = st.text_input("學生姓名", value="", max_chars=50)
    payment_date = st.date_input("繳費日期")
    payment_screenshot = st.file_uploader("上傳繳費截圖", type=["jpg", "jpeg", "png"])
    education_level = st.selectbox("學生學程度", ["國小", "國中", "高中"])
    purchase_options = st.multiselect("選擇購買方案", ["A", "B", "C"])
    
    submit_button = st.form_submit_button(label='提交')

if submit_button:
    if not student_name:
        st.error("學生姓名為必填項目")
    elif not payment_screenshot:
        st.error("繳費截圖為必填項目")
    elif not purchase_options:
        st.error("購買方案為必選項目")
    else:
        # Create directory for the student
        student_dir = os.path.join("data", student_name)
        os.makedirs(student_dir, exist_ok=True)
        
        # Save the uploaded image
        image_path = os.path.join(student_dir, payment_screenshot.name)
        with open(image_path, "wb") as f:
            f.write(payment_screenshot.getbuffer())
        
        # Save the form data to an Excel file
        data = {
            "學生姓名": [student_name],
            "繳費日期": [payment_date],
            "學生學程度": [education_level],
            "選擇購買方案": [', '.join(purchase_options)]
        }
        df = pd.DataFrame(data)
        excel_path = os.path.join(student_dir, "form_data.xlsx")
        df.to_excel(excel_path, index=False)
        
        st.success("表單提交成功")
        st.write(f"學生姓名: {student_name}")
        st.write(f"繳費日期: {payment_date}")
        st.image(payment_screenshot, caption='繳費截圖', use_column_width=True)
        st.write(f"學生學程度: {education_level}")
        st.write(f"選擇購買方案: {', '.join(purchase_options)}")

