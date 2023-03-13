from sqlalchemy.orm import Session

from db.crud import StudentRepo
from bot.engine import engine


def change_student_login(student_id: int, new_login: str) -> None:
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    repo.update_login(new_login=new_login, item_id=student_id)
    
    session.close()
    
    
def change_student_password(student_id: int, new_password: str) -> None:
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    repo.update_password(new_password=new_password, item_id=student_id)
    
    session.close()


def check(string: str) -> bool:
    # проверка на длину
    if not 2 <= len(string) <= 32:
        return False
    
    # проверка на символы
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ01234567890_'
    
    for i in string:
        if i not in alphabet:
            return False
    
    # прошло проверку
    return True


def check_login(login: str) -> bool:
    if not check(string=login):
        return False
    
    # проверка на уникальность
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    students = repo.read()
    
    for i in students:
        if i.login == login:
            return False
    
    session.close()
    
    # прошло проверку
    return True


def check_password(password: str) -> bool:
    return check(string=password)