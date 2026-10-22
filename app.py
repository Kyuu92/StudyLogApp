import streamlit as st
import pandas as pd
from collections import defaultdict
import re

# --- データの読み込み処理 ---
file_path = "study_log.txt"

def load_data():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        return []

lines = load_data()

# --- 画面のタイトル ---
st.title(" 学習ログ・分析ダッシュボード")

# --- タブによる画面切り替え ---
tab1, tab2, tab3 = st.tabs([" 記録一覧", " 内容別合計", "📈 統計・平均"])

# 【タブ1】記録一覧
with tab1:
    st.header("これまでの学習記録一覧")
    if not lines:
        st.warning("まだ記録がありません。Javaで記録を追加してください！")
    else:
        st.info(f"これまでの学習記録回数: {len(lines)} 回")
        for line in lines:
            st.text(line.strip())

# 【タブ2】内容別の合計
with tab2:
    st.header("内容ごとの合計勉強時間")
    category_hours = defaultdict(float)
    
    for line in lines:
        content_match = re.search(r"内容:\s*([^,]+)", line)
        hours_match = re.search(r"時間:\s*([0-9.]+)", line)
        if content_match and hours_match:
            content = content_match.group(1).strip()
            hours = float(hours_match.group(1))
            category_hours[content] += hours
            
    if category_hours:
        # 表（データフレーム）にして見やすく表示
        df = pd.DataFrame(list(category_hours.items()), columns=["学習内容", "合計時間(時間)"])
        st.dataframe(df, use_container_width=True)
        
        # 簡単な棒グラフを表示！
        st.bar_chart(df.set_index("学習内容"))
    else:
        st.info("集計できるデータがありません。")

# 【タブ3】統計・平均
with tab3:
    st.header("勉強時間の統計と平均")
    total_hours = 0.0
    daily_hours = defaultdict(float)

    for line in lines:
        hours_match = re.search(r"時間:\s*([0-9.]+)", line)
        date_match = re.search(r"日付:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", line)
        if hours_match:
            hours = float(hours_match.group(1))
            total_hours += hours
            if date_match:
                date_str = date_match.group(1)
                daily_hours[date_str] += hours

    studied_days = len(daily_hours)
    
    # メトリック（強調表示される数値カード）で綺麗に並べる
    col1, col2 = st.columns(2)
    col1.metric("総勉強時間", f"{total_hours:.1f} 時間")
    col2.metric("勉強日数", f"{studied_days} 日")

    st.divider()

    if studied_days > 0:
        avg_per_day = total_hours / studied_days
        avg_per_week = avg_per_day * 7
        avg_per_month = avg_per_day * 30

        col3, col4, col5 = st.columns(3)
        col3.metric("1日あたりの平均", f"{avg_per_day:.1f} 時間")
        col4.metric("1週間あたりの平均", f"{avg_per_week:.1f} 時間")
        col5.metric("1か月あたりの平均", f"{avg_per_month:.1f} 時間")
    else:
        st.info("日付データが含まれる記録がまだないため、平均を計算できません。")