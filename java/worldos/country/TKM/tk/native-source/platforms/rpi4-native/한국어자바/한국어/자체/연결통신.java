// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static birikme Aç(String salgy, int 접속번호) throws 입출력예외 {
        try { return birikme.Aç(salgy, 접속번호);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Aç(접속번호);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static Socket Birikme(String salgy, int port_baha) throws 입출력예외 {
        try { return new Socket(salgy, port_baha);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static ServerSocket 듣기(int port_baha) throws 입출력예외 {
        try { return new ServerSocket(port_baha);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static Socket 받기(ServerSocket serwer_baha) throws 입출력예외 {
        try { return serwer_baha.accept();
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
}
