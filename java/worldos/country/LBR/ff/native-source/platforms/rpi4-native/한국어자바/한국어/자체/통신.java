// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket udditde(int poor_njaru) throws 입출력예외 {
        try { return new DatagramSocket(poor_njaru);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void neldude(DatagramSocket 종단, int poor_njaru, String loowdi_njaru) throws 입출력예외 {
        try {
        neldude(종단, "127.0.0.1", poor_njaru, loowdi_njaru);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void neldude(DatagramSocket 종단, String ñiiɓirde, int poor_njaru, String loowdi_njaru) throws 입출력예외 {
        try {
        byte[] oktee_njaru = 문자.부호화(loowdi_njaru);
        종단.send(new DatagramPacket(oktee_njaru, oktee_njaru.length, InetAddress.getByName(ñiiɓirde), poor_njaru));
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] oktee_njaru = new byte[512]; DatagramPacket 전문 = new DatagramPacket(oktee_njaru, oktee_njaru.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(oktee_njaru, 0, 결과, 0, 결과.length); return 문자.dokkitde_keɓe(결과);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void uddude(DatagramSocket 종단) { 종단.close(); }
}
