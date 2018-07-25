import time

from mongoengine import connect, Q

from server.app.jsontoxml import toxml
from server.app.mongo_models import Detail, Record
import xlrd

dir = "tmp/"

connect(
    host = 'mongodb://localhost:27017/comp9321'
    # host = 'mongodb://jingxuan:asdf1234@ds149279.mlab.com:49279/my_mongodb_x'
)

def get_records_with_filter(filters):
    connect('record')
    result = []

    if 'year' in filters:
        for t in Record.objects(Q(area=filters['lgaName'][0])):
            # t.details._data
            details = []
            for d in t.details:
                if d['period'] == 'Jan-Dec ' + str(filters['year'][0]):
                     details.append(d._data)
            t.details = details
            # print(t._data)
            result.append(t._data)
        return (result)
    else:
        for t in Record.objects(Q(area=filters['lgaName'][0])| Q(area=filters['lgaName'][1])):
            # t.details._data
            details = []
            for d in t.details:
                details.append(d._data)
            t.details = details
            # print(t._data)
            result.append(t._data)
        return (result)



def get_all_records():
    connect('teacher')
    result = []
    for t in Record.objects:
        details = []
        for d in t.details:
            details.append(d._data)
        t.details = details
        result.append(t._data)
    # print(result)
    return result


def get_one_record(name):
    connect('record')
    result = []
    for t in Record.objects(area=name):
        # t.details._data
        details = []
        for d in t.details:
            details.append(d._data)
        t.details = details
    # print(t._data)
        result.append(t._data)
    return(result)

    # print(toxml(t._data))
def get_one_record_id(tid):
    connect('record')
    result = []
    for t in Record.objects(id=tid):
        # t.details._data
        details = []
        for d in t.details:
            details.append(d._data)
        t.details = details
    # print(t._data)
        result.append(t._data)
    return(result)

def delete_record_info(tid):
    connect('record')
    Record.objects(id=tid).delete()


def save_xlsx_data_to_monogo(name):

    data = xlrd.open_workbook(dir + name + ".xlsx")
    table = data.sheets()[0]
    nrows = table.nrows - 14
    offence_group = ""
    details = []
    for i in range(7, nrows):
        line = table.row_values(i)
        # print("---:",line)
        if(line[0]):
            offence_group = line[0]
        for j in range(13):
            if j < 10:
                details.append(Detail(i*100 + j, offence_group, line[1], table.row_values(5)[2 * int(j/2) + 2], table.row_values(6)[j % 2 + 2], str(line[j + 2])))
                # print((i*100 + j, offence_group, line[1], table.row_values(5)[2 * int(j/2) + 2], table.row_values(6)[j % 2 + 2], str(line[j + 2])))
            else:
                details.append(Detail(i*100 + j, offence_group, line[1], "" ,table.row_values(6)[j], str(line[j + 2])))
                # print((i*100 + j, offence_group, line[1], "" ,table.row_values(6)[j], str(line[j + 2])))
    record = Record(int(time.time()),table.row_values(0)[0], table.row_values(2)[0], name, details)
    connect('record')
    record.save()

    result = []
    for t in Record.objects(area=name):
        result.append(t._data)
        return result

if __name__ == '__main__':
    # save_xlsx_data_to_monogo("CanadaBay")
    # try:
    #     delete_record_info(1524543324)
    #     print("ok")
    # except Exception as e:
    #     print("daag")
    #     print(e)
    # a = get_one_record_id(1524577736)
    # print(a)
    print(get_records_with_filter({'lgaName': ['Albury','CentralDarling'], 'operation': 'and'}))