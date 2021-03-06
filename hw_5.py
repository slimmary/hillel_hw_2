from chek_for_work import check_full_name   # проверка ФИО
from chek_for_work import check_login   # проверка логине (не менее 5 символов)
from chek_for_work import check_address   # проверка почтового адреса
from chek_for_work import check_curator   # проверка контактов куратора
from chek_for_work import check_pay_form   # проверка формы оплаты 1 или 2
from chek_for_work import check_name_company   # проверка наименования компании если 1 форма оплаты
from chek_for_work import check_name_gps   # проверка имени производиетля регистратора
from chek_for_work import check_gps_rec_numb   # проверка ид.номера в зависимости от производиетля
from chek_for_work import check_name_sim   # проверка допустимых операторов сим-карт
from chek_for_work import check_sim_numb  # в зависимости от оператора проверка формата номера
from chek_for_work import check_fls_mark   # проверка маркировки Датчика Уровня Топлива (маркировка по виду и длинне)
from chek_for_work import check_fls_numb   # проверка номера ДУТ
from chek_for_work import check_price   # проверка тарифа ( цифра и больше 0)


class Client:
    def __init__(self):
        self._pay_form = check_pay_form()  # проверяем форму оплаты
        if self._pay_form == 1:
            self._name = check_name_company()  # если форма оплаты 1 (безнал), то проверяем название компании и форму
        else:
            self._name = check_full_name('клієнта')  # если клиент физ.лицо, то проверяем ФИО
        self._login = check_login()
        self._curator = check_curator()  # проверка контактов куратора
        self._address = check_address()  # адрес клиента
        self._gps_rec = []  # хранилище регистраторов клиента

    def __str__(self):
        return 'Клієнт: {}  \nІ\'мя користувача (login): {} \nФорма оплати: Ф{} \n{} \n{}'\
               '\nперелік реєстраторів, що належать клієнтові: {}'.format(self._name, self._login, self._pay_form, self._address, self._curator,"; ".join(self._gps_rec))

    def add_gps_rec(self,gps):  # присвоение регистратора клиенту
        return self._gps_rec.append(gps._gps_numb)

    def dell_gps_rec(self,gps):  # удаление регистратора (например при замене)
        return self._gps_rec.remove(gps._gps_numb)

    def mon_fee(self):  # подсчет квартальной абонплаты
        for gps in self._gps_rec:
            mon_fee = (sum(gps._rate()))*3
            return mon_fee


class Equipment:  # класс оборудование, комплектующие и услуги
    def __init__(self, name):
        self._name = name
        self._price = check_price('внутрішню', self._name)  # внутренняя цена
        self._price_client = check_price('для клієнта', self._name)  # цена для клиента


class Rate(Equipment):  # класс тарифов абон.платы

    def __init__(self, name='Тариф абон.плати'):  # создание тарифа
        self._rate_name = input('Введіть назву тарифу')
        super().__init__(name)

    def __str__(self):
        return '{} {} вартість - {}грн./міс.'.format(self._name,self._rate_name,self._price,)


class GpsRec(Equipment):
    def __init__(self, name='Реєстратор'):  # создание регистратора
        self._gps_name = check_name_gps()  # название произвоителя регистратора
        self._gps_numb = check_gps_rec_numb(self._gps_name)  # в зависимости от производителя номер регистратора
        super().__init__(name)
        self._sim = []  # хранилище присвоенных сим-карт
        self._rate = 0  # по умолчанию регистратор без присвоенного тарифа
        self._vehicle = self._gps_numb
        self._fls = []

    def add_sim(self, sim):  # присвоение сим карты( добавляем в список)
        if not isinstance(sim,SimCards):
            print('Ви намагаєтесь доати не існюучу сім-карту')
        return self._sim.append(sim._numb)

    def del_sim(self, sim):  # удаление сим-карты при замене, например
        if not isinstance(sim, SimCards):
            print('Ви намагаєтесь додати не існюучу сім-карту')
        return self._sim.remove(sim._numb)

    def add_rate(self,rate):
        if not isinstance(rate, Rate):  # присвоение тарифа (несколько тарифов могут суммироваться)
            print('Щось пішло не так. Ви намагаєтесь привласнити не тариф')
        else:
            self._rate = self._rate + rate._price
            return self._rate

    def del_rate(self,rate):  # удаление тарифа
        if not isinstance(rate, Rate):
            print('Щось пішло не так. Ви намагаєтесь привласнити не тариф')
        else:
            self._rate = self._rate - rate._price
            return self._rate

    def add_vehicle(self, vehicle):  # присваиваем ТС на которое установлен регистратор
        self._vehicle = vehicle
        return self._vehicle

    def del_vehicle(self):  # удаление ТС, в этом случае ТС будет равен номеру регистратора
        self._vehicle = self._gps_numb
        return self._vehicle

    def add_fls(self, fls):  # присвоение ДУТ
        return self._fls.append(str(fls))

    def del_fls(self, fls):  # удаление ДУТ
        return self._fls.remove(fls)

    def __str__(self):
        return '{} {} № {} \nсім-картки в реєстраторі:{}\nреєстратор встановлений на TЗ:{} ' \
               '\nдодаткове обладнання: {}'.format(self._name, self._gps_name, self._gps_numb, "; " .join(self._sim), self._vehicle, "; ".join(self._fls))


class FuelLevelSens(Equipment):  # создание датчика уровня топлива
    def __init__(self, name='ДВРП'):
        super().__init__(name)
        self._fls_name = input('Введіть тип ДВРП, наприклад "Игла-2"')
        self._fls_mark = check_fls_mark()   # проверка маркировки по длинне и виду датчика (Н-частотный, D-цифровой)
        self._fls_numb = check_fls_numb()  # проверка серийного номера ДУТа

    def __str__(self):
        return 'ДВРП {}: {}-{}'.format(self._fls_name,self._fls_mark,self._fls_numb)


class SimCards:
    def __init__(self):
        self._name = check_name_sim()   # проверка оператора сим-карты
        self._numb = check_sim_numb(self._name)  # проверяем, в зависимости от оператора разные форматы номеров

    def __str__(self):
        return 'Сім-картка оператор {} номер {}'.format(self._name,self._numb)


class Vehicle:  # класс транспортных средств
    def __init__(self):
        self._type = input('Введіть тип транспортного засобу (ТЗ), наприклад: трактор, легкове авто, тягач тощо')
        self._brand_model = input('Введіть марку/модель ТЗ')
        self._id = input('Введіть державний номер ТЗ або ідентифікатор')

    def __str__(self):
        return '{} {} державний номер {}'.format(self._type,self._brand_model,self._id)


sim1 = SimCards()
sim2 = SimCards()
rate1 = Rate()
rate2 = Rate()
# fls1 = FuelLevelSens()
car1 = Vehicle()
gps1 = GpsRec()
gps1.add_sim(sim1)
gps1.add_sim(sim2)
gps1.add_rate(rate1)
gps1.add_rate(rate2)
# gps1.add_fls(fls1)
gps1.add_vehicle(car1)


print(gps1)
# client1 = Client()
# client1.add_gps_rec(gps1)
# print(client1)