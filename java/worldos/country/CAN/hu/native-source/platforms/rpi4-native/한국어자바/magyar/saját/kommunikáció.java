// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** kommunikáció(通信): IPv4 UDP datagram. külső_ÉRTÉK 주소는 számjegy_ÉRTÉK 주소를 사용한다. */
public final class kommunikáció {
    private kommunikáció() {}
    public static DatagramSocket Megnyitás(int port_ÉRTÉK) throws I_O_kivétel {
        try { return new DatagramSocket(port_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void küld(DatagramSocket végpont, int port_ÉRTÉK, String Tartalom_ÉRTÉK) throws I_O_kivétel {
        try {
        küld(végpont, "127.0.0.1", port_ÉRTÉK, Tartalom_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void küld(DatagramSocket végpont, String CÍM, int port_ÉRTÉK, String Tartalom_ÉRTÉK) throws I_O_kivétel {
        try {
        byte[] bájt_ÉRTÉK = 문자.kódolás(Tartalom_ÉRTÉK);
        végpont.send(new DatagramPacket(bájt_ÉRTÉK, bájt_ÉRTÉK.length, InetAddress.getByName(CÍM), port_ÉRTÉK));
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static String fogad(DatagramSocket végpont) throws I_O_kivétel {
        try {
        byte[] bájt_ÉRTÉK = new byte[512]; DatagramPacket datagram = new DatagramPacket(bájt_ÉRTÉK, bájt_ÉRTÉK.length); végpont.receive(datagram);
        byte[] KR = new byte[datagram.getLength()]; System.arraycopy(bájt_ÉRTÉK, 0, KR, 0, KR.length); return 문자.visszafejt_adat(KR);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void IDŐTÚLLÉPÉS(DatagramSocket végpont, int 밀리초) throws I_O_kivétel {
        try { végpont.setSoTimeout(밀리초);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void Bezárás(DatagramSocket végpont) { végpont.close(); }
}
