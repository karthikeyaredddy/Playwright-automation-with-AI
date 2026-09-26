from openpyxl import load_workbook


class ExcelReader:

    @staticmethod
    def get_login_data(file_path):

        workbook = load_workbook(file_path)

        sheet = workbook.active

        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):

            data.append({

                "role": row[0],

                "tenant": row[1],

                "employee_id": row[2],

                "password": row[3],

                "app": row[4]

            })

        workbook.close()

        return data