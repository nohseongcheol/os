// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** З_єднання(連結)·Канал_запис(通路): 상대와 이어진 TCP байт_значення 흐름의 учасник. */
public final class зв_язок {
    private final java.net.Socket 표준연결;
    зв_язок(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static зв_язок Відкрити(String Адреса, int номер_порту) throws ввід_вивід_виняток {
        try {
            return new зв_язок(new java.net.Socket(Адреса, номер_порту));
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public вхідний_потік 입력() throws ввід_вивід_виняток {
        try { return new вхідний_потік(표준연결.getInputStream());
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public вихідний_потік Вивід() throws ввід_вивід_виняток {
        try { return new вихідний_потік(표준연결.getOutputStream());
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void 대기시간(int 밀리초) throws ввід_вивід_виняток {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public int номер_порту() { return 표준연결.getPort(); }
    public int місцевий_номер_порту() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Закрити() throws ввід_вивід_виняток {
        try { 표준연결.close();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
