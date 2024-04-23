from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, String, Date, Numeric, UniqueConstraint, Float
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import event
from app import db

Base = declarative_base()


class PozMag(db.Model):
    __tablename__ = 'pozmag'

    pozmag_id = Column(Integer, primary_key=True)
    liczba_sztuk = Column(Integer, nullable=False)

    magazyn_id_mag = Column(Integer, ForeignKey('magazyn.id_mag'), nullable=False)
    magazyn = relationship('Magazyn', back_populates='pozmag')

    rodzajczesci_id_czesci = Column(Numeric(10, 7), ForeignKey('rodzajczesci.id_czesci'))
    rodzajczesci = relationship('RodzajCzesci', back_populates='pozmag')

    def __repr__(self):
        return f"Pozmag(liczba_sztuk={self.liczba_sztuk}, rodzajczesci_id_czesci={self.rodzajczesci_id_czesci}, magazyn_id_mag={self.magazyn_id_mag})"


class Magazyn(db.Model):
    __tablename__ = 'magazyn'

    id_mag = Column(Integer, primary_key=True)
    nazwa = Column(String(100), nullable=False)
    pojemnosc_m3 = Column(Integer, nullable=False)

    adres_id_adresu = Column(Integer, ForeignKey('adres.id_adresu'), nullable=False)
    adres_magazynu = relationship('Adres', back_populates='magazyn')

    pozmag = relationship('PozMag', back_populates='magazyn')
    zamowienia = relationship('Zamowienie', back_populates='magazyn')


class Adres(db.Model):
    __tablename__ = 'adres'

    id_adresu = Column(Integer, primary_key=True)
    ulica = Column(String(100), nullable=False)
    numer_domu = Column(Integer, nullable=False)
    numer_mieszkania = Column(Integer)
    kod_pocztowy = Column(String(100), nullable=False)
    miasto = Column(String(100), nullable=False)
    kraj = Column(String(100), nullable=False)
    typ = Column(String(20), nullable=False)

    magazyn = relationship('Magazyn', back_populates='adres_magazynu', uselist=False)


class Maszyna(db.Model):
    __tablename__ = 'maszyna'

    id_masz = Column(Integer, primary_key=True)
    koszt = Column(Numeric(10, 2), nullable=False)
    data_zakupu = Column(Date, nullable=False)
    opis_stanu = Column(String(100))

    terminy_pracy = relationship('TerminMaszyna', back_populates='maszyna')


class Pojazd(db.Model):
    __tablename__ = 'pojazd'

    id_poj = Column(Integer, primary_key=True)
    marka = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    rok_produkcji = Column(Date)
    kolor = Column(String(50))
    rodzaj_paliwa = Column(String(50))
    przebieg_w_km = Column(Numeric(10))
    klient_id_uz = Column(Integer, nullable=False)

    zlecenia = relationship('Zlecenie', back_populates='pojazd')

    def __repr__(self):
        return f"Pojazd(id_poj={self.id_poj}, marka='{self.marka}', model='{self.model}')"


class RodzajCzesci(db.Model):
    __tablename__ = 'rodzajczesci'

    id_czesci = Column(Numeric(20, 7), nullable=False, primary_key=True)
    nazwa = Column(String(5), nullable=False)
    nr_katalogowy = Column(String(100), nullable=False)
    producent = Column(String(100), nullable=False)
    cena_za_sztuke = Column(Integer, nullable=False)

    pozmag = relationship('PozMag', back_populates='rodzajczesci')
    pozzam = relationship("PozZam", back_populates="rodzajczesci")
    uzycie_czesci = relationship('UzycieCzesci', back_populates='rodzaj_czesci')


    def __repr__(self):
        return f"RodzajCzesci(id_czesci={self.id_czesci}, nazwa={self.nazwa}, nr_katalogowy={self.nr_katalogowy}, producent={self.producent}, cena_za_sztuke={self.cena_za_sztuke})"
    

