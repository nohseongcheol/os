// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static зв_язок Відкрити(String Адреса, int номер_порту) throws ввід_вивід_виняток {
        try { return зв_язок.Відкрити(Адреса, номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static отримувати_порт 수신열기(int номер_порту) throws ввід_вивід_виняток {
        try { return отримувати_порт.Відкрити(номер_порту);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static Socket З_єднання(String Адреса, int порт_значення) throws ввід_вивід_виняток {
        try { return new Socket(Адреса, порт_значення);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static ServerSocket прослуховувати_учасник(int порт_значення) throws ввід_вивід_виняток {
        try { return new ServerSocket(порт_значення);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static Socket отримувати(ServerSocket сервер_значення) throws ввід_вивід_виняток {
        try { return сервер_значення.accept();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
