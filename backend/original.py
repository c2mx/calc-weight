# backend/original.py
# coding=utf-8

import pandas as pd
# import os

# 修改工作目录为当前文件所在目录
# os.chdir(os.path.dirname(__file__))


dens = 7850  
dens_gsw = 5.1 

def calc_weight(arr):
    wgt = [0]*2
    match arr[0]:
        case 'PL':
            match arr[2]:
                case 'D':
                    if len(arr) == 4:
                        wgt[0] = f't{arr[1]}×Φ{arr[3]}'
                        wgt[1] = 3.14*0.25*float(arr[1])*float(arr[3])*float(arr[3])*dens*1e-9
                    else:
                        wgt[0] = f't{arr[1]}×Φ{arr[3]}×Φ{arr[5]}'
                        wgt[1] = 3.14*0.25*float(arr[1])*(float(arr[3])*float(arr[3])-float(arr[5])*float(arr[5]))*dens*1e-9
                case 'A':
                    wgt[0] = f't{arr[1]}({arr[3]}mm^2)'
                    wgt[1] = float(arr[1])*float(arr[3])*dens*1e-9
                case _:
                    wgt[0] = f't{arr[1]}×{arr[2]}×{arr[3]}'
                    wgt[1] = float(arr[1])*float(arr[2])*float(arr[3])*dens*1e-9
        case 'PIP':
            wgt[0] = f'Φ{arr[1]}×{arr[2]}×{arr[3]}'
            wgt[1] = 3.14*0.25*float(arr[3])*(float(arr[1])*float(arr[1])-(float(arr[1])-2*float(arr[2]))*(float(arr[1])-2*float(arr[2])))*dens*1e-9
        case 'CHAN':
            wgt[0] = f'[{arr[1]}×{arr[2]}'
            wgt[1] = chan_weight(arr[1])*float(arr[2])*1e-3
        case 'L':
            wgt[0] = f'L{arr[1]}×{arr[2]}×{arr[3]}'
            wgt[1] = (float(arr[1])*float(arr[2])*2-float(arr[2])*float(arr[2]))*float(arr[3])*dens*1e-9
        case 'LB':
            wgt[0] = f'L{arr[1]}×{arr[2]}×{arr[3]}×{arr[4]}'
            wgt[1] = (float(arr[1])*float(arr[3])+float(arr[2])*float(arr[3])-float(arr[3])*float(arr[3]))*float(arr[4])*dens*1e-9
        case 'H':
            wgt[0] = f'H{arr[1]}×{arr[2]}×{arr[3]}×{arr[4]}×{arr[5]}'
            wgt[1] = (float(arr[2])*float(arr[4])*2+(float(arr[1])-2*float(arr[4]))*float(arr[3]))*float(arr[5])*dens*1e-9
        case 'ST':
            wgt[0] = f'□{arr[1]}×{arr[2]}×{arr[3]}'
            wgt[1] = (float(arr[1])*float(arr[1])-(float(arr[1])-2*float(arr[2]))*(float(arr[1])-2*float(arr[2])))*float(arr[3])*dens*1e-9
        case 'FST':
            wgt[0] = f'▯{arr[1]}×{arr[2]}×{arr[3]}×{arr[4]}'
            wgt[1] = (float(arr[1])*float(arr[2])-(float(arr[1])-2*float(arr[3]))*(float(arr[2])-2*float(arr[3])))*float(arr[4])*dens*1e-9
        case 'ROD':
            wgt[0] = f'Φ{arr[1]}×{arr[2]}'
            wgt[1] = 3.14*0.25*float(arr[1])*float(arr[1])*float(arr[2])*dens*1e-9
        case 'LWG':
            wgt[0] = f'Φ{arr[1]}×{arr[2]}'
            wgt[1] = 3.14*0.25*float(arr[1])*float(arr[1])*float(arr[2])*dens*1e-9
        case 'YG':
            wgt[0] = f'Φ{arr[1]}×{arr[2]}'
            wgt[1] = 3.14*0.25*float(arr[1])*float(arr[1])*float(arr[2])*dens*1e-9
        case 'GSW':
            wgt[0] = f'钢丝网({arr[1]}mm^2)'
            wgt[1] = float(arr[1])*dens_gsw*1e-6
        case _:
            wgt[0] = ''
            wgt[1] = 0
    return wgt

