// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** Sambung(連結)·Saluran_entri(通路): 상대와 이어진 TCP byte_VALUE 흐름의 peserta. */
public final class koneksi {
    private final java.net.Socket standar_pustaka_bridge;
    koneksi(java.net.Socket standar_pustaka_bridge) { this.standar_pustaka_bridge = standar_pustaka_bridge; }
    public static koneksi Buka(String surel, int nomor_port) throws I_O_pengecualian {
        try {
            return new koneksi(new java.net.Socket(surel, nomor_port));
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public aliran_input 입력() throws I_O_pengecualian {
        try { return new aliran_input(standar_pustaka_bridge.getInputStream());
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public aliran_output keluaranTeks() throws I_O_pengecualian {
        try { return new aliran_output(standar_pustaka_bridge.getOutputStream());
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { standar_pustaka_bridge.setSoTimeout(밀리초);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public int nomor_port() { return standar_pustaka_bridge.getPort(); }
    public int lokal_nomor_port() { return standar_pustaka_bridge.getLocalPort(); }
    public boolean 닫힘() { return standar_pustaka_bridge.isClosed(); }
    public boolean 연결됨() { return standar_pustaka_bridge.isConnected(); }
    public void Tutup() throws I_O_pengecualian {
        try { standar_pustaka_bridge.close();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
