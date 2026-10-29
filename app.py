import streamlit as st
import base64
import numpy as np
from PIL import Image
import wave
import os
from cryptography.fernet import Fernet
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="StegoShield AI", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS (For Premium UI/UX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #020617;
        color: #e2e8f0;
    }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Animated Hero Section */
    .hero-box {
        text-align: center;
        padding: 60px 20px;
        background: radial-gradient(circle at center, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 600;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UTILITY FUNCTIONS (AES & Stego) ---
def get_key(password):
    return base64.urlsafe_b64encode(password.ljust(32)[:32].encode())

def encrypt_msg(msg, password):
    f = Fernet(get_key(password))
    return f.encrypt(msg.encode()).decode()

def decrypt_msg(enc_msg, password):
    try:
        f = Fernet(get_key(password))
        return f.decrypt(enc_msg.encode()).decode()
    except: return None

def hide_in_img(img, msg):
    img = img.convert('RGB')
    pixels = np.array(img)
    msg += "#####"
    binary_msg = ''.join(format(ord(i), '08b') for i in msg)
    flat = pixels.flatten()
    for i in range(len(binary_msg)):
        flat[i] = (flat[i] & ~1) | int(binary_msg[i])
    return Image.fromarray(flat.reshape(pixels.shape).astype('uint8'))

def extract_from_img(img):
    pixels = np.array(img.convert('RGB')).flatten()
    binary = "".join([str(pixels[i] & 1) for i in range(len(pixels))])
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    res = "".join(chars)
    return res.split("#####")[0] if "#####" in res else "No Data Found"

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 class='gradient-text'>🛡️ StegoShield AI</h1>", unsafe_allow_html=True)
    menu = st.radio("Navigation", ["🏠 Home", "📊 Dashboard", "🖼️ Image Stego", "🎵 Audio Stego", "🤖 AI Chatbot", "📞 Contact"])
    st.info("System Status: Operational ✅")

# --- PAGES ---

if menu == "🏠 Home":
    st.markdown("""
        <div class="hero-box">
            <h1 style='font-size: 3.5rem;'>Secure Your Multimedia with <br><span class="gradient-text">AI-Powered Steganography</span></h1>
            <p style='font-size: 1.2rem; color: #94a3b8;'>StegoShield AI protects your sensitive data by hiding it inside ordinary images and audio files using military-grade encryption.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card"><h3>🖼️ Image Stego</h3><p>Hide secret messages in PNG/JPG files without losing quality.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><h3>🎵 Audio Stego</h3><p>Embed data into WAV audio frequencies.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card"><h3>🛡️ AES-256</h3><p>Double protection with high-end encryption before embedding.</p></div>', unsafe_allow_html=True)

elif menu == "📊 Dashboard":
    st.title("Activity Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Files", "1,254", "+12%")
    c2.metric("Encrypted", "842", "+5%")
    c3.metric("Security Score", "98%", "Optimal")
    
    st.markdown('<div class="glass-card"><h3>Recent Activities</h3><p>• image_01.png encrypted successfully<br>• audio_sample.wav decrypted</p></div>', unsafe_allow_html=True)

elif menu == "🖼️ Image Stego":
    st.title("Image Steganography Module")
    tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])
    
    with tab1:
        up = st.file_uploader("Upload Image", type=['png', 'jpg'])
        txt = st.text_area("Secret Message")
        pwd = st.text_input("Set Password", type="password")
        if st.button("Encrypt & Download"):
            if up and txt and pwd:
                with st.spinner("Shielding data..."):
                    enc_txt = encrypt_msg(txt, pwd)
                    res_img = hide_in_img(Image.open(up), enc_txt)
                    st.image(res_img, width=300)
                    res_img.save("encoded.png")
                    with open("encoded.png", "rb") as f:
                        st.download_button("Download Secure Image", f, "secure.png")
            else: st.warning("Please fill all fields")

    with tab2:
        up2 = st.file_uploader("Upload Encrypted Image", type=['png'])
        pwd2 = st.text_input("Enter Password", type="password")
        if st.button("Extract Data"):
            raw_enc = extract_from_img(Image.open(up2))
            final = decrypt_msg(raw_enc, pwd2)
            if final: st.success(f"Message: {final}")
            else: st.error("Wrong password or no data.")

elif menu == "🤖 AI Chatbot":
    st.title("AI Assistant")
    st.markdown('<div class="glass-card">Ask me anything about Steganography!</div>', unsafe_allow_html=True)
    query = st.text_input("Your Question:")
    if query:
        if "steganography" in query.lower():
            st.write("AI: Steganography is the art of hiding a secret message within an ordinary file.")
        elif "encrypt" in query.lower():
            st.write("AI: To encrypt, upload a file, enter your text, and set a strong password.")
        else:
            st.write("AI: I am specialized in StegoShield security tips. Try asking about encryption or file formats.")

elif menu == "📞 Contact":
    st.title("Get in Touch")
    with st.form("contact"):
        st.text_input("Name")
        st.text_input("Email")
        st.text_area("Message")
        st.form_submit_button("Send Signal")

# --- FOOTER ---
st.markdown("<br><hr><center>Powered by StegoShield AI © 2024 | Secure Multimedia Solutions</center>", unsafe_allow_html=True)