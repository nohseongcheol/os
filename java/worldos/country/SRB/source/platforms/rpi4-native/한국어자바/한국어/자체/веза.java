// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Повежи_се(連結)·Канал_унос(通路): 상대와 이어진 TCP бајт_вриједност 흐름의 крајња_тачка. */
public final class веза {
    private final java.net.Socket 표준연결;
    веза(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static веза Отвори(String адреса, int број_порта) throws У_И_изузетак {
        try {
            return new веза(new java.net.Socket(адреса, број_порта));
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public 입력흐름 입력() throws У_И_изузетак {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public 출력흐름 Излаз() throws У_И_изузетак {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void 대기시간(int 밀리초) throws У_И_изузетак {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public int број_порта() { return 표준연결.getPort(); }
    public int локални_број_порта() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Затворен() throws У_И_изузетак {
        try { 표준연결.close();
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
}
