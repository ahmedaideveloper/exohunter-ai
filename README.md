# 🌟 ExoHunter AI - Exoplanet Detection System

**Discover exoplanets using NASA data and machine learning!**

This system analyzes Kepler Object of Interest (KOI) data to classify astronomical objects as:
- **CONFIRMED** exoplanets
- **CANDIDATES** requiring further study  
- **FALSE POSITIVES** (not planets)

## Features
- 14 astronomical input parameters from Kepler mission data
- Random Forest machine learning classifier
- Real-time predictions with confidence scores
- Interactive web interface built with Gradio
- Pre-loaded example cases for testing

## How to Use
1. Enter values for the 14 astronomical parameters
2. Click "Submit" to get classification results
3. View detailed analysis with confidence percentages
4. Try the example inputs to see different classifications

## Technical Details
- **Model**: Random Forest Classifier (scikit-learn)
- **Accuracy**: ~44.5% on synthetic test data
- **Features**: 14 KOI parameters including orbital period, transit depth, stellar properties
- **Classes**: CONFIRMED, CANDIDATE, FALSE POSITIVE

## NASA Space Apps Challenge 2025
Created for the NASA Space Apps Challenge 2025 - Exoplanet Exploration track.

## License
MIT License