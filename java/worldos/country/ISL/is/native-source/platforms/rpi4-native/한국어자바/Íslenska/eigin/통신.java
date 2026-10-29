// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 tölustafur_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Opna(int gátt_VALUE) throws I_Ú_undantekning {
        try { return new DatagramSocket(gátt_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void senda(DatagramSocket endastöð, int gátt_VALUE, String Efni_VALUE) throws I_Ú_undantekning {
        try {
        senda(endastöð, "127.0.0.1", gátt_VALUE, Efni_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void senda(DatagramSocket endastöð, String slóð, int gátt_VALUE, String Efni_VALUE) throws I_Ú_undantekning {
        try {
        byte[] bæti_VALUE = 문자.부호화(Efni_VALUE);
        endastöð.send(new DatagramPacket(bæti_VALUE, bæti_VALUE.length, InetAddress.getByName(slóð), gátt_VALUE));
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static String 받기(DatagramSocket endastöð) throws I_Ú_undantekning {
        try {
        byte[] bæti_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bæti_VALUE, bæti_VALUE.length); endastöð.receive(전문);
        byte[] NIÐURSTAÐA = new byte[전문.getLength()]; System.arraycopy(bæti_VALUE, 0, NIÐURSTAÐA, 0, NIÐURSTAÐA.length); return 문자.dulráða_gögn(NIÐURSTAÐA);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void TIMEOUT(DatagramSocket endastöð, int 밀리초) throws I_Ú_undantekning {
        try { endastöð.setSoTimeout(밀리초);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void Loka(DatagramSocket endastöð) { endastöð.close(); }
}
