import tyaiShinher


def calculate_absentees(absentee_data):
    total_absences = 0
    total_late = 0
    
    # 迭代每個缺席情況和年級學期
    for absentee_type, grade_data in absentee_data.items():

        if absentee_type == '遲到':
            for term_data in grade_data.values():
                total_late += term_data  # 累加遲到次數
        if absentee_type == '曠課':
            for term_data in grade_data.values():
                total_absences += term_data  # 累加遲到次數
    
    return total_absences, total_late

arg1 = ""
arg2 = ""

response = tyaiShinher.get_credit(arg1, arg2)
print([response['Result']['合計實得學分'],response['Result']['必修通過百分比'],response['Result']['專業科目通過百分比'],response['Result']['實習科目通過百分比']])
response = tyaiShinher.get_work(arg1, arg2)

response = tyaiShinher.get_work(arg1, arg2)

print(calculate_absentees(response))