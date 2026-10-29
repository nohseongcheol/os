// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 lamba_Daraja 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Buɗe(int fot_Daraja) throws I_O_banbanchi {
        try { return new DatagramSocket(fot_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void Aika(DatagramSocket 종단, int fot_Daraja, String kunshiya_Daraja) throws I_O_banbanchi {
        try {
        Aika(종단, "127.0.0.1", fot_Daraja, kunshiya_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void Aika(DatagramSocket 종단, String imel, int fot_Daraja, String kunshiya_Daraja) throws I_O_banbanchi {
        try {
        byte[] bayit_Daraja = 문자.부호화(kunshiya_Daraja);
        종단.send(new DatagramPacket(bayit_Daraja, bayit_Daraja.length, InetAddress.getByName(imel), fot_Daraja));
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_banbanchi {
        try {
        byte[] bayit_Daraja = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bayit_Daraja, bayit_Daraja.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(bayit_Daraja, 0, 결과, 0, 결과.length); return 문자.Bude_Tarin_bayani(결과);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws I_O_banbanchi {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void Rufe(DatagramSocket 종단) { 종단.close(); }
}
