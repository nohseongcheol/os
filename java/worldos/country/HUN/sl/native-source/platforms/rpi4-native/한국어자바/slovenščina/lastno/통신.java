// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagram. zunanji_VALUE 주소는 številka_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Odpri(int vrata_VALUE) throws V_I_izjema {
        try { return new DatagramSocket(vrata_VALUE);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void poslati(DatagramSocket končna_točka, int vrata_VALUE, String vsebina_VALUE) throws V_I_izjema {
        try {
        poslati(končna_točka, "127.0.0.1", vrata_VALUE, vsebina_VALUE);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void poslati(DatagramSocket končna_točka, String naslov, int vrata_VALUE, String vsebina_VALUE) throws V_I_izjema {
        try {
        byte[] bajt_VALUE = 문자.kodirati(vsebina_VALUE);
        končna_točka.send(new DatagramPacket(bajt_VALUE, bajt_VALUE.length, InetAddress.getByName(naslov), vrata_VALUE));
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static String sprejeti_sprejemati_prejeti_prejemati(DatagramSocket končna_točka) throws V_I_izjema {
        try {
        byte[] bajt_VALUE = new byte[512]; DatagramPacket datagram = new DatagramPacket(bajt_VALUE, bajt_VALUE.length); končna_točka.receive(datagram);
        byte[] REZULTAT = new byte[datagram.getLength()]; System.arraycopy(bajt_VALUE, 0, REZULTAT, 0, REZULTAT.length); return 문자.dešifrirati_podatki(REZULTAT);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void TIMEOUT(DatagramSocket končna_točka, int 밀리초) throws V_I_izjema {
        try { končna_točka.setSoTimeout(밀리초);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void Zapri(DatagramSocket končna_točka) { končna_točka.close(); }
}
