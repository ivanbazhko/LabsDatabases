import psycopg2
import string
from tkinter import *
from tables_params import *
from queries_params import *
from validators import *

conn = ''
cursor = ''

def db_connect():
  global conn
  global cursor
  try:
        conn = psycopg2.connect(
            database="airport",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        print("Successfully connected to PostgreSQL")
  except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        
def on_closing():
  global conn
  finish = 0
  try:
    conn.close()
    print("Successfully disconnected from PostgreSQL")
  except Exception:
    pass
  root.destroy()

def add_data():
  global conn
  global cursor
  goodparam = 1
  lines = field1.get(1.0, END)
  data = [line for line in lines.split('\n') if line]
  table_data = getTableParams(selected_value1.get())
  if not len(data) == table_data[-1]:
    goodparam = 0
  q = 0
  if goodparam == 1:
    for z in range(0, table_data[-1]):
      if table_data[z + 1][3] == 'st':
        q += 1
      elif table_data[z + 1][3] == 's2':
        res = s2_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 's3':
        res = s3_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'nu':
        res = nu_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'n4':
        res = n4_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'fl':
        res = fl_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'tm':
        res = tm_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'np':
        res = np_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'nt':
        res = nt_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif table_data[z + 1][3] == 'wd':
        res = wd_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
  if goodparam == 1:
    stringtoadd = ''
    for datum in data:
      stringtoadd += '\'' + str(datum) + '\', '
      last_comma_index = stringtoadd.rfind(",")
    if last_comma_index != -1:
      stringtoadd = stringtoadd[:last_comma_index]
    try:
      cursor.execute(f"INSERT INTO {table_data[0]} VALUES ({stringtoadd});")
      conn.commit()
      show_data()
      field2.config(fg="green")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", f"Добавлено: {stringtoadd}!")
      field2.config(state=DISABLED)
    except (psycopg2.errors.UniqueViolation):
      field2.config(fg="red")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", "Ошибка: запись с таким первичным ключом уже существует!")
      field2.config(state=DISABLED)
      try:
        conn.close()
        db_connect()
      except Exception:
        pass
    except (psycopg2.errors.ForeignKeyViolation):
      field2.config(fg="red")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", "Ошибка: внешний ключ не найден!")
      field2.config(state=DISABLED)
      try:
        conn.close()
        db_connect()
      except Exception:
        pass
  else:
    field2.config(fg="red")
    field2.config(state=NORMAL)
    field2.delete("1.0", "end")
    field2.insert("1.0", "Неверный Ввод!")
    field2.config(state=DISABLED)
    
def upd_data():
  global conn
  global cursor
  goodparam = 1
  keyscount = 0
  keystuple = ()
  lines = field1.get(1.0, END)
  data = [line for line in lines.split('\n') if line]
  table_data = getTableParams(selected_value1.get())
  for d in range (0, table_data[-1]):
    if table_data[d + 1][0] == data[0]:
      keyscount += 1
      keystuple = keystuple + (table_data[d + 1],)
  if not keyscount > 0:
    goodparam = 0
  if goodparam == 1:
    for z in range(0, keyscount):
      if keystuple[z][3] == 'st':
        pass
      elif keystuple[z][3] == 's2':
        res = s2_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 's3':
        res = s3_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'nu':
        res = nu_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'n4':
        res = n4_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'fl':
        res = fl_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'tm':
        res = tm_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'np':
        res = np_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'nt':
        res = nt_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'wd':
        res = wd_val(data[1])
        if res:
          pass
        else:
          goodparam = 0
          break
        
        
        
        
        
        
        
        
        
  if goodparam == 1:
    keyscount = 0
    keystuple = ()
    for d in range (0, table_data[-1]):
      if table_data[d + 1][2] == 1:
        keyscount += 1
        keystuple = keystuple + (table_data[d + 1],)
    if not len(data) == (keyscount + 2):
      goodparam = 0
    q = 2
    if goodparam == 1:
      for z in range(0, keyscount):
        if keystuple[z][3] == 'st':
          q += 1
        elif keystuple[z][3] == 's2':
          res = s2_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 's3':
          res = s3_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'nu':
          res = nu_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'n4':
          res = n4_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'fl':
          res = fl_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'tm':
          res = tm_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'np':
          res = np_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'nt':
          res = nt_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
        elif keystuple[z][3] == 'wd':
          res = wd_val(data[q])
          if res:
            q += 1
          else:
            goodparam = 0
            break
  if goodparam == 1:
    stringtodel = ''
    w = 0
    for datum in data:
      if w >= 2:
        stringtodel += '\"' + str(keystuple[w - 2][0]) + '\" = \'' + str(datum) + '\' AND '
        last_and_index = stringtodel.rfind(" AND ")
      w += 1
    if last_and_index != -1:
      stringtodel = stringtodel[:last_and_index]
    stringtomod = '\"' + data[0] + '\" = \'' + data[1] + '\'' 
    try:
      cursor.execute(f"UPDATE {table_data[0]} SET {stringtomod} WHERE {stringtodel}")
      del_count = cursor.rowcount
      conn.commit()
      show_data()
      field2.config(fg="green")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      if del_count > 0:
        field2.insert("1.0", f"Обновлено: {stringtodel}!")
      else:
        field2.insert("1.0", f"Такой записи нет: {stringtodel}!")
      field2.config(state=DISABLED)
    except (psycopg2.errors.UniqueViolation):
      field2.config(fg="red")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", "Ошибка: запись с таким первичным ключом уже существует!")
      field2.config(state=DISABLED)
      try:
        conn.close()
        db_connect()
      except Exception:
        pass
    except (psycopg2.errors.ForeignKeyViolation):
      field2.config(fg="red")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", "Ошибка: нельзя изменить поле записи, на которое ссылаются другие записи!")
      field2.config(state=DISABLED)
      try:
        conn.close()
        db_connect()
      except Exception:
        pass
  else:
    field2.config(fg="red")
    field2.config(state=NORMAL)
    field2.delete("1.0", "end")
    field2.insert("1.0", "Неверный Ввод!")
    field2.config(state=DISABLED)
    
def del_data():
  global conn
  global cursor
  goodparam = 1
  keyscount = 0
  keystuple = ()
  lines = field1.get(1.0, END)
  data = [line for line in lines.split('\n') if line]
  table_data = getTableParams(selected_value1.get())
  for d in range (0, table_data[-1]):
    if table_data[d + 1][2] == 1:
      keyscount += 1
      keystuple = keystuple + (table_data[d + 1],)
  if not len(data) == keyscount:
    goodparam = 0
  q = 0
  if goodparam == 1:
    for z in range(0, keyscount):
      if keystuple[z][3] == 'st':
        q += 1
      elif keystuple[z][3] == 's2':
        res = s2_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 's3':
        res = s3_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'nu':
        res = nu_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'n4':
        res = n4_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'fl':
        res = fl_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'tm':
        res = tm_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'np':
        res = np_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'nt':
        res = nt_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
      elif keystuple[z][3] == 'wd':
        res = wd_val(data[q])
        if res:
          q += 1
        else:
          goodparam = 0
          break
  if goodparam == 1:
    stringtodel = ''
    w = 0
    for datum in data:
      stringtodel += '\"' + str(keystuple[w][0]) + '\" = \'' + str(datum) + '\' AND '
      last_and_index = stringtodel.rfind(" AND ")
      w += 1
    if last_and_index != -1:
      stringtodel = stringtodel[:last_and_index]
    try:
      cursor.execute(f"DELETE FROM {table_data[0]} WHERE {stringtodel};")
      del_count = cursor.rowcount
      conn.commit()
      show_data()
      field2.config(fg="green")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      if del_count > 0:
        field2.insert("1.0", f"Удалено: {stringtodel}!")
      else:
        field2.insert("1.0", f"Такой записи нет: {stringtodel}!")
      field2.config(state=DISABLED)
    except (psycopg2.errors.ForeignKeyViolation):
      field2.config(fg="red")
      field2.config(state=NORMAL)
      field2.delete("1.0", "end")
      field2.insert("1.0", "Ошибка: нельзя удалить запись, на которую ссылаются другие записи!")
      field2.config(state=DISABLED)
      try:
        conn.close()
        db_connect()
      except Exception:
        pass
  else:
    field2.config(fg="red")
    field2.config(state=NORMAL)
    field2.delete("1.0", "end")
    field2.insert("1.0", "Неверный Ввод!")
    field2.config(state=DISABLED)

def show_data():
        global conn
        global cursor
        table = getTableParams(selected_value1.get())
        cursor.execute(f"SELECT * FROM {table[0]};")
        rows = cursor.fetchall()
        i = 1
        mtext = ""
        j = table[-1]
        ftup = ()
        sumlen = 0
        counter = 0
        for m in range(j):
            ftup = ftup + (table[m + 1][0], table[m + 1][1],)
            sumlen += table[m + 1][1]
            counter += 1
        sumlen += counter + 1
        mtext += table[0] + ' (записей: ' + str(len(rows)) + ')\n'
        for x in range (sumlen):
            mtext += '='
        mtext += '\n'
        mtext += format_string_from_tuple(ftup)
        mtext += '\n'
        for x in range (sumlen):
            mtext += '='
        mtext += '\n'
        for row in rows:
            newtup = ()
            for k in range (j):
                newtup = newtup + (row[k], table[k + 1][1],)
            mtext += format_string_from_tuple(newtup)
            mtext += '\n'
            i += 1
        for x in range (sumlen):
            mtext += '='
        field.config(state=NORMAL)
        field.delete("1.0", "end")
        field.insert("1.0", mtext)
        field.config(state=DISABLED)
        
def ex_query():
        global conn
        global cursor
        query_to_ex = get_query_params(selected_value2.get())
        cursor.execute(query_to_ex[0][1])
        rows = cursor.fetchall()
        i = 1
        mtext = ""
        j = query_to_ex[-1]
        ftup = ()
        sumlen = 0
        counter = 0
        for m in range(j):
            ftup = ftup + (query_to_ex[m + 1][0], query_to_ex[m + 1][1],)
            sumlen += query_to_ex[m + 1][1]
            counter += 1
        sumlen += counter + 1
        mtext += query_to_ex[0][0] + ' (записей: ' + str(len(rows)) + ', запрос: ' + query_to_ex[0][1] + ')\n'
        for x in range (sumlen):
            mtext += '='
        mtext += '\n'
        mtext += format_string_from_tuple(ftup)
        mtext += '\n'
        for x in range (sumlen):
            mtext += '='
        mtext += '\n'
        for row in rows:
            newtup = ()
            for k in range (j):
                newtup = newtup + (row[k], query_to_ex[k + 1][1],)
            mtext += format_string_from_tuple(newtup)
            mtext += '\n'
            i += 1
        for x in range (sumlen):
            mtext += '='
        field.config(state=NORMAL)
        field.delete("1.0", "end")
        field.insert("1.0", mtext)
        field.config(state=DISABLED)
  

####################################################################

root = Tk()
root.title("Lab 6")
root.geometry("1500x750")
root.resizable(False, False)
root.config(bg="gray")

root.protocol("WM_DELETE_WINDOW", on_closing)

label = Frame(root, bg="white", padx=10, pady=10)
label.grid(row=0, column=0, padx=10, pady=10)
Label(label, text="ВЫВОД ДАННЫХ").pack()
field = Text(label, width=180, height=15)
field.pack(side=LEFT)
scrollbar = Scrollbar(label)
scrollbar.pack(side=RIGHT, fill=Y)
field.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=field.yview)
field.config(state=DISABLED)

