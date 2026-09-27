import os
import io
import json
import html
import zipfile
import uuid
import streamlit as st
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI SVG Studio",
    page_icon="🎨",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #777;
            margin-bottom: 25px;
        }

        .result-box {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #ddd;
            background: #fafafa;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    """
    Gets API key from Streamlit secrets or environment variable.
    Never hardcode your API key inside this file.
    """

    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    return api_key


# ============================================================
# GEMINI MODEL
# ============================================================

@st.cache_resource
def get_llm(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.7,
        google_api_key=api_key
    )


# ============================================================
# AI DESIGN SPEC GENERATION
# ============================================================

def generate_design_spec(
    llm,
    topic,
    category,
    design_type,
    style,
    template,
    color_theme
):
    """
    Gemini generates the content and design specification.
    Python later converts that specification into SVG.
    """

    prompt = f"""
You are an AI graphic design assistant.

Create a structured design specification for an SVG infographic/banner.

Topic: {topic}
Category: {category}
Design Type: {design_type}
Visual Style: {style}
Requested Template: {template}
Color Theme: {color_theme}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "short attractive title",
    "subtitle": "short supporting subtitle",
    "category": "{category}",
    "design_type": "{design_type}",
    "template": "{template}",
    "style": "{style}",
    "color_theme": "{color_theme}",
    "key_points": [
        "point 1",
        "point 2",
        "point 3",
        "point 4"
    ],
    "statistic": "optional important statistic or short fact",
    "quote": "optional short quote",
    "comparison_left": "optional left comparison",
    "comparison_right": "optional right comparison"
}}

Rules:
- Keep title under 60 characters.
- Keep subtitle under 100 characters.
- Each key point should be short.
- Do not use markdown.
- Do not include SVG code.
- Do not include explanations outside JSON.
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict):
                text_parts.append(str(item.get("text", "")))
            else:
                text_parts.append(str(item))

        content = "".join(text_parts)

    content = str(content).strip()

    # Remove accidental markdown code fences
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        spec = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned invalid JSON. Please try generating again."
        )

    return spec


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value):
    """
    Safely converts text into XML-safe text.
    """

    if value is None:
        return ""

    return html.escape(str(value))


def wrap_text(text, max_chars=42):
    """
    Simple text wrapping for SVG.
    """

    words = str(text).split()

    lines = []
    current = ""

    for word in words:

        if len(current) + len(word) + 1 <= max_chars:
            if current:
                current += " "
            current += word

        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def svg_text(
    text,
    x,
    y,
    font_size=24,
    fill="#111827",
    weight="400",
    anchor="start"
):
    """
    Creates an SVG text element.
    """

    lines = wrap_text(text, 45)

    output = []

    for index, line in enumerate(lines[:3]):

        line_y = y + (index * (font_size + 8))

        output.append(
            f'<text x="{x}" y="{line_y}" '
            f'font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{font_size}" '
            f'font-weight="{weight}" '
            f'fill="{fill}" '
            f'text-anchor="{anchor}">'
            f'{clean_text(line)}</text>'
        )

    return "\n".join(output)


# ============================================================
# COLOR THEMES
# ============================================================

COLOR_THEMES = {
    "Ocean Blue": {
        "background": "#EFF6FF",
        "primary": "#2563EB",
        "secondary": "#0EA5E9",
        "dark": "#0F172A",
        "card": "#FFFFFF"
    },

    "Modern Purple": {
        "background": "#F5F3FF",
        "primary": "#7C3AED",
        "secondary": "#A855F7",
        "dark": "#1E1B4B",
        "card": "#FFFFFF"
    },

    "Green": {
        "background": "#ECFDF5",
        "primary": "#059669",
        "secondary": "#10B981",
        "dark": "#064E3B",
        "card": "#FFFFFF"
    },

    "Orange": {
        "background": "#FFF7ED",
        "primary": "#EA580C",
        "secondary": "#F97316",
        "dark": "#431407",
        "card": "#FFFFFF"
    },

    "Dark": {
        "background": "#111827",
        "primary": "#60A5FA",
        "secondary": "#A78BFA",
        "dark": "#FFFFFF",
        "card": "#1F2937"
    }
}


# ============================================================
# SVG TEMPLATE 1 - FEATURE HIGHLIGHTS
# ============================================================

