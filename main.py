import kivy
import os
import mysql.connector
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from mysql.connector import Error
import hashlib



#Window.size = (1000,700)

class Manager(ScreenManager):
    pass

class Splashscreen(Screen):
    def switch(self, *args):
        self.parent.current = 'signin_win'

    def on_enter(self, *args):
        Clock.schedule_once(self.switch, 10)

class Signin(Screen):
    def switch(self, screen_name, *args):
        self.parent.current = str(screen_name)

    #def on_enter(self, *args):
    #    Clock.schedule_once(self.switch(), 3)

    def validate_user(self):
        connection = mysql.connector.connect(host='localhost',
                                             database='carwash',
                                             user='root',
                                             password='oyondi8363')
        cur = connection.cursor()

        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info

        username = user.text
        password = pwd.text

        if username == '' or password == '':
            info.text = '[color=#FF0000]username and/ or password required[/color]'
        else:
            cur.execute('SELECT * FROM carwash.users   ')
            user_det = cur.fetchall()
            for user in user_det:
                if username == user[4]:
                    #password = hashlib.sha256(password.encode()).hexdigest()
                    if password == user[3]:
                        if user[5] == 'Admin':
                            info.text = f'[color=#00FF00]Welcome back {user[5]} {user[4]} \n Logged In successfully!!![/color]'
                            self.parent.current = 'menu'
                        else:
                            info.text = f'[color=#00FF00]Welcome back {user[5]} {user[4]} \n Logged In successfully!!![/color]'
                            self.parent.current = 'menu'
                    else:
                        info.text = '[color=#FF0000]Invalid Password[/color]'
                        self.ids.pwd_field.text = ''
                else:
                    info.text = '[color=#FF0000]Invalid Username[/color]'

class LogoutPopup(FloatLayout):
    pass
class MainMenu(Screen):
    def log_out(self):
        show = LogoutPopup()
        popup_window = Popup(title='Log Out!!', content=show, auto_dismiss=False, size_hint=(None, None),
                             size=(400, 400))
        popup_window.open()

