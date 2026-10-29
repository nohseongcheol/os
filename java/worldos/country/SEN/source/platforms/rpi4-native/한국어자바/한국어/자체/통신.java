// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 siifar_xëyma 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket sos(int jël_xëyma) throws 입출력예외 {
        try { return new DatagramSocket(jël_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void Yónnee(DatagramSocket 종단, int jël_xëyma, String Këmb_xëyma) throws 입출력예외 {
        try {
        Yónnee(종단, "127.0.0.1", jël_xëyma, Këmb_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void Yónnee(DatagramSocket 종단, String dëkkuwaay, int jël_xëyma, String Këmb_xëyma) throws 입출력예외 {
        try {
        byte[] okte_xëyma = 문자.부호화(Këmb_xëyma);
        종단.send(new DatagramPacket(okte_xëyma, okte_xëyma.length, InetAddress.getByName(dëkkuwaay), jël_xëyma));
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] okte_xëyma = new byte[512]; DatagramPacket 전문 = new DatagramPacket(okte_xëyma, okte_xëyma.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(okte_xëyma, 0, 결과, 0, 결과.length); return 문자.fecci_mbir(결과);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void Tej(DatagramSocket 종단) { 종단.close(); }
}
