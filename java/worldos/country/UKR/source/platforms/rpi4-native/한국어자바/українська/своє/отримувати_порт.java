// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** отримувати_значення_cef4d8ab(受信)·порт_значення(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class отримувати_порт {
    private final java.net.ServerSocket 표준창구;
    private отримувати_порт(int номер_порту) throws ввід_вивід_виняток {
        try { 표준창구 = new java.net.ServerSocket(номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static отримувати_порт Відкрити(int номер_порту) throws ввід_вивід_виняток {
        try { return new отримувати_порт(номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public зв_язок отримувати() throws ввід_вивід_виняток {
        try { return new зв_язок(표준창구.accept());
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public int номер_порту() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws ввід_вивід_виняток {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Закрити() throws ввід_вивід_виняток {
        try { 표준창구.close();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
