// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 санарип_маани 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ачуу(int порт_маани) throws 입출력예외 {
        try { return new DatagramSocket(порт_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void жөнөтүү(DatagramSocket 종단, int порт_маани, String Мазмун_маани) throws 입출력예외 {
        try {
        жөнөтүү(종단, "127.0.0.1", порт_маани, Мазмун_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void жөнөтүү(DatagramSocket 종단, String дарек, int порт_маани, String Мазмун_маани) throws 입출력예외 {
        try {
        byte[] байт_маани = 문자.부호화(Мазмун_маани);
        종단.send(new DatagramPacket(байт_маани, байт_маани.length, InetAddress.getByName(дарек), порт_маани));
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] байт_маани = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_маани, байт_маани.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(байт_маани, 0, 결과, 0, 결과.length); return 문자.чечмелөө_берилмелер(결과);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void Жабуу(DatagramSocket 종단) { 종단.close(); }
}
