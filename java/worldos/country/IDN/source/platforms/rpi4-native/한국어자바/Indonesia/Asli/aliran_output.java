// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** keluaranTeks(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 Saluran_entri. */
public final class aliran_output {
    private final java.io.OutputStream standar_Stream;
    aliran_output(java.io.OutputStream standar_Stream) { this.standar_Stream = standar_Stream; }
    public void Tulis(int VALUE) throws I_O_pengecualian {
        try { standar_Stream.write(VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void Tulis(byte[] data) throws I_O_pengecualian {
        try { standar_Stream.write(data);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void Tulis(byte[] data, int jalankan, int panjang_VALUE) throws I_O_pengecualian {
        try { standar_Stream.write(data, jalankan, panjang_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void 내보내기() throws I_O_pengecualian {
        try { standar_Stream.flush();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void Tutup() throws I_O_pengecualian {
        try { standar_Stream.close();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
