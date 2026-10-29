// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** получавам_стойност_cef4d8ab(受信)·порт_стойност(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class получавам_порт {
    private final java.net.ServerSocket 표준창구;
    private получавам_порт(int номер_на_порт) throws В_И_изключение {
        try { 표준창구 = new java.net.ServerSocket(номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static получавам_порт Отваряне(int номер_на_порт) throws В_И_изключение {
        try { return new получавам_порт(номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public връзка получавам() throws В_И_изключение {
        try { return new връзка(표준창구.accept());
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public int номер_на_порт() { return 표준창구.getLocalPort(); }
    public void време_на_изчакване(int 밀리초) throws В_И_изключение {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Затворен() throws В_И_изключение {
        try { 표준창구.close();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
