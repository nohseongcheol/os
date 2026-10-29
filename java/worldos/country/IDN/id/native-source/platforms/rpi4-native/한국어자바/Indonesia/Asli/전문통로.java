// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** 전문(電文)·Saluran_entri(通路): 경계를 가진 UDP 자료를 주고받는 peserta. */
public final class 전문통로 {
    private final java.net.DatagramSocket standar_peserta;
    private 전문통로(int nomor_port) throws I_O_pengecualian {
        try { standar_peserta = komunikasi.Buka(nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static 전문통로 Buka(int nomor_port) throws I_O_pengecualian {
        try { return new 전문통로(nomor_port);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void kirim(String surel, int nomor_port, String data) throws I_O_pengecualian {
        try { komunikasi.kirim(standar_peserta, surel, nomor_port, data);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public String terima() throws I_O_pengecualian {
        try { return komunikasi.terima(standar_peserta);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { komunikasi.TIMEOUT(standar_peserta, 밀리초);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public int nomor_port() { return standar_peserta.getLocalPort(); }
    public boolean 닫힘() { return standar_peserta.isClosed(); }
    public void Tutup() { komunikasi.Tutup(standar_peserta); }
}
