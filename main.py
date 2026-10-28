from collections import defaultdict
import re

#データ読み込み処理
file_path = "study_log.txt"

# 1. 記録一覧を表示する関数
def show_records(lines):
    print("\n" + "="*30)
    print("---  記録一覧 ---")
    print("="*30)
    if not lines:
        print("まだ記録がありません。")
    else:
        #読み込んだすべての行を順番に画面に出力
        for line in lines:
            print(line.strip())

# 2. 内容ごとの合計を表示する関数
def show_category_totals(lines):
    print("\n" + "="*30)
    print("---  内容ごとの合計勉強時間 ---")
    print("="*30)

    # カテゴリごとの時間を格納する
    category_hours = defaultdict(float)
    for line in lines:

        #正規表現で「内容」と「時間」を正確に抽出
        content_match = re.search(r"内容:\s*([^,]+)", line)
        hours_match = re.search(r"時間:\s*([0-9.]+)", line)
        
        if content_match and hours_match:
            content = content_match.group(1).strip()
            hours = float(hours_match.group(1))
            # 同じ内容があれば時間を合算
            category_hours[content] += hours
    
    if category_hours:

        #集計結果を見やすく一覧形式で表示
        for content, total in category_hours.items():
            print(f"・ {content}: 合計 {total:.1f} 時間")
    else:
        print("集計できるデータがありません。")

# 3. 平均や統計を表示する関数
def show_statistics(lines):
    print("\n" + "="*30)
    print("---  勉強時間の平均と統計 ---")
    print("="*30)
    
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
                #日付ごとの勉強時間を集計
                daily_hours[date_str] += hours

    studied_days = len(daily_hours)
    print(f"・ 総勉強時間: {total_hours:.1f} 時間")
    print(f"・ 勉強日数: {studied_days} 日")

       #勉強した日数が1日以上ある場合のみ、各種平均を計算
    if studied_days > 0:

        avg_per_day = total_hours / studied_days
        avg_per_week = avg_per_day * 7
        avg_per_month = avg_per_day * 30
        print(f"・ 1日あたりの平均: {avg_per_day:.1f} 時間")
        print(f"・ 1週間あたりの平均: {avg_per_week:.1f} 時間")
        print(f"・ 1か月あたりの平均: {avg_per_month:.1f} 時間")
    else:
        print("・ 日付データが含まれる記録がまだないため、平均を計算できません。")

#メインのプログラム（メニューをループさせる）
def main():
    while True:
        #コンソール上に操作メニューを表示
        print("\n" + "="*30)
        print("---  学習ログ分析メニュー ---")
        print("[1] 記録一覧を見る")
        print("[2] 内容別の合計を見る")
        print("[3] 平均・統計データを見る")
        print("[0] アプリを終了する")
        print("="*30)
        
        choice = input("番号を選んでください (0-3): ").strip()

        #ファイルを読み込む（ファイルがない場合のエラー対策）
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("まだ 'study_log.txt' が見つかりません。先にJavaで記録を保存してください！")
            break

        # 選ばれた番号によって処理を分岐する
        if choice == "1":
            show_records(lines)
        elif choice == "2":
            show_category_totals(lines)
        elif choice == "3":
            show_statistics(lines)
        elif choice == "0":
            print("\nアプリを終了します。お疲れ様でした！")
            break
        else:
            print("\n 無効な入力です。0〜3の番号を入力してください。")

if __name__ == "__main__":
    main()