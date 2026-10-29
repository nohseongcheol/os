// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ọbula_valuu 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Mepee(int pọọt_valuu) throws 입출력예외 {
        try { return new DatagramSocket(pọọt_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void zìga(DatagramSocket 종단, int pọọt_valuu, String ndịnà_valuu) throws 입출력예외 {
        try {
        zìga(종단, "127.0.0.1", pọọt_valuu, ndịnà_valuu);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void zìga(DatagramSocket 종단, String àdreèsì, int pọọt_valuu, String ndịnà_valuu) throws 입출력예외 {
        try {
        byte[] baịtị_valuu = 문자.부호화(ndịnà_valuu);
        종단.send(new DatagramPacket(baịtị_valuu, baịtị_valuu.length, InetAddress.getByName(àdreèsì), pọọt_valuu));
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] baịtị_valuu = new byte[512]; DatagramPacket 전문 = new DatagramPacket(baịtị_valuu, baịtị_valuu.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(baịtị_valuu, 0, 결과, 0, 결과.length); return 문자.tụghee_edenzizo_datà(결과);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void Mechie(DatagramSocket 종단) { 종단.close(); }
}
