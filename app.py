
import streamlit as st
from datetime import date
import io, os, base64
from report_generator import generate_pdf

st.set_page_config(page_title="Sistem OPR – Auto Generate One Page Report", layout="wide")

st.title("📝 Sistem OPR – Auto Generate One Page Report")
st.caption("Isi maklumat program, upload gambar, dan jana PDF satu muka surat secara automatik.")

# Sidebar: logo default
with st.sidebar:
    st.header("⚙️ Tetapan")
    logo_file = st.file_uploader("Logo Sekolah (pilihan)", type=["png","jpg","jpeg"])
    st.markdown("---")
    st.write("Tip: Simpan logo agar digunakan sebagai default untuk setiap laporan.")

with st.form("opr_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Tajuk Program *")
        date_val = st.date_input("Tarikh", value=date.today())
        time_val = st.text_input("Masa", placeholder="cth: 8.00 pagi – 12.30 tengah hari")
        venue = st.text_input("Tempat")
        organiser = st.text_input("Anjuran / Penganjur")
    with col2:
        target = st.text_input("Sasaran / Peserta (contoh: Tahun 4-6, 120 murid)")
        colA, colB, colC = st.columns(3)
        with colA:
            att_students = st.number_input("Bil. Murid", min_value=0, step=1, value=0)
        with colB:
            att_teachers = st.number_input("Bil. Guru", min_value=0, step=1, value=0)
        with colC:
            att_parents = st.number_input("Bil. Ibu Bapa", min_value=0, step=1, value=0)
        prepared_by = st.text_input("Disediakan oleh (Nama) *")
        position = st.text_input("Jawatan (cth: Guru Pusat Sumber)")

    objectives = st.text_area("Objektif Program", height=80, placeholder="• Objektif 1\n• Objektif 2")
    activities = st.text_area("Ringkasan Aktiviti / Atur Cara", height=100, placeholder="Nyatakan aktiviti utama / atur cara ringkas")
    outcomes = st.text_area("Pencapaian / Impak", height=80, placeholder="Hasil / impak kepada murid, bukti pencapaian, dll.")
    recommendations = st.text_area("Cadangan / Penambahbaikan", height=80, placeholder="Saranan untuk sesi akan datang")

    images = st.file_uploader("Muat naik gambar program (hingga 3 keping)", type=["png","jpg","jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("🚀 Generate Report PDF", use_container_width=True)

if submitted:
    # Save uploaded assets temporarily
    logo_path = None
    if logo_file is not None:
        logo_path = os.path.join("tmp_logo_" + logo_file.name)
        with open(logo_path, "wb") as f:
            f.write(logo_file.read())

    image_paths = []
    if images:
        for i, img in enumerate(images[:3]):
            path = f"tmp_img_{i}_{img.name}"
            with open(path, "wb") as f:
                f.write(img.read())
            image_paths.append(path)

    data = {
        "title": title.strip() if title else "",
        "date": date_val.strftime("%d %B %Y") if date_val else "",
        "time": time_val,
        "venue": venue,
        "organiser": organiser,
        "target": target,
        "attendance": {"students": att_students, "teachers": att_teachers, "parents": att_parents},
        "objectives": objectives,
        "activities": activities,
        "outcomes": outcomes,
        "recommendations": recommendations,
        "prepared_by": prepared_by,
        "position": position,
        "report_date": date.today().strftime("%d %B %Y"),
        "logo_path": logo_path,
        "image_paths": image_paths,
    }

    # Basic validation
    missing = []
    if not data["title"]: missing.append("Tajuk Program")
    if not data["prepared_by"]: missing.append("Disediakan oleh")
    if missing:
        st.error("Sila lengkapkan medan wajib: " + ", ".join(missing))
    else:
        buffer = io.BytesIO()
        pdf_bytes = generate_pdf(buffer, data)
        st.success("Laporan berjaya dijana!")

        # Download button
        st.download_button(
            label="⬇️ Muat turun PDF",
            data=pdf_bytes.getvalue(),
            file_name=f"OPR_{data['title'].replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        # Preview PDF as iframe
        b64 = base64.b64encode(pdf_bytes.getvalue()).decode()
        pdf_iframe = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="680" type="application/pdf"></iframe>'
        st.markdown(pdf_iframe, unsafe_allow_html=True)

    # Cleanup temp files
    try:
        if logo_path and os.path.exists(logo_path):
            os.remove(logo_path)
        for p in image_paths:
            if os.path.exists(p):
                os.remove(p)
    except Exception:
        pass

st.markdown("---")
st.caption("© Sistem OPR Prototype – dibina dengan Streamlit + ReportLab")
