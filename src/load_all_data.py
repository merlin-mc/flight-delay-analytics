import pandas as pd
import os
import time

data_dir = 'data/raw/'
files = ['can_data_202601.txt', 'pek_data_202601.txt', 'pvg_data_202601.txt', 'sha_data_202601.txt', 'szx_data_202601.txt']

columns = ['id', 'flight_date', 'dep_airport', 'arr_airport', 'status', 
           'scheduled_dep_time', 'scheduled_arr_date', 'scheduled_arr_time', 
           'actual_dep_date', 'actual_dep_time', 'actual_arr_date', 'actual_arr_time', 'other']

all_dfs = []

start_time = time.time()

for file in files:
    file_path = os.path.join(data_dir, file)
    if os.path.exists(file_path):
        print(f"正在读取: {file}...")
        df = pd.read_csv(file_path, sep=',', header=None, names=columns, encoding='utf-8', 
                         on_bad_lines='skip', engine='python')
        all_dfs.append(df)
    else:
        print(f"❌ 找不到文件: {file_path}")

if all_dfs:
    df_all = pd.concat(all_dfs, ignore_index=True)
    print(f"\n✅ 五大机场数据全部读取成功！")
    print(f"总数据规模: {df_all.shape}")
    print(f"\n数据前 5 行:")
    print(df_all.head())
    
    os.makedirs('data/processed', exist_ok=True)
    df_all.to_csv('data/processed/all_airports.csv', index=False)
    print(f"\n✅ 数据已保存至 data/processed/all_airports.csv")
    print(f"耗时: {time.time() - start_time:.2f} 秒")