def chan_weight(model):
    match model:
        case '5':
            return 5.4
        case '6.3':
            return 6.6
        case '8':
            return 8
        case '10':
            return 10
        case '12.6':
            return 12.4
        case '14a':
            return 14.5
        case '14b':
            return 16.7
        case '16a':
            return 17.2
        case '16b':
            return 19.7
        case '18a':
            return 20.2
        case '18b':
            return 23
        case '20a':
            return 22.6
        case '20b':
            return 25.8
        case '22a':
            return 25
        case '22b':
            return 28.4
        case '25a':
            return 27.5
        case '25b':
            return 31.4
        case '25c':
            return 35.3
        case '28a':
            return 31.4
        case '28b':
            return 35.8
        case '28c':
            return 40.2
        case '32a':
            return 38.2
        case '32b':
            return 43.2
        case '32c':
            return 48.3
        case '36a':
            return 47.8
        case '36b':
            return 53.4
        case '36c':
            return 59.1
        case '40a':
            return 58.9
        case '40b':
            return 65.2
        case '40c':
            return 71.5
        case _:
            print('槽钢型号填写错误!!!!!!')
            return 0

def process_file(input_path='/tmp/data.xlsx', output_path='/tmp/result_data.xlsx'):
    output = ''
    data = pd.read_excel(input_path, sheet_name='Sheet1')
    rows = data.shape[0]
    cat_loc = [] 
    gj_include = [] 
    cat_name = [] 
    cat_num = [] 
    xiaoji = [] 
    gj = [] 
    gjxiaoji = []
    
    for i in range(0, rows):
        try:
            name = data.loc[i, 'name']
            mat = data.loc[i, 'mat']
            num = data.loc[i, 'num']
            mat_list = mat.split('-')
            if mat_list[0] == 'CAT':
                cat_loc.append(i)
                cat_name.append(name)
                cat_num.append(num)
            else:
                output += f'|{name}|{calc_weight(mat_list)[0]}|{round(calc_weight(mat_list)[1], 2)}|{num}|{round(int(num)*calc_weight(mat_list)[1],2)}|||||' + '\n'
                xiaoji.append(round(int(num)*calc_weight(mat_list)[1],2))
        except KeyError as e:
            print(f"Error: {e} column not found in the DataFrame.")
    
    for i in range(0, len(cat_loc)):
        if i+1 < len(cat_loc):
            gj_include.append(cat_loc[i+1]-cat_loc[i]-1)
        else:
            gj_include.append(rows-cat_loc[i]-1)
    
    jishu = [0]*(len(gj_include)+1)
    jishu[0] = 0
    running_sum = 0
    for i in range(1, len(gj_include)+1):
        running_sum += gj_include[i-1]
        jishu[i] = running_sum
    
    for i in range(0, len(jishu)-1):
        gj.append(round(sum(xiaoji[jishu[i]:jishu[i+1]]), 2))
    
    for i in range(0, len(gj)):
        gjxiaoji.append(round(gj[i]*cat_num[i], 2))
    
    data_lines = output.strip().split('\n')
    data_split = [line.split('|') for line in data_lines]
    df = pd.DataFrame(data_split, columns=[
        '构件名称', '材料名称', '材料规格', '单件重量kg', '数量', 
        '小计kg', '单构件重量kg', '每台包含数量', '构件重量小计kg', '总计kg', '备注'
    ])
     
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('A:A', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('B:B', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('C:C', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('D:D', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('E:E', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('F:F', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('G:G', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('H:H', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('I:I', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('J:J', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        worksheet.set_column('K:K', 20, writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        for i in range(0, len(jishu)-1):
            if jishu[i+1]-jishu[i] > 1:
                worksheet.merge_range(f'A{jishu[i]+2}:A{jishu[i+1]+1}', cat_name[i], writer.book.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
                worksheet.merge_range(f'G{jishu[i]+2}:G{jishu[i+1]+1}', gj[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
                worksheet.merge_range(f'H{jishu[i]+2}:H{jishu[i+1]+1}', cat_num[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
                worksheet.merge_range(f'I{jishu[i]+2}:I{jishu[i+1]+1}', gjxiaoji[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
            else:
                worksheet.write(f'A{jishu[i]+2}', cat_name[i], writer.book.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
                worksheet.write(f'G{jishu[i]+2}', gj[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
                worksheet.write(f'H{jishu[i]+2}', cat_num[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
                worksheet.write(f'I{jishu[i]+2}', gjxiaoji[i], writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
        if len(jishu) >= 2:
            worksheet.merge_range(f'J2:J{jishu[-1]+1}', sum(gjxiaoji), writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
            worksheet.merge_range(f'K2:K{jishu[-1]+1}', '注：重量为根据图纸最终尺寸计算的材料裸重，不含焊道重量。', writer.book.add_format({'align': 'center', 'valign': 'vcenter','text_wrap': True}))
        else:
            worksheet.write(f'J2', sum(gjxiaoji), writer.book.add_format({'align': 'center', 'valign': 'vcenter'}))
            worksheet.write(f'K2', '注：重量为根据图纸最终尺寸计算的材料裸重，不含焊道重量。', writer.book.add_format({'align': 'center', 'valign': 'vcenter','text_wrap': True}))
    
    print('重量统计完毕!结果保存在result_data.xlsx文件中')
