// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Ulanish(連結)·kanal_kiritish(通路): 상대와 이어진 TCP bayt_VALUE 흐름의 종단. */
public final class aloqa {
    private final java.net.Socket 표준연결;
    aloqa(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static aloqa Ochish(String manzil, int 접속번호) throws I_O_istisno {
        try {
            return new aloqa(new java.net.Socket(manzil, 접속번호));
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public 입력흐름 입력() throws I_O_istisno {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public 출력흐름 출력() throws I_O_istisno {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void TANAFFUS(int 밀리초) throws I_O_istisno {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Yopish() throws I_O_istisno {
        try { 표준연결.close();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
