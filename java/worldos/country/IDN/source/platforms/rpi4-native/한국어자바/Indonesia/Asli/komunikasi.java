// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** komunikasi(通信): IPv4 UDP 전문. eksternal_VALUE 주소는 angka_VALUE 주소를 사용한다. */
public final class komunikasi {
    private komunikasi() {}
    public static DatagramSocket Buka(int port_VALUE) throws I_O_pengecualian {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void kirim(DatagramSocket peserta, int port_VALUE, String Isi_VALUE) throws I_O_pengecualian {
        try {
        kirim(peserta, "127.0.0.1", port_VALUE, Isi_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void kirim(DatagramSocket peserta, String surel, int port_VALUE, String Isi_VALUE) throws I_O_pengecualian {
        try {
        byte[] byte_VALUE = 문자.부호화(Isi_VALUE);
        peserta.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(surel), port_VALUE));
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static String terima(DatagramSocket peserta) throws I_O_pengecualian {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALUE, byte_VALUE.length); peserta.receive(전문);
        byte[] hasil = new byte[전문.getLength()]; System.arraycopy(byte_VALUE, 0, hasil, 0, hasil.length); return 문자.dekripsikan_data(hasil);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void TIMEOUT(DatagramSocket peserta, int 밀리초) throws I_O_pengecualian {
        try { peserta.setSoTimeout(밀리초);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void Tutup(DatagramSocket peserta) { peserta.close(); }
}
