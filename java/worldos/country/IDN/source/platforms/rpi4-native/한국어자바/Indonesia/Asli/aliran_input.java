// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 Saluran_entri. */
public final class aliran_input {
    private final java.io.InputStream standar_Stream;
    aliran_input(java.io.InputStream standar_Stream) { this.standar_Stream = standar_Stream; }
    public int Baca() throws I_O_pengecualian {
        try { return standar_Stream.read();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public int Baca(byte[] data) throws I_O_pengecualian {
        try { return standar_Stream.read(data);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public int Baca(byte[] data, int jalankan, int panjang_VALUE) throws I_O_pengecualian {
        try { return standar_Stream.read(data, jalankan, panjang_VALUE);
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public void Tutup() throws I_O_pengecualian {
        try { standar_Stream.close();
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
