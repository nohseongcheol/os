// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagram. spoljni_VALUE 주소는 cifra_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket otvoren(int port_VALUE) throws U_I_izuzetak {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void poslati(DatagramSocket učesnik, int port_VALUE, String Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        poslati(učesnik, "127.0.0.1", port_VALUE, Sadržaj_VALUE);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void poslati(DatagramSocket učesnik, String adresa, int port_VALUE, String Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        byte[] bajt_VALUE = 문자.kodirati(Sadržaj_VALUE);
        učesnik.send(new DatagramPacket(bajt_VALUE, bajt_VALUE.length, InetAddress.getByName(adresa), port_VALUE));
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static String primiti(DatagramSocket učesnik) throws U_I_izuzetak {
        try {
        byte[] bajt_VALUE = new byte[512]; DatagramPacket datagram = new DatagramPacket(bajt_VALUE, bajt_VALUE.length); učesnik.receive(datagram);
        byte[] KR = new byte[datagram.getLength()]; System.arraycopy(bajt_VALUE, 0, KR, 0, KR.length); return 문자.dešifrovati_podaci(KR);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void TIMEOUT(DatagramSocket učesnik, int 밀리초) throws U_I_izuzetak {
        try { učesnik.setSoTimeout(밀리초);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void Zatvori(DatagramSocket učesnik) { učesnik.close(); }
}
