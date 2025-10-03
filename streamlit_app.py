import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import time

# Page configuration
st.set_page_config(
    page_title="ExoHunter AI - Exoplanet Detection",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
CURRENT_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(CURRENT_DIR, 'simple_model.pkl')
SCALER_PATH = os.path.join(CURRENT_DIR, 'scaler.pkl')
LABEL_ENCODER_PATH = os.path.join(CURRENT_DIR, 'label_encoder.pkl')

# Load Models and Scaler
@st.cache_resource
def load_models():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        with open(LABEL_ENCODER_PATH, 'rb') as f:
            label_encoder = pickle.load(f)
        return model, scaler, label_encoder, True
    except Exception as e:
        st.error(f"Error loading ML components: {e}")
        return None, None, None, False

model, scaler, label_encoder, models_loaded = load_models()

feature_columns = [
    'koi_period', 'koi_period_err1', 'koi_time0bk', 'koi_time0bk_err1',
    'koi_impact', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
    'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad'
]

# Mapping display names to actual column names
FEATURE_DISPLAY_MAP = {
    "Orbital Period (days)": "koi_period",
    "Orbital Period Error (days)": "koi_period_err1",
    "Transit Epoch (BJD)": "koi_time0bk",
    "Transit Epoch Error (BJD)": "koi_time0bk_err1",
    "Impact Parameter": "koi_impact",
    "Transit Duration (hours)": "koi_duration",
    "Transit Depth (ppm)": "koi_depth",
    "Planet Radius (Earth radii)": "koi_prad",
    "Equilibrium Temperature (K)": "koi_teq",
    "Insolation Flux (Earth flux)": "koi_insol",
    "Model SNR": "koi_model_snr",
    "Stellar Effective Temp (K)": "koi_steff",
    "Stellar Surface Gravity (log10(cm/s^2))": "koi_slogg",
    "Stellar Radius (Solar radii)": "koi_srad",
}

# Default values for inputs
DEFAULT_FEATURE_VALUES = {
    "koi_period": 50.0,
    "koi_period_err1": 0.1,
    "koi_time0bk": 130.0,
    "koi_time0bk_err1": 0.01,
    "koi_impact": 0.5,
    "koi_duration": 5.0,
    "koi_depth": 200.0,
    "koi_prad": 3.0,
    "koi_teq": 300.0,
    "koi_insol": 1.5,
    "koi_model_snr": 30.0,
    "koi_steff": 5500.0,
    "koi_slogg": 4.5,
    "koi_srad": 1.0,
}

def predict_exoplanet(input_values):
    """Main prediction function"""
    start_time = time.time()
    
    if not models_loaded:
        return "❌ Error: ML components not loaded. Please check if model files are present.", None
    
    try:
        # Create feature vector from inputs
        input_data = np.array(input_values).reshape(1, -1)
        
        # Scale the input data
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        
        # Get class names
        classes = label_encoder.classes_
        predicted_class = classes[prediction]
        
        processing_time = (time.time() - start_time) * 1000
        
        return predicted_class, prediction_proba, processing_time, classes
        
    except Exception as e:
        return f"❌ Error during prediction: {str(e)}", None

# Main App
def main():
    # Header
    st.title("🌟 ExoHunter AI - Exoplanet Detection System")
    st.markdown("**Discover exoplanets using NASA data and machine learning!**")
    
    # Info about the system
    with st.expander("ℹ️ About This System", expanded=False):
        st.markdown("""
        This system analyzes **Kepler Object of Interest (KOI)** data to classify astronomical objects as:
        - 🌍 **CONFIRMED** exoplanets
        - 🔍 **CANDIDATES** requiring further study  
        - ❌ **FALSE POSITIVES** (not planets)
        
        **Built for NASA Space Apps Challenge 2025**
        - **Model**: Random Forest Classifier (scikit-learn)
        - **Features**: 14 astronomical parameters from Kepler mission
        - **Accuracy**: ~44.5% on synthetic test data
        """)
    
    # Sidebar for inputs
    st.sidebar.header("🔧 Input Parameters")
    
    # Model status
    if models_loaded:
        st.sidebar.success("✅ Model loaded successfully!")
    else:
        st.sidebar.error("❌ Model not loaded")
        st.error("Please ensure model files (simple_model.pkl, scaler.pkl, label_encoder.pkl) are present.")
        return
    
    # Example presets
    st.sidebar.subheader("📋 Quick Examples")
    example_choice = st.sidebar.selectbox(
        "Choose an example:",
        ["Custom Values", "Likely Confirmed Exoplanet", "Likely Candidate", "Likely False Positive"]
    )
    
    # Example values
    examples = {
        "Likely Confirmed Exoplanet": [365.0, 0.1, 131.0, 0.01, 0.3, 6.0, 500.0, 1.2, 288.0, 1.0, 50.0, 5778.0, 4.44, 1.0],
        "Likely Candidate": [100.0, 0.2, 130.5, 0.02, 0.7, 4.0, 150.0, 2.5, 350.0, 2.0, 25.0, 6000.0, 4.2, 1.1],
        "Likely False Positive": [10.0, 1.0, 129.0, 0.1, 1.2, 1.0, 50.0, 0.5, 800.0, 10.0, 5.0, 4500.0, 4.8, 0.8]
    }
    
    # Create input fields
    input_values = []
    
    st.sidebar.subheader("🌌 Astronomical Parameters")
    
    for i, col in enumerate(feature_columns):
        # Get display name
        display_name = None
        for display, actual in FEATURE_DISPLAY_MAP.items():
            if actual == col:
                display_name = display
                break
        
        if display_name is None:
            display_name = col.replace('_', ' ').title()
        
        # Get default value
        if example_choice != "Custom Values" and example_choice in examples:
            default_value = examples[example_choice][i]
        else:
            default_value = DEFAULT_FEATURE_VALUES.get(col, 0.0)
        
        # Create input field
        value = st.sidebar.number_input(
            display_name,
            value=float(default_value),
            format="%.4f",
            key=f"input_{col}"
        )
        input_values.append(value)
    
    # Prediction button
    if st.sidebar.button("🚀 Classify Exoplanet", type="primary"):
        if models_loaded:
            # Make prediction
            result = predict_exoplanet(input_values)
            
            if len(result) == 4:  # Successful prediction
                predicted_class, prediction_proba, processing_time, classes = result
                
                # Main results display
                st.header("🎯 Classification Results")
                
                # Status with color coding
                if predicted_class == 'CONFIRMED':
                    st.success(f"🌍 **CONFIRMED EXOPLANET**")
                elif predicted_class == 'CANDIDATE':
                    st.warning(f"🔍 **PLANETARY CANDIDATE**")
                else:
                    st.error(f"❌ **FALSE POSITIVE**")
                
                # Processing time
                st.info(f"⚡ Processing Time: {processing_time:.2f} ms")
                
                # Confidence scores
                st.subheader("📊 Confidence Scores")
                
                # Create columns for confidence display
                cols = st.columns(3)
                for i, cls in enumerate(classes):
                    confidence = prediction_proba[i] * 100
                    with cols[i]:
                        if cls == predicted_class:
                            st.metric(
                                label=f"🎯 {cls}",
                                value=f"{confidence:.1f}%",
                                delta="PREDICTED"
                            )
                        else:
                            st.metric(
                                label=cls,
                                value=f"{confidence:.1f}%"
                            )
                
                # Input parameters summary
                st.subheader("📈 Input Parameters Used")
                
                # Create a nice table of input parameters
                param_data = []
                for i, (display_name, col_name) in enumerate(FEATURE_DISPLAY_MAP.items()):
                    param_data.append({
                        "Parameter": display_name,
                        "Value": f"{input_values[i]:.4f}"
                    })
                
                df_params = pd.DataFrame(param_data)
                st.dataframe(df_params, use_container_width=True)
                
                # Additional info
                st.subheader("ℹ️ About This Classification")
                if predicted_class == 'CONFIRMED':
                    st.info("**CONFIRMED** means this object shows strong evidence of being a genuine exoplanet based on the input parameters.")
                elif predicted_class == 'CANDIDATE':
                    st.info("**CANDIDATE** means this object shows some exoplanet characteristics but requires further investigation for confirmation.")
                else:
                    st.info("**FALSE POSITIVE** means this object is likely not an exoplanet - it could be a binary star system, data artifact, or other astrophysical phenomenon.")
                
            else:
                # Error occurred
                st.error(result)
        else:
            st.error("❌ Models not loaded. Cannot make predictions.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    🌟 <strong>ExoHunter AI</strong> - Built for NASA Space Apps Challenge 2025<br>
    Using Random Forest machine learning to classify Kepler exoplanet candidates
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()