buttonsstr = Frame(root, bg="gray", padx=45, pady=0)
buttonsstr.grid(row=1, column=0)

button1 = Button(buttonsstr, text="ВЫВЕСТИ ТАБЛИЦУ", command=show_data)
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = Button(buttonsstr, text="ВЫПОЛНИТЬ ЗАПРОС", command=ex_query)
button2.grid(row=0, column=1, padx=10, pady=10)

button3 = Button(buttonsstr, text="ДОБАВИТЬ", command=add_data)
button3.grid(row=0, column=2, padx=10, pady=10)

button4 = Button(buttonsstr, text="УДАЛИТЬ", command=del_data)
button4.grid(row=0, column=3, padx=10, pady=10)

button5 = Button(buttonsstr, text="ОБНОВИТЬ", command=upd_data)
button5.grid(row=0, column=4, padx=10, pady=10)

selected_value1 = StringVar()
selected_value1.set("Авиакомпании")
selected_value2 = StringVar()
selected_value2.set("Вывести список самолётов вместимостью от 100 до 200 пассажиров в обратном алфавитном порядке")

options1 = ["Авиакомпании", "Билеты", "Должности", "Допуски к направлениям", "Допуски к самолётам",
            "Направления", "Пассажиры", "Рейсы", "Самолёты", "Сотрудники"]

