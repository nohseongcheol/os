// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** comunicazione(通信): IPv4 UDP datagramma. esterno_VALORE 주소는 cifra_VALORE 주소를 사용한다. */
public final class comunicazione {
    private comunicazione() {}
    public static DatagramSocket Apri(int porta_VALORE) throws I_O_eccezione {
        try { return new DatagramSocket(porta_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void inviare(DatagramSocket endpoint, int porta_VALORE, String Contenuto_VALORE) throws I_O_eccezione {
        try {
        inviare(endpoint, "127.0.0.1", porta_VALORE, Contenuto_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void inviare(DatagramSocket endpoint, String e_mail, int porta_VALORE, String Contenuto_VALORE) throws I_O_eccezione {
        try {
        byte[] byte_VALORE = 문자.codificare(Contenuto_VALORE);
        endpoint.send(new DatagramPacket(byte_VALORE, byte_VALORE.length, InetAddress.getByName(e_mail), porta_VALORE));
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static String ricevere(DatagramSocket endpoint) throws I_O_eccezione {
        try {
        byte[] byte_VALORE = new byte[512]; DatagramPacket datagramma = new DatagramPacket(byte_VALORE, byte_VALORE.length); endpoint.receive(datagramma);
        byte[] risultato = new byte[datagramma.getLength()]; System.arraycopy(byte_VALORE, 0, risultato, 0, risultato.length); return 문자.decifrare_dati(risultato);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void TIMEOUT(DatagramSocket endpoint, int 밀리초) throws I_O_eccezione {
        try { endpoint.setSoTimeout(밀리초);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void Chiudi(DatagramSocket endpoint) { endpoint.close(); }
}
