// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** датаграмма(電文)·канал_ввод(通路): 경계를 가진 UDP 자료를 주고받는 участник. */
public final class датаграмма_канал {
    private final java.net.DatagramSocket стандарт_участник;
    private датаграмма_канал(int номер_порта) throws входные_данные_выход_исключение {
        try { стандарт_участник = коммуникация.Открыть(номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static датаграмма_канал Открыть(int номер_порта) throws входные_данные_выход_исключение {
        try { return new датаграмма_канал(номер_порта);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void написать(String АДРЕС, int номер_порта, String данные) throws входные_данные_выход_исключение {
        try { коммуникация.написать(стандарт_участник, АДРЕС, номер_порта, данные);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public String получить() throws входные_данные_выход_исключение {
        try { return коммуникация.получить(стандарт_участник);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void ТАЙМАУТ(int 밀리초) throws входные_данные_выход_исключение {
        try { коммуникация.ТАЙМАУТ(стандарт_участник, 밀리초);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public int номер_порта() { return стандарт_участник.getLocalPort(); }
    public boolean ИТ_службы_закрыто() { return стандарт_участник.isClosed(); }
    public void Закрыть() { коммуникация.Закрыть(стандарт_участник); }
}
