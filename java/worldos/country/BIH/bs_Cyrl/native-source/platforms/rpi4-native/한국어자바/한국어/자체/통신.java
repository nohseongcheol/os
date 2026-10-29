// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket отворити(int порт_вриједност) throws 입출력예외 {
        try { return new DatagramSocket(порт_вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void послати(DatagramSocket крајња_тачка, int порт_вриједност, String Садржај_вриједност) throws 입출력예외 {
        try {
        послати(крајња_тачка, "127.0.0.1", порт_вриједност, Садржај_вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void послати(DatagramSocket крајња_тачка, String адреса, int порт_вриједност, String Садржај_вриједност) throws 입출력예외 {
        try {
        byte[] бајт_вриједност = 문자.부호화(Садржај_вриједност);
        крајња_тачка.send(new DatagramPacket(бајт_вриједност, бајт_вриједност.length, InetAddress.getByName(адреса), порт_вриједност));
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static String 받기(DatagramSocket крајња_тачка) throws 입출력예외 {
        try {
        byte[] бајт_вриједност = new byte[512]; DatagramPacket 전문 = new DatagramPacket(бајт_вриједност, бајт_вриједност.length); крајња_тачка.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(бајт_вриједност, 0, 결과, 0, 결과.length); return 문자.дешифрирати_подаци(결과);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void 대기시간(DatagramSocket крајња_тачка, int 밀리초) throws 입출력예외 {
        try { крајња_тачка.setSoTimeout(밀리초);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void затворити(DatagramSocket крајња_тачка) { крајња_тачка.close(); }
}
