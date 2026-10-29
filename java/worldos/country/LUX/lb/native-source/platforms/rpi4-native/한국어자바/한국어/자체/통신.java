// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 Ziffer_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ariichten(int Port_VALUE) throws 입출력예외 {
        try { return new DatagramSocket(Port_VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void mailen(DatagramSocket 종단, int Port_VALUE, String Inhalt_VALUE) throws 입출력예외 {
        try {
        mailen(종단, "127.0.0.1", Port_VALUE, Inhalt_VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void mailen(DatagramSocket 종단, String Adress, int Port_VALUE, String Inhalt_VALUE) throws 입출력예외 {
        try {
        byte[] Byte_VALUE = 문자.부호화(Inhalt_VALUE);
        종단.send(new DatagramPacket(Byte_VALUE, Byte_VALUE.length, InetAddress.getByName(Adress), Port_VALUE));
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] Byte_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(Byte_VALUE, Byte_VALUE.length); 종단.receive(전문);
        byte[] Mooss = new byte[전문.getLength()]; System.arraycopy(Byte_VALUE, 0, Mooss, 0, Mooss.length); return 문자.decryptéieren_Daten(Mooss);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void Clôture(DatagramSocket 종단) { 종단.close(); }
}
