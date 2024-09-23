import streamlit as st
import sqlite3
import pandas as pd

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
        ''', (home_score - away_score, home_team,))
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, lose = standings.lose + 1, gd = standings.gd + ?
            WHERE team = ?
        ''', (away_score - home_score, away_team,))
    elif home_score == away_score:
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, draw = standings.draw + 1, point = standings.point + 1
            WHERE team = ?
        ''', (home_team,))
        cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, draw = standings.draw + 1, point = standings.point + 1
            WHERE team = ?
        ''', (away_team,))
    else:
       cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, win = standings.win + 1, point = standings.point + 3, gd = standings.gd + ?
            WHERE team = ?
        ''', (away_score - home_score, away_team,))
       cursor.execute('''
            UPDATE standings
            SET game = standings.game + 1, lose = standings.lose + 1, gd = standings.gd + ?
            WHERE team = ?
        ''', (home_score - away_score, home_team,)) 
    cursor.execute('''
    UPDATE gamenum
    SET gamenum = gamenum.gamenum + 1
    WHERE id = 1
    ''')
    conn.commit()

def reset():
    cursor.execute('''
    DELETE FROM matches
    ''')
    cursor.execute('''
    DELETE FROM standings
    ''')
    for team in teams:
        cursor.execute('''
            INSERT INTO standings (team, game, win, draw, lose, gd, point)
            VALUES (?, 0, 0, 0, 0, 0, 0)
        ''', (team,))
    cursor.execute('''
    UPDATE gamenum
    SET gamenum = 0
    WHERE id = 1
    ''')
    conn.commit()

def get_all_matches():
    cursor.execute('SELECT * FROM matches')
    matches = cursor.fetchall()
    return matches

def get_gamenum():
    cursor.execute('SELECT * FROM gamenum')
    gamenum = cursor.fetchall()
    gamenum = gamenum[0][1]
    return gamenum

def get_scoreboard():
    cursor.execute('SELECT * FROM standings')
    standings = cursor.fetchall()
    return standings

def keyfunc(x):
    return x[7] * 10000 + x[6]

st.set_page_config(page_title='D리그 순위표')

pages = ['일정', '순위표', '일정 입력', '결과 입력']
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
    st.title('순위표')
    scoreboard = get_scoreboard()
    scoreboard.sort(key=keyfunc, reverse=True)
    df = pd.DataFrame(scoreboard)
    df.columns = ['순위', '이름', '경기', '승', '무', '패', '득실', '승점']
    df['순위'] = [1,2,3,4,5,6,7]
    st.dataframe(df, hide_index=True, width=10000, height=300)

if page == '결과 입력':
    st.title('결과 입력')
    gamenum = get_gamenum()
    matches = get_all_matches()
    match = matches[gamenum]
    home_team = match[2]
    away_team = match[3]
    col1, col2, col3 = st.columns([8,1,8])
    with col1:
        home_score = st.number_input(home_team, min_value=0., max_value=10., value=0., step=1., format='%.0f', key=1001)
    with col2:
        st.write('vs')
    with col3:
        away_score = st.number_input(away_team, min_value=0., max_value=10., value=0., step=1., format='%.0f', key=1002) 
    if st.button('결과 저장'):
        update_result(gamenum + 1, home_team, away_team, home_score, away_score)
        st.rerun()
        
if page == '일정 입력':
    st.title('일정 입력')
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