// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ruang_pengguna 용어를 보존한다. saat_ini_item 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class berkas {
    private berkas() {}
    public static byte[] 바이트읽기(String Nama_2) throws I_O_pengecualian {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Nama_2);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_pengecualian("berkas Ukuran 제한"); 임시[수++] = (byte)VALUE; }
            byte[] hasil = new byte[수]; System.arraycopy(임시, 0, hasil, 0, 수); return hasil;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void tulis_byte_VALUE(String Nama_2, byte[] Isi_VALUE) throws I_O_pengecualian {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Nama_2);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Isi_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Isi_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static String Baca(String Nama_2) throws I_O_pengecualian {
        try { return 문자.dekripsikan_data(바이트읽기(Nama_2));
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
    public static void Tulis(String Nama_2, String Isi_VALUE) throws I_O_pengecualian {
        try { tulis_byte_VALUE(Nama_2, 문자.부호화(Isi_VALUE));
        } catch (java.io.IOException galat) { throw CONVERT_pengecualian.I_O(galat); }
        catch (RuntimeException galat) { throw CONVERT_pengecualian.Jalankan_perintah(galat); }
    }
}
