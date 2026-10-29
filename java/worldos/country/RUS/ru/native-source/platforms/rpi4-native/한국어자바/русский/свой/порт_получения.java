// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** получить_ЗНАЧЕН(受信)·порт_ЗНАЧЕН(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class порт_получения {
    private final java.net.ServerSocket стандарт_порт;
    private порт_получения(int номер_порта) throws входные_данные_выход_исключение {
        try { стандарт_порт = new java.net.ServerSocket(номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static порт_получения Открыть(int номер_порта) throws входные_данные_выход_исключение {
        try { return new порт_получения(номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public контакт получить() throws входные_данные_выход_исключение {
        try { return new контакт(стандарт_порт.accept());
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public int номер_порта() { return стандарт_порт.getLocalPort(); }
    public void ТАЙМАУТ(int 밀리초) throws входные_данные_выход_исключение {
        try { стандарт_порт.setSoTimeout(밀리초);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public boolean ИТ_службы_закрыто() { return стандарт_порт.isClosed(); }
    public void Закрыть() throws входные_данные_выход_исключение {
        try { стандарт_порт.close();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
}
