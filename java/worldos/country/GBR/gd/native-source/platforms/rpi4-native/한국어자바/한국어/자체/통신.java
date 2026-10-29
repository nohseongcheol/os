// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 figear_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket fosgail(int port_VALUE) throws 입출력예외 {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void cuir(DatagramSocket 종단, int port_VALUE, String susbaint_VALUE) throws 입출력예외 {
        try {
        cuir(종단, "127.0.0.1", port_VALUE, susbaint_VALUE);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void cuir(DatagramSocket 종단, String ADDRESS, int port_VALUE, String susbaint_VALUE) throws 입출력예외 {
        try {
        byte[] baidht_VALUE = 문자.부호화(susbaint_VALUE);
        종단.send(new DatagramPacket(baidht_VALUE, baidht_VALUE.length, InetAddress.getByName(ADDRESS), port_VALUE));
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] baidht_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(baidht_VALUE, baidht_VALUE.length); 종단.receive(전문);
        byte[] tomhas = new byte[전문.getLength()]; System.arraycopy(baidht_VALUE, 0, tomhas, 0, tomhas.length); return 문자.dì_chrioptaich_dàta(tomhas);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void dùin(DatagramSocket 종단) { 종단.close(); }
}