options2 = ["Вывести список самолётов вместимостью от 100 до 200 пассажиров в обратном алфавитном порядке", 
            "Вывести список билетов с указанием информации об авиакомпании, направлении и паспорте пассажира. Сортировать по названию авиакомпании", 
            "Вывести названия авиакомпаний из США", 
            "Вывести названия всех авиакомпаний по алфавиту, которые имеют рейсы", 
            "Вывести список сотрудников, которые имеют доступ к самолёту Concorde",
            "Вывести все должности с окладом более 80000. Сортировать по убыванию оклада", 
            "Вывести всех пассажиров, у которых номер паспорта начинается с AB", 
            "Вывести номера рейсов, которые вылетают по пятницам позже 13.00 но раньше 18.00", 
            "Вывести список всех направлений в Швеции и рейсы на это направление",
            "Вывести список самолётов Boeing по алфавиту и сотрудников, которые имеют к ним допуск", 
            "Вывести в верхнем регистре ФИО всех помощников пилота", 
            "Вывести список пассажиров, у которых от 10000 до 15000 бонусов и фамилией Сидоров/Сидорова", 
            "Вывести список пассажиров, которые купили билет на рейс авиакомпании Belavia (B2)", 
            "Вывести всех Офицеров авиационной безопасности, имеющих доступ к какому-либо направлению и само направление", 
            "Вывести в верхнем регистре названия должностей, на которых есть сотрудники с допуском к самолёту Airbus A320", 
            "Вывести страны, у которых более 1 направления с билетами и количество этих направлений", 
            "Вывести самолёты вместимостью более 300 от производителей, у которых есть самолёты вместимостью менее 150, к которым имеет доступ хотя бы 1 сотрудник и у которых есть рейсы", 
            "Вывести фамилии, которые встречаются и у сотрудников, и у пассажиров, имеющих билеты", 
            "Вывести имена, которые встречаются у сотрудников с должностью, содержащей слово техник, но не у пассажиров", 
            "Вывести самолёты вместимостью более 400, их среднюю вместимость и количество сотрудников, имеющих допуск к этим самолётам и к любому направлению", 
            "Вывести фамилии пассажиров, у которых (фамилий) есть более 1 билета и у пассажиров с этой фамилией бонусов больше, чем среднее расстояние до направлений", 
            "Вывести всех сотрудников, у которых есть допуск и к направлению, и к самолёту", 
            "Вывести минимальный и максимальный номера билетов, которые вылетают по пятницам от 08.00 до 18.00 по направлению, которое находится дальше любого направления в России", 
            "Вывести список всех авиакомпаний, в чьих странах есть направления и есть рейс с номером меньше среднего номера", 
            "Вывести сотрудников, имеющих допуски и к самолётам, и к направлениям, и у которых количество допусков к направлениям больше среднего количества допусков к самолётам", 
            "Вывести названия должностей, которые начинаются с ‘А’ и не имеют сотрудников и названия направлений, которые начинаются с ‘А’", 
            "Вывести сумму расстояний до направлений, сумму окладов и сумму количеств бонусов", 
            "Вывести названия должностей, на которых нет сотрудников, не имеющих допуска к самолёту", 
            "Вывести рейсы, у которых совпадают страна авиакомпании и страна направления", 
            "Вывести время вылета рейсов, которые выполняет авиакомпания, у которой есть билеты пассажиров с номером паспорта на ‘AB’"]

