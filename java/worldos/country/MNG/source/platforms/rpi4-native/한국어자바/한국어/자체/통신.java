// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 тоо_утга 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Нээх(int порт_утга) throws 입출력예외 {
        try { return new DatagramSocket(порт_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void илгээх(DatagramSocket 종단, int порт_утга, String Агуулга_утга) throws 입출력예외 {
        try {
        илгээх(종단, "127.0.0.1", порт_утга, Агуулга_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void илгээх(DatagramSocket 종단, String хаяг, int порт_утга, String Агуулга_утга) throws 입출력예외 {
        try {
        byte[] байт_утга = 문자.부호화(Агуулга_утга);
        종단.send(new DatagramPacket(байт_утга, байт_утга.length, InetAddress.getByName(хаяг), порт_утга));
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] байт_утга = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_утга, байт_утга.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(байт_утга, 0, 결과, 0, 결과.length); return 문자.шифрийг_задлах_өгөгдөл(결과);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void Хаах(DatagramSocket 종단) { 종단.close(); }
}
