import os
import shutil

async def serh_last_number_in_fulltext_folder() -> int:
    all_file_names = []
    for root, dirs, files in os.walk('\\\\REPO-RAO\\texts'): #//192.168.111.232/irbis64/Datai/REPO/texts
        if root == '\\\\REPO-RAO\\texts': # //192.168.111.232/irbis64/Datai/REPO/texts
            for filename in files:
                try:
                    n = int(filename[0])
                    all_file_names.append(int(filename[:filename.find('-')].strip()))
                except:
                    continue
    print('Last Number',sorted(all_file_names)[-1])
    return sorted(all_file_names)[-1]

async def process_send_pdf(file_name):
    file_destination ='\\\\REPO-RAO\\texts'
    out_file_name = ''
    last_number = await serh_last_number_in_fulltext_folder()
    if len(file_name)>30:
        out_file_name = f'{last_number+1} - {file_name[:24]}.pdf'
    else:
        out_file_name = f'{last_number+1} - {file_name}.pdf'
    #os.rename(file_name, f"{file_destination}\\{out_file_name}")
    print("rename")
    print('out_file_name', out_file_name)
    shutil.copy2(f'{file_name}', f'\\\\REPO-RAO\\texts\\{out_file_name}')
    print('send')
    os.remove(file_name)
    return f'{out_file_name}'
async def process_verify_pdf_on_server(file_name):
    for root, dirs, files in os.walk('\\\\REPO-RAO\\texts'):  # //192.168.111.232/irbis64/Datai/REPO/texts
        if root == '\\\\REPO-RAO\\texts':  # //192.168.111.232/irbis64/Datai/REPO/texts
            print('file_name =', file_name)
            for filename in files:
                if filename==file_name:
                    return True

    return False
