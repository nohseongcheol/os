// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static веза Отвори(String адреса, int број_порта) throws У_И_изузетак {
        try { return веза.Отвори(адреса, број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static 수신창구 수신열기(int број_порта) throws У_И_изузетак {
        try { return 수신창구.Отвори(број_порта);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static Socket Повежи_се(String адреса, int порт_вриједност) throws У_И_изузетак {
        try { return new Socket(адреса, порт_вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static ServerSocket слушати_крајња_тачка(int порт_вриједност) throws У_И_изузетак {
        try { return new ServerSocket(порт_вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static Socket 받기(ServerSocket сервер_вриједност) throws У_И_изузетак {
        try { return сервер_вриједност.accept();
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
}
