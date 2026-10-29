// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·порт_вриједност(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int број_порта) throws У_И_изузетак {
        try { 표준창구 = new java.net.ServerSocket(број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static 수신창구 Отвори(int број_порта) throws У_И_изузетак {
        try { return new 수신창구(број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public веза 받기() throws У_И_изузетак {
        try { return new веза(표준창구.accept());
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public int број_порта() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws У_И_изузетак {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Затворен() throws У_И_изузетак {
        try { 표준창구.close();
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
}