class PozZam(db.Model):
    __tablename__ = 'pozzam'

    rodzajczesci_id_czesci = Column(Numeric(20, 7), ForeignKey('rodzajczesci.id_czesci'), nullable=False)
    zamowienie_id_zam = Column(Integer, ForeignKey('zamowienie.id_zam'), nullable=False)
    liczba_sztuk = Column(Integer, nullable=False)

    rodzajczesci = relationship('RodzajCzesci', back_populates='pozzam')
    zamowienie = relationship('Zamowienie', back_populates='pozycje')

    __table_args__ = (
        PrimaryKeyConstraint('zamowienie_id_zam', 'rodzajczesci_id_czesci'),
        {},
    )

    def __repr__(self):
        return f"Pozzam(rodzajczesci_id_czesci={self.rodzajczesci_id_czesci}, zamowienie_id_zam={self.zamowienie_id_zam}, liczba_sztuk={self.liczba_sztuk})"
    

class Premia(db.Model):
    __tablename__ = 'premia'

    id_mech = Column(Integer, nullable=False)
    miesiąc = Column(Integer, nullable=False)
    rok = Column(Integer, nullable=False)
    wysokosc_premii = Column(Numeric(10), nullable=False)
    mechanik_id_uz = Column(Integer, ForeignKey('mechanik.id_uz'), nullable=False)

    mechanik = relationship('Mechanik', back_populates='premie')

    __table_args__ = (
        PrimaryKeyConstraint('id_mech', 'miesiac', 'rok'),
    )

    def __repr__(self):
        return f"Premia(id_mech={self.id_mech}, miesiąc={self.miesiąc}, rok={self.rok}, wysokosc_premii={self.wysokosc_premii})"
    

class ZrealNapr(db.Model):
    __tablename__ = 'zrealnapr'

    data_realizacji = Column(Date, nullable=False)
    cena_naprawy = Column(Numeric(10, 2), nullable=False)
    opis_po_naprawie = Column(String(1000))
    zlecenie_id_zlec = Column(Integer, ForeignKey('zlecenie.id_zlec'), nullable=False)
    id_napr = Column(Integer, primary_key=True)

    reklamacja = relationship('Reklamacja', back_populates='zrealnapr', uselist=False)
    zlecenie = relationship('Zlecenie', back_populates='zrealnapr')

    def __repr__(self):
        return f"Zrealnapr(data_realizacji='{self.data_realizacji}', cena_naprawy={self.cena_naprawy}, opis_po_naprawie='{self.opis_po_naprawie}', zlecenie_id_zlec={self.zlecenie_id_zlec}, id_napr={self.id_napr})"
    

class Reklamacja(db.Model):
    __tablename__ = 'reklamacja'

    id_rekl = Column(Integer, nullable=False, primary_key=True)
    opis = Column(String(1000))
    rozwiazanie_id_rozw = Column(Integer,  ForeignKey('rozwiazanie.id_rozw'), nullable=False)
    zrealnapr_id_napr = Column(Integer, ForeignKey('zrealnapr.id_napr'), nullable=False)

    zrealnapr = relationship('ZrealNapr', back_populates='reklamacja')
    rozwiazanie = relationship('Rozwiazanie', back_populates='reklamacja')

    def __repr__(self):
        return f"Reklamacja(id_rekl={self.id_rekl}, opis={self.opis}, rozwiazanie_id_rozw={self.rozwiazanie_id_rozw}, zrealnapr_id_napr={self.zrealnapr_id_napr})"
    

class Rozwiazanie(db.Model):
    __tablename__ = 'rozwiazanie'

    id_rozw = Column(Integer, primary_key=True)
    nazwa = Column(String(100), nullable=False)

    reklamacja = relationship('Reklamacja', back_populates='rozwiazanie')

    def __repr__(self):
        return f"Rozwiazanie(id_rozw={self.id_rozw}, nazwa={self.nazwa})"
    

class Stanowisko(db.Model):
    __tablename__ = 'stanowisko'

    id_stan = Column(Integer, primary_key=True)
    opis = Column(String(1000))

    terminy_pracy = relationship('TerminStanowisko', back_populates='stanowisko')

    def __repr__(self):
        return f"Stanowisko(id_stan={self.id_stan}, opis={self.opis})"
    

class Status(db.Model):
    __tablename__ = 'status'

    id_stat = Column(Integer, primary_key=True)
    opis = Column(String(1000), nullable=False)

    zlecenia = relationship('Zlecenie', back_populates='status')

    def __repr__(self):
        return f"Status(id_stat={self.id_stat}, opis={self.opis})"
    

