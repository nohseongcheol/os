// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 syfer_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket skep(int ombou_VALUE) throws I_O_uitsondering {
        try { return new DatagramSocket(ombou_VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void e_pos(DatagramSocket 종단, int ombou_VALUE, String Inhoud_VALUE) throws I_O_uitsondering {
        try {
        e_pos(종단, "127.0.0.1", ombou_VALUE, Inhoud_VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void e_pos(DatagramSocket 종단, String adres, int ombou_VALUE, String Inhoud_VALUE) throws I_O_uitsondering {
        try {
        byte[] greep_VALUE = 문자.부호화(Inhoud_VALUE);
        종단.send(new DatagramPacket(greep_VALUE, greep_VALUE.length, InetAddress.getByName(adres), ombou_VALUE));
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_uitsondering {
        try {
        byte[] greep_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(greep_VALUE, greep_VALUE.length); 종단.receive(전문);
        byte[] maatreël = new byte[전문.getLength()]; System.arraycopy(greep_VALUE, 0, maatreël, 0, maatreël.length); return 문자.dekripteer_data(maatreël);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void UITTELLING(DatagramSocket 종단, int 밀리초) throws I_O_uitsondering {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void Sluit(DatagramSocket 종단) { 종단.close(); }
}
