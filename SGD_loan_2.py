import pandas as pd
import numpy as np
import SGD_model

def recommend_loan2(age,rate,money):

    df_init = pd.read_csv('C:/Users/dlsrn/Desktop/핀테크_인턴쉽/데이터전처리_2/대출(금융)_init.csv', encoding="utf-8")

    user_bth = int(age)  # 유저 년생 입력
    user_bth_str = str(user_bth)
    user_bth_list = list(user_bth_str)
    user_bth_list.pop()
    user_bth_list.append('0')
    user_bth_str = "".join(user_bth_list)
    user_bth = int(user_bth_str)
    print(user_bth)

    user_rate = int(rate)  # 유저 이자 입력
    if user_rate != 0:
        user_rate = user_rate * 1000
    print(user_rate)

    user_AMT = money  # 유저 대출금액 입력
    user_AMT_list = list(user_AMT)
    while ',' in user_AMT_list:
        user_AMT_list.remove(',')
    user_AMT_str = "".join(user_AMT_list)
    user_AMT = int(user_AMT_str)
    user_AMT = int(user_AMT / 1000)
    print(user_AMT)

    # 조건에 따른 축출
    df_new = df_init[(df_init['BTH_YR'] < user_bth + 10) & (df_init['BTH_YR'] >= user_bth) &
                     (df_init['RATE'] <= user_rate + (user_rate * 0.5)) & (df_init['RATE'] >= user_rate - (user_rate * 0.5)) &
                     (df_init['LN_AMT'] <= user_AMT + (user_AMT * 0.2)) & (df_init['LN_AMT'] >= user_AMT - (user_AMT * 0.2))]

    df_new = df_new.reset_index()

    print("df_new : ",df_new)

    SCTR_CD_list = list(df_new['SCTR_CD'])
    LN_CD_1_list = list(df_new['LN_CD_1'])
    LN_CD_2_list = list(df_new['LN_CD_2'])
    LN_CD_3_list = list(df_new['LN_CD_3'])

    df_ready = []
    for i in range(0, len(df_new), 1):
        df_ready.append(
            str(SCTR_CD_list[i]) + '/' + str(LN_CD_1_list[i]) + '/' + str(LN_CD_2_list[i]) + '/' + str(LN_CD_3_list[i]))

    df_ready3 = pd.DataFrame(data=df_ready, columns=['total'])
    df_ready4 = df_new[['JOIN_SN']]

    df = pd.concat([df_ready4, df_ready3], axis=1)

    df["JOIN_SN"] = df["JOIN_SN"].apply(str)
    join_sn_df = list(df['JOIN_SN'])

    join_sn_df_result = []
    for value in join_sn_df:
        if value not in join_sn_df_result:
            join_sn_df_result.append(value)

    df["JOIN_SN"] = df["JOIN_SN"].apply(str)

    df_count = {}
    for i in range(0, len(join_sn_df_result), 1):
        df_yr = df[df['JOIN_SN'].str.contains(str(join_sn_df_result[i]), na=False)]
        df_count[join_sn_df_result[i]] = df_yr['total'].value_counts().head(5)

    df_count2 = {}
    for i in range(0, len(join_sn_df_result), 1):
        new_list = []
        for data in df_count[join_sn_df_result[i]].index:
            new_list.append(data)
        df_count2[join_sn_df_result[i]] = new_list

    total = list(df['total'])

    total_result = []
    for value in total:
        if value not in total_result:
            total_result.append(value)

    df_count3 = {}
    for key in df_count2.keys():
        df_count2_score = {}
        count = 5
        for j in range(0, len(df_count2[key]), 1):
            df_count2_score[df_count2[key][j]] = count
            count = count - 1
        df_count3[key] = df_count2_score

    result_list_2 = []
    for i in range(0, len(total_result), 1):
        result_list_1 = []
        for j in range(0, len(join_sn_df_result), 1):
            if total_result[i] in df_count3[join_sn_df_result[j]]:
                result_list_1.append(df_count3[join_sn_df_result[j]][total_result[i]])
            else:
                result_list_1.append(0)
        result_list_2.append(result_list_1)

    result_array = np.array(result_list_2)

    result_array_T = result_array.T

    print(result_array_T)

    final_df = pd.DataFrame(result_array_T, columns=total_result, index=join_sn_df_result)

    # 유저에게 상품을 추천하기 위해 행 추가
    user_input = []
    for i in range(0, len(final_df.columns), 1):
        user_input.append(0)

    new_row = pd.DataFrame([user_input], columns=final_df.columns)

    new_final_df = pd.concat([final_df.iloc[:0], new_row, final_df.iloc[0:]], ignore_index=True)

    SGD_array = np.array(new_final_df)

    R = SGD_array

    #-------------------------------------sgd모델 호출

    good_array=SGD_model.SGD_call(R)

    # -------------------------------------sgd모델 호출

    good_list = list(good_array[0])
    good_list2 = good_list

    good_list2.sort(reverse=True)
    print(good_list2)

    good_list2 = good_list2[0:5]

    good_list3 = []
    for i in range(0, len(good_list2), 1):
        good_list3.append(good_list.index(good_list2[i]))

    final_good = []
    for i in range(0, len(good_list3), 1):
        final_good.append(total_result[good_list3[i]])

    final_result = []
    for i in range(0, len(final_good), 1):
        final_result.append(final_good[i].split('/'))

    df_output = []
    for i in range(0, len(final_result), 1):
        df_output.append(df_new[(df_new['SCTR_CD'] == int(final_result[i][0])) &
                                (df_new['LN_CD_1'] == int(final_result[i][1])) &
                                (df_new['LN_CD_2'] == int(final_result[i][2])) &
                                (df_new['LN_CD_3'] == int(final_result[i][3]))])

    df_output3 = []
    for i in range(0, len(final_result), 1):
        df_output2 = df_output[i][['COM_SN', 'SCTR_CD', 'LN_CD_1', 'LN_CD_2', 'LN_CD_3', 'RATE']]
        df_output3.append(df_output2.values.tolist())

    df_output4 = []
    for i in range(0, len(df_output3), 1):
        my_list = df_output3[i]
        new_df_output3_list = []
        for v in my_list:
            if v not in new_df_output3_list:
                new_df_output3_list.append(v)
        df_output4.append(new_df_output3_list)

    # ---------------------------------딕셔너리--------------------------------------

    SCTR_CD_dic = {1: '국내은행',
                   2: '외국은행',
                   3: '신용협동기구',
                   5: '신용카드사',
                   6: '손해보험사',
                   8: '생명보험사',
                   10: '투신사',
                   12: '기타',
                   13: '신기술사·창투사·벤쳐캐피탈',
                   15: '증권사·종금사',
                   16: '리스사',
                   17: '할부금융사',
                   21: '상호저축은행',
                   24: '대부업권'}

    LN_CD_1_dic = {31: '개인대출', 37: '장기카드대출(카드론)', 41: '단기카드대출(현금서비스)'}

    LN_CD_2_dic = {0: '카드대출',
                   100: '신용대출 > 신용대출',
                   150: '신용대출 > 학자금대출',
                   170: '신용대출 > 전세자금대출',
                   200: '담보대출 > 예적금담보대출',
                   210: '담보대출 > 유가증권담보대출',
                   220: '담보대출 > 주택담보대출',
                   230: '담보대출 > 주택외부동산(토지,상가등)담보대출',
                   240: '담보대출 > 지급보증(보증서)담보대출',
                   245: '담보대출 > 보금자리론',
                   250: '담보대출 > 학자금지급보증대출',
                   260: '담보대출 > 주택연금대출',
                   270: '담보대출 > 전세자금(보증서, 질권 등)대출',
                   271: '담보대출 > 전세보증금담보대출',
                   290: '담보대출 > 기타담보대출',
                   400: '보험계약대출거래사실',
                   500: '할부금융 > 신차할부',
                   510: '할부금융 > 중고차할부',
                   590: '할부금융 > 기타할부',
                   700: '리스 > 금융리스',
                   710: '리스 > 운용리스'}

    LN_CD_3_dic = {0: '(서민금융아님)',
                   100: '새희망홀씨',
                   150: '햇살론15',
                   170: '햇살론17',
                   180: '햇살론youth',
                   190: '햇살론뱅크',
                   200: '햇살론',
                   300: '바꿔드림론',
                   350: '안전망대출',
                   360: '안전망대출Ⅱ',
                   900: '기타'}

    # ---------------------------------------------------------------------------

    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            df_output4[i][j][1] = SCTR_CD_dic[df_output4[i][j][1]]
            df_output4[i][j][2] = LN_CD_1_dic[df_output4[i][j][2]]
            df_output4[i][j][3] = LN_CD_2_dic[df_output4[i][j][3]]
            df_output4[i][j][4] = LN_CD_3_dic[df_output4[i][j][4]]
            df_output4[i][j][5] = round(df_output4[i][j][5] * 0.001, 1)

    x_1 = []
    x_2 = []
    count = 0
    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            for k in range(0, len(df_output4[i][j]), 1):
                x_2.append(df_output4[i][j][k])
                count = count + 1
                if count == 6:
                    x_1.append(x_2)
                    x_2 = []
                    count = 0
    print(x_1)
    return x_1