def create_feature_svg(spec, colors):

    title = clean_text(spec.get("title", "AI Innovation"))
    subtitle = clean_text(spec.get("subtitle", "Technology for the future"))

    points = spec.get("key_points", [])

    point1 = clean_text(points[0] if len(points) > 0 else "Smart solutions")
    point2 = clean_text(points[1] if len(points) > 1 else "Better performance")
    point3 = clean_text(points[2] if len(points) > 2 else "Scalable systems")
    point4 = clean_text(points[3] if len(points) > 3 else "Data-driven decisions")

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200"
     height="800"
     viewBox="0 0 1200 800">

    <rect width="1200" height="800" fill="{colors['background']}"/>

    <circle cx="1060" cy="120" r="170"
            fill="{colors['secondary']}"
            opacity="0.15"/>

    <circle cx="1100" cy="700" r="220"
            fill="{colors['primary']}"
            opacity="0.10"/>

    <text x="80" y="105"
          font-family="Arial, Helvetica, sans-serif"
          font-size="24"
          font-weight="600"
          fill="{colors['primary']}">
        {clean_text(spec.get("category", "Technology"))}
    </text>

    <text x="80" y="175"
          font-family="Arial, Helvetica, sans-serif"
          font-size="52"
          font-weight="700"
          fill="{colors['dark']}">
        {title}
    </text>

    <text x="80" y="225"
          font-family="Arial, Helvetica, sans-serif"
          font-size="22"
          fill="{colors['dark']}">
        {subtitle}
    </text>

    <rect x="80" y="285" width="500" height="175"
          rx="22"
          fill="{colors['card']}"/>

    <circle cx="125" cy="330" r="18" fill="{colors['primary']}"/>
    <text x="165" y="340"
          font-family="Arial"
          font-size="23"
          font-weight="600"
          fill="{colors['dark']}">
        {point1}
    </text>

    <rect x="80" y="485" width="500" height="175"
          rx="22"
          fill="{colors['card']}"/>

    <circle cx="125" cy="530" r="18" fill="{colors['secondary']}"/>
    <text x="165" y="540"
          font-family="Arial"
          font-size="23"
          font-weight="600"
          fill="{colors['dark']}">
        {point2}
    </text>

    <rect x="640" y="285" width="480" height="175"
          rx="22"
          fill="{colors['card']}"/>

    <circle cx="685" cy="330" r="18" fill="{colors['primary']}"/>
    <text x="725" y="340"
          font-family="Arial"
          font-size="23"
          font-weight="600"
          fill="{colors['dark']}">
        {point3}
    </text>

    <rect x="640" y="485" width="480" height="175"
          rx="22"
          fill="{colors['card']}"/>

    <circle cx="685" cy="530" r="18" fill="{colors['secondary']}"/>
    <text x="725" y="540"
          font-family="Arial"
          font-size="23"
          font-weight="600"
          fill="{colors['dark']}">
        {point4}
    </text>

</svg>
"""

    return svg


# ============================================================
# SVG TEMPLATE 2 - STEP BY STEP
# ============================================================

def create_steps_svg(spec, colors):

    title = clean_text(spec.get("title", "Step by Step Guide"))
    subtitle = clean_text(spec.get("subtitle", "A simple process"))

    points = spec.get("key_points", [])

    while len(points) < 4:
        points.append("Important step")

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200"
     height="800"
     viewBox="0 0 1200 800">

    <rect width="1200" height="800" fill="{colors['background']}"/>

    <text x="600" y="90"
          text-anchor="middle"
          font-family="Arial"
          font-size="48"
          font-weight="700"
          fill="{colors['dark']}">
        {title}
    </text>

    <text x="600" y="135"
          text-anchor="middle"
          font-family="Arial"
          font-size="21"
          fill="{colors['dark']}">
        {subtitle}
    </text>

    <line x1="180" y1="390"
          x2="1020" y2="390"
          stroke="{colors['primary']}"
          stroke-width="8"
          opacity="0.3"/>

    <circle cx="180" cy="390" r="65"
            fill="{colors['primary']}"/>

    <text x="180" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="34"
          font-weight="700"
          fill="white">1</text>

    <circle cx="460" cy="390" r="65"
            fill="{colors['secondary']}"/>

    <text x="460" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="34"
          font-weight="700"
          fill="white">2</text>

    <circle cx="740" cy="390" r="65"
            fill="{colors['primary']}"/>

    <text x="740" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="34"
          font-weight="700"
          fill="white">3</text>

    <circle cx="1020" cy="390" r="65"
            fill="{colors['secondary']}"/>

    <text x="1020" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="34"
          font-weight="700"
          fill="white">4</text>

    {svg_text(points[0], 180, 510, 20, colors["dark"], "600", "middle")}
    {svg_text(points[1], 460, 510, 20, colors["dark"], "600", "middle")}
    {svg_text(points[2], 740, 510, 20, colors["dark"], "600", "middle")}
    {svg_text(points[3], 1020, 510, 20, colors["dark"], "600", "middle")}

</svg>
"""

    return svg


