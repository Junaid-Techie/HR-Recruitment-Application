import server.config.settings as settings
import platform
import os
import pathlib
import tempfile
import uuid
from falcon_jinja2 import FalconTemplate


def get_temdir_path():
    if platform.system().lower() == "windows":
        local_app_data_folder_path = os.getenv('LOCALAPPDATA')
        temp_app_path = pathlib.Path(local_app_data_folder_path).joinpath('hire_office')
        temp_app_path.mkdir(parents=True, exist_ok=True)
        return temp_app_path
    else:
        temp_app_path = pathlib.Path(tempfile.gettempdir()).joinpath('hire_office')
        temp_app_path.mkdir(parents=True, exist_ok=True)
        return temp_app_path


def get_uploadfile_basepath(_dir):
    if platform.system().lower() == "windows":
        local_app_data_folder_path = "D:\\src\\hiring-office\\"
        temp_app_path = pathlib.Path(local_app_data_folder_path).joinpath('uploaded_files\\' + _dir)
        temp_app_path.mkdir(parents=True, exist_ok=True)
        return temp_app_path
    else:
        temp_app_path = pathlib.Path('').joinpath('uploaded_files')
        temp_app_path.mkdir(parents=True, exist_ok=True)
        return temp_app_path


def get_temp_file(ext):
    return pathlib.Path(get_temdir_path()).joinpath(f"{uuid.uuid4()}.'__'.{ext}")


def get_upload_filepath(ext, _dir):
    return pathlib.Path(get_uploadfile_basepath(_dir)).joinpath(f"{uuid.uuid4()}.'__'.{ext}")


def get_html_template_path():  ### need to work on this
    cur_path = os.path.dirname(__file__)
    if platform.system().lower() == "windows":
        # APP_DIR = os.path.abspath(os.path.dirname(__file__))
        # PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
        # print(PROJECT_ROOT)
        # path = os.path.join(os.path.abspath(cur_path), "\\ui")
        path = "D:\\src\hiring-office\server\\ui"
    else:
        # path = os.path.join(os.path.abspath(cur_path), '/ui')
        path = ''

    return (path)

    # falcon_template = FalconTemplate(path=get_html_template_path())
    # STATIC_PATH = falcon_template
    # print()
    # print(str(STATIC_PATH))
    # return falcon_template


def get_apptitle():
    return settings.ui_params[0].get('app_title')


def get_staticurl():
    return settings.ui_params[0].get('static')


def get_appurl():
    return str(settings.ui_params[0].get('protocal') + '://' + settings.ui_params[0].get('host') \
               + ':' + str(settings.ui_params[0].get('port')) + settings.ui_params[0].get('app_title'))


def get_select_options(Obj, ky, val, selected):
    output = ''
    for each_iter in Obj:
        if str(each_iter[val]) == 'None':
            continue
        if str(each_iter[ky]) in selected:
            print(each_iter[ky], each_iter[val])
            line = '<option value="' + str(each_iter[ky]) + '" selected>' + str(each_iter[val]) + '</option>'
        else:
            line = '<option value= "' + str(each_iter[ky]) + '" >' + str(each_iter[val]) + '</option>'
        output += line
    return output


def InterviewTypes():
    return ['Face 2 Face', 'Telephonic', 'Video Call', 'HR', 'Managerial']
