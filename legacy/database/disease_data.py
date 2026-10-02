from __future__ import annotations

from typing import Any


CATEGORY_TREATMENT = {
    "dermatology": {
        "medicines": [
            "Topical antifungal cream (as prescribed by doctor)",
            "Topical antibiotic gel (as prescribed by doctor)",
            "Oral antihistamine tablet (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Keep the affected skin clean and dry.",
            "Use mild, fragrance-free cleansers.",
            "Avoid scratching or picking skin lesions.",
        ],
        "precautions": [
            "Do not share towels, razors, or personal cosmetics.",
            "Avoid self-medicating with steroid creams.",
            "Consult a dermatologist if rash spreads quickly.",
        ],
        "specialization": "Dermatologist",
    },
    "infectious": {
        "medicines": [
            "Paracetamol for fever support (as prescribed by doctor)",
            "Oral rehydration salts (as prescribed by doctor)",
            "Disease-specific antimicrobial therapy (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Rest adequately and maintain hydration.",
            "Consume light, easy-to-digest meals.",
            "Monitor temperature and warning signs regularly.",
        ],
        "precautions": [
            "Avoid crowded areas while symptomatic.",
            "Follow strict hand hygiene.",
            "Seek urgent care for persistent high fever or confusion.",
        ],
        "specialization": "Infectious Disease Specialist",
    },
    "liver": {
        "medicines": [
            "Liver-supportive medicines (as prescribed by doctor)",
            "Antiviral therapy when indicated (as prescribed by doctor)",
            "Vitamin supplementation (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Drink adequate water and clear fluids.",
            "Eat low-fat, balanced meals.",
            "Get sufficient rest and avoid alcohol completely.",
        ],
        "precautions": [
            "Do not consume alcohol in any quantity.",
            "Avoid oily and heavily processed foods.",
            "Consult a hepatology specialist for follow-up.",
        ],
        "specialization": "Hepatologist",
    },
    "cardio": {
        "medicines": [
            "Blood pressure control medicine (as prescribed by doctor)",
            "Antiplatelet therapy when indicated (as prescribed by doctor)",
            "Lipid-lowering medicine when indicated (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Reduce salt intake and maintain hydration.",
            "Practice guided breathing and stress reduction.",
            "Track blood pressure regularly.",
        ],
        "precautions": [
            "Avoid smoking and excessive caffeine.",
            "Do not ignore chest pain, jaw pain, or arm pain.",
            "Call emergency services for severe chest symptoms.",
        ],
        "specialization": "Cardiologist",
    },
    "respiratory": {
        "medicines": [
            "Bronchodilator inhaler (as prescribed by doctor)",
            "Mucolytic or cough support medicine (as prescribed by doctor)",
            "Antibiotics/antivirals if indicated (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Use steam inhalation for congestion relief.",
            "Drink warm fluids and rest.",
            "Keep indoor air clean and dust-free.",
        ],
        "precautions": [
            "Avoid smoke, dust, and known respiratory triggers.",
            "Use a mask in crowded or polluted environments.",
            "Seek urgent care for breathlessness or low oxygen symptoms.",
        ],
        "specialization": "Pulmonologist",
    },
    "endocrine": {
        "medicines": [
            "Glucose-regulating medicine (as prescribed by doctor)",
            "Thyroid hormone/anti-thyroid medicine (as prescribed by doctor)",
            "Electrolyte support when indicated (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Maintain regular meal timings.",
            "Prioritize balanced low-glycemic nutrition.",
            "Sleep consistently and stay active.",
        ],
        "precautions": [
            "Do not skip prescribed endocrine medicines.",
            "Monitor blood sugar and thyroid follow-up tests.",
            "Carry a quick sugar source if prone to hypoglycemia.",
        ],
        "specialization": "Endocrinologist",
    },
    "neuro": {
        "medicines": [
            "Neurological symptom-control medicines (as prescribed by doctor)",
            "Vertigo/migraine relief medicine (as prescribed by doctor)",
            "Neuroprotective support when indicated (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Rest in a quiet, low-light environment.",
            "Stay hydrated and avoid sleep deprivation.",
            "Perform supervised balance exercises when advised.",
        ],
        "precautions": [
            "Avoid sudden head movements if dizzy.",
            "Do not drive during severe neurological symptoms.",
            "Seek emergency help for speech weakness or one-sided deficits.",
        ],
        "specialization": "Neurologist",
    },
    "ortho": {
        "medicines": [
            "Anti-inflammatory pain relief (as prescribed by doctor)",
            "Muscle relaxants when needed (as prescribed by doctor)",
            "Calcium/vitamin D supplements (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Use warm compress for stiffness relief.",
            "Practice light mobility and posture exercises.",
            "Take short walking breaks during prolonged sitting.",
        ],
        "precautions": [
            "Avoid heavy lifting with poor posture.",
            "Use ergonomic support while working.",
            "Consult orthopedics if pain persists or worsens.",
        ],
        "specialization": "Orthopedic Specialist",
    },
    "gastro": {
        "medicines": [
            "Acid-control medicine (as prescribed by doctor)",
            "Probiotic support (as prescribed by doctor)",
            "Antispasmodic medicine (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Eat small, frequent meals.",
            "Avoid spicy, oily, and late-night meals.",
            "Stay hydrated with clean fluids.",
        ],
        "precautions": [
            "Avoid alcohol and tobacco.",
            "Do not lie down immediately after meals.",
            "Seek urgent care for blood in stool or severe dehydration.",
        ],
        "specialization": "Gastroenterologist",
    },
    "urinary": {
        "medicines": [
            "Urinary antiseptic/antibiotic (as prescribed by doctor)",
            "Urinary pain-relief support (as prescribed by doctor)",
            "Hydration and electrolyte support (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Increase clean water intake.",
            "Maintain genital and urinary hygiene.",
            "Urinate regularly and avoid holding urine.",
        ],
        "precautions": [
            "Avoid dehydration and excessive caffeine.",
            "Use breathable cotton garments.",
            "Consult urology if fever or flank pain appears.",
        ],
        "specialization": "Urologist",
    },
    "immune": {
        "medicines": [
            "Immune-supportive therapy plan (as prescribed by doctor)",
            "Opportunistic infection prophylaxis (as prescribed by doctor)",
            "Long-term antiviral therapy (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Maintain high-protein nutritious meals.",
            "Sleep well and keep stress controlled.",
            "Follow regular medical appointments.",
        ],
        "precautions": [
            "Follow strict infection-prevention hygiene.",
            "Do not miss scheduled medications.",
            "Consult infectious disease specialist for ongoing care.",
        ],
        "specialization": "Infectious Disease Specialist",
    },
}


