import streamlit as st
import itertools
import pandas as pd

st.title("駅伝 最適区間配置ツール（PB差＋区間平均モデル）")

# 区間情報
sections = [
    ("1区", 10, 1.03),
    ("2区", 3, 0.97),
    ("3区", 8, 1.01),
    ("4区", 5, 1.00),
    ("5区", 5, 1.00),
    ("6区", 8, 1.02),
]

st.header("選手PB入力（分:秒）")

players = []
for i in range(6):
    st.subheader(f"選手{i+1}")
    pb5 = st.text_input(f"5000m PB（例 14:30）", key=f"pb5_{i}")
    pb10 = st.text_input(f"10000m PB（例 30:10）", key=f"pb10_{i}")
    players.append((pb5, pb10))

def to_minutes(t):
    m, s = t.split(":")
    return int(m) + float(s)/60

if st.button("最適区間配置を計算"):
    abilities = []
    for pb5, pb10 in players:
        if pb5 and pb10:
            v5 = to_minutes(pb5) / 5
            v10 = to_minutes(pb10) / 10
            abilities.append(0.6*v5 + 0.4*v10)
        else:
            st.error("全員分のPBを入力してください")
            st.stop()

    best_time = 1e9
    best_order = None

    for perm in itertools.permutations(range(6)):
        total = 0
        for sec, p in enumerate(perm):
            _, dist, coef = sections[sec]
            total += abilities[p] * dist * coef
        if total < best_time:
            best_time = total
            best_order = perm

    result = []
    for sec, p in enumerate(best_order):
        name, dist, coef = sections[sec]
        time = abilities[p] * dist * coef
        result.append([name, f"選手{p+1}", round(time, 2)])

    df = pd.DataFrame(result, columns=["区間", "担当", "期待タイム（分）"])
    st.dataframe(df)
    st.success(f"合計期待タイム：{round(best_time,2)} 分")
