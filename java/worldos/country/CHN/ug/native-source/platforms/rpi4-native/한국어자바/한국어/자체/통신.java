// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 خانا_قىممىتى 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ئاچ(int ئېغىز_قىممىتى) throws 입출력예외 {
        try { return new DatagramSocket(ئېغىز_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void ئەۋەتمەك(DatagramSocket 종단, int ئېغىز_قىممىتى, String مەزمۇن_قىممىتى) throws 입출력예외 {
        try {
        ئەۋەتمەك(종단, "127.0.0.1", ئېغىز_قىممىتى, مەزمۇن_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void ئەۋەتمەك(DatagramSocket 종단, String ئادرېس, int ئېغىز_قىممىتى, String مەزمۇن_قىممىتى) throws 입출력예외 {
        try {
        byte[] بايت_قىممىتى = 문자.부호화(مەزمۇن_قىممىتى);
        종단.send(new DatagramPacket(بايت_قىممىتى, بايت_قىممىتى.length, InetAddress.getByName(ئادرېس), ئېغىز_قىممىتى));
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] بايت_قىممىتى = new byte[512]; DatagramPacket 전문 = new DatagramPacket(بايت_قىممىتى, بايت_قىممىتى.length); 종단.receive(전문);
        byte[] ئۆلچەم = new byte[전문.getLength()]; System.arraycopy(بايت_قىممىتى, 0, ئۆلچەم, 0, ئۆلچەم.length); return 문자.شىفىر_يېشىش_مەلۇمات(ئۆلچەم);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void ۋاقىت_ئاشتى(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void ياپ(DatagramSocket 종단) { 종단.close(); }
}
