import streamlit as st
from PIL import Image
import os
from datetime import datetime
import tempfile
from barcode_detector import BarcodeDetector

# Configuration
st.set_page_config(
    page_title="OCR Barcode Detector",
    page_icon="📦",
    layout="wide"
)

# Initialize
@st.cache_resource
def load_detector():
    return BarcodeDetector()

detector = load_detector()

# Title
st.title("📦 OCR Barcode Detector")
st.markdown("---")

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Select Mode", ["Single Detection", "Batch Processing", "History"])

# Single Detection Mode
if mode == "Single Detection":
    st.header("Upload Image for Detection")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a barcode image",
            type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"]
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            st.caption(f"Size: {image.size[0]}x{image.size[1]} px")
    
    with col2:
        st.subheader("Results")
        
        if uploaded_file and st.button("🔍 Detect Barcode", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    # Save to temp
                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Detect
                    result = detector.extract_barcode(temp_path)
                    
                    # Save history
                    st.session_state.history.append({
                        'file': uploaded_file.name,
                        'time': datetime.now().strftime("%H:%M:%S"),
                        'result': result
                    })
                    
                    # Cleanup
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                    
                    # Show results
                    if result['success']:
                        st.success("✓ Barcode Found!")
                        st.code(f"b'{result['barcode_content']}'", language="python")
                        st.info(f"**Method:** {result['method'].upper()}")
                    else:
                        st.error("✗ No barcode detected")
                        st.warning(result['message'])
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Batch Mode
elif mode == "Batch Processing":
    st.header("Batch Process Images")
    
    uploaded_files = st.file_uploader(
        "Choose images",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process All", use_container_width=True):
        results = []
        temp_dir = tempfile.gettempdir()
        progress = st.progress(0)
        
        for idx, file in enumerate(uploaded_files):
            try:
                temp_path = os.path.join(temp_dir, file.name)
                
                with open(temp_path, 'wb') as f:
                    f.write(file.getbuffer())
                
                result = detector.extract_barcode(temp_path)
                
                results.append({
                    'filename': file.name,
                    'success': result['success'],
                    'barcode': result.get('barcode_content', 'N/A'),
                    'method': result.get('method', 'N/A')
                })
                
                try:
                    os.remove(temp_path)
                except:
                    pass
                
                progress.progress((idx + 1) / len(uploaded_files))
            
            except Exception as e:
                results.append({
                    'filename': file.name,
                    'success': False,
                    'barcode': 'ERROR',
                    'method': 'N/A'
                })
        
        # Summary
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(results))
        with col2:
            st.metric("Success", sum(1 for r in results if r['success']))
        with col3:
            st.metric("Failed", sum(1 for r in results if not r['success']))
        
        st.markdown("---")
        
        # Results
        for r in results:
            if r['success']:
                st.success(f"✓ {r['filename']}")
                st.code(f"b'{r['barcode']}'")
            else:
                st.error(f"✗ {r['filename']}")
            st.divider()
        
        # Download CSV
        csv = "filename,success,barcode,method\n"
        for r in results:
            csv += f"{r['filename']},{r['success']},{r['barcode']},{r['method']}\n"
        
        st.download_button("Download CSV", csv, "results.csv", "text/csv")

# History Mode
elif mode == "History":
    st.header("Detection History")
    
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            r = item['result']
            if r['success']:
                st.write(f"✓ {item['file']} - `b'{r['barcode_content']}'` ({item['time']})")
            else:
                st.write(f"✗ {item['file']} ({item['time']})")
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No history yet")

st.markdown("---")
st.caption("OCR Barcode Detector | Powered by PyZbar & EasyOCR")
