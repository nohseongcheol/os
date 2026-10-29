// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** текстовыйВывод(出力)과 поток_ЗНАЧЕН: 순서를 보존해 내보내는 바이트의 канал_ввод. */
public final class поток_вывода {
    private final java.io.OutputStream стандарт_поток;
    поток_вывода(java.io.OutputStream стандарт_поток) { this.стандарт_поток = стандарт_поток; }
    public void Запись(int ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { стандарт_поток.write(ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void Запись(byte[] данные) throws входные_данные_выход_исключение {
        try { стандарт_поток.write(данные);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void Запись(byte[] данные, int запустить, int длина_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { стандарт_поток.write(данные, запустить, длина_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void 내보내기() throws входные_данные_выход_исключение {
        try { стандарт_поток.flush();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void Закрыть() throws входные_данные_выход_исключение {
        try { стандарт_поток.close();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
}
