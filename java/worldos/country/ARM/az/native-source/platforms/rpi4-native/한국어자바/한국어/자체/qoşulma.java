// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Bağlan(連結)·kanal_daxiletmə(通路): 상대와 이어진 TCP bayt_VALUE 흐름의 종단. */
public final class qoşulma {
    private final java.net.Socket 표준연결;
    qoşulma(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static qoşulma Aç(String ünvan, int 접속번호) throws giriş_çıxış_istisna {
        try {
            return new qoşulma(new java.net.Socket(ünvan, 접속번호));
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public 입력흐름 입력() throws giriş_çıxış_istisna {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public 출력흐름 출력() throws giriş_çıxış_istisna {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void FASİLƏ(int 밀리초) throws giriş_çıxış_istisna {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Bağla() throws giriş_çıxış_istisna {
        try { 표준연결.close();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
}
