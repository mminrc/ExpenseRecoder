from tkinter import*
from tkinter import ttk, messagebox #ttk คือ ธีม ของ tk, messagebox คือ ไลเบอรี่ของการแสดงป้อบอัพแจ้งเตือน
import csv
from datetime import datetime
#--------------------Database-----------------
import sqlite3

# สร้าง Database
conn = sqlite3.connect('expense.sqlite3')
# สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

# สร้าง table ด้วยภาษา SQL 
'''
'รหัสรายการ (transactionid) TEXT'
'วัน-เวลา(datetime) TEXT'
'รายการ(orders) TEXT'
'ค่าใช้จ่าย(expense) REAL' :REAL = FLOAT
'จำนวน(quantity) INTRGER'
'รวมทั้งหมด(total) REAL'
'''
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transactionid TEXT,
                datetime TEXT,
                orders TEXT,
                expense REAL,
                quantity INTEGER,
                total REAL
            )""")
# ฟังก์ชันเพิ่มข้อมูล
def insert_expense(transactionid,datetime,orders,expense,quantity,total):
    ID = None
    with conn:
        c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
            (ID,transactionid,datetime,orders,expense,quantity,total))
    conn.commit() #การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก

# ฟังก์ชันอ่านข้อมูล
def show_expense():
    with conn:
        c.execute("SELECT * FROM expenselist")
        expense = c.fetchall() # fetchall() คือ คำสั่งในการดึงข้อมูลเข้ามา

    return expense

# ฟังก์ชันอัพเดทข้อมูล
def update_expense(transactionid,orders,expense,quantity,total):
    with conn:
        c.execute("""UPDATE expenselist SET orders=?, expense=?, quantity=?, total=? WHERE transactionid=?""",
            ([orders,expense,quantity,total,transactionid]))
    conn.commit()

# ฟังก์ชันลบข้อมูล
def delete_expense(transactionid):
    with conn:
        c.execute("DELETE FROM expenselist WHERE transactionid=?",([transactionid]))
    conn.commit()
#-----------------------------------------------

GUI = Tk() # T ตัวใหญ่
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Min') #ตั้งชื่อไตเติ้ล
# GUI.geometry('720x700+500+50') #ขนาดโปรแกรม+ระยะห่างจากขอบแนวแกนx+ระยะห่างจากขอบแนวแกนy

# ทำให้หน้าจอแอพอยู่ตรงกลาง
w = 720
h = 700

ws = GUI.winfo_screenwidth() # Screen width
hs = GUI.winfo_screenheight() # Screen height

x = (ws/2)-(w/2)
y = (hs/2)-(h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI หลักโดยจะวางจากบนลงล่าง, ipad = internal padding เป็นการกำหนดขนานของปุ่ม

# สร้างปุ่ม Menu
menubar = Menu(GUI)
GUI.config(menu=menubar)

# Flie menu and Exit menu
filemunu = Menu(menubar,tearoff=0) #tearoff คือ ทำให้ไม่สามารถดึงออกมาได้
menubar.add_cascade(label='File',menu=filemunu)
filemunu.add_command(label='Import csv')
filemunu.add_command(label='Import to Googlesheet')
def Exit():
    check = messagebox.askyesno('โปรดยืนยัน','คุณต้องการปิดโปรแกรมใช่หรือไม่ ?')
    if check == True:
        GUI.destroy()
filemunu.add_command(label = 'Exit',command=Exit)
# Help menu
halpmunu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=halpmunu)
halpmunu.add_command(label = 'About')
# Donate menu
def Donate():
    messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม ? ขอคนละ 100 บาท\n พร้อมเพย์: ')
donatemunu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemunu)
donatemunu.add_command(label='Donate',command=Donate)


# วิธีการสร้าง Tab
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1) #(fill=BOTH,expand=1) คือ ปรับแต่งตำแหน่ง

# การใส่รูป
icon_t1 = PhotoImage(file='t1_expense.png') #.subsample(2) = ย่อรูป
icon_t2 = PhotoImage(file='t2_expenselist.png')

Tab.add(T1,text= f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2,text= f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
# F1.place(x=100,y=50) #.palce() ติดปุ่มเข้ากับ GUI หลักแบบกำหนดตำแหน่งได้ ต้องมีค่าแกนx และค่าแกน y
F1.pack()

days = {'Mon':'วันจันทร์',
        'Tue':'วันอังคาร',
        'Wed':'วันพุธ',
        'Thu':'วันพฤหัสบดี',
        'Fri':'วันศุกร์',
        'Sat':'วันเสาร์',
        'Sun':'วันอาทิตย์'}

def Save(event=None):
    dt = datetime.now()
    expense = v_expense.get() # .get() คือ ดึงค่ามาจาก v_expense = StringVar()
    price = v_price.get()
    quantity = v_quantity.get()
    if expense == '' and price == '' and quantity == '':
        messagebox.showwarning('Error','โปรดตรวจสอบข้อมูลให้ครบถ้วน')
        return
    elif expense == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกราคาค่าใช้จ่าย')
        return
    try: # try คือ การดักจับ Error โดยลองทำส่วนนี้ก่อนถ้าทำไมได้จะเด้งไปที่ except 
        total = float(price)*int(quantity)
        today = datetime.now().strftime('%a')
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today]+'-'+dt
        print('{} รายการ: {} ราคา {} บาท'.format(dt,expense,price))
        print('จำนวน {} ชิ้น รวมทั้งหมด {} บาท'.format(quantity,total))
        text = 'รายการ: {} ราคา: {} บาท\n'.format(expense,price)
        text = text+'จำนวน: {} ชิ้น รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)
        # เคลียร์ข้อมูลเก่า
        v_expense.set('') # .set เป็นการกำหนดค่าแสดง
        v_price.set('')
        v_quantity.set('')

        insert_expense(transactionid,dt,expense,float(price),int(quantity),total)

        # บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
        # with คือ สั่งเปิด file แล้วปิดอัตโนมัติ, 'a' คือ การบันทึกเรื่อย ๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า, newline='' คือ ทำให้ข้อมูลไม่ต้องมีบรรทัดว่าง
            fw = csv.writer(f) #สร้าง function สำหรับเขียนข้อมูล
            data = [transactionid,dt,expense,price,quantity,total]
            fw.writerow(data)
        # ทำให้เคอร์เซอร์กลับไปตำแหน่งช่องกรอก E1
        E1.focus()
        update_table()
    except Exception as e: # Exception as e คือ การบ่งบอกเพื่อหาสาเหตุของการ Error จะใส่ก็ได้ไม่ใส่ก็ได้
        print('ERROR',e)
        messagebox.showwarning('Error','กรุณากรอกจำนวน')
        v_expense.set('') #.set เป็นการกำหนดค่าแสดง
        v_price.set('')
        v_quantity.set('')

# ทำให้สามารถกด Enter ได้
GUI.bind('<Return>',Save) # ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New' กรณีตั้งตัวอักษร

#--------------------Image-----------------
main_icon = PhotoImage(file='icon_shop.png')
Mainicon = Label(F1,image = main_icon)
Mainicon.pack()
#------------------------------------------

#--------------------text1-----------------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1) # .Entry คือ ช่องกรอกข้อมูล
E1.pack()
#------------------------------------------

#--------------------text2-----------------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#------------------------------------------

#--------------------text3-----------------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#------------------------------------------

icon_b1 = PhotoImage(file='b_save.png')
B2 = ttk.Button(F1,text=f'{"Save":<{15}}',command=Save,image=icon_b1,compound='right') # command ตามด้วยชื่องฟังก์ชัน
B2.pack(ipadx=50,ipady=20,pady=20) # pady = ระยะห่างระหว่างปุ่มในแนวแกน y

v_result = StringVar()
v_result.set('------------ผลลัพธ์------------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='green') # foreground คือ การเปลี่ยนสี
result.pack(pady=20)

#--------------------tab 2-----------------

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

# สร้าง Table

L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)


header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวมทั้งหมด']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()

'''
for i in range(len(header)):
    resulttable.heading(header[i],text=header[i])
'''
for h in header:
    resulttable.heading(h,text=h)

headerwidth = [120,180,170,80,80,80]
for h,w in zip(header,headerwidth): # zip คือ คำสั่งที่ใช้ในการจับคู่กัน
    resulttable.column(h,width=w)

alltransaction = {}

def updateCSV():
    with open('savedata.csv','w',newline='',encoding='utf-8') as f: # 'w' คือ การวางทับ
        fw = csv.writer(f)
        # เตรียมข้อมูลจาก alltransection ให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data) #multiple line from nested list [[],[],[]]

def UpdateSQL():
    data = list(alltransaction.values())
    for d in data:
        update_expense(d[0],d[2],d[3],d[4],d[5])


def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm ?','คุณต้องการลบใช่หรือไม่ ?')
    if check == True:
        select = resulttable.selection()
        data = resulttable.item(select) # ดึงไอเท็มนั้นมา
        data = data['values']
        transactionid = data[0]
        del alltransaction[str(transactionid)] # ลบข้อมูลใน Dict
        #updateCSV()
        delete_expense(str(transactionid)) # การลบในฐานข้อมูล
        update_table()
    else:
        pass

Bdelete = ttk.Button(T2,text='Delete',command=DeleteRecord)
Bdelete.place(x=30,y=320)

resulttable.bind('<Delete>',DeleteRecord)

def update_table():
    resulttable.delete(*resulttable.get_children()) # .get_children() คือ รหัสพิเศษ
    try:
        data = show_expense() # read_csv()
        for d in data:
            # สร้าง transaction data
            alltransaction[d[1]] = d[1:] # d[1] = transactionid
            resulttable.insert('',0,value=d[1:])
    except Exception as e:
        print(Erroe,e)

#--------------------Right Click Menu-----------------
def EditRecord():
    POPUP = Toplevel() # POPUP คล้าย ๆ กับ Tk แต่ Tk ประกาศได้ทีเดียว แต่ถ้าเราต้องสร้างอีกหน้าต่างนึง ต้องใช้ POPUP
    POPUP.title('Edit Record')
    # POPUP.geometry('500x400')
    w = 500
    h = 400

    ws = POPUP.winfo_screenwidth() #screen width
    hs = POPUP.winfo_screenheight() #screen height

    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    #--------------------text1-----------------
    L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
    v_expense = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1) # .Entry คือ ช่องกรอกข้อมูล
    E1.pack()
    #------------------------------------------

    #--------------------text2-----------------
    L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
    v_price = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
    E2.pack()
    #------------------------------------------

    #--------------------text3-----------------
    L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
    v_quantity = StringVar() # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
    E3.pack()
    #------------------------------------------

    def Edit():
        olddata = alltransaction[str(transactionid)]
        v1 = v_expense.get()
        v2 = float(v_price.get())
        v3 = int(v_quantity.get())
        total = v2*v3
        newdata = [olddata[0],olddata[1],v1,v2,v3,total]
        alltransaction[str(transactionid)] = newdata
        # updateCSV()
        UpdateSQL()
        # update_expense(olddata[0],olddata[1],v1,v2,v3,total) คือ การอัพเดทบางส่วนจากการแก้ไขบางส่วน
        update_table()
        POPUP.destroy() # สั่งปิด POPUP

    icon_b1 = PhotoImage(file='b_save.png')
    B2 = ttk.Button(POPUP,text=f'{"Save":<{15}}',image=icon_b1,compound='right',command=Edit) # command ตามด้วยชื่องฟังก์ชัน
    B2.pack(ipadx=50,ipady=20,pady=20) # pady = ระยะห่างระหว่างปุ่มในแนวแกน y

    # ดึงข้อมูลใน select record
    select = resulttable.selection()
    data = resulttable.item(select) # ดึงไอเท็มนั้นมา
    data = data['values']
    transactionid = data[0]
    # สั่ง SET ค่าเก่าไว้ตรงช่องกรอก
    v_expense.set(data[2])
    v_price.set(data[3])
    v_quantity.set(data[4])

    POPUP.mainloop()


rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
    rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup)

update_table()
UpdateSQL()
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()