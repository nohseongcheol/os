// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** Изход(出力)과 поток_стойност: 순서를 보존해 내보내는 바이트의 Канал_запис. */
public final class изходен_поток {
    private final java.io.OutputStream 표준흐름;
    изходен_поток(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Писане(int стойност) throws В_И_изключение {
        try { 표준흐름.write(стойност);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void Писане(byte[] данни) throws В_И_изключение {
        try { 표준흐름.write(данни);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void Писане(byte[] данни, int Стартиране, int 길이) throws В_И_изключение {
        try { 표준흐름.write(данни, Стартиране, 길이);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void 내보내기() throws В_И_изключение {
        try { 표준흐름.flush();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void Затворен() throws В_И_изключение {
        try { 표준흐름.close();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
