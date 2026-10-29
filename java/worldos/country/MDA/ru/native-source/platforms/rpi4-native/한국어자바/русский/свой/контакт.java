// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** Подключить(連結)·канал_ввод(通路): 상대와 이어진 TCP байт_ЗНАЧЕН 흐름의 участник. */
public final class контакт {
    private final java.net.Socket стандарт_библиотека_мост;
    контакт(java.net.Socket стандарт_библиотека_мост) { this.стандарт_библиотека_мост = стандарт_библиотека_мост; }
    public static контакт Открыть(String АДРЕС, int номер_порта) throws входные_данные_выход_исключение {
        try {
            return new контакт(new java.net.Socket(АДРЕС, номер_порта));
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public входной_поток входные_данные_ЗНАЧЕН() throws входные_данные_выход_исключение {
        try { return new входной_поток(стандарт_библиотека_мост.getInputStream());
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public поток_вывода текстовыйВывод() throws входные_данные_выход_исключение {
        try { return new поток_вывода(стандарт_библиотека_мост.getOutputStream());
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void ТАЙМАУТ(int 밀리초) throws входные_данные_выход_исключение {
        try { стандарт_библиотека_мост.setSoTimeout(밀리초);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public int номер_порта() { return стандарт_библиотека_мост.getPort(); }
    public int локальный_номер_порта() { return стандарт_библиотека_мост.getLocalPort(); }
    public boolean ИТ_службы_закрыто() { return стандарт_библиотека_мост.isClosed(); }
    public boolean 연결됨() { return стандарт_библиотека_мост.isConnected(); }
    public void Закрыть() throws входные_данные_выход_исключение {
        try { стандарт_библиотека_мост.close();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
}
