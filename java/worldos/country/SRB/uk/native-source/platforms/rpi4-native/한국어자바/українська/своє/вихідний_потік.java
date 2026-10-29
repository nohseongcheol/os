// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** Вивід(出力)과 потік_значення: 순서를 보존해 내보내는 바이트의 Канал_запис. */
public final class вихідний_потік {
    private final java.io.OutputStream 표준흐름;
    вихідний_потік(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Запис(int значення) throws ввід_вивід_виняток {
        try { 표준흐름.write(значення);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void Запис(byte[] дані) throws ввід_вивід_виняток {
        try { 표준흐름.write(дані);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void Запис(byte[] дані, int запустити, int 길이) throws ввід_вивід_виняток {
        try { 표준흐름.write(дані, запустити, 길이);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void 내보내기() throws ввід_вивід_виняток {
        try { 표준흐름.flush();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public void Закрити() throws ввід_вивід_виняток {
        try { 표준흐름.close();
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
