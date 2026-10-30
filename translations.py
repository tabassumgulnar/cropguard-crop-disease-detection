"""
CropGuard Centralized Trilingual Localization & Translation System
Supports English ('en'), Hindi ('hi'), and Marathi ('mr') across all pages,
widgets, forms, diagnostic cards, and epidemiological workflows.
Maintains state in st.session_state with seamless persistence across navigation.
"""

from typing import Dict, Any, Optional
try:
    import streamlit as st
except ImportError:
    st = None

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "mr": "मराठी (Marathi)",
}

# Master Trilingual UI Dictionary
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Navigation
    "nav_heading": {
        "en": "Navigation",
        "hi": "नेविगेशन",
        "mr": "नेव्हिगेशन",
    },
    "nav_home": {
        "en": "Home Dashboard",
        "hi": "मुख्य डैशबोर्ड",
        "mr": "मुख्य डॅशबोर्ड",
    },
    "nav_farmer": {
        "en": "Farmer Diagnostic Portal",
        "hi": "किसान निदान पोर्टल",
        "mr": "शेतकरी निदान पोर्टल",
    },
    "nav_officer": {
        "en": "Officer GIS Dashboard",
        "hi": "अधिकारी जीआईएस डैशबोर्ड",
        "mr": "अधिकारी जीआयएस डॅशबोर्ड",
    },
    "nav_advisory": {
        "en": "Trilingual IPM Catalog",
        "hi": "त्रैभाषीय आईपीएम कैटलॉग",
        "mr": "त्रिभाषिक आयपीएम मार्गदर्शिका",
    },
    "system_status": {
        "en": "System Status",
        "hi": "सिस्टम स्थिति",
        "mr": "प्रणाली स्थिती",
    },
    "vision_engine": {
        "en": "Vision Engine",
        "hi": "विजन इंजन",
        "mr": "व्हिजन इंजिन",
    },
    "db_operations": {
        "en": "Database Operations",
        "hi": "डेटाबेस संचालन",
        "mr": "डेटाबेस कृती",
    },
    "btn_seed_demo": {
        "en": "📥 Load Demo Data (~32 MH Reports)",
        "hi": "📥 डेमो डेटा लोड करें (32 रिपोर्ट)",
        "mr": "📥 डेमो डेटा भरा (३२ अहवाल)",
    },
    "btn_reset_db": {
        "en": "🗑️ Reset Database",
        "hi": "🗑️ डेटाबेस रीसेट करें",
        "mr": "🗑️ डेटाबेस रीसेट करा",
    },
    "btn_refresh": {
        "en": "🔄 Refresh Data",
        "hi": "🔄 डेटा ताज़ा करें",
        "mr": "🔄 माहिती रीफ्रेश करा",
    },
    "footer_credit": {
        "en": "CropGuard • Open-Source Agro-Informatics Platform",
        "hi": "क्रॉपगार्ड • ओपन-सोर्स कृषि-सूचना विज्ञान मंच",
        "mr": "क्रॉपगार्ड • मुक्त-स्रोत कृषी माहिती तंत्रज्ञान व्यासपीठ",
    },

    # Main Home Dashboard
    "home_tag": {
        "en": "Open-Source Agro-Informatics Platform",
        "hi": "ओपन-सोर्स कृषि-सूचना विज्ञान मंच",
        "mr": "मुक्त-स्रोत कृषी माहिती तंत्रज्ञान व्यासपीठ",
    },
    "home_title": {
        "en": "🌱 CropGuard: Early Crop Disease & Pest Detection",
        "hi": "🌱 क्रॉपगार्ड: फसल रोग एवं कीट प्रारंभिक पहचान",
        "mr": "🌱 क्रॉपगार्ड: पीक रोग व कीड त्वरित निदान",
    },
    "home_subtitle": {
        "en": "AI-Powered Plant Pathology, Open-Meteo Weather Epidemiology, and Trilingual Integrated Pest Management (IPM)",
        "hi": "एआई-संचालित पादप विकृति विज्ञान, ओपन-मेटियो मौसम महामारी विज्ञान और त्रैभाषीय एकीकृत कीट प्रबंधन (आईपीएम)",
        "mr": "एआय-आधारित वनस्पती रोगनिदान, ओपन-मेटिओ हवामान जोखीम विश्लेषण आणि त्रिभाषिक एकात्मिक कीड व्यवस्थापन (आयपीएम)",
    },
    "metrics_title": {
        "en": "Surveillance Database Metrics",
        "hi": "निगरानी डेटाबेस मेट्रिक्स",
        "mr": "सनियंत्रण डेटाबेस आकडेवारी",
    },
    "metrics_caption": {
        "en": "Live counts from local SQLite storage (cropguard.db). Reflects field entries and pre-seeded Maharashtra demo reports.",
        "hi": "स्थानीय SQLite स्टोरेज (cropguard.db) से लाइव रिकॉर्ड। इसमें फील्ड प्रविष्टियाँ और महाराष्ट्र डेमो डेटा शामिल हैं।",
        "mr": "स्थानिक SQLite साठवणुकीतील (cropguard.db) थेट आकडेवारी. यामध्ये प्रत्यक्ष नोंदी आणि महाराष्ट्र डेमो अहवाल समाविष्ट आहेत.",
    },
    "metric_total_reports": {
        "en": "Total Reports",
        "hi": "कुल रिपोर्ट",
        "mr": "एकूण अहवाल",
    },
    "metric_total_sub": {
        "en": "Stored in DB",
        "hi": "डेटाबेस में सुरक्षित",
        "mr": "डेटाबेसमध्ये साठवले",
    },
    "metric_pending": {
        "en": "Pending Review",
        "hi": "समीक्षा लंबित",
        "mr": "तपासणी प्रलंबित",
    },
    "metric_pending_sub": {
        "en": "Awaiting Officer",
        "hi": "अधिकारी समीक्षा प्रतीक्षित",
        "mr": "अधिकारी पडताळणी बाकी",
    },
    "metric_confirmed": {
        "en": "Confirmed Cases",
        "hi": "सत्यापित मामले",
        "mr": "प्रमाणित प्रकरणे",
    },
    "metric_confirmed_sub": {
        "en": "Officer Validated",
        "hi": "अधिकारी द्वारा प्रमाणित",
        "mr": "अधिकाऱ्यांनी प्रमाणित",
    },
    "metric_corrected": {
        "en": "Expert Corrected",
        "hi": "विशेषज्ञ द्वारा संशोधित",
        "mr": "तज्ज्ञांनी दुरुस्त केलेले",
    },
    "metric_corrected_sub": {
        "en": "Active Learning",
        "hi": "सक्रिय शिक्षण (डेटा)",
        "mr": "सक्रिय शिक्षण सुधारणा",
    },
    "metric_uncertain": {
        "en": "Uncertain (<60%)",
        "hi": "अनिश्चित (<६०%)",
        "mr": "अस्पष्ट (<६०%)",
    },
    "metric_uncertain_sub": {
        "en": "Safety Safeguard",
        "hi": "सुरक्षा प्रतिबंध",
        "mr": "सुरक्षा नियम लागू",
    },
    "core_modules_title": {
        "en": "CropGuard Core Modules",
        "hi": "क्रॉपगार्ड के मुख्य मॉड्यूल",
        "mr": "क्रॉपगार्डचे मुख्य विभाग",
    },
    "core_modules_caption": {
        "en": "Select a dedicated module to perform leaf diagnosis, monitor regional spatial outbreaks, or browse trilingual advisories.",
        "hi": "पत्ती रोग निदान, क्षेत्रीय प्रकोप निगरानी या त्रैभाषीय सलाह देखने के लिए उपयुक्त मॉड्यूल चुनें।",
        "mr": "पानावरील रोगनिदान, प्रादेशिक उद्रेक सनियंत्रण किंवा त्रिभाषिक सल्ला पाहण्यासाठी योग्य विभाग निवडा.",
    },
    "card_farmer_badge": {
        "en": "Farmer Diagnostic Edge",
        "hi": "किसान निदान सुविधा",
        "mr": "शेतकरी निदान कक्ष",
    },
    "card_farmer_title": {
        "en": "🌾 1. Farmer Diagnostic Portal",
        "hi": "🌾 १. किसान रोग निदान पोर्टल",
        "mr": "🌾 १. शेतकरी रोग निदान पोर्टल",
    },
    "card_farmer_desc": {
        "en": "Upload or take a photo of infected leaves for instant classification. Features top-3 probability distribution, live Open-Meteo weather risk alerts, and trilingual IPM recommendations.",
        "hi": "त्वरित वर्गीकरण के लिए प्रभावित पत्तियों की फोटो अपलोड करें या खींचें। शीर्ष-३ संभावना, लाइव मौसम जोखिम और एकीकृत कीट प्रबंधन (आईपीएम) मार्गदर्शन उपलब्ध।",
        "mr": "त्वरित निदानासाठी बाधित पानांचे छायाचित्र अपलोड करा किंवा कॅमेऱ्याने काढा. पहिल्या ३ संभाव्यता, थेट हवामान जोखीम आणि त्रिभाषिक आयपीएम सल्ला उपलब्ध.",
    },
    "card_farmer_btn": {
        "en": "Open Farmer Diagnostic Portal →",
        "hi": "किसान निदान पोर्टल खोलें →",
        "mr": "शेतकरी निदान पोर्टल उघडा →",
    },
    "card_officer_badge": {
        "en": "Surveillance & GIS",
        "hi": "निगरानी एवं जीआईएस",
        "mr": "सनियंत्रण आणि जीआयएस",
    },
    "card_officer_title": {
        "en": "🛡️ 2. Officer Surveillance Dashboard",
        "hi": "🛡️ २. अधिकारी निगरानी डैशबोर्ड",
        "mr": "🛡️ २. अधिकारी सनियंत्रण डॅशबोर्ड",
    },
    "card_officer_desc": {
        "en": "Interactive Folium GIS map with disease incidence pins, regional epidemic heatmaps across Maharashtra, disease frequency charts, and a human-in-the-loop audit tool to verify or correct diagnoses.",
        "hi": "महाराष्ट्र भर में रोग प्रकोप के लिए इंटरैक्टिव फोलियम जीआईएस मैप, हीटमैप, आवृत्ति चार्ट और निदान की पुष्टि या संशोधन के लिए विशेषज्ञ उपकरण।",
        "mr": "महाराष्ट्रभरातील रोग प्रसाराचा परस्परसंवादी फोलियम जीआयएस नकाशा, उष्णता नकाशा (हीटमॅप), वारंवारता आलेख आणि निदानाची पडताळणी किंवा दुरुस्ती करण्याचे साधन.",
    },
    "card_officer_btn": {
        "en": "Open Officer Surveillance Dashboard →",
        "hi": "अधिकारी निगरानी डैशबोर्ड खोलें →",
        "mr": "अधिकारी सनियंत्रण डॅशबोर्ड उघडा →",
    },
    "card_advisory_badge": {
        "en": "Knowledge Base",
        "hi": "कृषि ज्ञानकोश",
        "mr": "कृषी ज्ञानभांडार",
    },
    "card_advisory_title": {
        "en": "📚 3. Trilingual IPM Advisory Catalog",
        "hi": "📚 ३. त्रैभाषीय आईपीएम सलाह कैटलॉग",
        "mr": "📚 ३. त्रिभाषिक आयपीएम सल्ला मार्गदर्शिका",
    },
    "card_advisory_desc": {
        "en": "Searchable agricultural knowledge base covering 11 foliar pathogens in English, हिन्दी (Hindi), and मराठी (Marathi). Follows ICAR and KVK guidance prioritizing Cultural and Biological controls over chemicals.",
        "hi": "टमाटर, कपास और प्याज के ११ रोगों के लिए अंग्रेजी, हिन्दी और मराठी में खोज योग्य ज्ञानकोश। आईसीएआर और केवीके सिद्धांतों के अनुरूप जैविक व कृषि पद्धतियों को प्राथमिकता।",
        "mr": "टोमॅटो, कापूस आणि कांद्यावरील ११ रोगांसाठी इंग्रजी, हिंदी आणि मराठीत शोधता येणारी मार्गदर्शिका. आयसीएआर व केव्हीके शिफारशींनुसार सेंद्रिय व जैविक उपायांना प्राधान्य.",
    },
    "card_advisory_btn": {
        "en": "Browse Trilingual IPM Catalog →",
        "hi": "त्रैभाषीय आईपीएम कैटलॉग देखें →",
        "mr": "त्रिभाषिक आयपीएम मार्गदर्शिका पहा →",
    },

    # Farmer Diagnostic Portal
    "portal_banner_title": {
        "en": "🌾 Farmer Disease Diagnostic & IPM Advisory Portal",
        "hi": "🌾 किसान रोग निदान एवं एकीकृत कीट प्रबंधन (आईपीएम) पोर्टल",
        "mr": "🌾 शेतकरी पीक रोग निदान आणि एकात्मिक कीड व्यवस्थापन (आयपीएम) पोर्टल",
    },
    "portal_banner_subtitle": {
        "en": "Early symptom classification, local weather epidemiology, and actionable non-chemical crop defense",
        "hi": "प्रारंभिक लक्षण वर्गीकरण, स्थानीय मौसम महामारी विज्ञान और गैर-रासायनिक फसल सुरक्षा मार्गदर्शन",
        "mr": "लक्षण पडताळणी, स्थानिक हवामान जोखीम विश्लेषण आणि कृतीक्षम जैविक पीक संरक्षण उपाय",
    },
    "select_language_label": {
        "en": "🌐 Choose Language / भाषा / भाषा निवडा",
        "hi": "🌐 भाषा चुनें / Choose Language / भाषा निवडा",
        "mr": "🌐 भाषा निवडा / Choose Language / भाषा चुनें",
    },
    "select_crop_label": {
        "en": "🌱 Select Target Crop",
        "hi": "🌱 फसल चुनें",
        "mr": "🌱 पीक निवडा",
    },
    "select_location_label": {
        "en": "📍 Select Field Location",
        "hi": "📍 खेत का स्थान चुनें",
        "mr": "📍 शेताचे स्थान निवडा",
    },
    "step1_heading": {
        "en": "📸 Step 1: Provide Leaf Photo",
        "hi": "📸 चरण १: पौधे की पत्ती का फोटो दें",
        "mr": "📸 पायरी १: झाडाच्या पानाचा फोटो द्या",
    },
    "input_method_label": {
        "en": "Choose image input source:",
        "hi": "फोटो का स्रोत चुनें:",
        "mr": "फोटोचा स्रोत निवडा:",
    },
    "input_upload": {
        "en": "📁 Upload File",
        "hi": "📁 फ़ाइल अपलोड करें",
        "mr": "📁 फाईल अपलोड करा",
    },
    "input_camera": {
        "en": "📷 Use Camera Input",
        "hi": "📷 कैमरा उपयोग करें",
        "mr": "📷 कॅमेरा वापरा",
    },
    "input_samples": {
        "en": "🧪 Instant Test Demo Samples",
        "hi": "🧪 त्वरित परीक्षण नमूने",
        "mr": "🧪 झटपट चाचणी नमुने",
    },
    "upload_instruction": {
        "en": "Upload clear leaf photo (JPG/PNG)",
        "hi": "स्पष्ट पत्ती का फोटो अपलोड करें (JPG/PNG)",
        "mr": "पानाचा स्पष्ट फोटो अपलोड करा (JPG/PNG)",
    },
    "upload_help": {
        "en": "Take photo in good natural lighting against neutral background",
        "hi": "तटस्थ पृष्ठभूमि में अच्छी प्राकृतिक रोशनी में फोटो खींचें",
        "mr": "चांगल्या नैसर्गिक प्रकाशात स्पष्ट फोटो काढा",
    },
    "camera_instruction": {
        "en": "Capture live photo of affected leaf",
        "hi": "प्रभावित पत्ती का लाइव फोटो लें",
        "mr": "बाधित पानाचा थेट फोटो काढा",
    },
    "sample_instruction": {
        "en": "Select Sample Case:",
        "hi": "परीक्षण नमूना चुनें:",
        "mr": "चाचणी नमुना निवडा:",
    },
    "sample_helper_text": {
        "en": "Select a pre-configured sample to test diagnostic accuracy and safety safeguards:",
        "hi": "निदान सटीकता और सुरक्षा प्रतिबंधों की जांच के लिए पूर्व-कॉन्फ़िगर नमूना चुनें:",
        "mr": "रोगनिदान अचूकता आणि सुरक्षा नियमांची चाचणी घेण्यासाठी नमुना निवडा:",
    },
    "btn_run_diagnosis": {
        "en": "🔍 Run Disease Diagnosis",
        "hi": "🔍 रोग निदान जांचें",
        "mr": "🔍 रोग निदान तपासा",
    },
    "step2_heading": {
        "en": "🌦️ Step 2: Live Weather Epidemiology",
        "hi": "🌦️ चरण २: स्थानीय मौसम एवं रोग अनुकूलता विश्लेषण",
        "mr": "🌦️ पायरी २: स्थानिक हवामान आणि रोग जोखीम विश्लेषण",
    },
    "weather_fetching": {
        "en": "Fetching real-time atmospheric data from Open-Meteo...",
        "hi": "ओपन-मेटियो से वास्तविक समय का मौसम डेटा प्राप्त किया जा रहा है...",
        "mr": "ओपन-मेटिओ वरून थेट हवामानाची माहिती मिळवत आहे...",
    },
    "weather_temp": {
        "en": "🌡️ Temp",
        "hi": "🌡️ तापमान",
        "mr": "🌡️ तापमान",
    },
    "weather_humidity": {
        "en": "💧 Humidity",
        "hi": "💧 आर्द्रता",
        "mr": "💧 हवेतील आर्द्रता",
    },
    "weather_rain": {
        "en": "🌧️ Rainfall",
        "hi": "🌧️ वर्षा",
        "mr": "🌧️ पाऊस",
    },
    "weather_wind": {
        "en": "💨 Wind",
        "hi": "💨 वायु गति",
        "mr": "💨 वाऱ्याचा वेग",
    },
    "risk_high_badge": {
        "en": "⚠️ FUNGAL / PEST OUTBREAK RISK: HIGH",
        "hi": "⚠️ कवक / कीट प्रकोप जोखिम: उच्च",
        "mr": "⚠️ बुरशी / कीड उद्रेक जोखीम: उच्च",
    },
    "risk_med_badge": {
        "en": "⚡ FUNGAL / PEST OUTBREAK RISK: MEDIUM",
        "hi": "⚡ कवक / कीट प्रकोप जोखिम: मध्यम",
        "mr": "⚡ बुरशी / कीड उद्रेक जोखीम: मध्यम",
    },
    "risk_low_badge": {
        "en": "✅ FUNGAL / PEST OUTBREAK RISK: LOW",
        "hi": "✅ कवक / कीट प्रकोप जोखिम: कम (सामान्य)",
        "mr": "✅ बुरशी / कीड उद्रेक जोखीम: कमी (सामान्य)",
    },
    "step3_heading": {
        "en": "🎯 Step 3: Diagnostic Screening Results",
        "hi": "🎯 चरण ३: रोग निदान जांच परिणाम",
        "mr": "🎯 पायरी ३: रोग निदान तपासणी निकाल",
    },
    "screening_notice": {
        "en": "ℹ️ Preliminary Screening Notice: AI visual predictions are automated screening estimates based on surface foliar symptoms. They are designed to support early scouting and do not replace laboratory pathogen isolation, culturing, or molecular tests. Always evaluate plant symptoms alongside field history, soil condition, and local weather.",
        "hi": "ℹ️ प्रारंभिक जांच सूचना: एआई दृश्य भविष्यवाणियां पत्ती की सतह के लक्षणों पर आधारित स्वचालित प्रारंभिक अनुमान हैं। यह प्रयोगशाला परीक्षणों या विशेषज्ञ जांच का स्थान नहीं लेते हैं। हमेशा खेत के इतिहास और मौसम के साथ इनका मूल्यांकन करें।",
        "mr": "ℹ️ प्राथमिक तपासणी सूचना: एआय व्हिज्युअल अंदाज हे पानावरील बाह्य लक्षणांवर आधारित स्वयंचलित अंदाज आहेत. ही कोणतीही अंतिम प्रयोगशाळा चाचणी नाही. कृपया शेतातील परिस्थिती, माती आणि हवामानाचा विचार करूनच निर्णय घ्यावा.",
    },
    "candidate_breakdown_title": {
        "en": "📊 Top Candidate Disease Predictions (Probability Breakdown):",
        "hi": "📊 शीर्ष संभावित रोग भविष्यवाणियां (संभावना विवरण):",
        "mr": "📊 प्रमुख संभाव्य रोग अंदाज (संभाव्यता तपशील):",
    },
    "match_confidence_lbl": {
        "en": "Match Confidence",
        "hi": "संभावना प्रतिशत",
        "mr": "अंदाज संभाव्यता",
    },
    "possible_diagnosis_label": {
        "en": "Possible Disease Diagnosis",
        "hi": "संभावित रोग निदान",
        "mr": "संभाव्य रोग निदान",
    },
    "candidate_match_badge": {
        "en": "Automated Visual Screening Match",
        "hi": "स्वचालित दृश्य जांच अनुमान",
        "mr": "स्वयंचलित प्राथमिक तपासणी अंदाज",
    },
    "low_conf_heading": {
        "en": "Inconclusive / Low-Confidence Visual Screening",
        "hi": "अस्पष्ट / कम-विश्वास दृश्य जांच परिणाम",
        "mr": "अस्पष्ट / कमी खात्रीचा प्राथमिक तपासणी निकाल",
    },
    "low_conf_expl": {
        "en": "The most likely candidate is {disease}, but the visual confidence score ({conf}) is below the strict 60% reliability gate. Visual foliar patterns may overlap with non-parasitic nutritional chlorosis, mechanical injury, or secondary mold.",
        "hi": "सबसे संभावित रोग {disease} प्रतीत होता है, लेकिन दृश्य विश्वसनीयता स्कोर ({conf}) ६०% के सुरक्षा मानक से नीचे है। पत्ती के लक्षण पोषक तत्वों की कमी या धूप से झुलसने जैसे हो सकते हैं।",
        "mr": "सर्वात संभाव्य रोग {disease} दिसून येत आहे, परंतु विश्वासाचे प्रमाण ({conf}) ६०% सुरक्षा मर्यादेपेक्षा कमी आहे. हे लक्षण अन्नद्रव्यांची कमतरता किंवा हवामानातील बदलांमुळेही असू शकते.",
    },
    "photo_guide_title": {
        "en": "📸 Recommended steps to capture a more diagnostic photo for re-testing:",
        "hi": "📸 पुन: परीक्षण हेतु स्पष्ट और सटीक फोटो लेने के निर्देश:",
        "mr": "📸 पुन्हा अचूक तपासणीसाठी योग्य फोटो काढण्याच्या सूचना:",
    },
    "photo_guide_1": {
        "en": "Macro focus: Focus directly on the active margin where healthy green tissue meets the spot.",
        "hi": "मैक्रो फोकस: धब्बे और हरे स्वस्थ हिस्से के मिलन स्थल पर कैमरा केंद्रित करें।",
        "mr": "मॅक्रो फोकस: जिथे डाग आणि निरोगी हिरवा भाग मिळतो त्या कडेवर कॅमेरा रोखा.",
    },
    "photo_guide_2": {
        "en": "Leaf underside: Flip the leaf to check for powdery fuzz, pustules, or small insects.",
        "hi": "पत्ती का निचला भाग: पत्ती उलटकर सफेद फफूंद या छोटे कीड़े (थ्रिप्स, सफेद मक्खी) देखें।",
        "mr": "पानाची खालची बाजू: पान उलटून बुरशी, बारीक किडी (मावा, पांढरी माशी) तपासा.",
    },
    "photo_guide_3": {
        "en": "Natural light: Photograph in diffused morning daylight without camera flash glare.",
        "hi": "प्राकृतिक प्रकाश: सुबह की प्राकृतिक रोशनी में फोटो लें, तेज फ्लैश से बचें।",
        "mr": "नैसर्गिक प्रकाश: सकाळच्या सौम्य प्रकाशात फोटो काढा, कॅमेरा फ्लॅश टाळा.",
    },
    "photo_guide_4": {
        "en": "Canopy position: Note whether symptoms are isolated to oldest bottom leaves or new shoots.",
        "hi": "लक्षण का स्थान: ध्यान दें कि रोग निचली पुरानी पत्तियों पर है या नए कल्ले पर।",
        "mr": "पानाचे स्थान: रोग जुन्या खालच्या पानांवर आहे की वरच्या नवीन शेंड्यावर ते नोंदवा.",
    },

    # 5 Structured Actionable Sections
    "protocol_heading": {
        "en": "Actionable Farmer Disease Management Protocol",
        "hi": "किसान रोग प्रबंधन कार्ययोजना (५-सूत्रीय प्रोटोकॉल)",
        "mr": "शेतकरी रोग व्यवस्थापन कृती आराखडा (५-सूत्रीय कृती)",
    },
    "protocol_caption": {
        "en": "Structured recommendations following Integrated Pest Management (IPM) and ICAR / KVK agricultural extension guidance.",
        "hi": "एकीकृत कीट प्रबंधन (आईपीएम) और आईसीएआर/केवीके कृषि विस्तार दिशानिर्देशों के अनुरूप संरचित सिफारिशें।",
        "mr": "एकात्मिक कीड व्यवस्थापन (आयपीएम) आणि आयसीएआर/केव्हीके कृषी विज्ञान केंद्रांच्या शिफारशींनुसार मार्गदर्शक तत्त्वे.",
    },
    "sec_a_title": {
        "en": "🔍 A. Possible Disease & Observed Symptoms",
        "hi": "🔍 क. संभावित रोग और देखे गए लक्षण",
        "mr": "🔍 अ. संभाव्य रोग आणि दिसलेली लक्षणे",
    },
    "sec_b_title": {
        "en": "⚡ B. Immediate Steps the Farmer Can Take (First 24–48 Hours)",
        "hi": "⚡ ख. किसान द्वारा तत्काल उठाए जाने वाले कदम (पहले २४-४८ घंटे)",
        "mr": "⚡ ब. शेतकऱ्याने तातडीने करावयाची कृती (पहिल्या २४-४८ तासांत)",
    },
    "sec_c_title": {
        "en": "🛡️ C. Disease-Specific Prevention Methods",
        "hi": "🛡️ ग. रोग-विशिष्ट दीर्घकालिक रोकथाम उपाय",
        "mr": "🛡️ क. रोग-विशिष्ट दीर्घकालीन प्रतिबंधात्मक उपाय",
    },
    "sec_d_title": {
        "en": "💧 D. Crop Hygiene, Watering, Drainage & Field Monitoring",
        "hi": "💧 घ. फसल स्वच्छता, सिंचाई, जल निकासी और खेत निगरानी",
        "mr": "💧 ड. पीक स्वच्छता, पाणी नियोजन, निचरा आणि शेताची पाहणी",
    },
    "sec_e_title": {
        "en": "🏛️ E. When to Seek Confirmation from an Agricultural Expert",
        "hi": "🏛️ ङ. कृषि विशेषज्ञ या अधिकारी से कब संपर्क करें",
        "mr": "🏛️ इ. कृषी अधिकारी किंवा तज्ज्ञांशी कधी संपर्क साधावा",
    },

    # Section B details
    "sec_b_1": {
        "en": "1. Sanitary Pruning: Carefully clip and remove severely spotted or yellowed lower foliage that touches the soil. Do not drop clipped leaves onto the soil bed.",
        "hi": "१. संक्रमित पत्तियां तोड़ना: जमीन से छूने वाली अत्यधिक पीली या धब्बेदार निचली पत्तियों को सावधानी से काटें। कटी हुई पत्तियों को खेत की जमीन पर न छोड़ें।",
        "mr": "१. बाधित पाने कापणे: जमिनीला टेकलेली आणि तीव्र डाग पडलेली जुनी पाने काळजीपूर्वक छाटा. छाटलेली पाने शेतात जमिनीवर टाकू नका.",
    },
    "sec_b_2": {
        "en": "2. Safe Disposal: Bag the diseased clippings immediately and bury or burn them outside the field perimeter. Never throw them into active compost heaps.",
        "hi": "२. सुरक्षित निपटान: रोगग्रस्त पत्तियों को थैले में भरकर खेत से दूर गड्ढे में दबाएं या जलाएं। इन्हें कभी भी कम्पोस्ट खाद के गड्ढे में न डालें।",
        "mr": "२. सुरक्षित विल्हेवाट: काढलेली पाने गोणीत भरून शेताबाहेर खड्ड्यात गाडून टाका किंवा जाळून टाका. कंपोस्ट खताच्या खड्ड्यात कधीही टाकू नका.",
    },
    "sec_b_3": {
        "en": "3. Tool Sanitization: Disinfect pruning shears, sickles, and knives in a 70% alcohol solution or diluted bleach (1:9 water) between rows.",
        "hi": "३. औजारों की सफाई: कैंची या हंसिए को ७०% अल्कोहल या हल्के ब्लीच के घोल से साफ करें ताकि रोग दूसरे पौधों में न फैले।",
        "mr": "३. अवजारांचे निर्जंतुकीकरण: छाटणीची कात्री किंवा विळा ७०% अल्कोहोल किंवा सौम्य ब्लीचच्या पाण्याने स्वच्छ धुवून मगच इतर झाडांवर वापरा.",
    },
    "sec_b_4": {
        "en": "4. Foliage Drying: Suspend overhead sprinkler watering immediately. Pathogenic spores require a film of free water on leaf surfaces to germinate.",
        "hi": "४. फव्वारा सिंचाई बंद करें: पत्तियों पर ऊपर से पानी छिड़कने वाले स्प्रिंकलर तुरंत बंद करें। नमी मिलने पर फफूंद के बीजाणु तेजी से पनपते हैं।",
        "mr": "४. तुषार सिंचन थांबवा: पानावरील तुषार सिंचन त्वरित थांबवा. पानांवर पाणी साचून राहिल्यास बुरशीचे बीजाणू वेगाने वाढतात.",
    },
    "sec_b_5": {
        "en": "5. Restrict Field Traffic: Avoid walking through or tilling the crop while morning dew is present to minimize physical transmission of spores.",
        "hi": "५. ओस के समय खेत में न जाएं: सुबह की ओस रहने तक खेत में काम करने या चलने से बचें, ताकि कपड़ों या औजारों से संक्रमण न फैले।",
        "mr": "५. दवाच्या वेळी शेतात जाणे टाळा: सकाळचे दव सुकेपर्यंत शेतात मशागत करणे किंवा फिरणे टाळा, जेणेकरून बुरशीचा प्रसार होणार नाही.",
    },

    # Section D details
    "sec_d_watering": {
        "en": "Watering Management: Switch to drip irrigation at the root zone. Irrigate in early morning so moisture on lower leaves dries quickly with sunlight.",
        "hi": "सिंचाई प्रबंधन: जड़ों के पास ड्रिप सिंचाई का उपयोग करें। सुबह के समय पानी दें ताकि पत्तियों पर पड़ा पानी धूप से जल्दी सूख जाए।",
        "mr": "पाणी व्यवस्थापन: मुळांपाशी ठिबक सिंचनाचा वापर करा. शक्यतो सकाळी पाणी द्या जेणेकरून पानांवरील ओलावा सूर्यप्रकाशामुळे लवकर सुकेल.",
    },
    "sec_d_drainage": {
        "en": "Drainage & Raised Beds: Form 15–20 cm raised planting beds and clear drainage furrows to avoid root suffocation and collar rot during heavy rains.",
        "hi": "जल निकासी और उठी हुई क्यारियां: १५-२० सेमी उठी हुई क्यारियों (बेड) पर रोपाई करें और जल निकासी नालियां साफ रखें ताकि पानी जमा न हो।",
        "mr": "निचरा व गादीवाफे: १५-२० सेमी उंचीचे गादीवाफे (बेड) तयार करा आणि पाण्याचा निचरा करणारी चर स्वच्छ ठेवा जेणेकरून पाणी साचून मूळकुज होणार नाही.",
    },
    "sec_d_spacing": {
        "en": "Canopy Airflow: Maintain adequate crop spacing and train indeterminate vines on trellises to ensure constant air movement through foliage.",
        "hi": "हवा का संचार: पौधों के बीच उचित दूरी रखें और बेल वाली फसलों को तार-बांस के सहारे बांधें ताकि हवा का आवागमन सुगम रहे।",
        "mr": "हवेचे वहन: झाडांमध्ये योग्य अंतर ठेवा आणि वेलींना तारा किंवा बांबूचा आधार द्या जेणेकरून पालापाचोळ्यातून हवा खेळती राहील.",
    },
    "sec_d_weeding": {
        "en": "Bund Weed Sanitation: Keep field borders free from wild host weeds (e.g., Parthenium, wild Solanum) which act as green bridges for viruses and fungi.",
        "hi": "मेड़ों की सफाई: खेत की मेड़ों से गाजर घास और जंगली पौधों को हटाएं, क्योंकि वे रोग फैलाने वाले कीड़ों और फफूंद के आश्रय स्थल होते हैं।",
        "mr": "बांधावरील तणनियंत्रण: शेताच्या बांधावरील गाजरगवत आणि जंगली वनस्पती काढून टाका, कारण ते विषाणू आणि किडींचे मुख्य आश्रयस्थान असतात.",
    },
    "sec_d_monitoring": {
        "en": "Twice-Weekly Field Walks: Walk zigzag diagonals through the plot twice every week. Count affected plants and inspect undersides of leaves.",
        "hi": "सप्ताह में दो बार खेत का निरीक्षण: सप्ताह में दो बार खेत में जिग-जैग चलकर पत्तियों के निचले हिस्से की जांच करें और लक्षणों की निगरानी करें।",
        "mr": "आठवड्यातून दोनदा पाहणी: आठवड्यातून दोनदा शेतात तिरकस फेरफटका मारून पानांच्या खालच्या बाजूची तपासणी करा आणि रोगप्रसार नोंदवा.",
    },

    # Section E details
    "sec_e_triggers_title": {
        "en": "Immediate Expert Scouting Triggers — Contact your local Agriculture Officer or KVK if you observe:",
        "hi": "विशेषज्ञ सलाह के आवश्यक संकेत — तुरंत अपने नजदीकी कृषि अधिकारी या केवीके से संपर्क करें यदि:",
        "mr": "तज्ज्ञ सल्ल्याची तातडीची लक्षणे — खालील परिस्थिती दिसल्यास त्वरित कृषी अधिकारी किंवा केव्हीकेशी संपर्क साधा:",
    },
    "sec_e_1": {
        "en": "🚩 Rapid Expansion: Spotting or leaf death spreads across more than 15–20% of your plot within 48 to 72 hours.",
        "hi": "🚩 तेज फैलाव: यदि धब्बे या पीलापन २-३ दिनों के भीतर खेत के १५-२०% हिस्से में फैल जाए।",
        "mr": "🚩 जलद प्रसार: जर डाग किंवा पाने सुकण्याचे प्रमाण २ ते ३ दिवसांत शेतातील १५-२०% क्षेत्रावर पसरले.",
    },
    "sec_e_2": {
        "en": "🚩 Main Stem / Collar Cankers: Dark sunken lesions appear on main stems, tomato fruit stalks, or onion necks.",
        "hi": "🚩 मुख्य तने पर धब्बे: तने, फल के डंठल या प्याज की गर्दन पर गहरे धब्बे या सड़न दिखे।",
        "mr": "🚩 मुख्य खोडावर काळे डाग: मुख्य खोड, फळाचे देठ किंवा कांद्याच्या मानेवर काळे खोलगट डाग किंवा कूज दिसल्यास.",
    },
    "sec_e_3": {
        "en": "🚩 Total Daytime Wilting: Healthy-looking green plants suddenly collapse and wilt despite adequate soil moisture.",
        "hi": "🚩 अचानक मुरझाना: पर्याप्त नमी होने के बावजूद पौधे दिन में अचानक मुरझाकर सूखने लगें।",
        "mr": "🚩 झाडे एकदम कोमेजणे: जमिनीत पुरेशी ओल असतानाही झाडे अचानक कोमेजून सुकून जात असतील.",
    },
    "sec_e_4": {
        "en": "🚩 Heavy Vector Infestation: Dense swarms of whiteflies, thrips, or aphids congregate on young leaves.",
        "hi": "🚩 रस चूसक कीटों का भारी हमला: सफेद मक्खी, थ्रिप्स या माहू का झुंड नई पत्तियों पर दिखे।",
        "mr": "🚩 रसशोषक किडींचा प्रादुर्भाव: पांढरी माशी, थ्रिप्स (फुलकिडे) किंवा मावा यांचा पानांच्या मागे मोठा प्रादुर्भाव दिसल्यास.",
    },
    "sec_e_sample_guide": {
        "en": "How to Take a Sample to Krishi Vigyan Kendra (KVK): Collect 3–4 freshly affected leaves with both healthy and diseased margins. Place inside a dry paper envelope (not plastic). Note the crop age and recent sprays.",
        "hi": "कृषि विज्ञान केंद्र (KVK) ले जाने हेतु नमूना कैसे लें: ३-४ ताजी प्रभावित पत्तियां लें जिनमें स्वस्थ व रोगी दोनों हिस्से हों। उन्हें सूखे कागज के लिफाफे (प्लास्टिक नहीं) में रखें। फसल की उम्र और हालिया छिड़काव की जानकारी साथ ले जाएं।",
        "mr": "कृषी विज्ञान केंद्रात (KVK) नमुना कसा न्यावा: ३-४ ताजी बाधित पाने घ्या ज्यावर रोगट आणि निरोगी दोन्ही भाग असतील. नमुना सुक्या कागदी पाकिटात (प्लास्टिक पिशवीत नाही) ठेवा. पिकाचे वय आणि अलीकडील फवारण्यांची नोंद सोबत ठेवा.",
    },

    # Treatments Tabs
    "tab_bio": {
        "en": "🧫 Biological Controls (Eco-Friendly)",
        "hi": "🧫 जैविक नियंत्रण (पर्यावरण-अनुकूल)",
        "mr": "🧫 जैविक नियंत्रणे (पर्यावरणपूरक)",
    },
    "tab_chem": {
        "en": "⚠️ Chemical Interventions (Strictly Monitored Last Resort)",
        "hi": "⚠️ रासायनिक उपाय (कठोर निगरानी में अंतिम विकल्प)",
        "mr": "⚠️ रासायनिक फवारणी (केवळ शेवटचा नियंत्रित पर्याय)",
    },
    "tab_safe": {
        "en": "🦺 Operator Safety & Pre-Harvest Intervals (PHI)",
        "hi": "🦺 किसान सुरक्षा एवं तुड़ाई पूर्व अंतराल (PHI)",
        "mr": "🦺 शेतकरी सुरक्षा आणि काढणीपूर्व प्रतीक्षा काळ (PHI)",
    },
    "chem_warning": {
        "en": "⚠️ Responsible Chemical Usage Policy: Chemical fungicides or insecticides must only be considered if disease severity crosses the Economic Threshold Level (ETL) and cultural/biological steps fail. Never spray calendar-based preventive doses. Consult your local KVK or Agriculture Officer for approved CIBRC registrations.",
        "hi": "⚠️ जिम्मेदार रासायनिक उपयोग नीति: रासायनिक कीटनाशकों का उपयोग केवल तभी करें जब रोग आर्थिक नुकसान स्तर (ETL) पार कर जाए और जैविक उपाय विफल हों। बिना सोचे-समझे छिड़काव न करें। केंद्रीय कीटनाशक बोर्ड (CIBRC) द्वारा पंजीकृत दवाओं हेतु कृषि अधिकारी से सलाह लें।",
        "mr": "⚠️ जबाबदार रासायनिक वापर धोरण: रासायनिक बुरशीनाशकांचा वापर केवळ तेव्हाच करावा जेव्हा रोगाची तीव्रता आर्थिक नुकसान पातळी (ETL) ओलांडते आणि जैविक उपाय अपुरे पडतात. न विचारता फवारण्या करू नका. अधिकृत CIBRC नोंदणीकृत घटकांसाठी कृषी अधिकाऱ्यांचा सल्ला घ्या.",
    },
    "phi_note": {
        "en": "Pre-Harvest Interval (PHI): Always observe the legally mandated waiting period between spraying and harvest to ensure food safety for consumers.",
        "hi": "तुड़ाई पूर्व अंतराल (PHI): छिड़काव और फसल तुड़ाई के बीच निर्धारित दिनों का अंतर अवश्य रखें ताकि उपज में रसायन का अंश न रहे।",
        "mr": "काढणीपूर्व प्रतीक्षा काळ (PHI): फवारणी आणि फळे/भाजीपाला काढणीमध्ये आवश्यक दिवसांचे अंतर पाळा, जेणेकरून ग्राहकांसाठी अन्न सुरक्षित राहील.",
    },

    # Officer Surveillance Dashboard
    "officer_banner_title": {
        "en": "🛡️ Agriculture Officer Epidemiological Dashboard",
        "hi": "🛡️ कृषि अधिकारी महामारी विज्ञान निगरानी डैशबोर्ड",
        "mr": "🛡️ कृषी अधिकारी रोगनिदान व प्रादेशिक सनियंत्रण डॅशबोर्ड",
    },
    "officer_banner_subtitle": {
        "en": "Maharashtra Disease Surveillance, Hotspot Heatmapping & Ground-Truth Verification",
        "hi": "महाराष्ट्र रोग निगरानी, प्रकोप हॉटस्पॉट हीटमैपिंग एवं जमीनी सत्यापन",
        "mr": "महाराष्ट्र रोग सनियंत्रण, हॉटस्पॉट मॅपिंग आणि प्रत्यक्ष क्षेत्रीय पडताळणी",
    },
    "surveillance_scope": {
        "en": "Surveillance Scope",
        "hi": "निगरानी कार्यक्षेत्र",
        "mr": "सनियंत्रण कार्यक्षेत्र",
    },
    "surveillance_state": {
        "en": "State: Maharashtra\nFocus Districts: Pune, Nashik, Jalgaon, Ahmednagar, Solapur, Nagpur, Kolhapur",
        "hi": "राज्य: महाराष्ट्र\nप्रमुख जिले: पुणे, नासिक, जलगांव, अहमदनगर, सोलापुर, नागपुर, कोल्हापुर",
        "mr": "राज्य: महाराष्ट्र\nप्रमुख जिल्हे: पुणे, नाशिक, जळगाव, अहमदनगर, सोलापूर, नागपूर, कोल्हापूर",
    },
    "kpi_total_submissions": {
        "en": "Total Submissions",
        "hi": "कुल प्राप्त रिपोर्ट",
        "mr": "एकूण प्राप्त अहवाल",
    },
    "kpi_pending_review": {
        "en": "Pending Review",
        "hi": "समीक्षा हेतु लंबित",
        "mr": "पडताळणी बाकी",
    },
    "kpi_confirmed": {
        "en": "Confirmed",
        "hi": "सत्यापित",
        "mr": "प्रमाणित",
    },
    "kpi_corrected": {
        "en": "Corrected",
        "hi": "संशोधित",
        "mr": "दुरुस्त केलेले",
    },
    "kpi_uncertain": {
        "en": "Uncertain Flagged",
        "hi": "अनिश्चित चिह्नित",
        "mr": "अस्पष्ट चिन्हांकित",
    },
    "map_section_title": {
        "en": "🗺️ Maharashtra Spatial GIS Epidemiological Map",
        "hi": "🗺️ महाराष्ट्र स्थानिक जीआईएस रोग प्रकोप मानचित्र",
        "mr": "🗺️ महाराष्ट्र प्रादेशिक जीआयएस रोग प्रसार नकाशा",
    },
    "filter_crop_label": {
        "en": "Filter by Crop:",
        "hi": "फसल अनुसार फ़िल्टर:",
        "mr": "पिकानुसार निवडा:",
    },
    "filter_status_label": {
        "en": "Filter by Status:",
        "hi": "स्थिति अनुसार फ़िल्टर:",
        "mr": "स्थितीनुसार निवडा:",
    },
    "all_crops": {
        "en": "All Crops",
        "hi": "सभी फसलें",
        "mr": "सर्व पिके",
    },
    "all_statuses": {
        "en": "All Statuses",
        "hi": "सभी स्थितियां",
        "mr": "सर्व स्थिती",
    },
    "heat_map_toggle": {
        "en": "Show Density HeatMap Layer",
        "hi": "प्रकोप घनत्व हीटमैप परत दिखाएं",
        "mr": "उद्रेक घनता उष्णता नकाशा (हीटमॅप) स्तर दाखवा",
    },
    "analytics_title": {
        "en": "📈 Regional Disease Incidence Analytics",
        "hi": "📈 क्षेत्रीय रोग प्रकोप विश्लेषण",
        "mr": "📈 प्रादेशिक रोग उद्रेक विश्लेषण",
    },
    "reports_table_title": {
        "en": "📋 Field Surveillance Registry & Audit Trail",
        "hi": "📋 क्षेत्रीय निगरानी पंजी एवं ऑडिट ट्रेल",
        "mr": "📋 क्षेत्रीय सनियंत्रण नोंदवही व पडताळणी",
    },
    "audit_panel_title": {
        "en": "✍️ Human-in-the-Loop Expert Audit Panel",
        "hi": "✍️ विशेषज्ञ सत्यापन एवं सक्रिय शिक्षण पैनल",
        "mr": "✍️ तज्ज्ञ पडताळणी व सक्रिय शिक्षण विभाग",
    },
    "audit_select_report": {
        "en": "Select Report ID to Review:",
        "hi": "समीक्षा हेतु रिपोर्ट आईडी चुनें:",
        "mr": "पडताळणीसाठी अहवाल क्रमांक निवडा:",
    },
    "audit_expert_diagnosis": {
        "en": "Officer Ground-Truth Diagnosis:",
        "hi": "अधिकारी द्वारा सत्यापित निदान:",
        "mr": "अधिकाऱ्यांचे अंतिम प्रमाणित निदान:",
    },
    "audit_notes": {
        "en": "Official Field Observation Notes:",
        "hi": "अधिकारी क्षेत्रीय टिप्पणी:",
        "mr": "अधिकृत क्षेत्रीय निरीक्षण नोंद:",
    },
    "btn_confirm_diagnosis": {
        "en": "✅ Confirm Diagnosis",
        "hi": "✅ निदान सत्यापित करें",
        "mr": "✅ निदान प्रमाणित करा",
    },
    "btn_correct_diagnosis": {
        "en": "✏️ Update / Correct Diagnosis",
        "hi": "✏️ निदान संशोधित करें",
        "mr": "✏️ निदान दुरुस्त करा",
    },

    # Trilingual IPM Advisory Catalog
    "advisory_banner_title": {
        "en": "📚 Trilingual IPM Disease & Pest Advisory Catalog",
        "hi": "📚 त्रैभाषीय एकीकृत कीट प्रबंधन (आईपीएम) रोग परामर्श कैटलॉग",
        "mr": "📚 त्रिभाषिक एकात्मिक कीड व्यवस्थापन (आयपीएम) रोग सल्ला मार्गदर्शिका",
    },
    "advisory_banner_subtitle": {
        "en": "Integrated Pest Management (IPM) Protocols • Cultural • Biological • Chemical-Last • Safety",
        "hi": "एकीकृत कीट प्रबंधन प्रोटोकॉल • कृषि पद्धतियां • जैविक नियंत्रण • रासायनिक अंतिम विकल्प • सुरक्षा",
        "mr": "एकात्मिक कीड व्यवस्थापन मार्गदर्शक • मशागत उपाय • जैविक नियंत्रणे • रासायनिक शेवटचा पर्याय • सुरक्षा",
    },
    "search_advisory_label": {
        "en": "🔎 Search by symptom, disease, or pathogen:",
        "hi": "🔎 लक्षण, रोग या रोगजनक के नाम से खोजें:",
        "mr": "🔎 लक्षण, रोग किंवा कारणीभूत घटकानुसार शोधा:",
    },
    "part1_tab": {
        "en": "🛡️ Part I: Preventive Measures (Cultural & Biological)",
        "hi": "🛡️ भाग १: निवारक उपाय (कृषि एवं जैविक)",
        "mr": "🛡️ भाग १: प्रतिबंधात्मक उपाय (मशागत व जैविक)",
    },
    "part2_tab": {
        "en": "🧪 Part II: Monitored Treatment (Last Resort & Safety)",
        "hi": "🧪 भाग २: उपचार एवं सुरक्षा (अंतिम विकल्प)",
        "mr": "🧪 भाग २: नियंत्रित उपचार आणि सुरक्षा (शेवटचा पर्याय)",
    },
}

