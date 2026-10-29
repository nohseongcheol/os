// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static koneksi Buka(String surel, int nomor_port) throws I_O_pengecualian {
        try { return koneksi.Buka(surel, nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static terima_port 수신열기(int nomor_port) throws I_O_pengecualian {
        try { return terima_port.Buka(nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static Socket Sambung(String surel, int port_VALUE) throws I_O_pengecualian {
        try { return new Socket(surel, port_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static ServerSocket mendengarkan_peserta(int port_VALUE) throws I_O_pengecualian {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static Socket terima(ServerSocket server_VALUE) throws I_O_pengecualian {
        try { return server_VALUE.accept();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