DISEASE_BLUEPRINTS = [
    {
        "disease_name": "(vertigo) Paroymsal  Positional Vertigo",
        "description": "Paroxysmal positional vertigo causes short episodes of spinning sensations triggered by head movement.",
        "category": "neuro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Acne",
        "description": "Acne is an inflammatory skin condition involving clogged pores, pimples, and occasional painful nodules.",
        "category": "dermatology",
        "urgency_level": "Mild",
    },
    {
        "disease_name": "AIDS",
        "description": "AIDS is an advanced immune deficiency state due to HIV infection and requires specialist long-term care.",
        "category": "immune",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Alcoholic hepatitis",
        "description": "Alcoholic hepatitis is liver inflammation linked to prolonged alcohol use and can become life-threatening.",
        "category": "liver",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Allergy",
        "description": "Allergy is an exaggerated immune response to triggers like dust, foods, medications, or pollen.",
        "category": "dermatology",
        "urgency_level": "Mild",
    },
    {
        "disease_name": "Arthritis",
        "description": "Arthritis causes joint pain, swelling, and reduced mobility due to inflammation or degeneration.",
        "category": "ortho",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Bronchial Asthma",
        "description": "Bronchial asthma is a chronic airway condition causing wheeze, chest tightness, and episodic breathlessness.",
        "category": "respiratory",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Cervical spondylosis",
        "description": "Cervical spondylosis is age-related wear in the neck spine causing stiffness, pain, and nerve symptoms.",
        "category": "ortho",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Chicken pox",
        "description": "Chicken pox is a contagious viral infection causing fever and itchy blister-like skin eruptions.",
        "category": "infectious",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Chronic cholestasis",
        "description": "Chronic cholestasis indicates prolonged bile flow impairment that can affect liver function and digestion.",
        "category": "liver",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Common Cold",
        "description": "Common cold is an upper respiratory viral infection with sneezing, sore throat, and mild fever.",
        "category": "respiratory",
        "urgency_level": "Mild",
    },
    {
        "disease_name": "Dengue",
        "description": "Dengue is a mosquito-borne viral illness that can lead to severe dehydration and low platelet count.",
        "category": "infectious",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Diabetes",
        "description": "Diabetes is a metabolic disorder with persistently high blood sugar requiring long-term monitoring.",
        "category": "endocrine",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Dimorphic hemmorhoids(piles)",
        "description": "Hemorrhoids are swollen veins in the lower rectum or anus causing pain, bleeding, and discomfort.",
        "category": "gastro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Drug Reaction",
        "description": "Drug reactions include skin, gastrointestinal, or systemic responses after medication exposure.",
        "category": "dermatology",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Fungal infection",
        "description": "Fungal infections commonly affect skin folds and nails, producing redness, scaling, and itching.",
        "category": "dermatology",
        "urgency_level": "Mild",
    },
    {
        "disease_name": "Gastroenteritis",
        "description": "Gastroenteritis is inflammation of the stomach and intestines leading to vomiting and diarrhea.",
        "category": "gastro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "GERD",
        "description": "GERD is chronic acid reflux causing heartburn, chest discomfort, and sour regurgitation.",
        "category": "gastro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Heart attack",
        "description": "Heart attack occurs when blood flow to heart muscle is blocked and needs emergency intervention.",
        "category": "cardio",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "hepatitis A",
        "description": "Hepatitis A is an acute viral liver infection usually spread through contaminated food or water.",
        "category": "liver",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Hepatitis B",
        "description": "Hepatitis B is a blood-borne liver infection that can become chronic without proper treatment.",
        "category": "liver",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Hepatitis C",
        "description": "Hepatitis C is a viral liver disease that can silently progress to chronic liver damage.",
        "category": "liver",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Hepatitis D",
        "description": "Hepatitis D is a severe liver infection that occurs only with hepatitis B co-infection.",
        "category": "liver",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Hepatitis E",
        "description": "Hepatitis E is typically water-borne and causes acute liver inflammation with jaundice and fatigue.",
        "category": "liver",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Hypertension",
        "description": "Hypertension is persistently elevated blood pressure that raises cardiovascular risk over time.",
        "category": "cardio",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Hyperthyroidism",
        "description": "Hyperthyroidism is excess thyroid hormone activity causing weight loss, tremor, and rapid heartbeat.",
        "category": "endocrine",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Hypoglycemia",
        "description": "Hypoglycemia means low blood sugar and can cause sweating, shakiness, confusion, or fainting.",
        "category": "endocrine",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Hypothyroidism",
        "description": "Hypothyroidism is reduced thyroid function causing fatigue, weight gain, and sluggishness.",
        "category": "endocrine",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Impetigo",
        "description": "Impetigo is a contagious bacterial skin infection causing honey-colored crusted sores.",
        "category": "dermatology",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Jaundice",
        "description": "Jaundice is yellow discoloration due to elevated bilirubin and usually indicates liver or bile problems.",
        "category": "liver",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Malaria",
        "description": "Malaria is a mosquito-borne parasitic infection causing cyclical fever, chills, and weakness.",
        "category": "infectious",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Migraine",
        "description": "Migraine is a neurological headache disorder often associated with light sensitivity and nausea.",
        "category": "neuro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Osteoarthristis",
        "description": "Osteoarthritis is progressive wear-and-tear joint degeneration causing pain and stiffness.",
        "category": "ortho",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Paralysis (brain hemorrhage)",
        "description": "Paralysis from brain hemorrhage can cause sudden weakness, speech issues, and neurological emergency signs.",
        "category": "neuro",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Peptic ulcer diseae",
        "description": "Peptic ulcer disease involves erosions in stomach or duodenal lining causing burning abdominal pain.",
        "category": "gastro",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Pneumonia",
        "description": "Pneumonia is a lung infection that can impair breathing and oxygen levels.",
        "category": "respiratory",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Psoriasis",
        "description": "Psoriasis is an immune-mediated skin disorder causing thick, scaly, inflammatory plaques.",
        "category": "dermatology",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Tuberculosis",
        "description": "Tuberculosis is a bacterial infection, usually in the lungs, requiring prolonged supervised treatment.",
        "category": "infectious",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Typhoid",
        "description": "Typhoid is a systemic bacterial infection causing sustained fever, abdominal pain, and weakness.",
        "category": "infectious",
        "urgency_level": "Severe",
    },
    {
        "disease_name": "Urinary tract infection",
        "description": "UTI is infection in urinary pathways causing burning urination, urgency, and lower abdominal pain.",
        "category": "urinary",
        "urgency_level": "Moderate",
    },
    {
        "disease_name": "Varicose veins",
        "description": "Varicose veins are enlarged twisted leg veins causing heaviness, swelling, and aching discomfort.",
        "category": "cardio",
        "urgency_level": "Mild",
    },
]