# ============================================================
# SVG TEMPLATE 3 - STATISTICS
# ============================================================

def create_statistics_svg(spec, colors):

    title = clean_text(spec.get("title", "Key Statistics"))
    subtitle = clean_text(spec.get("subtitle", "Important numbers at a glance"))
    statistic = clean_text(
        spec.get("statistic", "85%")
    )

    points = spec.get("key_points", [])

    while len(points) < 3:
        points.append("Important insight")

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200"
     height="800"
     viewBox="0 0 1200 800">

    <rect width="1200" height="800"
          fill="{colors['background']}"/>

    <text x="80" y="100"
          font-family="Arial"
          font-size="48"
          font-weight="700"
          fill="{colors['dark']}">
        {title}
    </text>

    <text x="80" y="145"
          font-family="Arial"
          font-size="21"
          fill="{colors['dark']}">
        {subtitle}
    </text>

    <rect x="80" y="215"
          width="1040"
          height="250"
          rx="30"
          fill="{colors['primary']}"/>

    <text x="600" y="365"
          text-anchor="middle"
          font-family="Arial"
          font-size="90"
          font-weight="700"
          fill="white">
        {statistic}
    </text>

    <text x="600" y="420"
          text-anchor="middle"
          font-family="Arial"
          font-size="24"
          fill="white">
        Featured statistic
    </text>

    <rect x="80" y="525"
          width="310"
          height="150"
          rx="20"
          fill="{colors['card']}"/>

    <rect x="445" y="525"
          width="310"
          height="150"
          rx="20"
          fill="{colors['card']}"/>

    <rect x="810" y="525"
          width="310"
          height="150"
          rx="20"
          fill="{colors['card']}"/>

    {svg_text(points[0], 235, 580, 19, colors["dark"], "600", "middle")}
    {svg_text(points[1], 600, 580, 19, colors["dark"], "600", "middle")}
    {svg_text(points[2], 965, 580, 19, colors["dark"], "600", "middle")}

</svg>
"""

    return svg


# ============================================================
# SVG TEMPLATE 4 - COMPARISON
# ============================================================

def create_comparison_svg(spec, colors):

    title = clean_text(spec.get("title", "Comparison"))
    subtitle = clean_text(spec.get("subtitle", "Compare two approaches"))

    left = clean_text(
        spec.get("comparison_left", "Traditional Approach")
    )

    right = clean_text(
        spec.get("comparison_right", "Modern Approach")
    )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200"
     height="800"
     viewBox="0 0 1200 800">

    <rect width="1200" height="800"
          fill="{colors['background']}"/>

    <text x="600" y="90"
          text-anchor="middle"
          font-family="Arial"
          font-size="48"
          font-weight="700"
          fill="{colors['dark']}">
        {title}
    </text>

    <text x="600" y="135"
          text-anchor="middle"
          font-family="Arial"
          font-size="21"
          fill="{colors['dark']}">
        {subtitle}
    </text>

    <rect x="80" y="220"
          width="480"
          height="420"
          rx="28"
          fill="{colors['card']}"/>

    <rect x="640" y="220"
          width="480"
          height="420"
          rx="28"
          fill="{colors['card']}"/>

    <rect x="80" y="220"
          width="480"
          height="80"
          rx="28"
          fill="{colors['secondary']}"/>

    <rect x="640" y="220"
          width="480"
          height="80"
          rx="28"
          fill="{colors['primary']}"/>

    <text x="320" y="270"
          text-anchor="middle"
          font-family="Arial"
          font-size="25"
          font-weight="700"
          fill="white">
        {left}
    </text>

    <text x="880" y="270"
          text-anchor="middle"
          font-family="Arial"
          font-size="25"
          font-weight="700"
          fill="white">
        {right}
    </text>

    <circle cx="320" cy="390"
            r="75"
            fill="{colors['secondary']}"
            opacity="0.2"/>

    <text x="320" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="42"
          font-weight="700"
          fill="{colors['secondary']}">
        A
    </text>

    <circle cx="880" cy="390"
            r="75"
            fill="{colors['primary']}"
            opacity="0.2"/>

    <text x="880" y="405"
          text-anchor="middle"
          font-family="Arial"
          font-size="42"
          font-weight="700"
          fill="{colors['primary']}">
        B
    </text>

    <text x="320" y="520"
          text-anchor="middle"
          font-family="Arial"
          font-size="21"
          fill="{colors['dark']}">
        Different approach
    </text>

    <text x="880" y="520"
          text-anchor="middle"
          font-family="Arial"
          font-size="21"
          fill="{colors['dark']}">
        Improved approach
    </text>

</svg>
"""

    return svg


