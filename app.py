import streamlit as st
import qrcode
import base64
from io import BytesIO
from urllib.parse import quote_plus

# =========================================================
# CONFIGURATION
# =========================================================

# PASTE YOUR GOOGLE DRIVE LINK HERE!
# This is what the QR code will point to. 
# Make sure your Drive link is set to "Anyone with the link can view".
GDRIVE_LINK = "https://drive.google.com/file/d/1Tv5TbzRN2kDu03x8jcwwAuIhO-27MVGV/view?usp=sharing"

CONCERT_DATE = "Sunday, 22 November 2026"

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="A Little Mystery for My Yappy Shuno 💗",
    page_icon="💗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 8% 10%, #ffe5ed 0, transparent 30%),
            radial-gradient(circle at 92% 30%, #fce1f1 0, transparent 32%),
            linear-gradient(145deg, #fff9fb, #fff0f5 55%, #fff8fc);
    }
    [data-testid="stHeader"] { background: transparent; }
    
    /* We removed #MainMenu so the settings stay visible */
    footer { visibility: hidden; }
    
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #e89ab6, #cc6f97);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.72rem 1.3rem;
        font-weight: 700;
        transition: 0.2s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        color: white;
        border: 1px solid #b84f7c;
        transform: translateY(-2px);
    }
    
    h1, h2, h3 { color: #873f60 !important; font-family: 'Playfair Display', serif; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

if "stage" not in st.session_state:
    st.session_state.stage = st.query_params.get("stage", "welcome")
if "question_index" not in st.session_state:
    st.session_state.question_index = int(st.query_params.get("q_idx", 0))
if "answers_correct" not in st.session_state:
    st.session_state.answers_correct = int(st.query_params.get("score", 0))
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

def sync_state():
    st.query_params["stage"] = st.session_state.stage
    st.query_params["q_idx"] = str(st.session_state.question_index)
    st.query_params["score"] = str(st.session_state.answers_correct)

def next_stage(stage):
    st.session_state.stage = stage
    sync_state()
    st.rerun()

def google_search_link(search_term):
    url = "https://www.google.com/search?q=" + quote_plus(search_term)
    st.link_button("Need a clue? Search Google 🔎", url)

# =========================================================
# QUIZ QUESTIONS
# =========================================================

questions = [
    {
        "question": "Who sang with the MVR boys in the Kalyani remix?",
        "options": ["Shreya Ghoshal", "Sunidhi Chauhan", "Anjum 😂", "Jopu’s self-composed nonsense songs for you 🎤😂"],
        "answer": "Shreya Ghoshal",
        "search": "Kalyani remix MVR boys singer",
        "hint": "Think of that magical voice you absolutely adore. 🎶",
    },
    {
        "question": "Psst... there's an artist who was born in the same city as you. Who is this magical singer we're talking about? 👀",
        "options": ["Shreya Ghoshal", "Sunidhi Chauhan", "Lata Mangeshkar", "Jopu's imaginary friend"],
        "answer": "Shreya Ghoshal",
        "search": "Shreya Ghoshal born in West Bengal",
        "hint": "It's the same voice your Jopu is taking you to see! 🥰",
    },
    {
        "question": "If Jopu was planning a romantic mystery dinner for you, which song from the list translates to 'A little bit of alcohol'? 🥂",
        "options": ["Thodi Si Daaru", "Tere Liye", "Kalyani (Remix)", "Vaaroon Forever"],
        "answer": "Kalyani (Remix)",
        "search": "Shreya Ghoshal Thodi Si Daaru song",
        "hint": "Look at the 4th song on the screenshot I sent you. 🥂",
    },
    {
        "question": "Did you remind Jopu about a Bengaluru concert? What was his reaction at that moment? 👀🤨",
        "options": [
            "Acted way too normal... which was NOT normal 🤨",
            "Changed the topic faster than a Wi-Fi connection 💀",
            "Started smiling at his phone like a man hiding state secrets 📱",
            "Suddenly got busy and started acting all innocent 🤨💀"
        ],
        "answer": "Changed the topic faster than a Wi-Fi connection 💀",
        "search": "concerts happening in Bengaluru on 22 November 2026",
        "hint": "Why is Jopu acting like the main suspect in his own investigation? 🕵️‍♀️"
    },
    {
        "question": "Which song from the list was featured in the gritty crime series 'Mirzapur'? 🔪",
        "options": ["Vaaroon Forever", "Kalyani (Remix)", "Saibo", "Thodi Si Daaru"],
        "answer": "Vaaroon Forever",
        "search": "Vaaroon Forever Mirzapur song",
        "hint": "The title means 'Rain'. 🌧️",
    },
    {
        "question": "Which Bollywood film features the iconic song 'Dola Re Dola'? ✨",
        "options": ["Devdas", "Veer-Zaara", "Kal Ho Naa Ho", "Jab We Met"],
        "answer": "Devdas",
        "search": "Dola Re Dola song which film",
        "hint": "A Sanjay Leela Bhansali classic featuring Madhuri Dixit and Aishwarya Rai. 💃"
    },
    {
        "question": "The song 'Saibo' is from which suspenseful film? 🏙️",
        "options": ["Shor in the City", "Mirzapur", "Aashiqui 2", "Devdas"],
        "answer": "Shor in the City",
        "search": "Saibo song Shor in the City",
        "hint": "The title of the movie has the word 'City' in it. 🏙️",
    },
    {
        "question": "The beautiful song 'Teri Ore' belongs to which film? 💕",
        "options": ["Namastey London", "Singh Is Kinng", "Partner", "Rab Ne Bana Di Jodi"],
        "answer": "Singh Is Kinng",
        "search": "Teri Ore song film",
        "hint": "Akshay Kumar and Katrina Kaif. 💕",
    },
    {
        "question": "⚠️ **TRAP ACTIVATED:** I knew you'd make it this far. But this final lock requires 2 detectives, So request help from your buddy here obv you know whom i'm talking about. 👥",
        "options": ["The Unstoppable India Tour - SG", "The Magic Voice Tour", "Jopu's Secret Concert", "I can't solve this, I'm getting my friend!"],
        "answer": "The Unstoppable India Tour - SG",
        "search": "Shreya Ghoshal Unstoppable India Tour Bengaluru",
        "hint": "Which concert is happening in Bengaluru on 22nd November 2026?",
    },
]

# =========================================================
# STAGE 1 — WELCOME SCREEN
# =========================================================

if st.session_state.stage == "welcome":
    st.markdown("<h1 style='text-align: center;'>Hey, my yappy Shuno... 💗</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>You thought you knew everything about me? 🥺</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("### Okay... I have a confession to make. 🤭")
    st.write("I did a little something. Maybe it's a bit suspicious. Maybe I'm a little guilty. 😏")
    
    st.warning("Are you overthinking already? Good. I want you to. 😂")
    
    st.write("It's a little mystery. A big surprise. And something really cool waiting at the end for you. 👀✨")
    
    st.markdown("#### 💌 Your Jopu has a little plan...")
    st.info('**"No overthinking, Shuno. Just trust your Jopu. For once."** 😘')
    
    st.write("Psst... I need you to do something. Knowing you, you're already suspicious, right? 🤭")
    
    st.caption("*Proceed with caution. 🚨💗*")
    
    st.write("---")
    if st.button("Fine, Jopu... what have you done now? 🤨💗", use_container_width=True):
        next_stage("quiz")


# =========================================================
# STAGE 2 — QUIZ
# =========================================================

elif st.session_state.stage == "quiz":
    idx = st.session_state.question_index
    q = questions[idx]

    st.markdown(f"<h2 style='text-align: center;'>Question {idx + 1} of {len(questions)} 🕵️‍♀️</h2>", unsafe_allow_html=True)
    st.progress((idx + 1) / len(questions))

    st.write(f"### Case file #{idx + 1}")
    st.write(f"**{q['question']}**")
    
    if idx == len(questions) - 1:
        st.warning(f"📝 **NOTE:** {q['hint']} No hints from Jopu (ask Anjum) 👥")
    else:
        st.caption(f"*Hint: {q['hint']}*")

    google_search_link(q["search"])

    with st.form(key=f"question_form_{idx}"):
        selected = st.radio("Choose your answer, detective 💌", q["options"], index=None, key=f"answer_{idx}")
        submitted = st.form_submit_button("Lock in my answer 💗", use_container_width=True)

    if submitted:
        if selected is None:
            st.warning("Shuno, pick an answer first! 😂")
        elif selected == q["answer"]:
            st.session_state.feedback = ""
            st.session_state.answers_correct += 1
            if idx == len(questions) - 1:
                next_stage("team_prompt")
            else:
                st.session_state.question_index += 1
                st.session_state.feedback = "correct"
                sync_state() 
                st.rerun()
        else:
            st.session_state.feedback = "wrong"
            st.rerun()

    if st.session_state.feedback == "wrong":
        st.error("Not quite, my yappy Shuno! 😂 Try again, or use the Google clue above.")
    if st.session_state.feedback == "correct":
        st.session_state.feedback = ""
        st.success("That's my clever girl! 💗")

    st.write("---")
    st.caption(f"Case files solved: {st.session_state.answers_correct} / {len(questions)}")


# =========================================================
# STAGE 3 — THE FINAL PROMPT
# =========================================================

elif st.session_state.stage == "team_prompt":
    
    st.write("---")
    st.markdown("### 💌 Pssst... one last thing, Shuno.")

    st.write(
        "You've followed the clues and survived Jopu's suspicious behaviour. 😂"
    )

    st.write(
        "Now, take a deep breath, my yappy Shuno... "
        "because the moment you've been waiting for is finally here. 👀💗"
    )

    st.info(
        '"One mischievous Jopu, one very special Shuno, '
        'and one surprise made with all my love." 🥹💕'
    )

    st.markdown(
        "### Ready to discover your surprise, baby? 🎁💗"
    )
    st.write("---")

    if st.button("YES, SHOW ME MY SURPRISE! 🎁💗", use_container_width=True):
        next_stage("teaser")


# =========================================================
# STAGE 4 — THE TEASER (CLICKABLE QR CODE PAGE)
# =========================================================

elif st.session_state.stage == "teaser":
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>You've done it, detective! 🕵️‍♀️</h1>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 💌 Here is what I can tell you...")
    
    st.write(f"You are officially going on a date with your Jopu on **{CONCERT_DATE}**. 🥂💗")
    
    st.warning("But *where* are we going? And *who* are we seeing? That part is a secret hidden in the link below. 🤫")

    
    st.write(
        "I know you'll be opening this on your phone anyway 😂 "
        "but let's keep it dramatic! Scan the QR code or just tap it directly. "
        "BUTTT 👀💗 come back to this screen and hit the Continue button below... "
        "there's more surprise waiting for you, baby! 🎁🤭"
    )

    
    # Generate the QR Code directly from the GDRIVE_LINK
    if "PASTE_YOUR_GOOGLE_DRIVE_LINK_HERE" in GDRIVE_LINK or not GDRIVE_LINK.startswith("https://"):
        st.error("⚠️ **Hold up, Jopu!** You forgot to paste your Google Drive link at the top of the code. The QR code won't work until you do.")
        active_link = "https://drive.google.com" 
    else:
        active_link = GDRIVE_LINK.strip()
        
        try:
            qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
            qr.add_data(active_link)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="#873f60", back_color="#fff9fb").convert("RGB")
            
            image_buffer = BytesIO()
            qr_image.save(image_buffer, format="PNG")
            
            # Convert image to base64 so we can make it clickable
            img_base64 = base64.b64encode(image_buffer.getvalue()).decode()
            
            # Display clickable image
            st.markdown(
                f'''
                <div style="text-align: center;">
                    <a href="{active_link}" target="_blank">
                        <img src="data:image/png;base64,{img_base64}" width="100%" style="max-width: 350px; cursor: pointer; border-radius: 20px; box-shadow: 0 4px 15px rgba(176,85,123,0.2);" alt="Tap to open">
                    </a>
                    <p style="color: #873f60; font-weight: bold; margin-top: 15px; font-size: 1.1rem;">👆 Tap the QR code to open it directly! 👆</p>
                </div>
                ''', 
                unsafe_allow_html=True
            )
            
        except Exception as error:
            st.error(f"Couldn't generate the QR code: {error}")

    st.write("---")
    
    if st.button("I scanned it / opened the link! Let's continue... 🎁", use_container_width=True):
        next_stage("dance_gift")


# =========================================================
# STAGE 5 — KALYANI DANCE CHALLENGE
# =========================================================

elif st.session_state.stage == "dance_gift":
    st.markdown("<h2 style='text-align: center;'>One tiny request, Shuno... 💃</h2>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### ✨ Introducing... ✨")
    st.header("THE KALYANI DANCE CHALLENGE")
    
    st.write("If possible, I have one little wish.")
    st.write("I'd love you to record a short video of yourself doing the Kalyani dance. No pressure to make it perfect. Just you, your favourite moves, and that adorable energy I love so much.")
    
    st.info("And when you get home, I will be waiting to watch you perform the whole dance just for him. 🥹💗")
    
    st.write("Think of it as a tiny memory made just for us. Your smile, your dance, your moment.")
    st.markdown("#### Deal, my yappy Shuno? 🫶")
    
    st.write("---")
    st.caption("Only if you feel like it, diva girl. The real gift is always you. 💗")

    if st.button("OKAY JOPU, IT'S A DEAL! 💃💗", use_container_width=True):
        next_stage("final_goodbye")


# =========================================================
# STAGE 6 — FINAL GOODBYE
# =========================================================

elif st.session_state.stage == "final_goodbye":
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>Case Closed. 🕵️‍♀️💗</h2>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 💗 Made with love, by Jopu.")
    st.info('"Some memories are planned. The best ones are made together." ♡')
    st.write("---")

    st.markdown("<h3 style='text-align: center;'>I love you, my yappy Shuno. 💗</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Love,<br>your Jopu. ♡</p>", unsafe_allow_html=True)
    st.caption("End of investigation. Beginning of another lovely memory.")

    if st.button("Relive the surprise from the beginning ↺"):
        st.session_state.stage = "welcome"
        st.session_state.question_index = 0
        st.session_state.answers_correct = 0
        st.session_state.feedback = ""
        st.query_params.clear() 
        st.rerun()