# Disease names localized display dictionary
DISEASE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "tomato_early_blight": {
        "en": "Tomato Early Blight (Alternaria solani)",
        "hi": "टमाटर अगेती झुलसा / अल्टरनेरिया (Tomato Early Blight)",
        "mr": "टोमॅटो लवकर येणारा करपा (Tomato Early Blight)",
    },
    "tomato_late_blight": {
        "en": "Tomato Late Blight (Phytophthora infestans)",
        "hi": "टमाटर पछेती झुलसा / फाइटोफ्थोरा (Tomato Late Blight)",
        "mr": "टोमॅटो उशिरा येणारा करपा / तांब्या (Late Blight)",
    },
    "tomato_leaf_curl_virus": {
        "en": "Tomato Leaf Curl Virus (TYLCV)",
        "hi": "टमाटर पर्ण कुंचन विषाणु (Tomato Leaf Curl Virus)",
        "mr": "टोमॅटो पर्णगुच्छ / चुरडा-मुरडा विषाणू (Leaf Curl)",
    },
    "tomato_leaf_mold": {
        "en": "Tomato Leaf Mold (Passalora fulva)",
        "hi": "टमाटर पर्ण फफूंदी (Tomato Leaf Mold)",
        "mr": "टोमॅटो पानावरील बुरशी (Tomato Leaf Mold)",
    },
    "tomato_healthy": {
        "en": "Tomato - Healthy Foliage (No Disease)",
        "hi": "टमाटर - स्वस्थ पौधा (कोई रोग नहीं)",
        "mr": "टोमॅटो - निरोगी पीक (कोणताही रोग नाही)",
    },
    "cotton_bacterial_blight": {
        "en": "Cotton Bacterial Blight / Angular Spot",
        "hi": "कपास जीवाणु अंगमारी / कोणीय पत्ती धब्बा (Bacterial Blight)",
        "mr": "कापूस जिवाणू करपा / कोनीय ठिपके (Bacterial Blight)",
    },
    "cotton_leaf_curl": {
        "en": "Cotton Leaf Curl Disease (CLCuD)",
        "hi": "कपास पत्ती मरोड़ रोग (Cotton Leaf Curl Disease)",
        "mr": "कापूस पाने आकसणे / चुरडा रोग (Leaf Curl Virus)",
    },
    "cotton_bollworm": {
        "en": "Cotton Bollworm / Caterpillar Damage",
        "hi": "कपास सुंडी / इल्ली प्रकोप (Cotton Bollworm)",
        "mr": "कापूस बोंडअळी / अळीचा प्रादुर्भाव (Cotton Bollworm)",
    },
    "onion_purple_blotch": {
        "en": "Onion Purple Blotch (Alternaria porri)",
        "hi": "प्याज बैंगनी धब्बा रोग (Onion Purple Blotch)",
        "mr": "कांदा जांभळा करपा (Onion Purple Blotch)",
    },
    "onion_downy_mildew": {
        "en": "Onion Downy Mildew (Peronospora destructor)",
        "hi": "प्याज मृदुरोमिल आसिता (Onion Downy Mildew)",
        "mr": "कांदा केवडा / भुरीसारखा करपा (Downy Mildew)",
    },
    "onion_stemphylium_blight": {
        "en": "Onion Stemphylium Blight",
        "hi": "प्याज स्टेमफिलियम झुलसा रोग",
        "mr": "कांदा स्टेमफिलियम करपा रोग",
    },
}