class Termin(db.Model):
    __tablename__ = 'termin'

    id_wpisu = Column(Integer, primary_key=True)
    czas_rozpoczecia = Column(Date, nullable=False)
    czas_zakonczenia = Column(Date, nullable=False)
    mechanik_id_uz = Column(Integer, ForeignKey('mechanik.id_uz'), nullable=False)
    typ = Column(String(20), nullable=False)

    mechanik = relationship('Mechanik', back_populates='terminy')
    terminklienci = relationship('TerminKlient', back_populates='termin')
    terminstanowiska = relationship('TerminStanowisko', back_populates='termin')
    terminmaszyny = relationship('TerminMaszyna', back_populates='termin')

    def __repr__(self):
        return f"Termin(id_wpisu={self.id_wpisu}, czas_rozpoczecia={self.czas_rozpoczecia}, czas_zakonczenia={self.czas_zakonczenia}, mechanik_id_uz={self.mechanik_id_uz}, typ={self.typ})"
    

class TerminKlient(db.Model):
    __tablename__ = 'terminklient'

    id_wpisu = Column(Integer, ForeignKey('termin.id_wpisu'), primary_key=True)
    klient_id_uz = Column(Integer, ForeignKey('klient.id_uz'), nullable=False)

    klient = relationship('Klient', back_populates='terminy_spotkan')
    termin = relationship('Termin', back_populates='terminklienci')


    def __repr__(self):
        return f"TerminKlient(id_wpisu={self.id_wpisu}, klient_id_uz={self.klient_id_uz})"
    

class TerminMaszyna(db.Model):
    __tablename__ = 'terminmaszyna'

    id_wpisu = Column(Integer, ForeignKey('termin.id_wpisu'), primary_key=True)
    maszyna_id_masz = Column(Integer, ForeignKey('maszyna.id_masz'), nullable=False)
    zlecenie_id_zlec = Column(Integer, ForeignKey('zlecenie.id_zlec'), nullable=False)
    
    termin = relationship('Termin', back_populates='terminmaszyny')
    maszyna = relationship('Maszyna', back_populates='terminy_pracy')
    zlecenie = relationship('Zlecenie', back_populates='terminy_pracy_maszyna')


    def __repr__(self):
        return f"TerminMaszyna(id_wpisu={self.id_wpisu}, maszyna_id_masz={self.maszyna_id_masz}, zlecenie_id_zlec={self.zlecenie_id_zlec})"
    

class TerminStanowisko(db.Model):
    __tablename__ = 'terminstanowisko'

    id_wpisu = Column(Integer, ForeignKey('termin.id_wpisu'), primary_key=True)
    stanowisko_id_stan = Column(Integer,  ForeignKey('stanowisko.id_stan'), nullable=False)
    zlecenie_id_zlec = Column(Integer,  ForeignKey('zlecenie.id_zlec'), nullable=False)

    termin = relationship('Termin', back_populates='terminstanowiska')
    stanowisko = relationship('Stanowisko', back_populates='terminy_pracy')
    zlecenie = relationship('Zlecenie', back_populates='terminy_pracy_stanowisko')


    def __repr__(self):
        return f"TerminStanowisko(id_wpisu={self.id_wpisu}, stanowisko_id_stan={self.stanowisko_id_stan}, zlecenie_id_zlec={self.zlecenie_id_zlec})"


class UzycieCzesci(db.Model):
    __tablename__ = 'uzycieczesci'

    liczba_sztuk = Column(Integer)
    zlecenie_id_zlec = Column(Integer, ForeignKey('zlecenie.id_zlec'), primary_key=True)
    rodzajczesci_id_czesci = Column(Integer, ForeignKey('rodzajczesci.id_czesci'), nullable=False)

    zlecenie = relationship('Zlecenie', back_populates='uzycie_czesci')
    rodzaj_czesci = relationship('RodzajCzesci', back_populates='uzycie_czesci')


    def __repr__(self):
        return f"UzycieCzesci(liczba_sztuk={self.liczba_sztuk}, zlecenie_id_zlec={self.zlecenie_id_zlec}, rodzajczesci_id_czesci={self.rodzajczesci_id_czesci})"
    

