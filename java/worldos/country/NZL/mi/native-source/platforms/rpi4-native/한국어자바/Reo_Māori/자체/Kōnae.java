// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 kaiwhakamahi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Kōnae {
    private Kōnae() {}
    public static byte[] 바이트읽기(String Ingoa) throws 입출력예외 {
        try {
        FileInputStream roma_uara = new FileInputStream(Ingoa);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, uara;
            while ((uara = roma_uara.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Kōnae rahi 제한"); 임시[수++] = (byte)uara; }
            byte[] mēhua = new byte[수]; System.arraycopy(임시, 0, mēhua, 0, 수); return mēhua;
        } finally { roma_uara.close(); }
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void tuhi_paita_uara(String Ingoa, byte[] Ihirangi_uara) throws 입출력예외 {
        try {
        FileOutputStream roma_uara = new FileOutputStream(Ingoa);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Ihirangi_uara.length; Loop_INDEX++) roma_uara.write(Ihirangi_uara[Loop_INDEX] & 255); } finally { roma_uara.close(); }
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static String Pānuitia(String Ingoa) throws 입출력예외 {
        try { return 문자.wetemuna_raraunga(바이트읽기(Ingoa));
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static void Tuhia(String Ingoa, String Ihirangi_uara) throws 입출력예외 {
        try { tuhi_paita_uara(Ingoa, 문자.부호화(Ihirangi_uara));
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
}
