import streamlit as st
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

teams = ['김민규', '김환희', '노우찬', '박세중', '변상훈', '심이루', '염도현']

def add_match(match_id, home_team, away_team):
    cursor.execute('''
        INSERT INTO matches (match_id, home_team, away_team)
        VALUES (?, ?, ?)
    ''', (match_id, home_team, away_team))
    conn.commit()

def update_result(match_id, home_team, away_team, home_score, away_score):
    cursor.execute('''
        UPDATE matches
        SET home_score = ?, away_score = ?
        WHERE match_id = ?
    ''', (home_score, away_score, match_id))
    if home_score > away_score:
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, win = standings.win + 1, point = standings.point + 3, gd = standings.gd + ?
            WHERE team = ?
        ''', (home_score - away_score, home_team))
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, lose = standings.lose + 1, gd = standings.gd + ?
            WHERE team = ?
        ''', (away_score - home_score, away_team))
    elif home_score == away_score:
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, draw = standings.draw + 1, point = standings.point + 1
            WHERE team = ?
        ''', (home_team))
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, draw = standings.draw + 1, point = standings.point + 1
            WHERE team = ?
        ''', (away_team))
    else:
       cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, win = standings.win + 1, point = standings.point + 3, gd = standings.gd + ?
            WHERE team = ?
        ''', (away_score - home_score, away_team))
       cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, lose = standings.lose + 1, gd = standings.gd + ?
            WHERE team = ?
        ''', (home_score - away_score, home_team)) 
    conn.commit()

def reset():
    cursor.execute('''
    DELETE FROM matches
    ''')
    for team in teams:
        cursor.execute('''
            INSERT INTO standings (team, game, win, draw, lose, gd, point)
            VALUES (?, 0, 0, 0, 0, 0, 0)
        ''', (team,))
    conn.commit()

def get_all_matches():
    cursor.execute('SELECT * FROM matches')
    matches = cursor.fetchall()
    return matches

st.set_page_config(page_title='D리그 순위표')

pages = ['일정', '순위표', '플레이오프', '일정 입력', '결과 입력']
page = st.sidebar.selectbox('', pages)
schedule = {}

if page == '일정':
    matches = get_all_matches()
    for i in range(42):
        match = matches[i]
        if i%3 == 0:
            st.subheader(f'{i//3+1}라운드')
        col1, col2, col3 = st.columns([8,1,8])
        with col1:
            st.write(match[2])
        with col2:
            if match[4] == None:
                st.write('vs')
            else:
                st.write(f'{match[4]} : {match[5]}')
        with col3:
            st.write(match[3])
if page == '순위표':
    pass
if page == '플레이오프':
    pass
if page == '결과 입력':
    pass
if page == '일정 입력':
    st.title('일정')
    widget_id = (id for id in range(1, 100_00))
    for i in range(14):
        st.subheader(f'{i+1}라운드')
        for j in range(1, 4):
            col1, col2 , col3= st.columns([8, 1, 8])
            with col1:
                home_team = st.selectbox("홈팀", teams, key = next(widget_id))
            with col2:
                st.write('vs')
            with col3:
                away_team = st.selectbox("원정팀", teams, key = next(widget_id))
            schedule[i*3+j] = [home_team, away_team]
    if st.button('리그 시작'):
        reset()
        for i in range(1, 43):
            add_match(i, schedule[i][0], schedule[i][1])