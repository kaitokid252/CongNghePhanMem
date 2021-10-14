import pyodbc 
import datetime
conn = pyodbc.connect('Driver={SQL Server};'
						'Server=ADMIN\KAITO;'
						'Database=QuanLyNhaHang;'
						'Trusted_Connection=yes;')
class menu():
	def __init__(self,idfood,food,count):
		self.idfood=idfood
		self.food=food
		self.count=count
def giaodienmenu():
	cursorMenu= conn.cursor()
	cursorMenu.execute('SELECT * FROM Food')
	print ("ID\t\t\tFOOD\t\t\tPRICE")
	print ("---------------------------------------------------------------")
	for i in cursorMenu:
		print ("%s\t\t\t%s\t\t\t%d" % (i[0],i[1],i[2]))
	print ("---------------------------------------------------------------")
def giaodiengoimon():
	cursorTable=conn.cursor()
	kt=0
	cursorTable.execute('SELECT * FROM TableFood WHERE status=0')
	for i in cursorTable:
		kt=kt+1
	if(kt==0):
		print("Tất cả các bàn đều có người vui lòng quay lại sau.")
	else:
		cursorTable.execute('SELECT * FROM TableFood')
		print ("ID\t\t\tNAME\t\tSTATUS")
		print ("---------------------------------------------------------------")
		for i in cursorTable:
			if(i[2]==0):
				status="Trống"
			else:
				status="Có người"
			print ("%s\t\t\t%s\t\t%s" % (i[0],i[1],status))
		print ("---------------------------------------------------------------")
		kt=True
		while(kt):
			MaTable=int(input("Nhập ID bàn bạn muốn đặt: "))
			cursorTable.execute('SELECT * FROM TableFood WHERE id=(?)',(MaTable))
			kiemtra=0
			for i in cursorTable:
				kiemtra=kiemtra+1
				if(i[2]==0):
					kt=False
				else:
					print("Bàn bạn đặt đã có người vui lòng nhập lại ID bàn bạn muốn đặt.")
			if(not kt):
				print("Bạn đã đặt bàn thành công")
				cursorTable.execute('UPDATE TableFood SET status=1 WHERE id=(?)',(MaTable))
				conn.commit()
			if(kiemtra==0):
				print("Không ID này trong nhà hàng.Vui lòng nhập lại!")
		giaodienmenu()
		tongtien=0
		cursorBill=conn.cursor()
		cursorCount=conn.cursor()
		cursorBillInfo=conn.cursor()
		cursorMenu= conn.cursor()
		cursorBill.execute('INSERT INTO Bill(idTable,CheckIn,Checkout,Totalprice,status) VALUES (?,?,?,?,?)',(MaTable,datetime.datetime.today(),'',tongtien,0))
		conn.commit()
		dsmenu=[]
		while(True):
			print("Nhập 1: để gọi món")
			print("Nhập 2: để chốt hoá đơn")
			print("Nhập 3: Exit")
			test=int(input("Nhập lựa chọn: "))
			if(test==1):
				while(True):
					MaFood=int(input("Nhập ID món ăn bạn muốn gọi: "))
					cursorMenu.execute('SELECT id,name FROM Food WHERE id=(?)',(MaFood))
					kt=0
					for i in cursorMenu:
						NameFood=i[1]
						kt=kt+1
					if(kt==0):
						print("Nhập sai ID vui lòng nhập lại!")
					else:
						break
				while(True):
					soluong=int(input("Nhập số lượng bạn muốn gọi: "))
					if(soluong<1):
						print("Số lượng không thể nhỏ hơn 1! Vui lòng nhập lại.")
					else:
						Mondagoi=menu(MaFood,NameFood,soluong)
						dsmenu.append(Mondagoi)
						cursorCount.execute('SELECT count FROM Food WHERE id=(?)',(MaFood))
						for i in cursorCount:
							Dem=i[0]
						Dem=Dem+soluong
						cursorCount.execute('UPDATE Food SET count=(?) WHERE id=(?)',(Dem,MaFood))
						conn.commit()
						break
				print("Đặt món thành công.")
				cursorMenu.execute('SELECT * FROM Food WHERE id=(?)',(MaFood))
				for i in cursorMenu:
					tongtien=tongtien+i[2]*soluong
				cursorBill.execute('SELECT id FROM Bill WHERE idTable=(?) and status=0',(MaTable))
				for i in cursorBill:
					idBill=i[0]
				cursorBill.execute('UPDATE Bill SET Totalprice=(?) WHERE id=(?)',(tongtien,idBill))
				conn.commit()
			elif(test==2):
				if(tongtien==0):
					print("Bạn chưa chọn món nào để chốt hoá đơn!")
				else:
					print ("IdTable\t\t\tNAME\t\tSoLuong")
					for i in dsmenu:
						print("%d\t\t\t%s\t\t%d" %(i.idfood,i.food,i.count))
					print("Tổng tiền của bạn là:"+str(tongtien)+" VND")
			elif(test==3):
				break
			else:
				print("Nhập sai vui lòng nhập lại lựa chọn!")
