// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ulanyjy 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Faýl {
    private Faýl() {}
    public static byte[] 바이트읽기(String Ad) throws 입출력예외 {
        try {
        FileInputStream Stream_baha = new FileInputStream(Ad);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, baha;
            while ((baha = Stream_baha.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Faýl Ululyk 제한"); 임시[수++] = (byte)baha; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_baha.close(); }
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void ýaz_baýt_baha(String Ad, byte[] Mazmun_baha) throws 입출력예외 {
        try {
        FileOutputStream Stream_baha = new FileOutputStream(Ad);
        try { for (int sikl_indeks = 0; sikl_indeks < Mazmun_baha.length; sikl_indeks++) Stream_baha.write(Mazmun_baha[sikl_indeks] & 255); } finally { Stream_baha.close(); }
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static String Oka(String Ad) throws 입출력예외 {
        try { return 문자.koddan_aç_maglumat(바이트읽기(Ad));
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public static void Ýaz(String Ad, String Mazmun_baha) throws 입출력예외 {
        try { ýaz_baýt_baha(Ad, 문자.부호화(Mazmun_baha));
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
}
