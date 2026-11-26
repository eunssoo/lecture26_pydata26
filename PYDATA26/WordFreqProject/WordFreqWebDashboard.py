# 메뉴와 화면에 표시되는 내용만 들어갑니다.
import streamlit as st
import mylib.myTextAnalyzer as ta
import mylib.myStreamlitVisualizer as sv
import pandas as pd

with st.sidebar:
    datafile = st.file_uploader("분석할 파일 선택", type=['csv'])
    col_name = st.text_input('데이터가 있는 컬럼명').strip()

    if st.button("데이터 파일 확인"):
        if datafile is not None:
            try:
                data_df = ta.load_corpus(datafile)
            except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError, OSError) as e:
                st.error(f'CSV 파일을 읽을 수 없습니다: {e}')
            else:
                sv.view_raw_data_dialog(data_df)
        else:
            # status는 아직 생성되지 않았으므로 st.warning 사용
            st.warning('데이터 파일을 선택한 후 확인하세요.')

    st.write('## 설정')
    with st.form('my_form'):
        # 빈도수 그래프 관련 설정
        do_graph = st.checkbox('빈도수 그래프', value=True)
        num_word_graph = st.slider('단어 수', 10, 50, 20, 1)
        # wordcloud 관련 설정
        do_wordcloud = st.checkbox('워드클라우드')
        num_word_wc = st.slider('단어 수', 20, 500, 50, 10)
        submitted = st.form_submit_button('분석 시작')

st.title('단어 빈도수 시각화')
status = st.empty()
status.info('분석을 위한 설정을 하십시오.')

if submitted:
    if not do_graph and not do_wordcloud:
        status.error('분석 방법을 설정하세요.')
        st.stop()

    if datafile is None:
        status.error('분석할 CSV 파일을 선택하세요.')
        st.stop()

    if not col_name:
        status.error('데이터가 있는 컬럼명을 입력하세요.')
        st.stop()

    status.info('데이터 분석 중...')

    # 데이터 로딩
    try:
        corpus = ta.load_corpus(datafile)
    except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError, OSError) as e:
        status.error(f'CSV 파일을 읽을 수 없습니다: {e}')
        st.stop()

    # 사용자 입력 컬럼명 사용 및 존재 여부 확인
    target_col = col_name
    if target_col not in corpus.columns:
        status.error(f"'{target_col}' 컬럼이 없습니다. 컬럼명을 확인하세요.")
        st.stop()

    # 빈도수 산출
    counter = ta.get_freg_word(corpus, target_col)

    if not counter:
        status.warning('분석할 단어가 없습니다.')
        st.stop()

    status.info('분석 완료')

    # 사용자 설정에 따라 시각화
    if do_graph:
        st.info(f'빈도수 그래프({num_word_graph})')
        sv.visualize_graph(counter, num_word_graph)
    if do_wordcloud:
        st.info(f'워드클라우드({num_word_wc})')
        sv.visualize_wordcloud(counter, num_word_wc)
