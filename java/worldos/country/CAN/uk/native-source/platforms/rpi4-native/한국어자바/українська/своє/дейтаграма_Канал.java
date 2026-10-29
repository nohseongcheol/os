// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** дейтаграма(電文)·Канал_запис(通路): 경계를 가진 UDP 자료를 주고받는 учасник. */
public final class дейтаграма_Канал {
    private final java.net.DatagramSocket 표준종단;
    private дейтаграма_Канал(int номер_порту) throws ввід_вивід_виняток {
        try { 표준종단 = 통신.Відкрити(номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static дейтаграма_Канал Відкрити(int номер_порту) throws ввід_вивід_виняток {
        try { return new дейтаграма_Канал(номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void надсилати(String Адреса, int номер_порту, String дані) throws ввід_вивід_виняток {
        try { 통신.надсилати(표준종단, Адреса, номер_порту, дані);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public String отримувати() throws ввід_вивід_виняток {
        try { return 통신.отримувати(표준종단);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void 대기시간(int 밀리초) throws ввід_вивід_виняток {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public int номер_порту() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Закрити() { 통신.Закрити(표준종단); }
}
