// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 digid_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Agor(int porth_VALUE) throws I_O_eithriad {
        try { return new DatagramSocket(porth_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void anfon(DatagramSocket 종단, int porth_VALUE, String Cynnwys_VALUE) throws I_O_eithriad {
        try {
        anfon(종단, "127.0.0.1", porth_VALUE, Cynnwys_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void anfon(DatagramSocket 종단, String ADDRESS, int porth_VALUE, String Cynnwys_VALUE) throws I_O_eithriad {
        try {
        byte[] beit_VALUE = 문자.부호화(Cynnwys_VALUE);
        종단.send(new DatagramPacket(beit_VALUE, beit_VALUE.length, InetAddress.getByName(ADDRESS), porth_VALUE));
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_eithriad {
        try {
        byte[] beit_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(beit_VALUE, beit_VALUE.length); 종단.receive(전문);
        byte[] mesur = new byte[전문.getLength()]; System.arraycopy(beit_VALUE, 0, mesur, 0, mesur.length); return 문자.dadgryptio_data(mesur);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws I_O_eithriad {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void Cau(DatagramSocket 종단) { 종단.close(); }
}
