// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 foydalanuvchi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fayl {
    private Fayl() {}
    public static byte[] 바이트읽기(String Nomi) throws I_O_istisno {
        try {
        FileInputStream oqim_VALUE = new FileInputStream(Nomi);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = oqim_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_istisno("Fayl Hajmi 제한"); 임시[수++] = (byte)VALUE; }
            byte[] o_lchov = new byte[수]; System.arraycopy(임시, 0, o_lchov, 0, 수); return o_lchov;
        } finally { oqim_VALUE.close(); }
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void yozmoq_bayt_VALUE(String Nomi, byte[] tarkib_VALUE) throws I_O_istisno {
        try {
        FileOutputStream oqim_VALUE = new FileOutputStream(Nomi);
        try { for (int Loop_INDEX = 0; Loop_INDEX < tarkib_VALUE.length; Loop_INDEX++) oqim_VALUE.write(tarkib_VALUE[Loop_INDEX] & 255); } finally { oqim_VALUE.close(); }
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static String Oʻqish(String Nomi) throws I_O_istisno {
        try { return 문자.shifrsizlantirish_ma_lumotlar(바이트읽기(Nomi));
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void Yozish(String Nomi, String tarkib_VALUE) throws I_O_istisno {
        try { yozmoq_bayt_VALUE(Nomi, 문자.부호화(tarkib_VALUE));
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
