import streamlit as st
from PIL import Image
import os
import sys
import io
from datetime import datetime
import tempfile
import csv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ocr_engine import BarcodeDetector

# Page configuration
st.set_page_config(
    page_title="OCR Barcode Detector",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 16px;
            font-weight: bold;
        }
        .success-box {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .error-box {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .info-box {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detector' not in st.session_state:
    st.session_state.detector = BarcodeDetector()

if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

if 'current_image' not in st.session_state:
    st.session_state.current_image = None

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

if 'current_filename' not in st.session_state:
    st.session_state.current_filename = None


# Header
st.markdown("# 📦 OCR Barcode Detector")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    page = st.radio(
        "Select Mode:",
        ["🔍 Detect Barcode", "📊 Batch Processing", "📜 History"]
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.info("""
    **OCR Barcode Detector v1.0**
    
    A powerful tool for detecting and extracting barcode contents from images using multiple OCR methods.
    
    **Detection Methods:**
    - PyZbar (Direct barcode decoding)
    - Morphology + EasyOCR (Complex barcodes)
    - EasyOCR (General OCR fallback)
    
    **Supported Formats:**
    - JPG, PNG, BMP, GIF, TIFF
    """)


# Main Content
if page == "🔍 Detect Barcode":
    st.markdown("### Upload or Capture Barcode Image")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("#### Input Source")
        input_mode = st.radio(
            "Choose input",
            ["Upload image", "Camera capture"],
            horizontal=True,
            key="input_mode"
        )
        uploaded_file = None
        camera_photo = None
        if input_mode == "Upload image":
            uploaded_file = st.file_uploader(
                "Choose a barcode image",
                type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
                help="Upload an image containing a barcode"
            )
            source = uploaded_file
        else:
            camera_photo = st.camera_input(
                "Capture barcode",
                help="Use your webcam to scan a barcode"
            )
            source = camera_photo
        
        if source is not None:
            # Handle both uploaded files and camera images
            image_bytes = source.getvalue()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            st.session_state.current_image = image
            st.session_state.current_filename = getattr(source, "name", "captured_barcode.png")
            
            st.image(image, caption="Input Image", use_column_width=True)
            
            img_width, img_height = image.size
            st.caption(f"Resolution: {img_width}x{img_height} px")
    
    with col2:
        st.markdown("### Detection Results")
        
        if st.session_state.current_image is not None:
            if st.button("🔍 Detect Barcode", key="detect_btn", use_container_width=True):
                with st.spinner("🔄 Processing image... Please wait"):
                    try:
                        temp_dir = tempfile.gettempdir()
                        filename = st.session_state.current_filename or "barcode_input.png"
                        image_path = os.path.join(temp_dir, filename)
                        st.session_state.current_image.save(image_path)
                        
                        result = st.session_state.detector.extract_barcode(image_path)
                        st.session_state.current_result = result
                        
                        history_entry = {
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'filename': filename,
                            'result': result
                        }
                        st.session_state.detection_history.append(history_entry)
                        
                        try:
                            if os.path.exists(image_path):
                                os.remove(image_path)
                        except:
                            pass
                    
                    except Exception as e:
                        st.error(f"Error during detection: {str(e)}")
        
        if st.session_state.current_result is not None:
            result = st.session_state.current_result
            
            st.markdown("---")
            
            if result['success']:
                st.markdown(f"""
                <div class="success-box">
                    <h4>✓ Barcode Detected!</h4>
                    <p><strong>Content:</strong> <code>b'{result['barcode_content']}'</code></p>
                    <p><strong>Method:</strong> {result['method'].upper()}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Copy button
                st.code(f"b'{result['barcode_content']}'", language="python")
                
                # Full output
                with st.expander("📋 Full Output"):
                    st.write(result['message'])
            else:
                st.markdown(f"""
                <div class="error-box">
                    <h4>✗ No Barcode Detected</h4>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <p>📤 <strong>Upload an image</strong> to get started</p>
            </div>
            """, unsafe_allow_html=True)


elif page == "📊 Batch Processing":
    st.markdown("### Batch Process Multiple Images")
    
    st.info("""
    Upload multiple barcode images to process them in batch.
    Results will be displayed and can be downloaded as a summary.
    """)
    
    uploaded_files = st.file_uploader(
        "Choose barcode images",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
        accept_multiple_files=True,
        help="Upload multiple images for batch processing"
    )
    
    if uploaded_files:
        if st.button("🔍 Process All Images", use_container_width=True):
            with st.spinner(f"⏳ Processing {len(uploaded_files)} images..."):
                results = []
                progress_bar = st.progress(0)
                temp_dir = tempfile.gettempdir()
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Save temporary image
                        image_path = os.path.join(temp_dir, uploaded_file.name)
                        image = Image.open(uploaded_file)
                        image.save(image_path)
                        
                        # Run detection
                        result = st.session_state.detector.extract_barcode(image_path)
                        
                        results.append({
                            'filename': uploaded_file.name,
                            'success': result['success'],
                            'barcode': result.get('barcode_content', 'N/A'),
                            'method': result.get('method', 'N/A'),
                            'message': result['message']
                        })
                        
                        # Clean up
                        try:
                            if os.path.exists(image_path):
                                os.remove(image_path)
                        except:
                            pass  # Ignore cleanup errors
                        
                        # Update progress
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    except Exception as e:
                        results.append({
                            'filename': uploaded_file.name,
                            'success': False,
                            'barcode': 'ERROR',
                            'method': 'N/A',
                            'message': str(e)
                        })
                
                st.markdown("---")
                st.markdown("### Results Summary")
                
                # Statistics
                successful = sum(1 for r in results if r['success'])
                failed = len(results) - successful
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Images", len(results))
                with col2:
                    st.metric("Successful", successful, delta=f"+{successful}")
                with col3:
                    st.metric("Failed", failed, delta=f"-{failed}")
                
                st.markdown("---")
                
                # Results table
                st.markdown("### Detection Results")
                
                for result in results:
                    if result['success']:
                        status_icon = "✓"
                        status_color = "🟢"
                    else:
                        status_icon = "✗"
                        status_color = "🔴"
                    
                    st.write(f"{status_color} **{result['filename']}**")
                    if result['success']:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.code(f"b'{result['barcode']}'", language="python")
                        with col2:
                            st.caption(f"Method: {result['method']}")
                    else:
                        st.caption(f"Error: {result['message']}")
                    st.divider()
                
                # Download results
                csv_data = "filename,success,barcode,method\n"
                for result in results:
                    csv_data += f"{result['filename']},{result['success']},{result['barcode']},{result['method']}\n"
                
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_data,
                    file_name="barcode_results.csv",
                    mime="text/csv"
                )


elif page == "📜 History":
    st.markdown("### Detection History")
    
    if st.session_state.detection_history:
        st.info(f"Total detections: {len(st.session_state.detection_history)}")
        
        for idx, entry in enumerate(reversed(st.session_state.detection_history)):
            result = entry['result']
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if result['success']:
                    st.write(f"✓ **{entry['filename']}** → `b'{result['barcode_content']}'`")
                else:
                    st.write(f"✗ **{entry['filename']}** → No barcode detected")
            
            with col2:
                st.caption(entry['timestamp'])
            
            st.divider()
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.detection_history = []
            st.rerun()
    else:
        st.info("No detection history yet. Process some images to see them here.")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>OCR Barcode Detector v1.0 | Built with Streamlit</p>
    <p>Powered by PyZbar, EasyOCR, and OpenCV</p>
</div>
""", unsafe_allow_html=True)
