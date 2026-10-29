// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·fot_Daraja(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int lambar_kafa) throws I_O_banbanchi {
        try { 표준창구 = new java.net.ServerSocket(lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static 수신창구 Buɗe(int lambar_kafa) throws I_O_banbanchi {
        try { return new 수신창구(lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public haɗi 받기() throws I_O_banbanchi {
        try { return new haɗi(표준창구.accept());
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public int lambar_kafa() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws I_O_banbanchi {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Rufe() throws I_O_banbanchi {
        try { 표준창구.close();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
