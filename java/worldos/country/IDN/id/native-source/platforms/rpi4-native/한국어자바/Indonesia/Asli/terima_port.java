// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** terima_VALUE(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class terima_port {
    private final java.net.ServerSocket standar_port;
    private terima_port(int nomor_port) throws I_O_pengecualian {
        try { standar_port = new java.net.ServerSocket(nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static terima_port Buka(int nomor_port) throws I_O_pengecualian {
        try { return new terima_port(nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public koneksi terima() throws I_O_pengecualian {
        try { return new koneksi(standar_port.accept());
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public int nomor_port() { return standar_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { standar_port.setSoTimeout(밀리초);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public boolean 닫힘() { return standar_port.isClosed(); }
    public void Tutup() throws I_O_pengecualian {
        try { standar_port.close();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
