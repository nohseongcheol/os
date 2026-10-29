// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** 입력(入力)과 поток_стойност: 순서대로 들어오는 바이트를 읽는 Канал_запис. */
public final class входен_поток {
    private final java.io.InputStream 표준흐름;
    входен_поток(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Четене() throws В_И_изключение {
        try { return 표준흐름.read();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public int Четене(byte[] данни) throws В_И_изключение {
        try { return 표준흐름.read(данни);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public int Четене(byte[] данни, int Стартиране, int 길이) throws В_И_изключение {
        try { return 표준흐름.read(данни, Стартиране, 길이);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void Затворен() throws В_И_изключение {
        try { 표준흐름.close();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
