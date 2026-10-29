// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Излаз(出力)과 ток_вриједност: 순서를 보존해 내보내는 바이트의 Канал_унос. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Пише(int вриједност) throws У_И_изузетак {
        try { 표준흐름.write(вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void Пише(byte[] подаци) throws У_И_изузетак {
        try { 표준흐름.write(подаци);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void Пише(byte[] подаци, int Покрени, int дужина_вриједност) throws У_И_изузетак {
        try { 표준흐름.write(подаци, Покрени, дужина_вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void 내보내기() throws У_И_изузетак {
        try { 표준흐름.flush();
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void Затворен() throws У_И_изузетак {
        try { 표준흐름.close();
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
}
