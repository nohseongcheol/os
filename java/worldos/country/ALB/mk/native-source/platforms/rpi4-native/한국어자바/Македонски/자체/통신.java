// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 цифра_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Отвори(int порта_VALUE) throws В_И_исклучок {
        try { return new DatagramSocket(порта_VALUE);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void испрати(DatagramSocket 종단, int порта_VALUE, String Содржина_VALUE) throws В_И_исклучок {
        try {
        испрати(종단, "127.0.0.1", порта_VALUE, Содржина_VALUE);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void испрати(DatagramSocket 종단, String адреса, int порта_VALUE, String Содржина_VALUE) throws В_И_исклучок {
        try {
        byte[] бајт_VALUE = 문자.부호화(Содржина_VALUE);
        종단.send(new DatagramPacket(бајт_VALUE, бајт_VALUE.length, InetAddress.getByName(адреса), порта_VALUE));
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static String 받기(DatagramSocket 종단) throws В_И_исклучок {
        try {
        byte[] бајт_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(бајт_VALUE, бајт_VALUE.length); 종단.receive(전문);
        byte[] мерка = new byte[전문.getLength()]; System.arraycopy(бајт_VALUE, 0, мерка, 0, мерка.length); return 문자.дешифрирај_податоци(мерка);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws В_И_исклучок {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void Затвори(DatagramSocket 종단) { 종단.close(); }
}
