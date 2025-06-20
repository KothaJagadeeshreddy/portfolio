import streamlit as st
import sqlite3
from streamlit.components.v1 import html
import random
import time

# --- Page Config ---
st.set_page_config(
    page_title="Jagadeeshreddy's Portfolio", 
    page_icon=":rocket:", 
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Default Font ---
font_family_css = "'Poppins', sans-serif"

# --- Custom CSS ---
# --- Custom CSS ---
custom_css = f"""
    <style>
    html, body, .stApp {{
        font-family: {font_family_css};
        color: #222;
        background-color: #f4f4f4;
        line-height: 1.6;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700;
        color: #222;
        margin-top: 0;
    }}

    .stButton button {{
        background: linear-gradient(135deg, #0066cc, #00aaff);
        color: white;
        border: none;
        font-size: 15px;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}

    .stButton button:hover {{
        background: linear-gradient(135deg, #004d99, #0088cc);
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }}

    .stTable th, .stTable td {{
        text-align: left;
        padding: 12px;
        font-size: 15px;
        color: #222;
    }}

    /* Smooth scrolling */
    html {{
        scroll-behavior: smooth;
    }}

    /* Section styling - Updated with gradient backgrounds */
    .section {{
        padding: 3rem 2.5rem;
        margin: 2rem 0;
        border-radius: 16px;
        background: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        border-left: 6px solid;
    }}

    .section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(to bottom, var(--accent-color), var(--accent-color-light));
    }}

    .section:hover {{
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
        transform: translateY(-8px);
    }}

    /* Section-specific colors with CSS variables */
    #home {{
        --accent-color: #0066cc;
        --accent-color-light: #00ccff;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
    }}

    #about {{
        --accent-color: #4CAF50;
        --accent-color-light: #8BC34A;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f1f8fe 0%, #e3f2fd 100%);
    }}

    #experiences {{
        --accent-color: #FF5722;
        --accent-color-light: #FF9800;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f8f9fa 0%, #eceff1 100%);
    }}

    #projects {{
        --accent-color: #9C27B0;
        --accent-color-light: #E91E63;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f1f8fe 0%, #ede7f6 100%);
    }}

    #skills {{
        --accent-color: #009688;
        --accent-color-light: #4DB6AC;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f8f9fa 0%, #e0f2f1 100%);
    }}

    #certifications {{
        --accent-color: #673AB7;
        --accent-color-light: #9C27B0;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f1f8fe 0%, #f3e5f5 100%);
    }}

    #contact {{
        --accent-color: #00BCD4;
        --accent-color-light: #4DD0E1;
        border-left-color: var(--accent-color);
        background: linear-gradient(135deg, #f1f8fe 0%, #e0f7fa 100%);
    }}

    /* Hide anchor links */
    .anchor-link {{
        position: relative;
        top: -80px;
        visibility: hidden;
    }}

    /* Sidebar styling */
    .sidebar {{
        background: linear-gradient(135deg, #f8f9fa 0%, #eceff1 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 6px solid #0066cc;
    }}

    /* Navigation tags styling */
    .nav-tags-container {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 2rem;
    }}

    .nav-tag {{
        display: inline-block;
        padding: 1rem 1.5rem;
        background-color: #f0f4f8;
        color: #495057;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        border: none;
        width: 100%;
        text-align: left;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}

    .nav-tag:hover {{
        background: linear-gradient(135deg, #e0e6eb, #d1d8e0);
        color: 	#d62828;
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .nav-tag.active {{
        background: linear-gradient(135deg, #0066cc, #00aaff);
        color: white;
        box-shadow: 0 4px 12px rgba(0,102,204,0.2);
    }}

    /* Skills section styling */
    .category {{
        margin-bottom: 40px;
    }}

    .category-title {{
        font-size: 24px;
        font-weight: 700;
        color: var(--accent-color);
        margin-bottom: 15px;
        padding-left: 15px;
        border-left: 6px solid var(--accent-color);
    }}

    .skills {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }}

    .skill-box {{
        background: linear-gradient(135deg, var(--accent-color-light), var(--accent-color));
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }}

    .skill-box:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}

    /* Certifications styling */
    .cert-container {{
        margin-bottom: 40px;
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        font-family: {font_family_css};
        transition: all 0.3s ease;
        border-left: 6px solid var(--accent-color);
        position: relative;
        overflow: hidden;
    }}

    .cert-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(to bottom, var(--accent-color), var(--accent-color-light));
    }}

    .cert-container:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    }}

    .cert-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }}

    .cert-title {{
        font-weight: 700;
        font-size: 1.4rem;
        color: var(--accent-color);
    }}

    .cert-issuer {{
        font-weight: 600;
        color: #555;
        margin-top: 8px;
    }}

    .cert-date {{
        color: white;
        font-size: 0.9rem;
        background: linear-gradient(135deg, var(--accent-color), var(--accent-color-light));
        padding: 6px 12px;
        border-radius: 20px;
    }}

    .cert-description {{
        margin-top: 20px;
        color: #444;
        line-height: 1.7;
        font-size: 1.05rem;
    }}

    .cert-link {{
        margin-top: 20px;
        display: inline-block;
        padding: 10px 20px;
        background: linear-gradient(135deg, var(--accent-color), var(--accent-color-light));
        color: white;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    .cert-link:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}

    /* Project cards */
    .project-card {{
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        transition: all 0.3s ease;
        border-left: 6px solid var(--accent-color);
        position: relative;
        overflow: hidden;
    }}

    .project-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(to bottom, var(--accent-color), var(--accent-color-light));
    }}

    .project-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    }}

    .project-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--accent-color);
        margin-bottom: 15px;
    }}

    .project-tech {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }}

    .tech-tag {{
        background: linear-gradient(135deg, var(--accent-color-light), var(--accent-color));
        color: white;
        padding: 6px 14px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
    }}

    .project-links {{
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }}

    .project-link {{
        padding: 8px 16px;
        background: linear-gradient(135deg, var(--accent-color), var(--accent-color-light));
        color: white;
        border-radius: 8px;
        text-decoration: none;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    .project-link:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}

    /* Contact form styling */
    .contact-form input,
    .contact-form textarea {{
        width: 100%;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-family: {font_family_css};
        transition: all 0.3s;
        font-size: 1rem;
    }}

    .contact-form input:focus,
    .contact-form textarea:focus {{
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(var(--accent-color-rgb), 0.1);
        outline: none;
    }}

    .contact-form textarea {{
        height: 180px;
        resize: vertical;
    }}

    .contact-form button {{
        padding: 15px 30px;
        background: linear-gradient(135deg, var(--accent-color), var(--accent-color-light));
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-family: {font_family_css};
        transition: all 0.3s;
        font-weight: 600;
        width: 100%;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    .contact-form button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}

    .form-success {{
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        display: none;
        text-align: center;
        font-weight: 600;
    }}

    /* Top navigation styling */
    .top-nav-container {{
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: rgba(255, 255, 255, 0.98);
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        z-index: 9999;
        display: flex;
        gap: 15px;
        backdrop-filter: blur(8px);
    }}

    .top-nav-tag {{
        text-decoration: none;
        padding: 10px 16px;
        color: #333;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s;
        font-family: {font_family_css};
        font-size: 1rem;
    }}

    .top-nav-tag:hover {{
        background: linear-gradient(135deg, #f0f0f0, #e0e0e0);
        color: #000;
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    /* Stats cards */
    .stats-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
    }}

    .stat-card {{
        flex: 1;
        min-width: 180px;
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s;
        border-left: 6px solid var(--accent-color);
    }}

    .stat-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    }}

    .stat-value {{
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--accent-color);
        margin-bottom: 10px;
    }}

    .stat-label {{
        font-size: 1.1rem;
        color: #666;
        font-weight: 600;
    }}

    /* Animation */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .section {{
        animation: fadeIn 0.8s ease-out forwards;
    }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .top-nav-container {{
            display: none;
        }}
        
        .section {{
            padding: 2rem 1.5rem;
        }}
        
        .stat-card {{
            min-width: 100%;
        }}
    }}
    </style>"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- JavaScript for scrolling and form handling ---
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
        
        // Store current section in session storage
        sessionStorage.setItem('currentSection', '{section_id}');
    </script>
    """
    html(js)

def show_form_success():
    js = """
    <script>
        document.querySelector('.form-success').style.display = 'block';
        setTimeout(() => {
            document.querySelector('.form-success').style.display = 'none';
        }, 5000);
    </script>
    """
    html(js)

# --- DB Setup ---
conn = sqlite3.connect("portfolio.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
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

cursor.execute('''
CREATE TABLE IF NOT EXISTS testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    title TEXT,
    content TEXT,
    avatar TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    authors TEXT,
    venue TEXT,
    year TEXT,
    link TEXT,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    excerpt TEXT,
    link TEXT,
    read_time TEXT
)
''')

# --- Sidebar Navigation ---
def add_sidebar():
    #st.sidebar.image("images/IMG_7317.JPG", width=150, caption="Jagadeeshreddy Kotha")

    st.sidebar.markdown("""
    <div style="text-align:center; margin-bottom: 20px;">
        <h2 style="margin-bottom: 5px;">Jagadeeshreddy Kotha</h2>
        <p style="color: #666; margin-top: 0;">AI/ML Engineer & Full Stack Developer</p>
        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
            <a href="https://github.com/KothaJagadeeshreddy" target="_blank" style="color: black; font-size: 24px;"><i class="fab fa-github"></i></a>
            <a href="https://www.linkedin.com/in/jagadeeshreddy-kotha" target="_blank" style="color: #0077b5; font-size: 24px;"><i class="fab fa-linkedin"></i></a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation tags in sidebar
    st.sidebar.markdown("""
    <div class="sidebar">
        <div class="nav-tags-container">
            <a href="#home" class="nav-tag active" data-section="home">🏠 Home</a>
            <a href="#about" class="nav-tag" data-section="about">👤 About</a>
            <a href="#experiences" class="nav-tag" data-section="experiences">💼 Experiences</a>
            <a href="#projects" class="nav-tag" data-section="projects">📁 Projects</a>
            <a href="#skills" class="nav-tag" data-section="skills">🛠 Skills</a>
            <a href="#certifications" class="nav-tag" data-section="certifications">🏆 Certifications</a>
            <a href="#contact" class="nav-tag" data-section="contact">📨 Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar footer
    st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 20px; font-size: 0.8rem; color: #666;">
        © 2025 Jagadeeshreddy Kotha<br>
        Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# --- Navigation Tags (Top Right) ---
def add_nav_tags():
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Sections ---
def show_home_section():
    st.markdown('<div class="anchor-link" id="home"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            ### 👋Hello, I'm Jagadeeshreddy  
    A passionate **Software Engineer** specializing in **AI/ML, Web Development, and System Design**.
    
    I design and build intelligent, scalable solutions to solve real-world problems through innovative technology.  
    Whether it's a deep learning model or a full-stack application, I bring ideas to life with precision and creativity.""")
        st.subheader("🔍 What You'll Find Here:")
        st.markdown("""
            - **About**: My background, education, and interests  
            - **Experiences**: Professional roles and key contributions  
            - **Projects**: Selected technical projects and case studies  
            - **Skills**: Tools, technologies, and domains I work with  
            - **Certifications**: Professional credentials and qualifications
            - **Contact**: Let's connect!
            """)        
        st.markdown("""
        <div style="margin-top: 30px;">
            <a href="#contact" class="nav-tag" style="display: inline-block; text-decoration: none; margin-right: 10px;">
                Get In Touch <i class="fas fa-arrow-right"></i>
            </a>
            <a href="https://github.com/KothaJagadeeshreddy" target="_blank" class="nav-tag" style="display: inline-block; text-decoration: none;">
                View My Work <i class="fab fa-github"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("images/IMG_7317.JPG", width=250, caption="Jagadeeshreddy Kotha")
    
    st.markdown("---")
    
    # Stats section
    st.subheader("📊 My Stats")
    col1, col2   = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">2</div>
            <div class="stat-label">Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">2</div>
            <div class="stat-label">Certifications</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_about_section():
    st.markdown('<div class="anchor-link" id="about"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.title("🙋‍♂️ About Me")
    
    st.markdown("""
        ### Who Am I?
        
        I'm a passionate **Software Engineer** specializing in **Artificial Intelligence and Machine Learning**, 
        with strong expertise in **Full Stack Development**. I love turning complex problems into elegant solutions 
        through code and algorithms.
        
        With a solid foundation in **data structures, algorithms, and system design**, I enjoy building 
        intelligent systems that can learn and adapt. My goal is to create technology that makes a 
        meaningful impact on people's lives.
        """)
        
    st.markdown("""
        ### My Approach
        
        - 🔍 **Problem-first mindset**: Understand the problem deeply before jumping to solutions
        - 🛠 **Right tools for the job**: Choose technologies based on requirements, not trends
        - 📈 **Data-driven decisions**: Let metrics guide development and improvements
        - 🤝 **Collaborative spirit**: Work effectively in teams and communicate clearly
        """)
    
    
    st.markdown("---")
    
    st.subheader("🎓 Education")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **B.Tech - Computer Science & Engineering**  
        *Annamacharya Institute of Technology & Sciences, Hyderabad*  
        *2019 - 2023*  
        - GPA: 6.7/10  
        - Specialization in computer science and engineering  
        - Final Year Project: Abnormal Driving Assessment
        """)
    
    with col2:
        st.markdown("""
        **Intermediate (MPC)**  
        *Narayana Jr. College, Hyderabad*  
        *2017 - 2019*  
        - Percentage: 95%  
        - Focus on Mathematics, Physics, Chemistry
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_experiences_section():
    st.markdown('<div class="anchor-link" id="experiences"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("👨‍💻 Professional Experience")
    
    with st.expander("🚀 Software Engineer | Lyros Technologies Private Limited (FEB 2025 – Present)", expanded=True):
        st.markdown("""
        * Designed and implemented **end-to-end machine learning pipelines** including data collection, preprocessing, feature engineering, model training, and evaluation for real-world AI applications.
        * Developed and fine-tuned **supervised and unsupervised models** (Regression, Classification, Clustering, NLP) using **Scikit-learn, TensorFlow, and PyTorch**, resulting in a **10% increase in model accuracy**.
        * Applied **hyperparameter tuning**, **cross-validation**, and **ensemble methods** to optimize performance, reducing model inference time by **12%**.
        * Built **automated data pipelines** using **Pandas, NumPy, and SQL** to clean and process large-scale datasets, improving data efficiency by **15%**.
        * Created **interactive data visualizations** with **Matplotlib, Seaborn, and Plotly** to derive insights and support strategic decision-making.
        * Performed **statistical analysis**, including **hypothesis testing** and **A/B testing**, to validate model performance and assess business impact.
        * Deployed ML models as **scalable APIs** using **Flask, FastAPI, and Streamlit**, delivering intuitive, user-friendly interfaces.
        * Containerized applications using **Docker** and managed microservices deployment with **Minikube (Kubernetes)**.
        * Set up **CI/CD pipelines** using **GitHub Actions** and deployed applications seamlessly to the cloud with **Render**.
        * Collaborated using **Agile methodologies**, leveraging tools like **Jira** and **GitHub Projects** for sprint planning and progress tracking.
        * Tracked experiments and ensured reproducibility with **MLflow** and **Weights & Biases (W\&B)**.
        * Conducted thorough **code reviews**, maintained clean, modular codebases, and used **Git/GitHub** for version control and collaboration.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_projects_section():
    st.markdown('<div class="anchor-link" id="projects"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("📁 My Projects")
    
    projects = [
        {
            "title": "Abnormal Driving Assessment ",
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
            "tech": ["Python", "OpenCV", "YOLOv8", "TensorFlow", "Keras", "Tkinter", "Pygame"],
            "github": "https://github.com/KothaJagadeeshreddy/Abnormal-Driving-Asessment.git",
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
    - NLP: Keyword Matching, OpenAI  
    - Automation: Selenium  
    - Backend: Python
    """,
            "tech": ["Python", "SpeechRecognition", "pyttsx3", "OpenAI API", "Selenium"],
            "github": "https://github.com/KothaJagadeeshreddy/PERSONAL-VOICE-ASSISSTANT.git",
        }
    ]


    for project in projects:
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">{project['title']}</div>
            <div>{project['description']}</div>
            <div class="project-tech">
                {''.join([f'<span class="tech-tag">{tech}</span>' for tech in project['tech']])}
            </div>
            <div class="project-links">
                <a href="{project['github']}" target="_blank" class="project-link">
                    <i class="fab fa-github"></i> Code
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def skills_section():
    st.markdown('<div class="anchor-link" id="skills"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.title("🧠 Skills & Technologies")

    # Custom CSS for better alignment
    st.markdown("""
    <style>
        .skill-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 5px;
        }
        .skill-img {
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ----------- Programming Languages -----------
    st.markdown("### 💻 Programming Languages")
    lang_logos = {
        "Python": "https://img.icons8.com/color/48/000000/python.png",
        "Java": "https://img.icons8.com/color/48/000000/java-coffee-cup-logo.png",
        "C++": "https://img.icons8.com/color/48/000000/c-plus-plus-logo.png",
        "JavaScript": "https://img.icons8.com/color/48/000000/javascript.png",
        "SQL": "https://img.icons8.com/ios-filled/50/000000/sql.png"
    }
    cols = st.columns(len(lang_logos))
    for col, (lang, url) in zip(cols, lang_logos.items()):
        with col:
            st.markdown(f"""
            <div class="skill-container">
                <img class="skill-img" src="{url}" width="40">
                <div>{lang}</div>
            </div>
            """, unsafe_allow_html=True)

    # ----------- AI/ML -----------
    st.markdown("### 🤖 AI / ML")
    ml_logos = {
        "TensorFlow": "https://img.icons8.com/color/48/000000/tensorflow.png",
        "PyTorch": "https://img.icons8.com/color/48/pytorch.png",
        "scikit-learn": "https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg",
        "Pandas": "https://img.icons8.com/color/48/000000/pandas.png",
        "NumPy": "https://img.icons8.com/color/48/000000/numpy.png"
    }
    cols = st.columns(len(ml_logos))
    for col, (lib, url) in zip(cols, ml_logos.items()):
        with col:
            st.markdown(f"""
            <div class="skill-container">
                <img class="skill-img" src="{url}" width="40">
                <div>{lib}</div>
            </div>
            """, unsafe_allow_html=True)

    # ----------- Web Development -----------
    st.markdown("### 🌐 Web Development")
    web_logos = {
        "HTML": "https://img.icons8.com/color/48/000000/html-5.png",
        "CSS": "https://img.icons8.com/color/48/000000/css3.png",
        "JavaScript": "https://img.icons8.com/color/48/000000/javascript.png",
        "React": "https://img.icons8.com/color/48/000000/react-native.png",
        "Streamlit": "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png"
    }
    cols = st.columns(len(web_logos))
    for col, (tool, url) in zip(cols, web_logos.items()):
        with col:
            st.markdown(f"""
            <div class="skill-container">
                <img class="skill-img" src="{url}" width="40">
                <div>{tool}</div>
            </div>
            """, unsafe_allow_html=True)

    # ----------- Frameworks & Libraries -----------
    st.markdown("### 📚 Frameworks & Libraries")
    fw_logos = {
        "Flask": "https://img.icons8.com/ios-filled/50/000000/flask.png",
        "Django": "https://img.icons8.com/color/48/000000/django.png",
        "FastAPI": "https://cdn.worldvectorlogo.com/logos/fastapi-1.svg",
        "OpenCV": "https://img.icons8.com/color/48/000000/opencv.png"
    }
    cols = st.columns(len(fw_logos))
    for col, (fw, url) in zip(cols, fw_logos.items()):
        with col:
            st.markdown(f"""
            <div class="skill-container">
                <img class="skill-img" src="{url}" width="40">
                <div>{fw}</div>
            </div>
            """, unsafe_allow_html=True)

    # ----------- Tools & Platforms -----------
    st.markdown("### 🛠 Tools & Platforms")
    tools_logos = {
        "Git": "https://img.icons8.com/color/48/000000/git.png",
        "GitHub": "https://img.icons8.com/ios-glyphs/48/000000/github.png",
        "Docker": "https://img.icons8.com/color/48/000000/docker.png",
        "VS Code": "https://img.icons8.com/color/48/000000/visual-studio-code-2019.png",
        "Linux": "https://img.icons8.com/color/48/000000/linux.png"
    }
    cols = st.columns(len(tools_logos))
    for col, (tool, url) in zip(cols, tools_logos.items()):
        with col:
            st.markdown(f"""
            <div class="skill-container">
                <img class="skill-img" src="{url}" width="40">
                <div>{tool}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

def show_certifications_section():
    st.markdown('<div class="anchor-link" id="certifications"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    st.title("🏆 Certifications & Achievements")
    
    certifications = [
        {
            "title": "Full Stack Development Certification",
            "issuer": "Bosscoder Academy",
            "date": "Issued 2024",
            "description": "Completed comprehensive training in full-stack development, covering front-end and back-end technologies, system design, and deployment strategies. The program included hands-on projects building scalable web applications with modern frameworks.",
            "link": "https://storage.googleapis.com/bosscoderplatformindia.appspot.com/Completion_Certificates/Jagadeeshreddy%20Kotha_Transformer.pdf",
            "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "System Design", "Docker", "AWS", "Data Structures & Algorithms"]
        },
        {
            "title": "Machine Learning Certification",
            "issuer": "Udemy",
            "date": "Issued 2025",
            "description": "Completed hands-on training in machine learning algorithms, model evaluation, and practical implementation using Python and scikit-learn. Covered topics from linear regression to deep learning and model deployment.",
            "link": "https://www.udemy.com/certificate/UC-ec15fd9e-78e3-4c1a-b4d7-05cd13d79a11",
            "skills": ["Machine Learning", "Python", "Scikit-learn", "Neural Networks", "Data Preprocessing", "Model Evaluation"]
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
                <strong>Skills Validated:</strong> {', '.join(cert['skills'])}
            </div>
            <a href="{cert['link']}" target="_blank" class="cert-link">
                <i class="fas fa-external-link-alt"></i> View Credential
            </a>
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
        I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
        """)
        
        contact_form = """
        <form action="https://formsubmit.co/kothajagadeeshreddy123@gmail.com" method="POST" class="contact-form">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message" required></textarea>
            <button type="submit">Send Message <i class="fas fa-paper-plane"></i></button>
        </form>
        <div class="form-success">
            <i class="fas fa-check-circle"></i> Thank you for your message! I'll get back to you soon.
        </div>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        
        if st.button("Send Test Message"):
            show_form_success()
    
    with col2:
        st.markdown("""
        ### Contact Information
        
        **Email:**  
        [kothajagadeeshreddy123@gmail.com](mailto:kothajagadeeshreddy123@gmail.com)
        
        **Social Profiles:**  
        [<i class="fab fa-linkedin"></i> LinkedIn](https://www.linkedin.com/in/jagadeeshreddy-kotha)  
        [<i class="fab fa-github"></i> GitHub](https://github.com/KothaJagadeeshreddy)  
        
        **Location:**  
        <i class="fas fa-map-marker-alt"></i> Hyderabad, India
        
        **Availability:**  
        <i class="fas fa-calendar-check"></i> Open to new opportunities
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### My Digital Presence
        
        <div style="display: flex; gap: 15px; margin-top: 20px;">
            <a href="https://github.com/KothaJagadeeshreddy" target="_blank" style="font-size: 24px; color: #333;">
                <i class="fab fa-github"></i>
            </a>
            <a href="https://www.linkedin.com/in/jagadeeshreddy-kotha" target="_blank" style="font-size: 24px; color: #0077b5;">
                <i class="fab fa-linkedin"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
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
    st.markdown("""
    <div style="text-align:center; font-size:16px; padding:20px; color: #666;">
        <p>Crafted with ❤️ using Python and Streamlit</p>
        <p>© 2025 Jagadeeshreddy Kotha. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()