class Members(Screen):

    def fill_table(self):
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM members')
        members_list = cursor.fetchall()

        members_container = self.ids.member_records
        for members in members_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            members_container.add_widget(details)
            member_id = members[0]
            member_fname = members[1]
            member_lname = members[2]
            memberid = Label(text=str(member_id), size_hint_x=.3, color=(.2, .2, .2, 1))
            memberfname = Label(text=member_fname.title(), size_hint_x=.4, color=(.2, .2, .2, 1))
            memberlname = Label(text=member_lname.title(), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(memberid)
            details.add_widget(memberfname)
            details.add_widget(memberlname)
        cursor.close()
        db.close()

    def show_members(self):
        self.ids.member_records.clear_widgets()
        self.fill_table()

    def add_member(self):
        member_id = self.ids.id_inp.text
        member_fname = str(self.ids.fname_inp.text)
        member_lname = str(self.ids.lname_inp.text)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='carwash',
                                                 user='root',
                                                 password='oyondi8363')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO members (id,fname, lname) 
                                    VALUES (%s, %s, %s) """

            recordTuple = (member_id, member_fname, member_lname)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            self.ids.id_inp.text = ''
            self.ids.fname_inp.text = ''
            self.ids.lname_inp.text = ''
            show =MemberPopup()
            popup_window = Popup(title = 'Member Added', content = show, size_hint = (None,None), size = (400,400))
            popup_window.open()
        except mysql.connector.Error as error:
            error_msg = ("Failed to insert into MySQL table \n" + str(error))
            error_txt = Label(text=str(error_msg), size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            error_popup = Popup(title='Error!!', content=error_txt, size_hint=(None, None), size=(400, 400))
            error_popup.open()

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


class MemberPopup(FloatLayout):
    pass

class Services(Screen):
    def add_service(self):
        service_id = int(self.ids.service_id.text)
        service = str(self.ids.service.text)
        description = str(self.ids.description.text)
        cost = int(self.ids.cost.text)
        servicestaff_id = int(self.ids.servicestaff_id.text)
        servicereg_no = int(self.ids.servicereg_no.text)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='carwash',
                                                 user='root',
                                                 password='oyondi8363')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO services (serviceid, service, description, cost, staffid, regno) 
                                    VALUES (%s, %s, %s, %s, %s, %s) """

            recordTuple = (service_id, service,description,cost,servicestaff_id,servicereg_no)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            self.ids.service_id.text = ''
            self.ids.service.text = ''
            self.ids.description.text = ''
            self.ids.cost.text = ''
            self.ids.servicestaff_id.text = ''
            self.ids.servicereg_no.text = ''
            show = Label(text='Service added successfully !', size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            popup_window = Popup(title = 'Service Added', content = show, size_hint = (None,None), size = (400,400))
            popup_window.open()
        except mysql.connector.Error as error:
            error_msg = ("Failed to insert into MySQL table \n" + str(error))
            error_txt = Label(text=str(error_msg), size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            error_popup = Popup(title='Error!!', content=error_txt, size_hint=(None, None), size=(400, 400))
            error_popup.open()

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


class Staff(Screen):
    def fillstaff_table(self):
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM staff')
        staff_list = cursor.fetchall()

        staff_container = self.ids.staff_records
        for staff in staff_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            staff_container.add_widget(details)
            staffid = staff[0]
            nationalid = staff[1]
            fname = staff[2]
            lname = staff[3]
            staff_id = Label(text=str(staffid), size_hint_x=.3, color=(.2, .2, .2, 1))
            national_id = Label(text=str(nationalid), size_hint_x=.3, color=(.2, .2, .2, 1))
            stafffname = Label(text=str(fname), size_hint_x=.4, color=(.2, .2, .2, 1))
            stafflname = Label(text=str(lname), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(staff_id)
            details.add_widget(national_id)
            details.add_widget(stafffname)
            details.add_widget(stafflname)
        cursor.close()
        db.close()

    def show_staff(self):
        self.ids.staff_records.clear_widgets()
        self.fillstaff_table()

    def add_staff(self):
        staff_id = self.ids.staffid_inp.text
        national_id = self.ids.id_inp.text
        staff_fname = str(self.ids.firstname_inp.text)
        staff_lname = str(self.ids.lastname_inp.text)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='carwash',
                                                 user='root',
                                                 password='oyondi8363')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO staff (staffid,id,fname, lname) 
                                    VALUES (%s, %s, %s, %s) """

            recordTuple = (staff_id, national_id, staff_fname, staff_lname)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            self.ids.staffid_inp.text = ''
            self.ids.id_inp.text = ''
            self.ids.firstname_inp.text = ''
            self.ids.lastname_inp.text = ''

            show =Label(text='Staff added successfully !', size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            popup_window = Popup(title = 'Staff Added', content = show, size_hint = (None,None), size = (400,400))
            popup_window.open()
        except mysql.connector.Error as error:
            error_msg = ("Failed to insert into MySQL table \n" + str(error))
            error_txt = Label(text=str(error_msg), size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            error_popup = Popup(title='Error!!', content=error_txt, size_hint=(None, None), size=(400, 400))
            error_popup.open()

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()



class AddCar(Screen):
    def add_car(self):
        reg_no = int(self.ids.reg_no.text)
        model = str(self.ids.model.text)
        car_color = str(self.ids.car_color.text)
        owner_id = int(self.ids.owner_id.text)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='carwash',
                                                 user='root',
                                                 password='oyondi8363')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO cars (regno,model, color, id) 
                                    VALUES (%s, %s, %s,%s) """

            recordTuple = (reg_no, model,car_color,owner_id)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            self.ids.reg_no.text = ''
            self.ids.model.text = ''
            self.ids.car_color.text = ''
            self.ids.owner_id.text = ''
            show = Label(text='Car added successfully !', size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            popup_window = Popup(title = 'Car Added', content = show, size_hint = (None,None), size = (400,400))
            popup_window.open()
        except mysql.connector.Error as error:
            error_msg = ("Failed to insert into MySQL table \n" + str(error))
            error_txt = Label(text=str(error_msg), size_hint=(.6,.2),pos_hint={"x":.2, "top":1})
            error_popup = Popup(title='Error!!', content=error_txt, size_hint=(None, None), size=(400, 400))
            error_popup.open()

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

class Records(Screen):
    pass

class Financial(Screen):
    def on_enter(self):
        self.ids.financial_records.clear_widgets()
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('''SELECT serviceid, service, cost, staff.staffid, staff.fname FROM services JOIN staff ON services.staffid = staff.staffid''')
        financial_list = cursor.fetchall()

        financial_container = self.ids.financial_records
        for finances in financial_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            financial_container.add_widget(details)
            serviceid = finances[0]
            service_ = finances[1]
            cost = finances[2]
            staffid = finances[3]
            staffname = finances[4]
            service_id = Label(text=str(serviceid), size_hint_x=.3, color=(.2, .2, .2, 1))
            service_ = Label(text=str(service_), size_hint_x=.3, color=(.2, .2, .2, 1))
            cost_ = Label(text=str(cost), size_hint_x=.4, color=(.2, .2, .2, 1))
            svstaff_id = Label(text=str(staffid), size_hint_x=.3, color=(.2, .2, .2, 1))
            svstaff_name = Label(text=str(staffname), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(service_id)
            details.add_widget(service_)
            details.add_widget(cost_)
            details.add_widget(svstaff_id)
            details.add_widget(svstaff_name)
        cursor.close()
        db.close()

class ServiceRecords(Screen):
    def on_enter(self):
        self.ids.service_records.clear_widgets()
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM services')
        service_list = cursor.fetchall()

        service_container = self.ids.service_records
        for service in service_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            service_container.add_widget(details)
            serviceid = service[0]
            service_ = service[1]
            cost = service[3]
            staffid = service[4]
            regno = service[5]
            service_id = Label(text=str(serviceid), size_hint_x=.3, color=(.2, .2, .2, 1))
            service_ = Label(text=str(service_), size_hint_x=.3, color=(.2, .2, .2, 1))
            cost_ = Label(text=str(cost), size_hint_x=.4, color=(.2, .2, .2, 1))
            svstaff_id = Label(text=str(staffid), size_hint_x=.3, color=(.2, .2, .2, 1))
            svreg_no = Label(text=str(regno), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(service_id)
            details.add_widget(service_)
            details.add_widget(cost_)
            details.add_widget(svstaff_id)
            details.add_widget(svreg_no)
        cursor.close()
        db.close()

class UserRecords(Screen):
    def on_enter(self):
        self.ids.users_records.clear_widgets()
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users')
        users_list = cursor.fetchall()

        users_container = self.ids.users_records
        for user in users_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            users_container.add_widget(details)
            staffid = user[0]
            fname = user[1]
            lname = user[2]
            password = user[3]
            username = user[4]
            designations = user[5]
            staff_id = Label(text=str(staffid), size_hint_x=.3, color=(.2, .2, .2, 1))
            f_name = Label(text=str(fname), size_hint_x=.3, color=(.2, .2, .2, 1))
            l_name = Label(text=str(lname), size_hint_x=.4, color=(.2, .2, .2, 1))
            password_ = Label(text=str(password), size_hint_x=.3, color=(.2, .2, .2, 1))
            username_ = Label(text=str(username), size_hint_x=.3, color=(.2, .2, .2, 1))
            designations_ = Label(text=str(designations), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(staff_id)
            details.add_widget(f_name)
            details.add_widget(l_name)
            details.add_widget(password_)
            details.add_widget(username_)
            details.add_widget(designations_)
        cursor.close()
        db.close()

    def adduser(self):
        staff_id = int(self.ids.staffid_input.text)
        f_name = str(self.ids.fname_input.text)
        l_name = str(self.ids.lname_input.text)
        password = str(self.ids.password_input.text)
        username = str(self.ids.username_input.text)
        designation = str(self.ids.designation_input.text)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='carwash',
                                                 user='root',
                                                 password='oyondi8363')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO users (staffid, fname, lname, password, username, designations) 
                                    VALUES (%s, %s, %s, %s, %s, %s) """

            recordTuple = (staff_id, f_name, l_name, password, username, designation)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            self.ids.staffid_input.text = ''
            self.ids.fname_input.text = ''
            self.ids.lname_input.text = ''
            self.ids.password_input.text = ''
            self.ids.username_input.text = ''
            self.ids.designation_input.text = ''
            show = Label(text='User added successfully !', size_hint=(.6, .2), pos_hint={"x": .2, "top": 1})
            popup_window = Popup(title='User Added', content=show, size_hint=(None, None), size=(400, 400))
            popup_window.open()
        except mysql.connector.Error as error:
            error_msg = ("Failed to insert into MySQL table \n" + str(error))
            error_txt = Label(text=str(error_msg), size_hint=(.6, .2), pos_hint={"x": .2, "top": 1})
            error_popup = Popup(title='Error!!', content=error_txt, size_hint=(None, None), size=(400, 400))
            error_popup.open()

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
            self.on_enter()



class CarRecords(Screen):
    def on_enter(self):
        self.ids.cars_records.clear_widgets()
        db = mysql.connector.connect(host='localhost', user='root', passwd='oyondi8363', database='carwash')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cars')
        cars_list = cursor.fetchall()

        cars_container = self.ids.cars_records
        for car in cars_list:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            cars_container.add_widget(details)
            regno = car[0]
            model = car[1]
            color = car[2]
            ownerid = car[3]
            reg_no = Label(text=str(regno), size_hint_x=.3, color=(.2, .2, .2, 1))
            car_model = Label(text=str(model), size_hint_x=.3, color=(.2, .2, .2, 1))
            car_color = Label(text=str(color), size_hint_x=.4, color=(.2, .2, .2, 1))
            owner_id = Label(text=str(ownerid), size_hint_x=.3, color=(.2, .2, .2, 1))
            details.add_widget(reg_no)
            details.add_widget(car_model)
            details.add_widget(car_color)
            details.add_widget(owner_id)
        cursor.close()
        db.close()

class About(Screen):
    pass

kv = Builder.load_file('Carwash.kv')

class CarWashApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    CarWashApp().run()


