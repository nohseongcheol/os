// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** kommunikation(通信): IPv4 UDP datagram. extern_värde 주소는 siffra_värde 주소를 사용한다. */
public final class kommunikation {
    private kommunikation() {}
    public static DatagramSocket Öppna(int port_värde) throws indata_utleverans_fel {
        try { return new DatagramSocket(port_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void skicka(DatagramSocket deltagare, int port_värde, String Innehåll_värde) throws indata_utleverans_fel {
        try {
        skicka(deltagare, "127.0.0.1", port_värde, Innehåll_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void skicka(DatagramSocket deltagare, String Adress, int port_värde, String Innehåll_värde) throws indata_utleverans_fel {
        try {
        byte[] byte_värde = 문자.koda(Innehåll_värde);
        deltagare.send(new DatagramPacket(byte_värde, byte_värde.length, InetAddress.getByName(Adress), port_värde));
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static String få(DatagramSocket deltagare) throws indata_utleverans_fel {
        try {
        byte[] byte_värde = new byte[512]; DatagramPacket datagram = new DatagramPacket(byte_värde, byte_värde.length); deltagare.receive(datagram);
        byte[] RESULTAT = new byte[datagram.getLength()]; System.arraycopy(byte_värde, 0, RESULTAT, 0, RESULTAT.length); return 문자.avkryptera_data(RESULTAT);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void TIMEOUT(DatagramSocket deltagare, int 밀리초) throws indata_utleverans_fel {
        try { deltagare.setSoTimeout(밀리초);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void Stäng(DatagramSocket deltagare) { deltagare.close(); }
}
