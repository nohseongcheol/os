// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** Свързване(連結)·Канал_запис(通路): 상대와 이어진 TCP байт_стойност 흐름의 участник. */
public final class връзка {
    private final java.net.Socket 표준연결;
    връзка(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static връзка Отваряне(String адрес, int номер_на_порт) throws В_И_изключение {
        try {
            return new връзка(new java.net.Socket(адрес, номер_на_порт));
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public входен_поток 입력() throws В_И_изключение {
        try { return new входен_поток(표준연결.getInputStream());
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public изходен_поток Изход() throws В_И_изключение {
        try { return new изходен_поток(표준연결.getOutputStream());
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void време_на_изчакване(int 밀리초) throws В_И_изключение {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public int номер_на_порт() { return 표준연결.getPort(); }
    public int локален_номер_на_порт() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Затворен() throws В_И_изключение {
        try { 표준연결.close();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
