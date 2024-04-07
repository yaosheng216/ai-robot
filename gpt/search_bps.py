import concurrent
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'inner-ssh-tunnel.gbank.team'
app.config['MYSQL_PORT'] = 1101
app.config['MYSQL_USER'] = 'humin'
app.config['MYSQL_PASSWORD'] = '5XMjBgPed29s3QD2'
app.config['MYSQL_DB'] = 'gaming_report'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def main():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT
                u.id AS user_id,
                u.country,
                CASE
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) BETWEEN 143 AND 1430 THEN '1-10'
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) BETWEEN 1431 AND 7150 THEN '10-50'
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) BETWEEN 7151 AND 14300 THEN '50-100'
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) BETWEEN 14301 AND 71500 THEN '100-500'
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) BETWEEN 71501 AND 143000 THEN '500-1000'
                    WHEN SUM(ugdr.chip_outpay - ugdr.chip_incoming) > 143000 THEN '500-1000'
                    ELSE '0'
                END AS GGR_range,
                SUM(ugdr.chip_outpay - ugdr.chip_incoming) AS GGR
            FROM gaming_log.user_game_daily_report_new ugdr
            JOIN gaming_center.user u ON ugdr.user_id = u.id
            WHERE ugdr.cts BETWEEN '2024-02-01 00:00:00' AND '2024-02-29 23:59:59'
            AND u.country = 'ke'
            AND ugdr.game_id < 1000 OR ugdr.game_id > 3000
            GROUP BY u.id""")
        data = cur.fetchall()
        cur.close()

        df = pd.DataFrame()
        # 创建线程池执行分表数据查询
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_df = {executor.submit(process_data, d): d for d in data}
            for future in concurrent.futures.as_completed(future_to_df):
                df_bps = future.result()
                df = pd.concat([df, df_bps])

        df.to_excel(f'D:/soft/bps_data.xlsx', index=False)


# 查询用户bps数据
def process_data(data):
    with app.app_context():
        ranges = data['GGR_range']
        if ranges != '0':
            user_id = data['user_id']
            last_id = get_last_digits(user_id)
            cur = mysql.connection.cursor()
            cur.execute(f"""
                    SELECT
                        *
                    FROM gaming_report.bps_trans_log_{last_id}
                    WHERE
                        user_id = {user_id}
                        AND cts BETWEEN '2024-02-01 00:00:00' AND '2024-02-29 23:59:59'
                    """)
            data_bps = cur.fetchall()
            print("data is :", data_bps)
            cur.close()

            df_bps = pd.DataFrame(data_bps)
            return df_bps


def get_last_digits(user_id):
    last_two_digits = str(user_id)[-2:]
    if int(last_two_digits) >= 10:
        return last_two_digits
    else:
        return str(user_id)[-1:]


if __name__ == '__main__':
    main()
