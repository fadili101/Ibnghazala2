import streamlit as st
import pytesseract
from PIL import Image
import io
import base64

# Configure le chemin de Tesseract si nécessaire
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Capture d'image via Webcam et OCR avec PyTesseract")

# Widget HTML/JS pour capturer une image depuis la webcam
html_code = """
<script>
async function captureImage() {
    const video = document.createElement('video');
    video.style.display = 'none';
    document.body.appendChild(video);

    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    await video.play();

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    stream.getTracks().forEach(track => track.stop());
    document.body.removeChild(video);

    return dataUrl;
}

function sendToStreamlit() {
    captureImage().then(dataUrl => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'captured_image';
        input.value = dataUrl;
        document.forms[0].appendChild(input);
        document.forms[0].submit();
    });
}
</script>
<button onclick="sendToStreamlit()">Capture Image</button>
"""

# Intégration du HTML/JS dans Streamlit
captured_image = st.components.v1.html(html_code, height=100)

# Récupération de l'image capturée en base64
if "captured_image" in st.experimental_get_query_params():
    data_url = st.experimental_get_query_params()["captured_image"][0]
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    
    # Chargement de l'image dans PIL
    image = Image.open(io.BytesIO(image_data))
    st.image(image, caption="Image capturée", use_column_width=True)

    # Extraction de texte via PyTesseract
    extracted_text = pytesseract.image_to_string(image)
    st.subheader("Texte extrait :")
    st.text(extracted_text)
