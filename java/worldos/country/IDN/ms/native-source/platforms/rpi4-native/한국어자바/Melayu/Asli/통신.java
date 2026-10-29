// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 digit_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Buka(int port_VALUE) throws I_O_pengecualian {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void e_mel_9aee63bd(DatagramSocket peserta, int port_VALUE, String Kandungan_VALUE) throws I_O_pengecualian {
        try {
        e_mel_9aee63bd(peserta, "127.0.0.1", port_VALUE, Kandungan_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void e_mel_9aee63bd(DatagramSocket peserta, String e_mel, int port_VALUE, String Kandungan_VALUE) throws I_O_pengecualian {
        try {
        byte[] bait_VALUE = 문자.부호화(Kandungan_VALUE);
        peserta.send(new DatagramPacket(bait_VALUE, bait_VALUE.length, InetAddress.getByName(e_mel), port_VALUE));
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static String 받기(DatagramSocket peserta) throws I_O_pengecualian {
        try {
        byte[] bait_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bait_VALUE, bait_VALUE.length); peserta.receive(전문);
        byte[] ukuran = new byte[전문.getLength()]; System.arraycopy(bait_VALUE, 0, ukuran, 0, ukuran.length); return 문자.nyahsulit_data(ukuran);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void TIMEOUT(DatagramSocket peserta, int 밀리초) throws I_O_pengecualian {
        try { peserta.setSoTimeout(밀리초);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void Tutup(DatagramSocket peserta) { peserta.close(); }
}
