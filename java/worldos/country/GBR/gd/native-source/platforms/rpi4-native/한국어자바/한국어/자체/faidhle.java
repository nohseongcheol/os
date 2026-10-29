// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 cleachdaiche 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class faidhle {
    private faidhle() {}
    public static byte[] 바이트읽기(String Ainm) throws 입출력예외 {
        try {
        FileInputStream sruth_VALUE = new FileInputStream(Ainm);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = sruth_VALUE.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("faidhle atharraich_am_meud 제한"); 임시[수++] = (byte)VALUE; }
            byte[] tomhas = new byte[수]; System.arraycopy(임시, 0, tomhas, 0, 수); return tomhas;
        } finally { sruth_VALUE.close(); }
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void sgrìobh_baidht_VALUE(String Ainm, byte[] susbaint_VALUE) throws 입출력예외 {
        try {
        FileOutputStream sruth_VALUE = new FileOutputStream(Ainm);
        try { for (int lùb_INDEX = 0; lùb_INDEX < susbaint_VALUE.length; lùb_INDEX++) sruth_VALUE.write(susbaint_VALUE[lùb_INDEX] & 255); } finally { sruth_VALUE.close(); }
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static String 읽기(String Ainm) throws 입출력예외 {
        try { return 문자.dì_chrioptaich_dàta(바이트읽기(Ainm));
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static void sgrìobh(String Ainm, String susbaint_VALUE) throws 입출력예외 {
        try { sgrìobh_baidht_VALUE(Ainm, 문자.부호화(susbaint_VALUE));
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
}
