
from datetime import datetime, date
import json
import requests


auth = 'ced3cf6ffcaa2edf9077d01ee568dc0b'

FinGrp_list= ['020000','030300','050000'] # 권역코드 [은행 020000], [저축은행 030300], [보험 050000]

page = '1'

result_Prdt_Info = []
result_Prdt_Option = []

for FinGrp in FinGrp_list:
    url = f'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth={auth}&topFinGrpNo={FinGrp}&pageNo={page}'
    res= requests.get(url)
    res_json = json.loads(res.text)

    for baseList in res_json['result']['baseList']:

        fin_Grp_code = FinGrp
        dcls_month = baseList['dcls_month']    # 공시 제출월  (key)
        fin_co_no = baseList['fin_co_no']        # 금융회사코드  (key)
        kor_co_name = baseList['kor_co_nm']         # 금융회사명
        fin_prdt_code = baseList['fin_prdt_cd']     # 금융상품코드  (key)
        fin_prdt_name = baseList['fin_prdt_nm']     # 금융상품명
        join_way = baseList['join_way']             # 가입방법
        loan_inci_expn = baseList['loan_inci_expn'] # 대출 부대비용
        erly_rpay_fee = baseList['erly_rpay_fee']   # 중도상환 수수료
        dly_rate = baseList['dly_rate']            # 연체 이자율
        loan_lmt = baseList['loan_lmt']            # 대출 한도
        dcls_strt_day = baseList['dcls_strt_day']  # 공시 시작일
        dcls_end_day = baseList['dcls_end_day']    # 공시 종료일
        fin_co_subm_day = baseList['fin_co_subm_day']# 금융회사 제출일
        input_date = datetime.now().isoformat()
        createdat = input_date # 생성일시
        updatedat = input_date # 업데이트 일시

        result_Prdt_Info.append([fin_Grp_code,dcls_month, fin_co_no,
                                        kor_co_name, fin_prdt_code, fin_prdt_name, join_way, loan_inci_expn, erly_rpay_fee,
                                        dly_rate,loan_lmt, dcls_strt_day, dcls_end_day, fin_co_subm_day,
                                        input_date, createdat, updatedat])


    for optionList in res_json['result']['optionList']:

        dcls_month = optionList['dcls_month']
        mrtg_type= optionList['mrtg_type']    # 담보유형코드
        fin_co_no = optionList['fin_co_no']  # 금융회사코드
        fin_prdt_code = optionList['fin_prdt_cd']  # 금융상품코드
        mrtg_type_nm = optionList['mrtg_type_nm'] # 담보유형
        rpay_type = optionList['rpay_type']       # 대출상환유형 코드
        rpay_type_nm = optionList['rpay_type_nm']     # 대출상환 유형
        lend_rate_type = optionList['lend_rate_type']  # 대출금리유형 코드
        lend_rate_type_nm = optionList['lend_rate_type_nm'] # 대출금리유형
        lend_rate_min = optionList['lend_rate_min'] # 대출금리_최저[소수점 2자리]
        lend_rate_max = optionList['lend_rate_max'] # 대출금리_최고[소수점 2자리]
        lend_rate_avg = optionList['lend_rate_avg'] # 전일 취급 평균금리 [소수점 2자리]
        createdat = input_date # 생성일시
        updatedat = input_date # 업데이트 일시

        result_Prdt_Option.append([dcls_month,fin_co_no, fin_prdt_code,mrtg_type, mrtg_type_nm,
                                        rpay_type, rpay_type_nm, lend_rate_type, lend_rate_type_nm, lend_rate_min, lend_rate_max,
                                        lend_rate_avg, createdat, updatedat])

import pandas as pd
import pymysql
import logging
conn = pymysql.connect(host = '127.0.0.1',
                       user = 'root', passwd = "DATA456852zz!!", db = 'scraping_interest', charset= 'utf8')
cur = conn.cursor()


