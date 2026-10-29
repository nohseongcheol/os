// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** входные_данные_ЗНАЧЕН(入力)과 поток_ЗНАЧЕН: 순서대로 들어오는 바이트를 읽는 канал_ввод. */
public final class входной_поток {
    private final java.io.InputStream стандарт_поток;
    входной_поток(java.io.InputStream стандарт_поток) { this.стандарт_поток = стандарт_поток; }
    public int Чтение() throws входные_данные_выход_исключение {
        try { return стандарт_поток.read();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public int Чтение(byte[] данные) throws входные_данные_выход_исключение {
        try { return стандарт_поток.read(данные);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public int Чтение(byte[] данные, int запустить, int длина_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { return стандарт_поток.read(данные, запустить, длина_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public void Закрыть() throws входные_данные_выход_исключение {
        try { стандарт_поток.close();
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
}
