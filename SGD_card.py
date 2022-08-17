import pandas as pd
import SGD_model

def recommend_card(age, credit, cash):



    df_init = pd.read_csv('C:/Users/dlsrn/Desktop/핀테크_인턴쉽/데이터전처리_2/카드_init.csv')

    user_bth = int(age)  # 유저 년생 입력
    user_bth_str = str(user_bth)
    user_bth_list = list(user_bth_str)
    user_bth_list.pop()
    user_bth_list.append('0')
    user_bth_str = "".join(user_bth_list)
    user_bth = int(user_bth_str)
    print(user_bth)

    cd_usg_LMT = credit  # 유저 신용판매한도금액 입력
    cd_usg_LMT_list = list(cd_usg_LMT)
    while ',' in cd_usg_LMT_list:
        cd_usg_LMT_list.remove(',')
    cd_usg_LMT_str = "".join(cd_usg_LMT_list)
    cd_usg_LMT = int(cd_usg_LMT_str)
    cd_usg_LMT = int(cd_usg_LMT / 1000)
    print(cd_usg_LMT)

    cd_ca_LMT = cash  # 유저 현금서비스한도금액 입력
    cd_ca_LMT_list = list(cd_ca_LMT)
    while ',' in cd_ca_LMT_list:
        cd_ca_LMT_list.remove(',')
    cd_ca_LMT_str = "".join(cd_ca_LMT_list)
    cd_ca_LMT = int(cd_ca_LMT_str)
    cd_ca_LMT = int(cd_ca_LMT / 1000)
    print(cd_ca_LMT)

    # 조건에 따른 축출
    df_new = df_init[(df_init['BTH_YR'] < user_bth + 10) & (df_init['BTH_YR'] >= user_bth) &
                     (df_init['CD_USG_LMT'] <= cd_usg_LMT + (cd_usg_LMT * 0.2)) & (
                                 df_init['CD_USG_LMT'] > cd_usg_LMT - (cd_usg_LMT * 0.2)) &
                     (df_init['CD_CA_LMT'] <= cd_ca_LMT + (cd_ca_LMT * 0.2)) & (
                                 df_init['CD_CA_LMT'] > cd_ca_LMT - (cd_ca_LMT * 0.2))]

    df_new = df_new.reset_index()

    SCTR_CD_list = list(df_new['SCTR_CD'])
    CD_OPN_CD_1_list = list(df_new['CD_OPN_CD_1'])
    CD_OPN_CD_2_list = list(df_new['CD_OPN_CD_2'])

    df_ready = []
    for i in range(0, len(df_new), 1):
        df_ready.append(str(SCTR_CD_list[i]) + '/' + str(CD_OPN_CD_1_list[i]) + '/' + str(CD_OPN_CD_2_list[i]))

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
                                (df_new['CD_OPN_CD_1'] == float(final_result[i][1])) &
                                (df_new['CD_OPN_CD_2'] == float(final_result[i][2]))])

    df_output3 = []
    for i in range(0, len(final_result), 1):
        df_output2 = df_output[i][['COM_SN', 'SCTR_CD', 'CD_OPN_CD_1', 'CD_OPN_CD_2']]
        df_output3.append(df_output2.values.tolist())

    df_output4 = []
    for i in range(0, len(df_output3), 1):
        my_list = df_output3[i]
        new_df_output3_list = []
        for v in my_list:
            if v not in new_df_output3_list:
                new_df_output3_list.append(v)
        df_output4.append(new_df_output3_list)

    #---------------------------------딕셔너리--------------------------------------

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

    CD_USG_LMT_dic = {81: '신용카드', 83: '신용체크카드'}
    CD_CA_LMT_dic = {1: '개인카드', 2: '개인기업카드'}

    # ---------------------------------------------------------------------------

    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            df_output4[i][j][0] = int(df_output4[i][j][0])
            df_output4[i][j][1] = SCTR_CD_dic[df_output4[i][j][1]]
            df_output4[i][j][2] = CD_USG_LMT_dic[df_output4[i][j][2]]
            df_output4[i][j][3] = CD_CA_LMT_dic[df_output4[i][j][3]]

    x_1 = []
    x_2 = []
    count = 0
    for i in range(0, len(df_output4), 1):
        for j in range(0, len(df_output4[i]), 1):
            for k in range(0, len(df_output4[i][j]), 1):
                x_2.append(df_output4[i][j][k])
                count = count + 1
                if count == 4:
                    x_1.append(x_2)
                    x_2 = []
                    count = 0
    print(x_1)

    return x_1