class Uzytkownik(db.Model):
    __tablename__ = 'uzytkownik'

    id_uz = Column(Integer, primary_key=True)
    imie = Column(String(100), nullable=False)
    nazwisko = Column(String(100), nullable=False)
    nr_telefonu = Column(String(50), nullable=False)
    adres_mailowy = Column(String(100), nullable=False)
    skrot_hasla = Column(String(100), nullable=False)
    adres_id_adresu = Column(Integer, nullable=False)
    typ = Column(String(20), nullable=False)

    def __repr__(self):
        return f"Uzytkownik(id_uz={self.id_uz}, imie='{self.imie}', nazwisko='{self.nazwisko}', nr_telefonu='{self.nr_telefonu}', adres_mailowy='{self.adres_mailowy}', skrot_hasla='{self.skrot_hasla}', adres_id_adresu={self.adres_id_adresu}, typ='{self.typ}')"
 
    
class Klient(db.Model):
    __tablename__ = 'klient'

    id_uz = Column(Integer, ForeignKey('uzytkownik.id_uz'), primary_key=True)

    uzytkownik = relationship(Uzytkownik, uselist=False, backref='klient')
    terminy_spotkan = relationship('TerminKlient', back_populates='klient')

    def __repr__(self):
        return f"Klient(id_uz={self.id_uz})"


class Administrator(db.Model):
    __tablename__ = 'administrator'

    id_uz = Column(Integer, ForeignKey('uzytkownik.id_uz'), primary_key=True)

    uzytkownik = relationship(Uzytkownik, uselist=False, backref='administrator')

    def __repr__(self):
        return f"Administrator(id_uz={self.id_uz})"
    

class Mechanik(db.Model):
    __tablename__ = 'mechanik'

    id_uz = Column(Integer, ForeignKey('uzytkownik.id_uz'), primary_key=True)
    pensja = Column(Numeric(10, 2), nullable=False)

    uzytkownik = relationship(Uzytkownik, uselist=False, backref='mechanik')
    premie = relationship('Premia', back_populates='mechanik')
    terminy = relationship('Termin', back_populates='mechanik')
    zlecenia = relationship('Zlecenie', back_populates='mechanik')

    def __repr__(self):
        return f"Mechanik(id_uz={self.id_uz}, pensja={self.pensja})"


class Zamowienie(db.Model):
    __tablename__ = 'zamowienie'

    id_zam = Column(Integer, primary_key=True)
    data_zlozenia = Column(TIMESTAMP)
    data_odebrania = Column(Date)
    magazyn_id_mag = Column(Integer, ForeignKey('magazyn.id_mag'), nullable=False)

    pozycje = relationship("PozZam", back_populates="zamowienie")
    magazyn = relationship('Magazyn', back_populates='zamowienia')

    def __repr__(self):
        return f"Zamowienie(id_zam={self.id_zam}, data_zlozenia='{self.data_zlozenia}', data_odebrania='{self.data_odebrania}', magazyn_id_mag={self.magazyn_id_mag})"


class Zlecenie(db.Model):
    __tablename__ = 'zlecenie'

    id_zlec = Column(Integer, primary_key=True)
    opis_przed_naprawa = Column(String(1000), nullable=False)
    data_przyjecia = Column(Date, nullable=False)
    szacowany_czas_naprawy = Column(Integer, nullable=False)
    pojazd_id_poj = Column(Integer, ForeignKey('pojazd.id_poj'), nullable=False)
    status_id_stat = Column(Integer, ForeignKey('status.id_stat'), nullable=False)
    mechanik_id_uz = Column(Integer, ForeignKey('mechanik.id_uz'), nullable=False)

    terminy_pracy_maszyna = relationship('TerminMaszyna', back_populates='zlecenie')
    terminy_pracy_stanowisko = relationship('TerminStanowisko', back_populates='zlecenie')
    uzycie_czesci = relationship('UzycieCzesci', back_populates='zlecenie')
    mechanik = relationship('Mechanik', back_populates='zlecenia')
    pojazd = relationship('Pojazd', back_populates='zlecenia')
    status = relationship('Status', back_populates='zlecenia')
    zrealnapr = relationship('ZrealNapr', back_populates='zlecenie')

    def __repr__(self):
        return f"Zlecenie(id_zlec={self.id_zlec}, opis_przed_naprawa='{self.opis_przed_naprawa}', data_przyjecia='{self.data_przyjecia}', szacowany_czas_naprawy={self.szacowany_czas_naprawy}, pojazd_id_poj={self.pojazd_id_poj}, status_id_stat={self.status_id_stat}, mechanik_id_uz={self.mechanik_id_uz})"
    


