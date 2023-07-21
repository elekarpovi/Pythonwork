#Реализовать консольное приложение заметки, с сохранением, чтением,
#добавлением, редактированием и удалением заметок. Заметка должна
#содержать идентификатор, заголовок, тело заметки и дату/время создания или
#последнего изменения заметки. Сохранение заметок необходимо сделать в
#формате json или csv формат (разделение полей рекомендуется делать через
#точку с запятой).

import datetime as dt
import uuid
import json


class Notebook:
    
    def __init__(self, name):
        self.name = name
        self.records_dict = dict()
        self.date_filter_day = 0
        self.date_filter_month = 0
        self.date_filter_year = 0


    def add_record(self):
        head = input('Input a new records head: ')
        body = input('Input a new records body: ')
        record = [head, body,dt.datetime.now().strftime("%d-%m-%Y в %H:%M:%S")]
        self.records_dict[str(uuid.uuid4())] = record


    def del_record(self, record_id):
        del self.records_dict[record_id]


    def find_record_by_head(self):
        head = input('Input the records head: ')
        for (record_id, record) in self.records_dict.items():
            if head.lower() in record[0].lower():
                print('Found record:')
                self.print_record_by_id(record_id)
                return record_id
        print('Such record was not found.')
        return None


    def print_record_by_id(self, record_id):
        record = self.records_dict[record_id]
        print(f'{record[0]}\t{record[2]}')      
        print(record[1])
        print('-----------')


    def print_records_lists(self, flag):
        if 0 < self.date_filter_year: 
            print(f'Date filter enabled: records later than {self.date_filter_day}-{self.date_filter_month}-{self.date_filter_year}')
        for (record_id, record) in self.records_dict.items():
            year = int(str(record[2])[6:10])
            month = int(str(record[2])[3:5])
            day = int(str(record[2])[0:2])
            if year > self.date_filter_year or ( year == self.date_filter_year and month >self.date_filter_month ) or ( year == self.date_filter_year and month == self.date_filter_month and day >= self.date_filter_day ) :
                    if flag: print(f'{record[0]}\t{record[2]}') 
                    else: self.print_record_by_id(record_id)    
            


    def make_date_filter(self):
        while True:
            year = int(input('Input Year:'))
            month = int(input('Input Month number:'))
            day = int(input('Input Day number:'))
            if 0 < day < 32 and 0 < month < 13 and 0 < year < 2500: break
            print('Wrong date. Try again.')

        self.date_filter_year = year
        self.date_filter_month = month
        self.date_filter_day = day
       


class Json_file_service:
    
    def load_notebook():
        try:
            with open('volume1.json', 'r',encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return dict()
        

    def save_notebook(notebook):
        with open('volume1.json', 'w',encoding='UTF-8') as file:
         json.dump(notebook.records_dict, file)


def main():
    
    n = Notebook("Volume 1")
    
    print("List of commands:")
    print('load\t - load notebook')
    print('save\t - save notebook and exit')
    print('add\t - add a new record')
    print('edit\t - find and edit a record')
    print('del\t - find and delete a record')
    print('find\t - find a record by head')
    print('date\t - choose a date filter')
    print('heads\t - print a list of record heads')
    print('records\t - print a list of records')
    print('exit\t - shut down the program')
    while True:
        match input('Input a command: '):
            case 'save':
                Json_file_service.save_notebook(n)
                print('The data has been saved.')
                break
            case 'load':
                n.records_dict = Json_file_service.load_notebook()
                if len(n.records_dict) > 0: print('The data has been uploaded.')
                else: print('There is no data to upload.')
            case 'exit':
                if input('Do you want to save data before exiting the program Y/N: ') in 'Yy':
                        Json_file_service.save_notebook(n)
                        print('The data has been saved.') 
                break
            case 'add':
                n.add_record()
                print('A new record has been created.')
            case 'edit':
                record_id = n.find_record_by_head()
                if record_id != None and input('Edit this record Y/N: ') in 'Yy':
                    n.add_record()
                    n.del_record(record_id)
                    print('The record has been edited.')
                    
            case 'del':
                record_id = n.find_record_by_head()
                if record_id != None and input('Delete this record Y/N: ') in 'Yy1':
                    n.del_record(record_id)
                    print('The record has been deleted.')
            case 'find':
                 n.find_record_by_head()
            case 'date':
                n.make_date_filter()
            case 'heads':
                n.print_records_lists(True)
            case 'records':
                n.print_records_lists(False)
            case _:
                print("Bad command. Try again.")


if __name__ == '__main__':
    main()