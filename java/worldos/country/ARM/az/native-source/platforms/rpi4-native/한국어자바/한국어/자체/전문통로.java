// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanal_daxiletmə(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws giriş_çıxış_istisna {
        try { 표준종단 = 통신.Aç(접속번호);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static 전문통로 Aç(int 접속번호) throws giriş_çıxış_istisna {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void göndərmək(String ünvan, int 접속번호, String verilənlər) throws giriş_çıxış_istisna {
        try { 통신.göndərmək(표준종단, ünvan, 접속번호, verilənlər);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public String 받기() throws giriş_çıxış_istisna {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void FASİLƏ(int 밀리초) throws giriş_çıxış_istisna {
        try { 통신.FASİLƏ(표준종단, 밀리초);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Bağla() { 통신.Bağla(표준종단); }
}
