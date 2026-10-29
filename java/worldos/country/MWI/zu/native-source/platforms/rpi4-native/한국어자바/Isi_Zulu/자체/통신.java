// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 idijithi_inani 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Vula(int intuba_inani) throws 입출력예외 {
        try { return new DatagramSocket(intuba_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void Thumela(DatagramSocket 종단, int intuba_inani, String Okuqukethwe_inani) throws 입출력예외 {
        try {
        Thumela(종단, "127.0.0.1", intuba_inani, Okuqukethwe_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void Thumela(DatagramSocket 종단, String ikheli, int intuba_inani, String Okuqukethwe_inani) throws 입출력예외 {
        try {
        byte[] ibhayithi_inani = 문자.부호화(Okuqukethwe_inani);
        종단.send(new DatagramPacket(ibhayithi_inani, ibhayithi_inani.length, InetAddress.getByName(ikheli), intuba_inani));
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] ibhayithi_inani = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ibhayithi_inani, ibhayithi_inani.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(ibhayithi_inani, 0, 결과, 0, 결과.length); return 문자.guqulela_imininingwane(결과);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void Vala(DatagramSocket 종단) { 종단.close(); }
}
