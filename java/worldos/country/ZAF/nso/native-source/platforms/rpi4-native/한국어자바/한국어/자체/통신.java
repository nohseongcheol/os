// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Bula(int phote_boleng) throws 입출력예외 {
        try { return new DatagramSocket(phote_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void Romela(DatagramSocket 종단, int phote_boleng, String Diteng_boleng) throws 입출력예외 {
        try {
        Romela(종단, "127.0.0.1", phote_boleng, Diteng_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void Romela(DatagramSocket 종단, String atrese, int phote_boleng, String Diteng_boleng) throws 입출력예외 {
        try {
        byte[] paete_boleng = 문자.부호화(Diteng_boleng);
        종단.send(new DatagramPacket(paete_boleng, paete_boleng.length, InetAddress.getByName(atrese), phote_boleng));
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] paete_boleng = new byte[512]; DatagramPacket 전문 = new DatagramPacket(paete_boleng, paete_boleng.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(paete_boleng, 0, 결과, 0, 결과.length); return 문자.boetša_sekeng_data(결과);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void Tswalela(DatagramSocket 종단) { 종단.close(); }
}
