// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datogram. vanjski_VALUE 주소는 znamenka_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Otvori(int prebaciti_VALUE) throws U_I_iznimka {
        try { return new DatagramSocket(prebaciti_VALUE);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void slati(DatagramSocket sudionik, int prebaciti_VALUE, String Sadržaj_VALUE) throws U_I_iznimka {
        try {
        slati(sudionik, "127.0.0.1", prebaciti_VALUE, Sadržaj_VALUE);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void slati(DatagramSocket sudionik, String adresa, int prebaciti_VALUE, String Sadržaj_VALUE) throws U_I_iznimka {
        try {
        byte[] bajt_VALUE = 문자.kodirati(Sadržaj_VALUE);
        sudionik.send(new DatagramPacket(bajt_VALUE, bajt_VALUE.length, InetAddress.getByName(adresa), prebaciti_VALUE));
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static String primiti(DatagramSocket sudionik) throws U_I_iznimka {
        try {
        byte[] bajt_VALUE = new byte[512]; DatagramPacket datogram = new DatagramPacket(bajt_VALUE, bajt_VALUE.length); sudionik.receive(datogram);
        byte[] REZULTAT = new byte[datogram.getLength()]; System.arraycopy(bajt_VALUE, 0, REZULTAT, 0, REZULTAT.length); return 문자.dešifrirati_podaci(REZULTAT);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void TIMEOUT(DatagramSocket sudionik, int 밀리초) throws U_I_iznimka {
        try { sudionik.setSoTimeout(밀리초);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void Zatvori(DatagramSocket sudionik) { sudionik.close(); }
}
