// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ruang_pengguna 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fail {
    private Fail() {}
    public static byte[] 바이트읽기(String Nama) throws I_O_pengecualian {
        try {
        FileInputStream strim_VALUE = new FileInputStream(Nama);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = strim_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_pengecualian("Fail Saiz 제한"); 임시[수++] = (byte)VALUE; }
            byte[] ukuran = new byte[수]; System.arraycopy(임시, 0, ukuran, 0, 수); return ukuran;
        } finally { strim_VALUE.close(); }
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void tulis_bait_VALUE(String Nama, byte[] Kandungan_VALUE) throws I_O_pengecualian {
        try {
        FileOutputStream strim_VALUE = new FileOutputStream(Nama);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Kandungan_VALUE.length; Loop_INDEX++) strim_VALUE.write(Kandungan_VALUE[Loop_INDEX] & 255); } finally { strim_VALUE.close(); }
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static String Baca(String Nama) throws I_O_pengecualian {
        try { return 문자.nyahsulit_data(바이트읽기(Nama));
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static void Tulis(String Nama, String Kandungan_VALUE) throws I_O_pengecualian {
        try { tulis_bait_VALUE(Nama, 문자.부호화(Kandungan_VALUE));
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
