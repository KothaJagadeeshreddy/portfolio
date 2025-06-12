import streamlit as st
import sqlite3
from streamlit.components.v1 import html

# --- Page Config ---
st.set_page_config(page_title="Jagadeeshreddy's Portfolio", page_icon=":wave:", layout="wide")

# --- Default Font ---
font_family_css = "'Poppins', sans-serif"

# --- Custom CSS ---
custom_css = f"""
<style>
html, body, .stApp {{
    font-family: {font_family_css};
    color: #222;
    background-color: #f4f4f4;
}}

h1, h2, h3, h4, h5, h6 {{
    font-weight: 600;
    color: #222;
}}

.stButton button {{
    background-color: #007bff;
    color: white;
    border: none;
    font-size: 15px;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    font-weight: 500;
    transition: background-color 0.3s ease;
}}

.stButton button:hover {{
    background-color: #0056b3;
}}

.stTable th, .stTable td {{
    text-align: left;
    padding: 8px;
    font-size: 15px;
    color: #222;
}}

/* Smooth scrolling */
html {{
    scroll-behavior: smooth;
}}

/* Section styling */
.section {{
    padding: 2rem 1.5rem;
    margin: 1rem 0;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}}

.section:hover {{
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}}

/* Alternate section colors */
#home {{
    background-color: #f8f9fa;
}}

#about {{
    background-color: #f1f8fe;
}}

#experiences {{
    background-color: #f8f9fa;
}}

#projects {{
    background-color: #f1f8fe;
}}

#skills {{
    background-color: #f8f9fa;
}}

#certifications {{
    background-color: #f1f8fe;
}}

#contact {{
    background-color: #f8f9fa;
}}

/* Hide anchor links */
.anchor-link {{
    position: relative;
    top: -80px;
    visibility: hidden;
}}

/* Sidebar styling */
.sidebar {{
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

/* Navigation tags styling */
.nav-tags-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.5rem;
}}

.nav-tag {{
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #e9ecef;
    color: #495057;
    border-radius: 20px;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
    border: 1px solid #dee2e6;
}}

.nav-tag:hover {{
    background-color: #dee2e6;
    color: #212529;
    transform: translateY(-2px);
}}

.nav-tag.active {{
    background-color: #007bff;
    color: white;
    border-color: #007bff;
}}

/* Skills section styling */
.category {{
    margin-bottom: 30px;
}}

.category-title {{
    font-size: 22px;
    font-weight: 600;
    color: #333333;
    margin-bottom: 10px;
    border-left: 4px solid #4CAF50;
    padding-left: 10px;
}}

.skills {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}}

.skill-box {{
    background-color: #e0f7fa;
    color: #004d40;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    transition: background-color 0.3s;
}}

.skill-box:hover {{
    background-color: #b2ebf2;
}}

/* Certifications styling */
.cert-container {{
    margin-bottom: 30px;
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    font-family: {font_family_css};
}}

.cert-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}}

.cert-title {{
    font-weight: 600;
    font-size: 1.1rem;
    color: #2E86AB;
}}

.cert-issuer {{
    font-weight: 500;
    color: #555;
}}

.cert-date {{
    color: #777;
    font-size: 0.9rem;
}}

.cert-description {{
    margin-top: 10px;
    color: #444;
    line-height: 1.5;
}}

.cert-link {{
    margin-top: 10px;
    display: inline-block;
    padding: 6px 12px;
    background-color: #e0f7fa;
    color: #006064;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
}}

.cert-link:hover {{
    background-color: #b2ebf2;
    color: #004d40;
}}

/* Contact form styling */
.contact-form input,
.contact-form textarea {{
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: {font_family_css};
}}

.contact-form textarea {{
    height: 150px;
}}

.contact-form button {{
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: {font_family_css};
    transition: background-color 0.3s;
}}

.contact-form button:hover {{
    background-color: #0056b3;
}}

/* Top navigation styling */
.top-nav-container {{
    position: fixed;
    top: 10px;
    right: 20px;
    background-color: rgba(255, 255, 255, 0.95);
    padding: 10px 15px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    z-index: 9999;
    display: flex;
    gap: 10px;
}}

.top-nav-tag {{
    text-decoration: none;
    padding: 8px 12px;
    color: #333;
    font-weight: 500;
    border-radius: 4px;
    transition: background-color 0.3s, color 0.3s;
    font-family: {font_family_css};
}}

.top-nav-tag:hover {{
    background-color: #f0f0f0;
    color: #000;
}}

.top-nav-tag.active {{
    background-color: #0066cc;
    color: white;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- JavaScript for scrolling ---
def scroll_to(section_id):
    js = f"""
    <script>
        document.getElementById('{section_id}').scrollIntoView({{ behavior: 'smooth' }});
        document.querySelectorAll('.nav-tag, .top-nav-tag').forEach(tag => {{
            tag.classList.remove('active');
            if(tag.getAttribute('data-section') === '{section_id}') {{
                tag.classList.add('active');
            }}
        }});
    </script>
    """
    html(js)

# --- DB Setup ---
conn = sqlite3.connect("portfolio.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    company TEXT,
    dates TEXT,
    technologies TEXT
)
''')
conn.commit()

# --- Sidebar Navigation ---
def add_sidebar():
    st.sidebar.image("images/IMG_7317.JPG", width=150)

    st.sidebar.markdown("""
    <div style="text-align:center; margin-bottom: 20px;">
        <h2 style="margin-bottom: 5px;">Jagadeeshreddy Kotha</h2>
        <p style="color: #666; margin-top: 0;">Software Engineer</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation tags in sidebar
    st.sidebar.markdown("""
    <div class="sidebar">
        <div class="nav-tags-container">
            <a href="#home" class="nav-tag active" data-section="home">Home</a>
            <a href="#about" class="nav-tag" data-section="about">About</a>
            <a href="#experiences" class="nav-tag" data-section="experiences">Experiences</a>
            <a href="#projects" class="nav-tag" data-section="projects">Projects</a>
            <a href="#skills" class="nav-tag" data-section="skills">Skills</a>
            <a href="#certifications" class="nav-tag" data-section="certifications">Certifications</a>
            <a href="#contact" class="nav-tag" data-section="contact">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Navigation Tags (Top Right) ---
def add_nav_tags():
    st.markdown("""
    <div class="top-nav-container">
        <a href="#home" class="top-nav-tag active" data-section="home">Home</a>
        <a href="#about" class="top-nav-tag" data-section="about">About</a>
        <a href="#experiences" class="top-nav-tag" data-section="experiences">Experiences</a>
        <a href="#projects" class="top-nav-tag" data-section="projects">Projects</a>
        <a href="#skills" class="top-nav-tag" data-section="skills">Skills</a>
        <a href="#certifications" class="top-nav-tag" data-section="certifications">Certifications</a>
        <a href="#contact" class="top-nav-tag" data-section="contact">Contact</a>
    </div>
    """, unsafe_allow_html=True)

# --- Sections ---
def show_home_section():
    st.markdown('<div class="anchor-link" id="home"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("👋 Welcome to My Portfolio")
    st.markdown("""
    ### Hello, I'm Jagadeeshreddy  
    A passionate **Software Engineer** specializing in **AI/ML, Web Development, and System Design**.
    
    I design and build intelligent, scalable solutions to solve real-world problems through innovative technology.  
    Whether it's a deep learning model or a full-stack application, I bring ideas to life with precision and creativity.
    """)

    st.markdown("---")
    st.subheader("🔍 What You'll Find Here:")
    st.markdown("""
    - **About**: My background, education, and interests  
    - **Experiences**: Professional roles and key contributions  
    - **Projects**: Selected technical projects and case studies  
    - **Skills**: Tools, technologies, and domains I work with  
    - **Certifications**: Professional credentials and qualifications
    - **Contact**: Let's connect!
    """)

    st.markdown("---", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="background-color: #d9edf7; padding: 10px; border-radius: 5px;">
            <span style="color: black;">📢 <em>Feel free to explore the app and reach out if you're interested in collaborating!</em></span>
        </div>
        """,
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_about_section():
    st.markdown('<div class="anchor-link" id="about"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("🙋‍♂️ About Me")
    st.write("""
    ### Software Engineer
    Passionate and detail-oriented Software Engineer with expertise in Artificial Intelligence and Machine Learning.
    Strong foundation in data structures, algorithms, and software development.
    Experienced in developing AI-driven applications, implementing deep learning models,
    and optimizing machine learning algorithms.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🎓 Education")
        st.markdown("""
        **B.Tech - Computer Science & Engineering**  
        Annamacharya Institute of Technology & Sciences, Hyderabad  
        *2019 - 2023*  
        
        **Intermediate (MPC)**  
        Narayana Jr. College, Hyderabad  
        *2017 - 2019*
        """)

    with col2:
        st.write("### 📌 Interests")
        st.markdown("""
        - AI & Machine Learning
        - Web & App Development
        - Data Science and Analytics
        - Cloud Computing
        - Open Source Contributions
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_experiences_section():
    st.markdown('<div class="anchor-link" id="experiences"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("👨🏽‍💻 Professional Experience")
    
    with st.expander("Software Engineer | Lyros Technologies Private Limited (FEB 2025 – Present)", expanded=True):
        st.markdown("""
        - Participating in a structured training program focused on Artificial Intelligence and Machine Learning (AI/ML)
        - Developing expertise in key AI/ML skills and technologies, including Python, scikit-learn, deep learning
        - Engaging in hands-on projects to apply theoretical AI/ML knowledge in real-world scenarios
        - Collaborating with industry professionals and mentors to enhance technical and professional competencies
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_projects_section():
    st.markdown('<div class="anchor-link" id="projects"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("📁 My Projects")
    
    projects = [
        {
            "title": "Abnormal Driving Assessment System",
            "description": """
**Project Duration:** June 2022 - December 2022  
**Overview:**  
Developed a computer vision system that detects and classifies abnormal driving behaviors in real-time using deep learning. The system analyzes driver actions through video feeds to identify dangerous activities like phone usage, drowsiness, and lane departures, generating immediate audio-visual alerts.

**Key Features:**
- Real-time behavior detection at 24 FPS
- 87.44% classification accuracy
- Configurable alert system
- User-friendly dashboard

**Technologies Used:**  
- Computer Vision: OpenCV, YOLOv8
- Deep Learning: TensorFlow/Keras
- Backend: Python
- GUI: Tkinter, Pygame
""",
            "tech": ["OpenCV", "YOLOv8", "TensorFlow", "Python", "Tkinter", "Pygame"],
            "github": "https://github.com/KothaJagadeeshreddy/Abnormal-Driving-Asessment.git"
        },
        {
            "title": "Personal Voice Assistant",
            "description": """
**Project Duration:** January 2023 - July 2023  
**Overview:**  
Built a voice-activated assistant to perform tasks such as answering questions, setting reminders, playing music, and controlling smart devices using speech recognition and NLP.

**Key Features:**
- ~85% command recognition accuracy
- Integrated with multiple APIs (weather, search, email)
- Fast response time (0.8s average)
- Customizable wake word

**Technologies Used:**  
- Speech Recognition: SpeechRecognition, pyttsx3
- NLP: Keyword matching and OpenAI
- Automation: Selenium
- Backend: Python
""",
            "tech": ["Python", "SpeechRecognition", "pyttsx3", "gTTS", "OpenAI API", "Selenium"],
            "github": "https://github.com/KothaJagadeeshreddy/PERSONAL-VOICE-ASSISSTANT.git"
        },
    ]

    for project in projects:
        with st.expander(f"🚀 {project['title']}"):
            st.markdown(project["description"])
            st.markdown(f"**Technologies:** {', '.join(project['tech'])}")
            st.markdown(f"[View on GitHub]({project['github']})")
    
    st.markdown('</div>', unsafe_allow_html=True)

def skills_section():
    st.markdown('<div class="anchor-link" id="skills"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("🧠 Skills & Technologies")

    html_code = f'''
    <div class="category">
        <div class="category-title">Programming Languages</div>
        <div class="skills">
            <div class="skill-box">Python</div>
            <div class="skill-box">Java</div>
            <div class="skill-box">C++</div>
            <div class="skill-box">JavaScript</div>
            <div class="skill-box">SQL</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">AI/ML Technologies</div>
        <div class="skills">
            <div class="skill-box">Machine Learning</div>
            <div class="skill-box">Deep Learning</div>
            <div class="skill-box">Natural Language Processing (NLP)</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">Frameworks & Libraries</div>
        <div class="skills">
            <div class="skill-box">Spring</div>
            <div class="skill-box">Scikit-learn</div>
            <div class="skill-box">Keras</div>
            <div class="skill-box">Matplotlib</div>
            <div class="skill-box">Pandas</div>
            <div class="skill-box">NumPy</div>
            <div class="skill-box">Seaborn</div>
            <div class="skill-box">Streamlit</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">Web Development</div>
        <div class="skills">
            <div class="skill-box">React</div>
            <div class="skill-box">Node.js</div>
            <div class="skill-box">HTML5</div>
            <div class="skill-box">CSS3</div>
            <div class="skill-box">Flask</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">Databases</div>
        <div class="skills">
            <div class="skill-box">MySQL</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">Tools & Platforms</div>
        <div class="skills">
            <div class="skill-box">Git/GitHub</div>
            <div class="skill-box">Docker</div>
            <div class="skill-box">Kubernetes</div>
            <div class="skill-box">AWS</div>
        </div>
    </div>

    <div class="category">
        <div class="category-title">Other</div>
        <div class="skills">
            <div class="skill-box">System Design</div>
            <div class="skill-box">Data Structures & Algorithms</div>
            <div class="skill-box">Problem Solving</div>
        </div>
    </div>
    '''
    st.markdown(html_code, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_certifications_section():
    st.markdown('<div class="anchor-link" id="certifications"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("📜 Certifications & Achievements")
    
    certifications = [
        {
            "title": "Full Stack Development Certification",
            "issuer": "Bosscoder Academy",
            "date": "Issued 2024",
            "description": "Completed comprehensive training in full-stack development, covering front-end and back-end technologies, system design, and deployment strategies.",
            "link": "#",
            "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "System Design", "Docker", "AWS","Data Structures & Algorithms"]
        },
        {
            "title": "Machine Learning Certification",
            "issuer": "Udemy",
            "date": "Issued 2025",
            "description": "Completed hands-on training in machine learning algorithms, model evaluation, and practical implementation using Python and scikit-learn.",
            "link": "#",
            "skills": ["Machine Learning", "Python", "Scikit-learn", "Neural Networks", "Data Preprocessing"]
        }
    ]
    
    for cert in certifications:
        st.markdown(f"""
        <div class="cert-container">
            <div class="cert-header">
                <div>
                    <div class="cert-title">{cert['title']}</div>
                    <div class="cert-issuer">{cert['issuer']}</div>
                </div>
                <div class="cert-date">{cert['date']}</div>
            </div>
            <div class="cert-description">
                {cert['description']}
            </div>
            <div style="margin-top: 10px;">
                <strong>Skills:</strong> {', '.join(cert['skills'])}
            </div>
            <a href="{cert['link']}" target="_blank" class="cert-link">View Credential</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_contact_section():
    st.markdown('<div class="anchor-link" id="contact"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("📨 Contact Me") 
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Let's Connect!
        Interested in collaborating or have questions? Feel free to reach out through the form or my social profiles.
        """)
        
        contact_form = """
        <form action="https://formsubmit.co/kothajagadeeshreddy123@gmail.com" method="POST" class="contact-form">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message" required></textarea>
            <button type="submit">Send Message</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### Contact Information
        **Email:**  
        [kothajagadeeshreddy123@gmail.com](mailto:kothajagadeeshreddy123@gmail.com)
        
        **Social Profiles:**  
        [LinkedIn](https://www.linkedin.com/in/jagadeeshreddy-kotha)  
        [GitHub](https://github.com/KothaJagadeeshreddy)  
        
        **Location:**  
        Hyderabad, India
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main App ---
def main():
    add_sidebar()
    add_nav_tags()
    
    # Display all sections with scroll functionality
    show_home_section()
    show_about_section()
    show_experiences_section()
    show_projects_section()
    skills_section()
    show_certifications_section()
    show_contact_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; font-size:16px; padding:20px;">
            Crafted with ❤️ using Python and Streamlit. © 2025 Jagadeeshreddy Kotha
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()