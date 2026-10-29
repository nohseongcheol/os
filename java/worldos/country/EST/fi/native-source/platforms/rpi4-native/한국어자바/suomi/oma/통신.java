// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagrammi. ulkoinen_ARVO 주소는 numero_ARVO 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Avaa(int portti_ARVO) throws I_O_poikkeus {
        try { return new DatagramSocket(portti_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void lähettää(DatagramSocket päätepiste, int portti_ARVO, String Sisältö_ARVO) throws I_O_poikkeus {
        try {
        lähettää(päätepiste, "127.0.0.1", portti_ARVO, Sisältö_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void lähettää(DatagramSocket päätepiste, String OSOITE, int portti_ARVO, String Sisältö_ARVO) throws I_O_poikkeus {
        try {
        byte[] tavu_ARVO = 문자.koodata(Sisältö_ARVO);
        päätepiste.send(new DatagramPacket(tavu_ARVO, tavu_ARVO.length, InetAddress.getByName(OSOITE), portti_ARVO));
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static String saada(DatagramSocket päätepiste) throws I_O_poikkeus {
        try {
        byte[] tavu_ARVO = new byte[512]; DatagramPacket datagrammi = new DatagramPacket(tavu_ARVO, tavu_ARVO.length); päätepiste.receive(datagrammi);
        byte[] TULOS = new byte[datagrammi.getLength()]; System.arraycopy(tavu_ARVO, 0, TULOS, 0, TULOS.length); return 문자.pura_salaus_data(TULOS);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void AIKAKATKAISU(DatagramSocket päätepiste, int 밀리초) throws I_O_poikkeus {
        try { päätepiste.setSoTimeout(밀리초);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void Sulje(DatagramSocket päätepiste) { päätepiste.close(); }
}
