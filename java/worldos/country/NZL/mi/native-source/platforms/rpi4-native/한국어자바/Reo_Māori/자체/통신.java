// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 mati_uara 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Huaki(int kawe_uara) throws 입출력예외 {
        try { return new DatagramSocket(kawe_uara);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void tuku(DatagramSocket 종단, int kawe_uara, String Ihirangi_uara) throws 입출력예외 {
        try {
        tuku(종단, "127.0.0.1", kawe_uara, Ihirangi_uara);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void tuku(DatagramSocket 종단, String ADDRESS, int kawe_uara, String Ihirangi_uara) throws 입출력예외 {
        try {
        byte[] paita_uara = 문자.부호화(Ihirangi_uara);
        종단.send(new DatagramPacket(paita_uara, paita_uara.length, InetAddress.getByName(ADDRESS), kawe_uara));
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] paita_uara = new byte[512]; DatagramPacket 전문 = new DatagramPacket(paita_uara, paita_uara.length); 종단.receive(전문);
        byte[] mēhua = new byte[전문.getLength()]; System.arraycopy(paita_uara, 0, mēhua, 0, mēhua.length); return 문자.wetemuna_raraunga(mēhua);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void KUA_PAU_TE_WĀ(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void Kati(DatagramSocket 종단) { 종단.close(); }
}
