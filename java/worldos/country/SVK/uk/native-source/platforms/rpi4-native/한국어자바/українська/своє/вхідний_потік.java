// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** 입력(入力)과 потік_значення: 순서대로 들어오는 바이트를 읽는 Канал_запис. */
public final class вхідний_потік {
    private final java.io.InputStream 표준흐름;
    вхідний_потік(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Читання() throws ввід_вивід_виняток {
        try { return 표준흐름.read();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public int Читання(byte[] дані) throws ввід_вивід_виняток {
        try { return 표준흐름.read(дані);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public int Читання(byte[] дані, int запустити, int 길이) throws ввід_вивід_виняток {
        try { return 표준흐름.read(дані, запустити, 길이);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void Закрити() throws ввід_вивід_виняток {
        try { 표준흐름.close();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