_FALLBACK_LANG = "en"

def init_language_state():
    """Ensures language state exists in st.session_state."""
    if st is not None:
        if "language" not in st.session_state:
            st.session_state["language"] = "en"


def get_current_language() -> str:
    """Returns current language code ('en', 'hi', or 'mr')."""
    if st is not None:
        return st.session_state.get("language", "en")
    return _FALLBACK_LANG


def set_current_language(lang_code: str):
    """Sets current language code in session state."""
    global _FALLBACK_LANG
    if lang_code in SUPPORTED_LANGUAGES:
        if st is not None:
            st.session_state["language"] = lang_code
        _FALLBACK_LANG = lang_code


def t(key: str, lang_code: Optional[str] = None) -> str:
    """
    Translates a UI key.
    Falls back to English ('en') if translation is missing.
    Returns key if neither exists.
    """
    if lang_code is None:
        lang_code = get_current_language()

    entry = TRANSLATIONS.get(key)
    if entry:
        return entry.get(lang_code, entry.get("en", key))
    return key


def get_disease_name(disease_id: str, lang_code: Optional[str] = None) -> str:
    """Returns localized disease display name."""
    if lang_code is None:
        lang_code = get_current_language()

    entry = DISEASE_TRANSLATIONS.get(disease_id)
    if entry:
        return entry.get(lang_code, entry.get("en", disease_id.replace("_", " ").title()))
    return disease_id.replace("_", " ").title()


def render_language_selector(sidebar: bool = True, key_prefix: str = "global"):
    """
    Renders standardized language dropdown widget that persists in session state.
    Triggers st.rerun() if user changes language, ensuring immediate application.
    """
    if st is None:
        return "en"

    init_language_state()
    current_lang = get_current_language()

    lang_labels = ["English", "हिन्दी (Hindi)", "मराठी (Marathi)"]
    lang_codes = ["en", "hi", "mr"]
    code_to_idx = {"en": 0, "hi": 1, "mr": 2}

    current_idx = code_to_idx.get(current_lang, 0)
    container = st.sidebar if sidebar else st

    label_text = "🌐 Language / भाषा / भाषा निवडा"
    widget_key = f"{key_prefix}_lang_selector"

    choice = container.selectbox(
        label_text,
        options=lang_labels,
        index=current_idx,
        key=widget_key,
        help="Select user interface language (English, हिन्दी, मराठी)",
    )

    chosen_idx = lang_labels.index(choice)
    new_lang = lang_codes[chosen_idx]

    if new_lang != current_lang:
        st.session_state["language"] = new_lang
        st.rerun()

    return new_lang
