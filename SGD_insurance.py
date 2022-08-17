import pandas as pd
import SGD_model

def recommend_insurance(age, residence, payment):

    df_init = pd.read_csv('C:/Users/dlsrn/Desktop/핀테크_인턴쉽/데이터전처리_2/보험_init.csv')
    df_init = df_init[['JOIN_SN', 'BTH_YR', 'GENDER', 'IS_KRN', 'SCTR_CD', 'COM_SN', 'IS_ME', 'POL_SN', 'CT_RLPS_GBN_CD',
         'CT_IN_RLTN_CD', 'IS_INDIV', 'GIS_CD', 'IS_GRP_INS', 'INS_GBN_CD', 'CT_PY_AMT']]

    GIS_CD_dic = {'서울': 11,
                  '부산': 21,
                  '대구': 22,
                  '인천': 23,
                  '광주': 24,
                  '대전·세종': 25,
                  '울산': 26,
                  '경기': 31,
                  '강원': 32,
                  '충북': 33,
                  '충남': 34,
                  '전북': 35,
                  '전남': 36,
                  '경북': 37,
                  '경남': 38,
                  '(없음)': 99}

    user_bth = int(age)  # 유저 년생 입력
    user_bth_str = str(user_bth)
    user_bth_list = list(user_bth_str)
    user_bth_list.pop()
    user_bth_list.append('0')
    user_bth_str = "".join(user_bth_list)
    user_bth = int(user_bth_str)
    print(user_bth)

    gic_CD = residence   # 유저 거주지 입력
    gic_CD_num = GIS_CD_dic[gic_CD]
    print(gic_CD_num)

    ct_py_AMT = payment  # 유저 납입보험료 입력CT_PY_AMT
    ct_py_AMT_list = list(ct_py_AMT)
    while ',' in ct_py_AMT_list:
        ct_py_AMT_list.remove(',')
    ct_py_AMT_str = "".join(ct_py_AMT_list)
    ct_py_AMT = int(ct_py_AMT_str)
    ct_py_AMT = int(ct_py_AMT / 1000)
    print(ct_py_AMT)

    # 조건에 따른 축출
    df_new = df_init[(df_init['BTH_YR'] < user_bth + 10) & (df_init['BTH_YR'] >= user_bth) &  # 1997년 => 1990년대
                     (df_init['GIS_CD'] == gic_CD_num) &
                     (df_init['CT_PY_AMT'] <= ct_py_AMT + (ct_py_AMT * 0.2)) & (
                                 df_init['CT_PY_AMT'] > ct_py_AMT - (ct_py_AMT * 0.2))]

    df_new = df_new.reset_index()

    SCTR_CD_list = list(df_new['SCTR_CD'])
    INS_GBN_CD_list = list(df_new['INS_GBN_CD'])

    df_ready = []
    for i in range(0, len(df_new), 1):
        df_ready.append(str(SCTR_CD_list[i]) + '/' + str(INS_GBN_CD_list[i]))

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
            # print("1.",total_result[i],end="")
            # print("=>",join_sn_df_result[j], ":",df_count3[join_sn_df_result[j]],end="")
            if total_result[i] in df_count3[join_sn_df_result[j]]:
                # print("=>",df_count3[join_sn_df_result[j]][total_result[i]],)
                result_list_1.append(df_count3[join_sn_df_result[j]][total_result[i]])
                # print("=>",result_list_1)
            else:
                # print("=>","0")
                result_list_1.append(0)
                # print("=>",result_list_1)
        result_list_2.append(result_list_1)

    import numpy as np
    result_array = np.array(result_list_2)

    result_array_T = result_array.T

    final_df = pd.DataFrame(result_array_T, columns=total_result, index=join_sn_df_result)

    # 유저에게 상품을 추천하기 위해 행 추가
    user_input = []
    for i in range(0, len(final_df.columns), 1):
        user_input.append(0)

    new_row = pd.DataFrame([user_input], columns=final_df.columns)

    new_final_df = pd.concat([final_df.iloc[:0], new_row, final_df.iloc[0:]], ignore_index=True)

    SGD_array = np.array(new_final_df)

    R=SGD_array

    # -------------------------------------sgd모델 호출

    good_array = SGD_model.SGD_call(R)

    # -------------------------------------sgd모델 호출

    good_list = list(good_array[0])
    good_list
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
                                (df_new['INS_GBN_CD'] == int(final_result[i][1]))])

    df_output3 = []
    for i in range(0, len(final_result), 1):
        df_output2 = df_output[i][['COM_SN', 'SCTR_CD', 'INS_GBN_CD']]
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

    INS_GBN_CD_dic = {1: '종신보험',
                      2: '정기보험',
                      3: '질병(건강)보험',
                      4: '상해보험',
                      5: '암보험',
                      6: '간병(요양)보험',
                      7: '어린이보험',
                      8: '치아보험',
                      9: '연금저축보험',
                      10: '연금보험',
                      11: '저축보험(양로보험 포함)',
                      12: '교육보험',
                      13: '운전자보험',
                      14: '여행자보험',
                      15: '골프보험',
                      16: '실손의료보험',
                      17: '자동차보험',
                      18: '화재/재물보험',
                      19: '배상책임보험',
                      20: '화재·특종(배상책임·재물)보험',
                      99: '기타보험'}

    # ---------------------------------------------------------------------------

    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            df_output4[i][j][0] = int(df_output4[i][j][0])
            df_output4[i][j][1] = SCTR_CD_dic[df_output4[i][j][1]]
            df_output4[i][j][2] = INS_GBN_CD_dic[df_output4[i][j][2]]

    x_1 = []
    x_2 = []
    count = 0
    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            for k in range(0, len(df_output4[i][j]), 1):
                x_2.append(df_output4[i][j][k])
                count = count + 1
                if count == 3:
                    x_1.append(x_2)
                    x_2 = []
                    count = 0
    print(x_1)

    return x_1

