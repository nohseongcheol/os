// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagram. ekstern_VERDI 주소는 siffer_VERDI 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Åpne(int port_VERDI) throws I_U_unntak {
        try { return new DatagramSocket(port_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void sende(DatagramSocket deltaker, int port_VERDI, String Innhold_VERDI) throws I_U_unntak {
        try {
        sende(deltaker, "127.0.0.1", port_VERDI, Innhold_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void sende(DatagramSocket deltaker, String e_post, int port_VERDI, String Innhold_VERDI) throws I_U_unntak {
        try {
        byte[] byte_VERDI = 문자.부호화(Innhold_VERDI);
        deltaker.send(new DatagramPacket(byte_VERDI, byte_VERDI.length, InetAddress.getByName(e_post), port_VERDI));
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static String motta(DatagramSocket deltaker) throws I_U_unntak {
        try {
        byte[] byte_VERDI = new byte[512]; DatagramPacket datagram = new DatagramPacket(byte_VERDI, byte_VERDI.length); deltaker.receive(datagram);
        byte[] KR = new byte[datagram.getLength()]; System.arraycopy(byte_VERDI, 0, KR, 0, KR.length); return 문자.dekryptere_data(KR);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void TIMEOUT(DatagramSocket deltaker, int 밀리초) throws I_U_unntak {
        try { deltaker.setSoTimeout(밀리초);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void Lukk(DatagramSocket deltaker) { deltaker.close(); }
}