DOCTOR_SEED_DATA = [
    {
        "id": 1,
        "name": "Dr. Aryan Mehta",
        "specialization": "General Physician",
        "experience": "14 years experience",
        "rating": 4.8,
        "avatar_type": "male_1",
        "bio": "Primary care specialist focused on comprehensive diagnosis and patient-friendly guidance.",
    },
    {
        "id": 2,
        "name": "Dr. Priya Sharma",
        "specialization": "Gastroenterologist",
        "experience": "11 years experience",
        "rating": 4.9,
        "avatar_type": "female_1",
        "bio": "Digestive health expert with special interest in liver and intestinal disorders.",
    },
    {
        "id": 3,
        "name": "Dr. Vikram Nair",
        "specialization": "Cardiologist",
        "experience": "16 years experience",
        "rating": 4.8,
        "avatar_type": "male_2",
        "bio": "Cardiac specialist with expertise in emergency risk triage and long-term heart care.",
    },
    {
        "id": 4,
        "name": "Dr. Ananya Rao",
        "specialization": "Pulmonologist",
        "experience": "10 years experience",
        "rating": 4.7,
        "avatar_type": "female_2",
        "bio": "Respiratory physician focused on asthma, pneumonia, and chronic airway diseases.",
    },
    {
        "id": 5,
        "name": "Dr. Rohan Kulkarni",
        "specialization": "Neurologist",
        "experience": "13 years experience",
        "rating": 4.8,
        "avatar_type": "male_3",
        "bio": "Neurology consultant specializing in vertigo, migraine, and cerebrovascular risk.",
    },
    {
        "id": 6,
        "name": "Dr. Meera Iyer",
        "specialization": "Endocrinologist",
        "experience": "12 years experience",
        "rating": 4.9,
        "avatar_type": "female_3",
        "bio": "Hormonal and metabolic care specialist managing diabetes and thyroid disorders.",
    },
    {
        "id": 7,
        "name": "Dr. Kunal Bhatia",
        "specialization": "Dermatologist",
        "experience": "9 years experience",
        "rating": 4.6,
        "avatar_type": "male_4",
        "bio": "Skin specialist with clinical focus on inflammatory and infectious dermatoses.",
    },
    {
        "id": 8,
        "name": "Dr. Sneha Kapoor",
        "specialization": "Infectious Disease Specialist",
        "experience": "15 years experience",
        "rating": 4.9,
        "avatar_type": "female_4",
        "bio": "Infectious disease consultant supporting fever protocols and antimicrobial stewardship.",
    },
    {
        "id": 9,
        "name": "Dr. Neel Joshi",
        "specialization": "Orthopedic Specialist",
        "experience": "12 years experience",
        "rating": 4.7,
        "avatar_type": "male_5",
        "bio": "Musculoskeletal expert focused on spine, joint degeneration, and functional recovery.",
    },
    {
        "id": 10,
        "name": "Dr. Aditi Verma",
        "specialization": "Urologist",
        "experience": "8 years experience",
        "rating": 4.6,
        "avatar_type": "female_5",
        "bio": "Urology specialist for urinary infections and lower urinary tract health.",
    },
    {
        "id": 11,
        "name": "Dr. Farhan Ali",
        "specialization": "Hepatologist",
        "experience": "14 years experience",
        "rating": 4.8,
        "avatar_type": "male_6",
        "bio": "Liver specialist dedicated to viral hepatitis and chronic liver disease management.",
    },
]


SPECIALIZATION_TO_DOCTOR_ID = {
    "General Physician": 1,
    "Gastroenterologist": 2,
    "Cardiologist": 3,
    "Pulmonologist": 4,
    "Neurologist": 5,
    "Endocrinologist": 6,
    "Dermatologist": 7,
    "Infectious Disease Specialist": 8,
    "Orthopedic Specialist": 9,
    "Urologist": 10,
    "Hepatologist": 11,
}


def get_disease_seed_data() -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for disease in DISEASE_BLUEPRINTS:
        treatment = CATEGORY_TREATMENT[disease["category"]]
        payload.append(
            {
                "disease_name": disease["disease_name"],
                "description": disease["description"],
                "medicines": treatment["medicines"],
                "home_remedies": treatment["home_remedies"],
                "precautions": treatment["precautions"],
                "urgency_level": disease["urgency_level"],
            }
        )
    return payload


def get_disease_specialization_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for disease in DISEASE_BLUEPRINTS:
        category = str(disease["category"])
        mapping[str(disease["disease_name"])] = str(CATEGORY_TREATMENT[category]["specialization"])
    return mapping
