// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** communicatie(通信): IPv4 UDP datagram. extern_WAARDE 주소는 cijfer_WAARDE 주소를 사용한다. */
public final class communicatie {
    private communicatie() {}
    public static DatagramSocket Openen(int poort_WAARDE) throws I_O_uitzondering {
        try { return new DatagramSocket(poort_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void e_mailen(DatagramSocket eindpunt, int poort_WAARDE, String Inhoud_WAARDE) throws I_O_uitzondering {
        try {
        e_mailen(eindpunt, "127.0.0.1", poort_WAARDE, Inhoud_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void e_mailen(DatagramSocket eindpunt, String ADRES, int poort_WAARDE, String Inhoud_WAARDE) throws I_O_uitzondering {
        try {
        byte[] byte_WAARDE = 문자.coderen(Inhoud_WAARDE);
        eindpunt.send(new DatagramPacket(byte_WAARDE, byte_WAARDE.length, InetAddress.getByName(ADRES), poort_WAARDE));
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static String ontvangen(DatagramSocket eindpunt) throws I_O_uitzondering {
        try {
        byte[] byte_WAARDE = new byte[512]; DatagramPacket datagram = new DatagramPacket(byte_WAARDE, byte_WAARDE.length); eindpunt.receive(datagram);
        byte[] resultaat = new byte[datagram.getLength()]; System.arraycopy(byte_WAARDE, 0, resultaat, 0, resultaat.length); return 문자.ontsleutelen_gegevens(resultaat);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void TIMEOUT(DatagramSocket eindpunt, int 밀리초) throws I_O_uitzondering {
        try { eindpunt.setSoTimeout(밀리초);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void Sluiten(DatagramSocket eindpunt) { eindpunt.close(); }
}