Info_col_name = ['fin_Grp_code','dcls_month', 'fin_co_no','kor_co_name', 'fin_prdt_code',
                 'fin_prdt_name', 'join_way', 'loan_inci_expn', 'erly_rpay_fee',
                 'dly_rate','loan_lmt', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day',
                 'input_date', 'createdat', 'updatedat']
result_Prdt_Info_df = pd.DataFrame(result_Prdt_Info,columns = Info_col_name)

Option_col_name = ['dcls_month', 'fin_co_no','fin_prdt_code','mrtg_type', 'mrtg_type_nm','rpay_type', 'rpay_type_nm', 'lend_rate_type',
                   'lend_rate_type_nm', 'lend_rate_min', 'lend_rate_max','lend_rate_avg', 'createdat', 'updatedat']
result_Prdt_Option_df = pd.DataFrame(result_Prdt_Option, columns = Option_col_name)
#result_Prdt_Option_df['lend_rate_avg'] = (result_Prdt_Option_df['lend_rate_min']+result_Prdt_Option_df['lend_rate_max'])/2


result_Prdt_Option_df = result_Prdt_Option_df.dropna(axis=0)
result_Prdt_Option_df.duplicated(subset=['dcls_month', 'fin_co_no', 'fin_prdt_code','rpay_type']).sum()
try:
    # SQL 접속
    test_list = result_Prdt_Info_df.values.tolist()
    sql = """
        INSERT INTO judam_prdt_info
        (fin_Grp_code,dcls_month, fin_co_no, kor_co_name, fin_prdt_code,
        fin_prdt_name, join_way, loan_inci_expn, erly_rpay_fee, dly_rate, loan_lmt,
         dcls_strt_day, dcls_end_day, fin_co_subm_day,input_date, createdat, updatedat)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        fin_Grp_code=VALUES(fin_Grp_code), dcls_month=VALUES(dcls_month), fin_co_no=VALUES(fin_co_no), kor_co_name=VALUES(kor_co_name), fin_prdt_code=VALUES(fin_prdt_code),
         fin_prdt_name=VALUES(fin_prdt_name), join_way=VALUES(join_way),
        loan_inci_expn=VALUES(loan_inci_expn), erly_rpay_fee=VALUES(erly_rpay_fee), dly_rate=VALUES(dly_rate), loan_lmt=VALUES(loan_lmt),
        dcls_strt_day=VALUES(dcls_strt_day),dcls_end_day=VALUES(dcls_end_day),fin_co_subm_day=VALUES(fin_co_subm_day),
         input_date=VALUES(input_date),createdat=VALUES(createdat),updatedat=VALUES(updatedat)
        """
    cur.executemany(sql, test_list)
    conn.commit()
    test_list_option = result_Prdt_Option_df.values.tolist()
    sql = """
        INSERT INTO judam_prdt_option
        (dcls_month, fin_co_no, fin_prdt_code, mrtg_type ,mrtg_type_nm, rpay_type, rpay_type_nm, lend_rate_type,
                   lend_rate_type_nm, lend_rate_min, lend_rate_max,lend_rate_avg, createdat, updatedat)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE 
        dcls_month=VALUES(dcls_month),fin_co_no=VALUES(fin_co_no), fin_prdt_code=VALUES(fin_prdt_code),mrtg_type=VALUES(mrtg_type), mrtg_type_nm=VALUES(mrtg_type_nm), rpay_type=VALUES(rpay_type), rpay_type_nm=VALUES(rpay_type_nm), lend_rate_type=VALUES(lend_rate_type),
         lend_rate_type_nm=VALUES(lend_rate_type_nm), lend_rate_min=VALUES(lend_rate_min),
        lend_rate_max=VALUES(lend_rate_max), lend_rate_avg=VALUES(lend_rate_avg), createdat=VALUES(createdat), updatedat=VALUES(updatedat)
        """
    cur.executemany(sql, test_list_option)
    conn.commit()
    print('완료')

except Exception :
    logging.exception("message")

finally:
    cur.close()
    conn.close()