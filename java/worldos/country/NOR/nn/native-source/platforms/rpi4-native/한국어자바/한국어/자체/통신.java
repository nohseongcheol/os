// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. ekstern_VALUE 주소는 siffer_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Opna(int port_VALUE) throws I_U_unntak {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void sende(DatagramSocket endepunkt, int port_VALUE, String Innhald_VALUE) throws I_U_unntak {
        try {
        sende(endepunkt, "127.0.0.1", port_VALUE, Innhald_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void sende(DatagramSocket endepunkt, String ADDRESS, int port_VALUE, String Innhald_VALUE) throws I_U_unntak {
        try {
        byte[] byte_VALUE = 문자.부호화(Innhald_VALUE);
        endepunkt.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(ADDRESS), port_VALUE));
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static String 받기(DatagramSocket endepunkt) throws I_U_unntak {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALUE, byte_VALUE.length); endepunkt.receive(전문);
        byte[] forretningsmål = new byte[전문.getLength()]; System.arraycopy(byte_VALUE, 0, forretningsmål, 0, forretningsmål.length); return 문자.dekryptere_data(forretningsmål);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void TIMEOUT(DatagramSocket endepunkt, int 밀리초) throws I_U_unntak {
        try { endepunkt.setSoTimeout(밀리초);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void Lukk(DatagramSocket endepunkt) { endepunkt.close(); }
}