def thaydoi():
	giaodienmenu()
	cursorMenu= conn.cursor()
	kt=True
	while(kt):
		cursorMenu.execute('SELECT id FROM Food')
		maFood=int(input("Chọn ID món bạn muốn thay đổi giá: "))
		for i in cursorMenu:
			if(i[0]==maFood):
				kt=False
				break
		if(kt==True):
			print("Không có ID này vui lòng nhập lại!")
	while(True):
		gia=int(input("Nhập giá mà bạn muốn đổi: "))
		if(gia<1):
			print("Giá không hợp lí vui lòng nhập lại!")
		else:
			break
	cursorMenu.execute('UPDATE Food SET price=(?) WHERE id=(?)',(gia,maFood))
	conn.commit()
	print("Thay đổi giá món ăn thành công.")	
	giaodienmenu()
def suamenu():
	giaodienmenu()
	while(True):
		cursorMenu= conn.cursor()
		cursorBillInfo=conn.cursor()
		print("1:Xoá món ăn")
		print("2:Thêm món ăn")
		print("3:Exit")
		test=int(input("Nhập lựa chọn: "))
		if(test==1):
			kt=True
			while(kt):
				cursorMenu.execute('SELECT id FROM Food')
				maFood=int(input("Nhập ID món ăn bạn muốn xoá: "))
				for i in cursorMenu:
						if(i[0]==maFood):
							kt=False
				if(kt):
					print("Không có ID này vui lòng nhập lại!")
			while(True):
				check=input("Bạn đã chắc chắn muốn xoá dữ liệu này không(Y/N): ")
				if(check=='Y' or check=='y'):
					cursorMenu.execute('DELETE FROM Food WHERE id=(?)',(maFood))
					conn.commit()
					print("Đã xoá thành công.")
					giaodienmenu()
					break
				elif(check=='N' or check=='n'):
					break
				else:
					print("Nhập sai vui lòng nhập lại.")
		elif(test==2):
			kt=True
			NUll=0
			while(kt):
				cursorMenu.execute('SELECT id FROM Food')
				maFood=int(input("Nhập ID món bạn muốn thêm: "))
				for i in cursorMenu:
					NUll=NUll+1
					if(i[0]==maFood):
						print("Nhập lại ID, ID đã tồn tại!")
						kt=True
						break
					else:
						kt=False
				if(NUll==0):
					break
			kt=True
			while(kt):
				monan=input("Nhập tên món ăn bạn muốn thêm: ")
				if(monan==''):
					print("Vui lòng nhập tên món ăn!")
				else:
					NUll=0
					cursorMenu.execute('SELECT name FROM Food')
					for i in cursorMenu:
						NUll=NUll+1
						if(i[0]==monan):
							print('Tên này đã có trong menu.Vui lòng nhập lại!')
							kt=True
							break
						else:
							kt=False
					if(NUll==0):
						break
			while(True):
				gia=int(input("Nhập giá món ăn: "))
				if(gia<1):
					print("Giá không hợp lý vui lòng nhập lại!")
				else:
					break
			cursorMenu.execute("INSERT INTO Food(id,name,price) VALUES (?,?,?)",(maFood,monan,gia))
			conn.commit()
			print("Thêm món ăn thành công.")
			giaodienmenu()
		elif(test==3):
			break
		else:
			print("Không có lựa chọn này vui lòng chọn lại!")
def dangnhap():
	cursorAcc=conn.cursor()
	kt=True
	while(kt):
		cursorAcc.execute('SELECT * FROM Account')
		while (True):
			account=input("Nhập tên đăng nhập:")
			if(account==''):
				print('Vui lòng nhập tên đăng nhập!')
			else:
				break
		while(True):
			password=input("Nhập mật khẩu:")
			if(password==''):
				print('Vui lòng nhập mật khẩu!')
			else:
				break
		for i in cursorAcc:
			if(account==i[0] and password==i[1]):
				kt=False
		if(kt):	
			print("Tài khoản hoặc mật khẩu của ban bị sai,vui lòng nhập lại!")
	giaodienAdmin()
def giaodienAdmin():
	while(True):
		print("1:Xem menu")
		print("2:Đặt món,chọn bàn")
		print("3:Thay đổi giá của món ăn")
		print("4:Thay đổi menu")
		print("5:Xem hoá đơn chưa thanh toán")
		print("6:Xem tổng doanh thu trong ngày")
		print("7:Exit")
		test=int(input("Nhập lựa chọn của bạn: "))
		if(test==1):
			giaodienmenu()
		elif(test==2):
			giaodiengoimon()
		elif(test==3):
			thaydoi()
		elif(test==4):
			suamenu()
		elif(test==5):
			Bill()
		elif(test==6):
			checkDoanhthu()
		elif(test==7):
			break
		else:
			print("Nhập sai vui lòng nhập lại.")
