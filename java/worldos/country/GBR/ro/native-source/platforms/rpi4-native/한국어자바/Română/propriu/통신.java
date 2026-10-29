// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP diagramă_informații. extern_VALUE 주소는 cifră_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Deschide(int muta_VALUE) throws I_O_excepție {
        try { return new DatagramSocket(muta_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void trimite(DatagramSocket participant, int muta_VALUE, String Conținut_VALUE) throws I_O_excepție {
        try {
        trimite(participant, "127.0.0.1", muta_VALUE, Conținut_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void trimite(DatagramSocket participant, String adresa, int muta_VALUE, String Conținut_VALUE) throws I_O_excepție {
        try {
        byte[] byte_VALUE = 문자.codifica(Conținut_VALUE);
        participant.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(adresa), muta_VALUE));
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static String primi(DatagramSocket participant) throws I_O_excepție {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket diagramă_informații = new DatagramPacket(byte_VALUE, byte_VALUE.length); participant.receive(diagramă_informații);
        byte[] KR = new byte[diagramă_informații.getLength()]; System.arraycopy(byte_VALUE, 0, KR, 0, KR.length); return 문자.decripta_date(KR);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void TIMEOUT(DatagramSocket participant, int 밀리초) throws I_O_excepție {
        try { participant.setSoTimeout(밀리초);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void Închide(DatagramSocket participant) { participant.close(); }
}
