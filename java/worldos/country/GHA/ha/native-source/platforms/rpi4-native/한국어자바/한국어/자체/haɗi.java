// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Haɗi(連結)·tasha_Mashigar_bayanai(通路): 상대와 이어진 TCP bayit_Daraja 흐름의 종단. */
public final class haɗi {
    private final java.net.Socket 표준연결;
    haɗi(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static haɗi Buɗe(String imel, int lambar_kafa) throws I_O_banbanchi {
        try {
            return new haɗi(new java.net.Socket(imel, lambar_kafa));
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public 입력흐름 입력() throws I_O_banbanchi {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public 출력흐름 출력() throws I_O_banbanchi {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void 대기시간(int 밀리초) throws I_O_banbanchi {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public int lambar_kafa() { return 표준연결.getPort(); }
    public int na_gida_lambar_kafa() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Rufe() throws I_O_banbanchi {
        try { 표준연결.close();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
