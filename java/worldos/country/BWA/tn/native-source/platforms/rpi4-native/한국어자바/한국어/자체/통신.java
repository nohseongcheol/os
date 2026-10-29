// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 dijite_Boleng 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket bula(int gorogisetsa_Boleng) throws 입출력예외 {
        try { return new DatagramSocket(gorogisetsa_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void romela(DatagramSocket 종단, int gorogisetsa_Boleng, String Diteng_Boleng) throws 입출력예외 {
        try {
        romela(종단, "127.0.0.1", gorogisetsa_Boleng, Diteng_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void romela(DatagramSocket 종단, String aterese, int gorogisetsa_Boleng, String Diteng_Boleng) throws 입출력예외 {
        try {
        byte[] baete_Boleng = 문자.부호화(Diteng_Boleng);
        종단.send(new DatagramPacket(baete_Boleng, baete_Boleng.length, InetAddress.getByName(aterese), gorogisetsa_Boleng));
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] baete_Boleng = new byte[512]; DatagramPacket 전문 = new DatagramPacket(baete_Boleng, baete_Boleng.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(baete_Boleng, 0, 결과, 0, 결과.length); return 문자.Sirolola_tshedimosetso(결과);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void tswala(DatagramSocket 종단) { 종단.close(); }
}
