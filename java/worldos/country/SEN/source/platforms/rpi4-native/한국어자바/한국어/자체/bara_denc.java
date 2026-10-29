// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 kiy_jariñoo_internet 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class bara_denc {
    private bara_denc() {}
    public static byte[] 바이트읽기(String tur_253d1510) throws 입출력예외 {
        try {
        FileInputStream dawal_xëyma = new FileInputStream(tur_253d1510);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, xëyma;
            while ((xëyma = dawal_xëyma.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("bara_denc tolluwaay 제한"); 임시[수++] = (byte)xëyma; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { dawal_xëyma.close(); }
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void biir_okte_xëyma(String tur_253d1510, byte[] Këmb_xëyma) throws 입출력예외 {
        try {
        FileOutputStream dawal_xëyma = new FileOutputStream(tur_253d1510);
        try { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Këmb_xëyma.length; wërngël_àlluwa_tur++) dawal_xëyma.write(Këmb_xëyma[wërngël_àlluwa_tur] & 255); } finally { dawal_xëyma.close(); }
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static String 읽기(String tur_253d1510) throws 입출력예외 {
        try { return 문자.fecci_mbir(바이트읽기(tur_253d1510));
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static void biir(String tur_253d1510, String Këmb_xëyma) throws 입출력예외 {
        try { biir_okte_xëyma(tur_253d1510, 문자.부호화(Këmb_xëyma));
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
}
