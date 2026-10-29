// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP paketų_kelio_schema. išorinis_VALUE 주소는 skaitmuo_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Atverti(int jungtis_VALUE) throws Į_I_išimtis {
        try { return new DatagramSocket(jungtis_VALUE);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void siųsti(DatagramSocket dalyvis, int jungtis_VALUE, String Turinys_VALUE) throws Į_I_išimtis {
        try {
        siųsti(dalyvis, "127.0.0.1", jungtis_VALUE, Turinys_VALUE);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void siųsti(DatagramSocket dalyvis, String ADDRESS, int jungtis_VALUE, String Turinys_VALUE) throws Į_I_išimtis {
        try {
        byte[] baitas_VALUE = 문자.koduoti(Turinys_VALUE);
        dalyvis.send(new DatagramPacket(baitas_VALUE, baitas_VALUE.length, InetAddress.getByName(ADDRESS), jungtis_VALUE));
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static String gauti(DatagramSocket dalyvis) throws Į_I_išimtis {
        try {
        byte[] baitas_VALUE = new byte[512]; DatagramPacket paketų_kelio_schema = new DatagramPacket(baitas_VALUE, baitas_VALUE.length); dalyvis.receive(paketų_kelio_schema);
        byte[] REZULTATAS = new byte[paketų_kelio_schema.getLength()]; System.arraycopy(baitas_VALUE, 0, REZULTATAS, 0, REZULTATAS.length); return 문자.iššifruoti_duomenys(REZULTATAS);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void SKIRTASIS_LAIKAS(DatagramSocket dalyvis, int 밀리초) throws Į_I_išimtis {
        try { dalyvis.setSoTimeout(밀리초);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void Užverti(DatagramSocket dalyvis) { dalyvis.close(); }
}
