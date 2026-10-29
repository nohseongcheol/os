// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ċifra_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket fetaħ(int port_VALUE) throws 입출력예외 {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void bagħat(DatagramSocket 종단, int port_VALUE, String Kontenut_VALUE) throws 입출력예외 {
        try {
        bagħat(종단, "127.0.0.1", port_VALUE, Kontenut_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void bagħat(DatagramSocket 종단, String ADDRESS, int port_VALUE, String Kontenut_VALUE) throws 입출력예외 {
        try {
        byte[] byte_VALUE = 문자.부호화(Kontenut_VALUE);
        종단.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(ADDRESS), port_VALUE));
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALUE, byte_VALUE.length); 종단.receive(전문);
        byte[] miżura = new byte[전문.getLength()]; System.arraycopy(byte_VALUE, 0, miżura, 0, miżura.length); return 문자.ddeċifra_data(miżura);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void agħlaq(DatagramSocket 종단) { 종단.close(); }
}
