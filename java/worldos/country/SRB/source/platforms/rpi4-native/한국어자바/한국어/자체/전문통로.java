// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·Канал_унос(通路): 경계를 가진 UDP 자료를 주고받는 крајња_тачка. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int број_порта) throws У_И_изузетак {
        try { 표준종단 = 통신.Отвори(број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static 전문통로 Отвори(int број_порта) throws У_И_изузетак {
        try { return new 전문통로(број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void послати(String адреса, int број_порта, String подаци) throws У_И_изузетак {
        try { 통신.послати(표준종단, адреса, број_порта, подаци);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public String 받기() throws У_И_изузетак {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public void 대기시간(int 밀리초) throws У_И_изузетак {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public int број_порта() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Затворен() { 통신.Затворен(표준종단); }
}
