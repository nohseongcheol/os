// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Отвори(int 창구) throws 입출력예외 {
        try { return new DatagramSocket(창구);
        } catch (java.io.IOException ГРЕШКА) { throw 예외변환.입출력(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw 예외변환.실행(ГРЕШКА); }
    }
    public static void 보내기(DatagramSocket 종단, int 창구, String 내용) throws 입출력예외 {
        try {
        보내기(종단, "127.0.0.1", 창구, 내용);
        } catch (java.io.IOException ГРЕШКА) { throw 예외변환.입출력(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw 예외변환.실행(ГРЕШКА); }
    }
    public static void 보내기(DatagramSocket 종단, String 주소, int 창구, String 내용) throws 입출력예외 {
        try {
        byte[] 바이트 = 문자.부호화(내용);
        종단.send(new DatagramPacket(바이트, 바이트.length, InetAddress.getByName(주소), 창구));
        } catch (java.io.IOException ГРЕШКА) { throw 예외변환.입출력(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw 예외변환.실행(ГРЕШКА); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] 바이트 = new byte[512]; DatagramPacket 전문 = new DatagramPacket(바이트, 바이트.length); 종단.receive(전문);
        byte[] ИСХОД = new byte[전문.getLength()]; System.arraycopy(바이트, 0, ИСХОД, 0, ИСХОД.length); return 문자.복호화(ИСХОД);
        } catch (java.io.IOException ГРЕШКА) { throw 예외변환.입출력(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw 예외변환.실행(ГРЕШКА); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw 예외변환.입출력(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw 예외변환.실행(ГРЕШКА); }
    }
    public static void Затворен(DatagramSocket 종단) { 종단.close(); }
}
