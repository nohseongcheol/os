// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static qoşulma Aç(String ünvan, int 접속번호) throws giriş_çıxış_istisna {
        try { return qoşulma.Aç(ünvan, 접속번호);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static 수신창구 수신열기(int 접속번호) throws giriş_çıxış_istisna {
        try { return 수신창구.Aç(접속번호);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static Socket Bağlan(String ünvan, int port_VALUE) throws giriş_çıxış_istisna {
        try { return new Socket(ünvan, port_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static ServerSocket 듣기(int port_VALUE) throws giriş_çıxış_istisna {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws giriş_çıxış_istisna {
        try { return server_VALUE.accept();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
}
