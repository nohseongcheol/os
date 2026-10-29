// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 рақам_қимат 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket кушодан(int порт_қимат) throws 입출력예외 {
        try { return new DatagramSocket(порт_қимат);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void фиристодан(DatagramSocket 종단, int порт_қимат, String Мӯҳтаво_қимат) throws 입출력예외 {
        try {
        фиристодан(종단, "127.0.0.1", порт_қимат, Мӯҳтаво_қимат);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void фиристодан(DatagramSocket 종단, String суроға, int порт_қимат, String Мӯҳтаво_қимат) throws 입출력예외 {
        try {
        byte[] байт_қимат = 문자.부호화(Мӯҳтаво_қимат);
        종단.send(new DatagramPacket(байт_қимат, байт_қимат.length, InetAddress.getByName(суроға), порт_қимат));
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] байт_қимат = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_қимат, байт_қимат.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(байт_қимат, 0, 결과, 0, 결과.length); return 문자.рамзкушоӣ_кардан_иттилоот(결과);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void Пӯшидан(DatagramSocket 종단) { 종단.close(); }
}
