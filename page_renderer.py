"""Access 퀴즈 이벤트 페이지 공용 렌더러 (Streamlit)

HTML 파일의 스타일과 본문을 읽어 Streamlit 화면에 그대로 렌더링합니다.
페이지 내용을 바꾸려면 해당 HTML 파일만 수정하면 됩니다.
"""
import base64
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent


@st.cache_data
def load_page(path: str, mtime: float) -> tuple[str, str]:
    # mtime 을 캐시 키에 넣어 index.html 이 바뀌면 바로 다시 읽도록 함
    html = Path(path).read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    body = re.search(r"<body[^>]*>(.*?)</body>", html, re.S).group(1)
    # 페이지 전용 스타일이 Streamlit 화면 전체에 번지지 않도록 body/html 규칙을 래퍼로 한정
    style = style.replace("html{-webkit-text-size-adjust:100%}", "")
    style = re.sub(r"(?m)^\s*body\{", "  .aq-page{", style)
    # 로컬 이미지(assets/...)를 데이터 URI로 바꿔 Streamlit 화면에서도 보이게 함
    base = Path(path).parent

    def inline(m):
        f = base / m.group(1)
        if not f.exists():
            return m.group(0)
        mime = "image/svg+xml" if f.suffix == ".svg" else f"image/{f.suffix.lstrip('.')}"
        return f'src="data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"'

    body = re.sub(r'src="(assets/[^"]+)"', inline, body)
    return style, body



def render(html_name: str, page_title: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    html_path = ROOT / html_name
    style, body = load_page(str(html_path), html_path.stat().st_mtime)

    # Streamlit 기본 여백·헤더·푸터 숨기기 + 폰트
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');
        header[data-testid="stHeader"], footer:not(.site-footer), #MainMenu,
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {display:none !important;}
        .stApp {background:#F3F5F9;}
        .block-container, [data-testid="stMainBlockContainer"] {
            padding:0 !important; max-width:100% !important;
        }
        [data-testid="stVerticalBlock"] {gap:0 !important;}
        /* 공유 영역 프레임이 내용 높이에 맞춰 늘어나도록 */
        [data-testid="stElementContainer"]:has(> iframe) {height:auto !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 공유 버튼 영역은 스크립트가 필요해서 별도 프레임(components.html)으로 렌더링
    m = re.search(r"<!--SHARE:START-->(.*?)<!--SHARE:END-->", body, re.S)
    if not m:
        st.html(f'<style>{style}</style><div class="aq-page">{body}</div>')
        return
    before, share, after = body[: m.start()], m.group(1), body[m.end():]
    grounds = re.findall(r"--ground:(#[0-9A-Fa-f]{3,6})", style)
    page_bg = grounds[-1] if grounds else "#F3F5F9"
    st.html(f'<style>{style}</style><div class="aq-page">{before}</div>')
    components.html(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap' rel='stylesheet'>"
        f"<style>html,body{{margin:0;background:{page_bg}}}</style></head><body>{share}</body></html>",
        height=190,
    )
    st.html(f'<style>{style}</style><div class="aq-page">{after}</div>')
