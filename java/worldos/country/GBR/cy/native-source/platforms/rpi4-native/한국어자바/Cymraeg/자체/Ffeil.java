// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 defnyddiwr 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Ffeil {
    private Ffeil() {}
    public static byte[] 바이트읽기(String Enw) throws I_O_eithriad {
        try {
        FileInputStream ffrwd_VALUE = new FileInputStream(Enw);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = ffrwd_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_eithriad("Ffeil Maint 제한"); 임시[수++] = (byte)VALUE; }
            byte[] mesur = new byte[수]; System.arraycopy(임시, 0, mesur, 0, 수); return mesur;
        } finally { ffrwd_VALUE.close(); }
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void ysgrifennu_beit_VALUE(String Enw, byte[] Cynnwys_VALUE) throws I_O_eithriad {
        try {
        FileOutputStream ffrwd_VALUE = new FileOutputStream(Enw);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Cynnwys_VALUE.length; Loop_INDEX++) ffrwd_VALUE.write(Cynnwys_VALUE[Loop_INDEX] & 255); } finally { ffrwd_VALUE.close(); }
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static String Darllen(String Enw) throws I_O_eithriad {
        try { return 문자.dadgryptio_data(바이트읽기(Enw));
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static void Ysgrifennu(String Enw, String Cynnwys_VALUE) throws I_O_eithriad {
        try { ysgrifennu_beit_VALUE(Enw, 문자.부호화(Cynnwys_VALUE));
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