# ============================================================
# SVG TEMPLATE 5 - QUOTE / HIGHLIGHT
# ============================================================

def create_highlight_svg(spec, colors):

    title = clean_text(spec.get("title", "Important Insight"))
    subtitle = clean_text(spec.get("subtitle", "A thought worth remembering"))

    quote = clean_text(
        spec.get(
            "quote",
            "Innovation begins with a better question."
        )
    )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200"
     height="800"
     viewBox="0 0 1200 800">

    <rect width="1200"
          height="800"
          fill="{colors['background']}"/>

    <circle cx="1050"
            cy="100"
            r="180"
            fill="{colors['primary']}"
            opacity="0.12"/>

    <circle cx="100"
            cy="720"
            r="160"
            fill="{colors['secondary']}"
            opacity="0.12"/>

    <text x="600"
          y="120"
          text-anchor="middle"
          font-family="Arial"
          font-size="25"
          font-weight="600"
          fill="{colors['primary']}">
        {title}
    </text>

    <rect x="120"
          y="210"
          width="960"
          height="350"
          rx="35"
          fill="{colors['card']}"/>

    <text x="600"
          y="320"
          text-anchor="middle"
          font-family="Georgia"
          font-size="80"
          fill="{colors['primary']}">
        “
    </text>

    {svg_text(
        quote,
        600,
        390,
        31,
        colors["dark"],
        "600",
        "middle"
    )}

    <text x="600"
          y="650"
          text-anchor="middle"
          font-family="Arial"
          font-size="22"
          fill="{colors['dark']}">
        {subtitle}
    </text>

