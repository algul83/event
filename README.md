# Access 퀴즈 이벤트 페이지

| 페이지 | 주소 | 메인 파일 | 내용 파일 |
|---|---|---|---|
| AccessMedicine | acm-event.streamlit.app | `app.py` | `index.html` |
| AccessPharmacy | acp-event.streamlit.app | `acp_app.py` | `acp.html` |

McGraw Hill AccessMedicine 퀴즈 이벤트 안내 페이지입니다. PC·태블릿·모바일 반응형.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `index.html` | 이벤트 페이지 원본 (단독으로 열어도 동작) |
| `app.py` | `index.html`을 Streamlit 화면으로 렌더링 |
| `requirements.txt` | Streamlit 의존성 |
| `.streamlit/config.toml` | 테마·툴바 설정 |

페이지 문구나 링크를 바꾸려면 `index.html`만 수정하면 됩니다.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 배포

1. https://share.streamlit.io 에서 GitHub 계정으로 로그인
2. **Create app** → 이 저장소 선택, Branch `main`, Main file `app.py`
3. **Deploy** → 발급된 `*.streamlit.app` 주소로 공유
