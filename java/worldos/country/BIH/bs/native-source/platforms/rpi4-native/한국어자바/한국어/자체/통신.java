// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. iz_eksternog_izvora_VALUE 주소는 cifra_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Otvori(int port_VALUE) throws U_I_izuzetak {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void poslati(DatagramSocket završna_tačka, int port_VALUE, String Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        poslati(završna_tačka, "127.0.0.1", port_VALUE, Sadržaj_VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void poslati(DatagramSocket završna_tačka, String adresa, int port_VALUE, String Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        byte[] bajt_VALUE = 문자.부호화(Sadržaj_VALUE);
        završna_tačka.send(new DatagramPacket(bajt_VALUE, bajt_VALUE.length, InetAddress.getByName(adresa), port_VALUE));
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static String 받기(DatagramSocket završna_tačka) throws U_I_izuzetak {
        try {
        byte[] bajt_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bajt_VALUE, bajt_VALUE.length); završna_tačka.receive(전문);
        byte[] mjera = new byte[전문.getLength()]; System.arraycopy(bajt_VALUE, 0, mjera, 0, mjera.length); return 문자.dešifrirati_podaci(mjera);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void TIMEOUT(DatagramSocket završna_tačka, int 밀리초) throws U_I_izuzetak {
        try { završna_tačka.setSoTimeout(밀리초);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void Zatvori(DatagramSocket završna_tačka) { završna_tačka.close(); }
}
