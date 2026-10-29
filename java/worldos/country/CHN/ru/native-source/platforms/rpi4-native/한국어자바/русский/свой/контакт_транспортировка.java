// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
import java.net.*;
public final class контакт_транспортировка {
    private контакт_транспортировка() {}
    public static контакт Открыть(String АДРЕС, int номер_порта) throws входные_данные_выход_исключение {
        try { return контакт.Открыть(АДРЕС, номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static порт_получения 수신열기(int номер_порта) throws входные_данные_выход_исключение {
        try { return порт_получения.Открыть(номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static Socket Подключить(String АДРЕС, int порт_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { return new Socket(АДРЕС, порт_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static ServerSocket ожидать_передачи_данных_участник(int порт_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { return new ServerSocket(порт_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static Socket получить(ServerSocket сервер_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { return сервер_ЗНАЧЕН.accept();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
}
