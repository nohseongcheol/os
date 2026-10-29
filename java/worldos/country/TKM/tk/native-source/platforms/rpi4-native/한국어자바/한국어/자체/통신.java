// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 san_baha 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Aç(int port_baha) throws 입출력예외 {
        try { return new DatagramSocket(port_baha);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void iber(DatagramSocket 종단, int port_baha, String Mazmun_baha) throws 입출력예외 {
        try {
        iber(종단, "127.0.0.1", port_baha, Mazmun_baha);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void iber(DatagramSocket 종단, String salgy, int port_baha, String Mazmun_baha) throws 입출력예외 {
        try {
        byte[] baýt_baha = 문자.부호화(Mazmun_baha);
        종단.send(new DatagramPacket(baýt_baha, baýt_baha.length, InetAddress.getByName(salgy), port_baha));
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] baýt_baha = new byte[512]; DatagramPacket 전문 = new DatagramPacket(baýt_baha, baýt_baha.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(baýt_baha, 0, 결과, 0, 결과.length); return 문자.koddan_aç_maglumat(결과);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void Ýap(DatagramSocket 종단) { 종단.close(); }
}
