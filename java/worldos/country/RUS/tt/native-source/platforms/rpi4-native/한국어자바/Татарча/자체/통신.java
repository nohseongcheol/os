// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 сан_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ачу(int порт_VALUE) throws 입출력예외 {
        try { return new DatagramSocket(порт_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void җибәрү(DatagramSocket 종단, int порт_VALUE, String Эчтәлек_VALUE) throws 입출력예외 {
        try {
        җибәрү(종단, "127.0.0.1", порт_VALUE, Эчтәлек_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void җибәрү(DatagramSocket 종단, String адрес, int порт_VALUE, String Эчтәлек_VALUE) throws 입출력예외 {
        try {
        byte[] байт_VALUE = 문자.부호화(Эчтәлек_VALUE);
        종단.send(new DatagramPacket(байт_VALUE, байт_VALUE.length, InetAddress.getByName(адрес), порт_VALUE));
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] байт_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_VALUE, байт_VALUE.length); 종단.receive(전문);
        byte[] үлчәм = new byte[전문.getLength()]; System.arraycopy(байт_VALUE, 0, үлчәм, 0, үлчәм.length); return 문자.шифрны_ачу_мәгълүмат(үлчәм);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void КӨТҮВАКЫТЫЧЫГУ(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void Yap(DatagramSocket 종단) { 종단.close(); }
}
