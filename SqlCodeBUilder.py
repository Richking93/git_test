''' sql 업로드 코드 사용법

Sql_Upload(sql 컬럼 네임 ex,테이블 네임(str))
따옴표 안에 띄어쓰기, 엔터 상관없이 집어넣고 Sql_Upload 돌리면

사용 예시
test_names = """fin_Grp_code,dcls_month , fin_co_no,
                                        kor_co_name, fin_prdt_code, fin_prdt_name, join_way, loan_inci_expn , erly_rpay_fee ,
                                        dly_rate ,loan_lmt , dcls_strt_day ,dcls_end_day, fin_co_subm_day,
                                 createdat,updatedat"""
table_names = "jeonse_prdt_info"

Sql_Upload(test_names, table_names)

아웃풋 예시 프린트로 반환한다.
['fin_Grp_code', 'dcls_month', 'fin_co_no', 'kor_co_name', 'fin_prdt_code', 'fin_prdt_name', 'join_way', 'loan_inci_expn', 'erly_rpay_fee', 'dly_rate', 'loan_lmt', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day', 'createdat', 'updatedat']


"""
INSERT INTO jeonse_prdt_info
(fin_Grp_code,dcls_month,fin_co_no,kor_co_name,fin_prdt_code,fin_prdt_name,join_way,loan_inci_expn,erly_rpay_fee,dly_rate,loan_lmt,dcls_strt_day,dcls_end_day,fin_co_subm_day,createdat,updatedat )
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
fin_Grp_code = VALUES(fin_Grp_code), dcls_month = VALUES(dcls_month), fin_co_no = VALUES(fin_co_no), kor_co_name = VALUES(kor_co_name), fin_prdt_code = VALUES(fin_prdt_code), fin_prdt_name = VALUES(fin_prdt_name), join_way = VALUES(join_way), loan_inci_expn = VALUES(loan_inci_expn), erly_rpay_fee = VALUES(erly_rpay_fee), dly_rate = VALUES(dly_rate), loan_lmt = VALUES(loan_lmt), dcls_strt_day = VALUES(dcls_strt_day), dcls_end_day = VALUES(dcls_end_day), fin_co_subm_day = VALUES(fin_co_subm_day), createdat = VALUES(createdat), updatedat = VALUES(updatedat)
"""

'''




def Uploader(Column_list,Table_name) :
    no = len(Column_list)
    data = Column_list
    print(f"\"\"\"")
    print(f"INSERT INTO {Table_name}")
    print("(",end ="")
    cnt = 0
    for i in data:
        cnt += 1
        if (cnt < no):
            print(f"{i},", end = "")
        else:
            print(f"{i} )")
            cnt = 0

    print("VALUES (", end ="")
    for i in range(no):
        cnt += 1
        if (cnt < no):
            print("%s, ", end = "")
        else:
            print("%s)")
            cnt = 0

    print("ON DUPLICATE KEY UPDATE")

    for i in data:
        cnt += 1
        if (cnt < no):
            print(f"{i} = VALUES({i}), ", end = "")
        else:
            print(f"{i} = VALUES({i})")
            cnt = 0

    print(f"\"\"\"")
    print('Upload quary done')


def Sql_Upload(input_text,Table_name):
    #(변수명 집합을 [a,b,c] > ['a','b','c'] 로변환
    test_output = ''.join(input_text.split())
    test_output = test_output.split(',')
    print(test_output)

    # 변환된 텍스트를 SQL쿼리 업데이트로 변환
    ret = Uploader(test_output,Table_name)
    return ret


test_names = """fin_Grp_code,dcls_month , fin_co_no,
                                        kor_co_name, fin_prdt_code, fin_prdt_name, join_way, loan_inci_expn , erly_rpay_fee ,
                                        dly_rate ,loan_lmt , dcls_strt_day ,dcls_end_day, fin_co_subm_day,
                                 createdat,updatedat"""
table_names = "jeonse_prdt_info"

Sql_Upload(test_names, table_names)