</svg>
"""

    return svg


# ============================================================
# TEMPLATE SELECTOR
# ============================================================

def render_svg(spec, theme_name):

    colors = COLOR_THEMES.get(
        theme_name,
        COLOR_THEMES["Ocean Blue"]
    )

    template = str(
        spec.get("template", "feature")
    ).lower()

    design_type = str(
        spec.get("design_type", "")
    ).lower()

    if "step" in template or "process" in design_type:
        return create_steps_svg(spec, colors)

    if "stat" in template or "stat" in design_type:
        return create_statistics_svg(spec, colors)

    if "comparison" in template or "compare" in design_type:
        return create_comparison_svg(spec, colors)

    if (
        "quote" in template
        or "highlight" in template
        or "quote" in design_type
    ):
        return create_highlight_svg(spec, colors)

    return create_feature_svg(spec, colors)


# ============================================================
# ZIP CREATION
# ============================================================

def create_zip(svg_text, filename):

    memory_file = io.BytesIO()

    with zipfile.ZipFile(
        memory_file,
        mode="w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        zip_file.writestr(
            filename,
            svg_text
        )

    memory_file.seek(0)

    return memory_file.getvalue()


# ============================================================
# CHAT SESSION STATE
# ============================================================

def create_new_chat(name="New Chat"):
    return {
        "name": name,
        "messages": [],
        "svg_result": None,
        "svg_spec": None,
        "svg_filename": None,
        "batch_results": []
    }


if "chats" not in st.session_state:

    first_chat_id = str(uuid.uuid4())

    st.session_state.chats = {
        first_chat_id: create_new_chat()
    }

    st.session_state.active_chat_id = first_chat_id


# ============================================================
# LOAD ACTIVE CHAT
# ============================================================

active_chat = st.session_state.chats[
    st.session_state.active_chat_id
]


st.session_state.messages = active_chat["messages"]

st.session_state.svg_result = active_chat["svg_result"]

st.session_state.svg_spec = active_chat["svg_spec"]

st.session_state.svg_filename = active_chat["svg_filename"]

st.session_state.batch_results = active_chat["batch_results"]


# ============================================================
# SAVE ACTIVE CHAT
# ============================================================

def save_active_chat():

    chat = st.session_state.chats[
        st.session_state.active_chat_id
    ]

    chat["messages"] = st.session_state.messages

    chat["svg_result"] = st.session_state.svg_result

    chat["svg_spec"] = st.session_state.svg_spec

    chat["svg_filename"] = st.session_state.svg_filename

    chat["batch_results"] = st.session_state.batch_results

# ============================================================
# HEADER
# ============================================================

st.title("🎨 AI SVG Studio")

st.caption(
    "Create professional AI-powered SVG banners and infographics "
    "from a simple natural-language design brief."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # ========================================================
    # CHAT MANAGER
    # ========================================================

    st.header("💬 Chats")

    # NEW CHAT
    if st.button(
        "➕ New Chat",
        use_container_width=True
        ):
        save_active_chat()
        
        new_chat_id = str(uuid.uuid4())
        
        st.session_state.chats[new_chat_id] = create_new_chat()
        
        st.session_state.active_chat_id = new_chat_id
        
        st.rerun()


    # CHAT LIST
    for chat_id, chat in list(st.session_state.chats.items()):

        col1, col2 = st.columns([5, 1])

        with col1:

            is_active = (
                chat_id == st.session_state.active_chat_id
            )

            label = (
                "🟢 " if is_active else "💬 "
            ) + chat["name"]

            if st.button(
                label,
                key=f"chat_{chat_id}",
                use_container_width=True
                ):
                
                save_active_chat()
                
                st.session_state.active_chat_id = chat_id
                
                selected_chat = st.session_state.chats[chat_id]
                
                st.session_state.messages = selected_chat["messages"]
                
                st.session_state.svg_result = selected_chat["svg_result"]
                
                st.session_state.svg_spec = selected_chat["svg_spec"]
                
                st.session_state.svg_filename = selected_chat["svg_filename"]
                
                st.session_state.batch_results = selected_chat["batch_results"]
                
                st.rerun()


        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{chat_id}",
                help="Delete chat"
            ):

                # Keep at least one chat
                if len(st.session_state.chats) == 1:

                    new_chat_id = str(uuid.uuid4())

                    st.session_state.chats = {
                        new_chat_id: create_new_chat()
                    }

                    st.session_state.active_chat_id = new_chat_id

                else:

                    del st.session_state.chats[chat_id]

                    if chat_id == st.session_state.active_chat_id:

                        st.session_state.active_chat_id = next(
                            iter(st.session_state.chats)
                        )

                st.rerun()


    st.divider()


    # ========================================================
    # DESIGN SETTINGS
    # ========================================================

    st.header("⚙️ Design Settings")

    category = st.selectbox(
        "Category",
        [
            "Technology",
            "Business",
            "Education",
            "Healthcare",
            "Finance",
            "Marketing",
            "Cybersecurity",
            "E-Commerce",
            "Sustainability",
            "Productivity"
        ]
    )

    design_type = st.selectbox(
        "Design Type",
        [
            "Feature Highlights",
            "Step-by-Step",
            "Statistics",
            "Comparison",
            "Quote / Highlight"
        ]
    )

    style = st.selectbox(
        "Visual Style",
        [
            "Modern",
            "Minimal",
            "Professional",
            "Corporate",
            "Creative"
        ]
    )

    template = st.selectbox(
        "Template",
        [
            "Feature",
            "Steps",
            "Statistics",
            "Comparison",
            "Highlight"
        ]
    )

    color_theme = st.selectbox(
        "Color Theme",
        list(COLOR_THEMES.keys())
    )

    st.divider()

    st.subheader("🔢 Generation")

    generation_mode = st.radio(
        "Generation Mode",
        [
            "Single SVG",
            "Batch SVG"
        ]
    )

    if generation_mode == "Batch SVG":

        number_of_svgs = st.slider(
            "Number of SVGs",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )

        st.caption(
            f"Maximum supported: {number_of_svgs} SVGs"
        )

    else:

        number_of_svgs = 1

    st.divider()

    if st.button(
        "🗑️ Clear",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.svg_result = None

        st.session_state.svg_spec = None

        st.session_state.svg_filename = None

        st.session_state.batch_results = []
        
        save_active_chat()

        st.rerun()


# ============================================================
# API KEY CHECK
# ============================================================

api_key = get_api_key()

if not api_key:

    st.warning(
        "⚠️ Google Gemini API key is not configured."
    )

    st.info(
        "Add GOOGLE_API_KEY inside "
        ".streamlit/secrets.toml"
    )

    st.code(
        'GOOGLE_API_KEY = "YOUR_API_KEY_HERE"',
        language="toml"
    )

    st.stop()


# ============================================================
# CHAT HEADER
# ============================================================

st.subheader("💬 AI Design Assistant")

st.caption(
    "Describe what you want to create. "
    "Example: Create a modern infographic about Generative AI "
    "with 4 key benefits for businesses."
)


# ============================================================
# PREVIOUS CHAT
# ============================================================

# ============================================================
# FULL SIZE SVG MODAL
# ============================================================

@st.dialog("🖼️ Full Size SVG Preview", width="large")
def show_full_svg(item):

    st.caption(item["filename"])

    components.html(
        item["svg"],
        height=720,
        scrolling=True
    )

    st.download_button(
        "⬇️ Download SVG",
        data=item["svg"],
        file_name=item["filename"],
        mime="image/svg+xml",
        use_container_width=True,
        key=f"modal_download_{item['filename']}"
    )


# ============================================================
# PREVIOUS CHAT
# ============================================================

for message_index, message in enumerate(
    st.session_state.messages
):

    # ========================================================
    # USER MESSAGE
    # ========================================================

    if message["role"] == "user":

        with st.chat_message("user"):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # ASSISTANT MESSAGE
    # ========================================================

    else:

        with st.chat_message("assistant"):

            # ------------------------------------------------
            # AI RESPONSE
            # ------------------------------------------------

            st.markdown(
                message["content"]
            )


            # =================================================
            # OUTPUT DATA
            # =================================================

            batch_items = message.get(
                "batch_results"
            )

            is_batch = bool(batch_items)

            if is_batch:

                preview_item = batch_items[0]

                svg = preview_item["svg"]

                filename = preview_item["filename"]

                spec = preview_item["spec"]

            else:

                svg = message.get("svg")

                filename = message.get(
                    "filename",
                    "ai_svg_design.svg"
                )

                spec = message.get(
                    "spec"
                )


            # =================================================
            # LIVE PREVIEW
            # =================================================

            if svg:

                st.divider()

                preview_col1, preview_col2 = st.columns(
                    [8, 1]
                )

                with preview_col1:

                    st.subheader(
                        "🖼️ Live Preview"
                    )

                with preview_col2:

                    if st.button(
                        "⛶",
                        key=f"history_fullscreen_{message_index}",
                        help="Open full-size preview"
                    ):

                        show_full_svg(
                            {
                                "svg": svg,
                                "filename": filename
                            }
                        )


                # ------------------------------------------------
                # SVG PREVIEW
                # ------------------------------------------------

                components.html(
                    svg,
                    height=650,
                    scrolling=True
                )


                # =================================================
                # DOWNLOAD
                # =================================================

                st.subheader(
                    "📥 Download"
                )

                download_col1, download_col2, download_col3 = st.columns(
                    3
                )


                # ------------------------------------------------
                # DOWNLOAD SVG
                # ------------------------------------------------

                with download_col1:

                    st.download_button(
                        "⬇️ Download SVG",
                        data=svg,
                        file_name=filename,
                        mime="image/svg+xml",
                        use_container_width=True,
                        key=f"history_download_svg_{message_index}"
                    )


                # ------------------------------------------------
                # DOWNLOAD ZIP
                # ------------------------------------------------

                with download_col2:

                    if is_batch:

                        batch_buffer = io.BytesIO()

                        with zipfile.ZipFile(
                            batch_buffer,
                            "w",
                            zipfile.ZIP_DEFLATED
                        ) as zip_file:

                            for item in batch_items:

                                zip_file.writestr(
                                    item["filename"],
                                    item["svg"]
                                )

                        batch_buffer.seek(0)

                        zip_data = batch_buffer.getvalue()

                        zip_filename = (
                            f"svg_collection_{message_index + 1}.zip"
                        )

                    else:

                        zip_data = create_zip(
                            svg,
                            filename
                        )

                        zip_filename = filename.replace(
                            ".svg",
                            ".zip"
                        )


                    st.download_button(
                        "📦 Download ZIP",
                        data=zip_data,
                        file_name=zip_filename,
                        mime="application/zip",
                        use_container_width=True,
                        key=f"history_download_zip_{message_index}"
                    )


                # ------------------------------------------------
                # DOWNLOAD JSON
                # ------------------------------------------------

                with download_col3:

                    st.download_button(
                        "🧾 Download JSON",
                        data=json.dumps(
                            spec,
                            indent=2
                        ),
                        file_name=filename.replace(
                            ".svg",
                            ".json"
                        ),
                        mime="application/json",
                        use_container_width=True,
                        key=f"history_download_json_{message_index}"
                    )


                # =================================================
                # DETAILS
                # =================================================

                with st.expander(
                    "🤖 View AI Design Specification"
                ):

                    st.json(
                        spec
                    )


                with st.expander(
                    "🔍 View SVG Source Code"
                ):

                    st.code(
                        svg,
                        language="xml"
                    )


            # =================================================
            # BATCH COLLECTION
            # =================================================

            if is_batch:

                st.divider()

                st.subheader(
                    f"📦 Generated Collection "
                    f"({len(batch_items)} SVGs)"
                )

                st.caption(
                    "Click the ⛶ button to view any design in full size."
                )


                # ------------------------------------------------
                # COLLECTION GRID
                # ------------------------------------------------

                for start in range(
                    0,
                    len(batch_items),
                    3
                ):

                    row = st.columns(3)

                    for column, item in zip(
                        row,
                        batch_items[start:start + 3]
                    ):

                        with column:

                            header_col1, header_col2 = st.columns(
                                [5, 1]
                            )


                            with header_col1:

                                st.caption(
                                    item["filename"]
                                )


                            with header_col2:

                                if st.button(
                                    "⛶",
                                    key=(
                                        f"history_expand_"
                                        f"{message_index}_"
                                        f"{item['filename']}"
                                    ),
                                    help="View full size"
                                ):

                                    show_full_svg(
                                        item
                                    )


                            components.html(
                                item["svg"],
                                height=260,
                                scrolling=False
                            )


                            st.download_button(
                                "⬇️ Download",
                                data=item["svg"],
                                file_name=item["filename"],
                                mime="image/svg+xml",
                                use_container_width=True,
                                key=(
                                    f"history_batch_download_"
                                    f"{message_index}_"
                                    f"{item['filename']}"
                                )
                            )

# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Describe your banner or infographic..."
)


# ============================================================
# GENERATION
# ============================================================

if user_prompt:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )
    current_chat = st.session_state.chats[
        st.session_state.active_chat_id
    ]
    if current_chat["name"] == "New Chat":
        
        clean_prompt = user_prompt.strip()
        
        current_chat["name"] = (
            
            clean_prompt[:32]
            + ("..." if len(clean_prompt) > 32 else "")
            )

    with st.chat_message("user"):

        st.markdown(
            user_prompt
        )


    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🤖 Gemini is creating your design..."
            ):

                llm = get_llm(
                    api_key
                )

                # =================================================
                # SINGLE SVG
                # =================================================

                if generation_mode == "Single SVG":

                    spec = generate_design_spec(
                        llm=llm,
                        topic=user_prompt,
                        category=category,
                        design_type=design_type,
                        style=style,
                        template=template,
                        color_theme=color_theme
                    )

                    svg = render_svg(
                        spec,
                        color_theme
                    )

                    safe_name = "".join(
                        character
                        for character in user_prompt.lower()
                        if character.isalnum()
                        or character in " _-"
                    )

                    safe_name = (
                        safe_name
                        .strip()
                        .replace(" ", "_")
                    )

                    safe_name = (
                        safe_name[:45]
                        or "ai_svg_design"
                    )

                    filename = (
                        f"{safe_name}.svg"
                    )

                    st.session_state.svg_result = svg

                    st.session_state.svg_spec = spec

                    st.session_state.svg_filename = filename
                    
                    save_active_chat()


                    response = (
                        "✅ **Your SVG has been generated successfully!**\n\n"
                        f"🎨 Template: `{spec.get('template', template)}`  \n"
                        f"✨ Style: `{spec.get('style', style)}`  \n"
                        f"🎯 Category: `{spec.get('category', category)}`"
                    )

                    st.markdown(
                        response
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "svg": svg,
                            "filename": filename,
                            "spec": spec
                        }
                    )
                    save_active_chat()
                    st.rerun()


                # =================================================
                # BATCH SVG
                # =================================================

                else:

                    # Generate one AI specification first.
                    # The reusable Python renderer then creates
                    # multiple SVG outputs without making 100
                    # unnecessary Gemini calls.

                    base_spec = generate_design_spec(
                        llm=llm,
                        topic=user_prompt,
                        category=category,
                        design_type=design_type,
                        style=style,
                        template=template,
                        color_theme=color_theme
                    )

                    batch_results = []

                    theme_names = list(
                        COLOR_THEMES.keys()
                    )

                    template_names = [
                        "Feature",
                        "Steps",
                        "Statistics",
                        "Comparison",
                        "Highlight"
                    ]

                    progress = st.progress(
                        0
                    )

                    for index in range(
                        number_of_svgs
                    ):

                        variation = dict(
                            base_spec
                        )

                        # Cycle through templates
                        variation["template"] = (
                            template_names[
                                index % len(template_names)
                            ]
                        )

                        # Cycle through themes
                        current_theme = (
                            theme_names[
                                index % len(theme_names)
                            ]
                        )

                        # Make the design type follow
                        # the selected template
                        template_value = (
                            variation["template"]
                            .lower()
                        )

                        if template_value == "steps":

                            variation["design_type"] = (
                                "Step-by-Step"
                            )

                        elif template_value == "statistics":

                            variation["design_type"] = (
                                "Statistics"
                            )

                        elif template_value == "comparison":

                            variation["design_type"] = (
                                "Comparison"
                            )

                        elif template_value == "highlight":

                            variation["design_type"] = (
                                "Quote / Highlight"
                            )

                        else:

                            variation["design_type"] = (
                                "Feature Highlights"
                            )

                        generated_svg = render_svg(
                            variation,
                            current_theme
                        )

                        generated_filename = (
                            f"svg_design_{index + 1:03d}.svg"
                        )

                        batch_results.append(
                            {
                                "filename": generated_filename,
                                "svg": generated_svg,
                                "spec": variation,
                                "theme": current_theme
                            }
                        )

                        progress.progress(
                            (index + 1)
                            / number_of_svgs
                        )

                    st.session_state.batch_results = (
                        batch_results
                    )

                    # First SVG becomes the main preview
                    if batch_results:

                        first = batch_results[0]

                        st.session_state.svg_result = (
                            first["svg"]
                        )

                        st.session_state.svg_spec = (
                            first["spec"]
                        )

                        st.session_state.svg_filename = (
                            first["filename"]
                        )

                    response = (
                        f"✅ **{number_of_svgs} SVG designs generated!**\n\n"
                        "The designs use reusable Python SVG "
                        "templates with different layouts "
                        "and color themes."
                    )

                    st.markdown(
                        response
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "svg": (
                                batch_results[0]["svg"]
                                if batch_results
                                else None
                                ),
                            "filename": (
                                batch_results[0]["filename"]
                                if batch_results
                                else None
                                ),
                            "spec": (
                                batch_results[0]["spec"]
                                if batch_results
                                else None
                                ),
                            "batch_results": batch_results
                            }
                        )
                    save_active_chat()
                    st.rerun()


        except Exception as error:

            error_message = (
                "❌ Generation failed. "
                "Please try again."
            )

            st.error(
                error_message
            )

            st.exception(
                error
            )