str2 = Frame(root, bg="gray", padx=45, pady=0)
str2.grid(row=2, column=0)

str2_1 = Frame(str2, bg="white", padx=45, pady=10)
str2_1.grid(row=0, column=0)
Label(str2_1, text="ВЫБОР ТАБЛИЦЫ").pack()
dropdown1 = OptionMenu(str2_1, selected_value1, *options1)
dropdown1.pack()

str2_2 = Frame(str2, bg="white", padx=45, pady=10)
str2_2.grid(row=0, column=1)
Label(str2_2, text="ВЫБОР ЗАПРОСА").pack()
dropdown2 = OptionMenu(str2_2, selected_value2, *options2)
dropdown2.pack()

container3 = Frame(root, bg="gray", padx=45, pady=10)
container3.grid(row=3, column=0)

str3 = Frame(container3, bg="gray", padx=45, pady=10)
str3.grid(row=0, column=0)

lab1 = Label(str3, text="ВВОД ДАННЫХ").pack()
field1 = Text(str3, width=60, height=15)
field1.pack(side=LEFT)
scrollbar1 = Scrollbar(str3)
scrollbar1.pack(side=RIGHT, fill=Y)
field1.config(yscrollcommand=scrollbar1.set)
scrollbar1.config(command=field1.yview)

str4 = Frame(container3, bg="gray", padx=45, pady=10)
str4.grid(row=0, column=1)

lab2 = Label(str4, text="СТАТУС").pack()
field2 = Text(str4, width=60, height=15)
field2.pack(side=LEFT)
scrollbar2 = Scrollbar(str4)
scrollbar2.pack(side=RIGHT, fill=Y)
field2.config(yscrollcommand=scrollbar2.set)
scrollbar2.config(command=field2.yview)
field2.config(state=DISABLED)

db_connect()

root.mainloop()

####################################################################
