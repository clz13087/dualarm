import os
import glob
import pandas as pd

# 入力パスと出力パス
# input_base_path = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap"
# output_base_path = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap_fortrain"
input_base_path = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/mocap"
output_base_path = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/mocap_fortrain"
taskcount = 37

# 1から7のフォルダを順に処理
for i in range(1, taskcount+1):
    # フォルダパスの作成
    folder_path = os.path.join(input_base_path, str(i))
    
    # ファイルパターンを使ってファイルを検索
    left_file_pattern = os.path.join(folder_path, "Transform_Participant_1_*.csv")
    right_file_pattern = os.path.join(folder_path, "Transform_Participant_2_*.csv")
    
    # 該当ファイルを取得（globで検索）
    left_files = glob.glob(left_file_pattern)
    right_files = glob.glob(right_file_pattern)
    
    # ファイルが見つからなかった場合のエラー処理
    if not left_files or not right_files:
        print(f"{i}フォルダ内のファイルが見つかりません。")
        continue

    # 各フォルダで一致する最初のファイルを使用
    left_file = left_files[0]
    right_file = right_files[0]

    # CSVファイルの読み込み(Pandas内部でfloatに変換される際に桁落ち等が発生，dtype="object"をつけて型変換されない)
    left_data = pd.read_csv(left_file, dtype=object)
    right_data = pd.read_csv(right_file, dtype=object)
    
    # 共通の時間列の取得
    time_column = left_data["time"]
    
    # ヘッダーの設定
    combined_data = pd.DataFrame({
        "time": time_column,
        "leftx": left_data["x"],
        "lefty": left_data["y"],
        "leftz": left_data["z"],
        "rightx": right_data["x"],
        "righty": right_data["y"],
        "rightz": right_data["z"],
        "leftqx": left_data["qx"],
        "leftqy": left_data["qy"],
        "leftqz": left_data["qz"],
        "leftqw": left_data["qw"],
        "rightqx": right_data["qx"],
        "rightqy": right_data["qy"],
        "rightqz": right_data["qz"],
        "rightqw": right_data["qw"],
    })
    
    # データ数の取得
    length = len(combined_data)
    
    # 出力ファイル名の作成（例: 1フォルダの場合 -> 20241003_1528_length.csv）
    date_part = os.path.basename(left_file).split('_')[3]
    time_part = os.path.basename(left_file).split('_')[4].split('.')[0]
    output_filename = f"{date_part}_{time_part}_{length}.csv"
    os.makedirs(output_base_path, exist_ok=True)
    output_file_path = os.path.join(output_base_path, output_filename)
    
    # CSVファイルの書き出し
    combined_data.to_csv(output_file_path, index=False)
    print(f"{i}フォルダ内のデータの結合と出力が完了しました。")

print("全て完了しました。")
