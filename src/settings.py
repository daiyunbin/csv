#出力先ディレクトリ
CSV_PATH = "./csv"

#csv出力しないテーブル名
IGNORED_TABLE = {
    "auth_permission",
}  

#csv出力するテーブルから特定カラムを外す
IGNORED_TABLE_COLUMN = {
    "authenticate_user":{
        "password",
    }
}
