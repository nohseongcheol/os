// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagram. externý_VALUE 주소는 číslica_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Otvoriť(int port_VALUE) throws vstup_a_výstup_výnimka {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void odoslať(DatagramSocket účastník, int port_VALUE, String obsah_VALUE) throws vstup_a_výstup_výnimka {
        try {
        odoslať(účastník, "127.0.0.1", port_VALUE, obsah_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void odoslať(DatagramSocket účastník, String adresa, int port_VALUE, String obsah_VALUE) throws vstup_a_výstup_výnimka {
        try {
        byte[] Byte_VALUE = 문자.kódovať(obsah_VALUE);
        účastník.send(new DatagramPacket(Byte_VALUE, Byte_VALUE.length, InetAddress.getByName(adresa), port_VALUE));
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static String dostať(DatagramSocket účastník) throws vstup_a_výstup_výnimka {
        try {
        byte[] Byte_VALUE = new byte[512]; DatagramPacket datagram = new DatagramPacket(Byte_VALUE, Byte_VALUE.length); účastník.receive(datagram);
        byte[] KR = new byte[datagram.getLength()]; System.arraycopy(Byte_VALUE, 0, KR, 0, KR.length); return 문자.dešifrovať_údaje(KR);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void TIMEOUT(DatagramSocket účastník, int 밀리초) throws vstup_a_výstup_výnimka {
        try { účastník.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void Zatvoriť(DatagramSocket účastník) { účastník.close(); }
}
