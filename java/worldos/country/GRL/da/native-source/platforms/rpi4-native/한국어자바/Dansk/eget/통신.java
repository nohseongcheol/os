// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagram. ekstern_VÆRDI 주소는 ciffer_VÆRDI 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Åbn(int port_VÆRDI) throws I_O_undtagelse {
        try { return new DatagramSocket(port_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void maile(DatagramSocket slutpunkt, int port_VÆRDI, String Indhold_VÆRDI) throws I_O_undtagelse {
        try {
        maile(slutpunkt, "127.0.0.1", port_VÆRDI, Indhold_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void maile(DatagramSocket slutpunkt, String mail, int port_VÆRDI, String Indhold_VÆRDI) throws I_O_undtagelse {
        try {
        byte[] byte_VÆRDI = 문자.kode(Indhold_VÆRDI);
        slutpunkt.send(new DatagramPacket(byte_VÆRDI, byte_VÆRDI.length, InetAddress.getByName(mail), port_VÆRDI));
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static String modtage(DatagramSocket slutpunkt) throws I_O_undtagelse {
        try {
        byte[] byte_VÆRDI = new byte[512]; DatagramPacket datagram = new DatagramPacket(byte_VÆRDI, byte_VÆRDI.length); slutpunkt.receive(datagram);
        byte[] KR = new byte[datagram.getLength()]; System.arraycopy(byte_VÆRDI, 0, KR, 0, KR.length); return 문자.dekryptere_data(KR);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void TIMEOUT(DatagramSocket slutpunkt, int 밀리초) throws I_O_undtagelse {
        try { slutpunkt.setSoTimeout(밀리초);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void Luk(DatagramSocket slutpunkt) { slutpunkt.close(); }
}
