// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 utent 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class fajl {
    private fajl() {}
    public static byte[] 바이트읽기(String isem) throws 입출력예외 {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(isem);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("fajl daqqas 제한"); 임시[수++] = (byte)VALUE; }
            byte[] miżura = new byte[수]; System.arraycopy(임시, 0, miżura, 0, 수); return miżura;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void kiteb_byte_VALUE(String isem, byte[] Kontenut_VALUE) throws 입출력예외 {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(isem);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Kontenut_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Kontenut_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static String 읽기(String isem) throws 입출력예외 {
        try { return 문자.ddeċifra_data(바이트읽기(isem));
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public static void kiteb(String isem, String Kontenut_VALUE) throws 입출력예외 {
        try { kiteb_byte_VALUE(isem, 문자.부호화(Kontenut_VALUE));
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
}