def giaodienKhach():
	while(True):
		print("1:Xem menu")
		print("2:Đặt món,chọn bàn")
		print("3:Exit")
		test=int(input("Nhập lựa chọn của bạn: "))
		if(test==1):
			giaodienmenu()
		elif(test==2):
			giaodiengoimon()
			break
		elif(test==3):
			break
		else:
			print("Nhập sai vui lòng nhập lại.")
def Bill():
	cursorTable=conn.cursor()
	Table={}
	cursorTable.execute('SELECT id,name FROM TableFood')
	for i in cursorTable:
		Table[i[0]]=i[1]
	while(True):
		cursorBill=conn.cursor()
		cursorMenu=conn.cursor()
		cursorBill.execute('SELECT * FROM Bill WHERE status=0' )
		print ("ID\t\t\tNAME_TABLE\tCheckIn\t\t\t\t\t\tTotal_Price")
		for i in cursorBill:
			print ("%d\t\t\t%s\t\t%s\t\t\t%d" % (i[0],Table[i[1]],i[2],i[4]))
		print("1:Chọn hoá đơn thanh toán")
		print("2:Thoát")
		test=int(input("Nhập lựa chọn của bạn: "))
		if(test==1):
			kt=True
			while(kt):
				cursorBill.execute('SELECT * FROM Bill WHERE status=0')
				maBill=int(input("Chọn ID hoá đơn thanh toán: "))
				for i in cursorBill:
					if(maBill==i[0]):
						kt=False
						MaTable=i[1]
				if(kt==True):
					print("Nhập sai ID vui lòng nhập lại.")
			cursorBill.execute('SELECT Totalprice FROM Bill WHERE id=(?)',maBill)
			for i in cursorBill:
				print("Tổng tiền hoá đơn là:",i[0])
			cursorBill.execute('UPDATE Bill SET Checkout=(?),status=(?) WHERE id=(?)',(datetime.datetime.today(),1,maBill))
			conn.commit()
			cursorTableFood=conn.cursor()
			cursorTableFood.execute('UPDATE TableFood SET status=(?) WHERE id=(?)',(0,MaTable))
			conn.commit()
		elif(test==2):
			break
		else:
			print("Nhập sai vui lòng nhập lại.")
def checkDoanhthu():
	cursorBill=conn.cursor()
	while(True):
		print("1:Xem doanh thu của ngày hôm nay")
		print("2:Xem doanh thu của tháng")
		print("3:Xem doanh thu của quý")
		print("4:Exit")
		test=int(input("Nhập lựa chọn của bạn: "))
		if(test==1):
			cursorBill.execute('SELECT Totalprice FROM Bill WHERE status=1 And day(Checkout)=(?) and month(Checkout)=(?) and year(Checkout)=(?)',(datetime.date.today().day,datetime.date.today().month,datetime.date.today().year))
			Tongdoanhso=0
			for i in cursorBill:
				Tongdoanhso=Tongdoanhso+i[0]
			print("Tổng doanh số ngày hôm nay là: ",Tongdoanhso,"VND")
		elif(test==2):
			while(True):
				thang=int(input("Nhập tháng bạn muốn xem: "))
				if(thang<=0 or thang>12):
					print("Nhập tháng sai vui lòng nhập lại!")
				else:
					break
			Tongdoanhso=0
			cursorBill.execute('SELECT Totalprice FROM Bill WHERE status=1 and month(Checkout)=(?) and year(Checkout)=(?)',(thang,datetime.date.today().year))
			for i in cursorBill:
				Tongdoanhso=Tongdoanhso+i[0]
			print("Doanh số của tháng "+str(thang)+" là:",Tongdoanhso,"VND")
		elif(test==3):
			while(True):
				quy=int(input("Nhập quý bạn muốn xem: "))
				if(quy<=0 or quy>4):
					print("Nhập sai quý vui lòng nhập lại!")
				else:
					break
			thang=quy*3
			Tongdoanhso=0
			for x in range(0,3):
				cursorBill.execute('SELECT Totalprice FROM Bill WHERE status=1 and month(Checkout)=(?) and year(Checkout)=(?)',(thang,datetime.date.today().year))
				for i in cursorBill:
					Tongdoanhso=Tongdoanhso+i[0]
				thang=thang-1
			print("Doanh số của quý "+str(quy)+" là:",Tongdoanhso,"VND")
		elif(test==4):
			break
		else:
			print("Nhập sai vui lòng nhập lại.")
def giaodienBandau():
	while(True):
		print("1:Đăng nhập để quản lý nhà hàng.")
		print("2:Là Khách hàng muốn xem menu và gọi món.")
		test=int(input("Nhập lựa chọn: "))
		if(test==1):
			dangnhap()
			break
		elif(test==2):
			giaodienKhach()
			break
		else:
			print("Nhập sai vui lòng nhập lại.")
giaodienBandau()