def arc_fkarc_2_klient(target, connection, **kwargs):
    session = Session.object_session(target)

    d = session.query(Uzytkownik.typ).filter(Uzytkownik.id_uz == target.id_uz).scalar()

    if d is None or d != 'klient':
        raise ValueError("FK Klient_Uzytkownik_FK in Table Klient violates Arc constraint on Table Uzytkownik - discriminator column typ doesn't have value 'klient'")
    
    print("Event listener executed successfully")


def arc_fkarc_2_administrator(target, connection, **kwargs):
    session = Session.object_session(target)

    d = session.query(Uzytkownik.typ).filter(Uzytkownik.id_uz == target.id_uz).scalar()

    if d is None or d != 'administrator':
        raise ValueError("FK Administrator_Uzytkownik_FK in Table Administrator violates Arc constraint on Table Uzytkownik - discriminator column typ doesn't have value 'administrator'")

    print("Event listener executed successfully")


def arc_fkarc_2_mechanik(target, connection, **kwargs):
    session = Session.object_session(target)

    d = session.query(Uzytkownik.typ).filter(Uzytkownik.id_uz == target.id_uz).scalar()

    if d is None or d != 'mechanik':
        raise ValueError("FK Mechanik_Uzytkownik_FK in Table Mechanik violates Arc constraint on Table Uzytkownik - discriminator column typ doesn't have value 'mechanik'")

    print("Event listener executed successfully")


def arc_fkarc_1_terminklient(target, connection, **kwargs):
    session = Session.object_session(target)

    d = session.query(Termin.typ).filter(Termin.id_wpisu == target.id_wpisu).scalar()

    if d is None or d != 'klient':
        raise ValueError("FK TerminKlient_Termin_FK in Table TerminKlient violates Arc constraint on Table Termin - discriminator column typ doesn't have value 'klient'")

    print("Event listener executed successfully")


def arc_fkarc_1_terminmaszyna(target, connection, **kwargs):
    session = Session.object_session(target)

    d = session.query(Termin.typ).filter(Termin.id_wpisu == target.id_wpisu).scalar()

    if d is None or d != 'maszyna':
        raise ValueError("FK TerminMaszyna_Termin_FK in Table TerminMaszyna violates Arc constraint on Table Termin - discriminator column typ doesn't have value 'maszyna'")

    print("Event listener executed successfully")

def arc_fkarc_1_terminstanowisko(mapper, connection, target):
    session = Session.object_session(target)

    d = session.query(Termin.typ).filter(Termin.id_wpisu == target.id_wpisu).scalar()

    if d is None or d != 'stanowisko':
        raise ValueError("FK TerminStanowisko_Termin_FK in Table TerminStanowisko violates Arc constraint on Table Termin - discriminator column typ doesn't have value 'stanowisko'")
        
    print("Event listener executed successfully")


event.listen(Klient, 'before_insert', arc_fkarc_2_klient)
event.listen(Klient, 'before_update', arc_fkarc_2_klient)
event.listen(Administrator, 'before_insert', arc_fkarc_2_administrator)
event.listen(Administrator, 'before_update', arc_fkarc_2_administrator)
event.listen(Mechanik, 'before_insert', arc_fkarc_2_mechanik)
event.listen(Mechanik, 'before_update', arc_fkarc_2_mechanik)
event.listen(TerminKlient, 'before_insert', arc_fkarc_1_terminklient)
event.listen(TerminKlient, 'before_update', arc_fkarc_1_terminklient)
event.listen(TerminMaszyna, 'before_insert', arc_fkarc_1_terminmaszyna)
event.listen(TerminMaszyna, 'before_update', arc_fkarc_1_terminmaszyna)
event.listen(TerminStanowisko, 'before_insert', arc_fkarc_1_terminstanowisko)
event.listen(TerminStanowisko, 'before_update', arc_fkarc_1_terminstanowisko)
