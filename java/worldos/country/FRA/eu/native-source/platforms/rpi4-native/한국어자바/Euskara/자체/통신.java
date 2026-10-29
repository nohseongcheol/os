// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 digitu_balio 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ireki(int ataka_balio) throws S_I_salbuespen {
        try { return new DatagramSocket(ataka_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void bidali(DatagramSocket amaiera_puntu, int ataka_balio, String eduki_balio) throws S_I_salbuespen {
        try {
        bidali(amaiera_puntu, "127.0.0.1", ataka_balio, eduki_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void bidali(DatagramSocket amaiera_puntu, String helbide, int ataka_balio, String eduki_balio) throws S_I_salbuespen {
        try {
        byte[] byte_balio = 문자.부호화(eduki_balio);
        amaiera_puntu.send(new DatagramPacket(byte_balio, byte_balio.length, InetAddress.getByName(helbide), ataka_balio));
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static String 받기(DatagramSocket amaiera_puntu) throws S_I_salbuespen {
        try {
        byte[] byte_balio = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_balio, byte_balio.length); amaiera_puntu.receive(전문);
        byte[] EMAITZA = new byte[전문.getLength()]; System.arraycopy(byte_balio, 0, EMAITZA, 0, EMAITZA.length); return 문자.desenkriptatu_datuak(EMAITZA);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void DENBORA_MUGA(DatagramSocket amaiera_puntu, int 밀리초) throws S_I_salbuespen {
        try { amaiera_puntu.setSoTimeout(밀리초);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void Itxi(DatagramSocket amaiera_puntu) { amaiera_puntu.close(); }
}
