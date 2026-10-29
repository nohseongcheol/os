// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 kullanıcı_alanı 용어를 보존한다. geçerli_öğe 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class dosya {
    private dosya() {}
    public static byte[] 바이트읽기(String İsim) throws G_Ç_özel_durum {
        try {
        FileInputStream akış_değer = new FileInputStream(İsim);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, değer;
            while ((değer = akış_değer.read()) != -1) { if (수 == 임시.length) throw new G_Ç_özel_durum("dosya Boyut 제한"); 임시[수++] = (byte)değer; }
            byte[] sonuç = new byte[수]; System.arraycopy(임시, 0, sonuç, 0, 수); return sonuç;
        } finally { akış_değer.close(); }
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void yazma_bayt_değer(String İsim, byte[] içerik_değer) throws G_Ç_özel_durum {
        try {
        FileOutputStream akış_değer = new FileOutputStream(İsim);
        try { for (int Loop_Dizin = 0; Loop_Dizin < içerik_değer.length; Loop_Dizin++) akış_değer.write(içerik_değer[Loop_Dizin] & 255); } finally { akış_değer.close(); }
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static String Okuma(String İsim) throws G_Ç_özel_durum {
        try { return 문자.şifre_çözmek_veri(바이트읽기(İsim));
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void Yazma(String İsim, String içerik_değer) throws G_Ç_özel_durum {
        try { yazma_bayt_değer(İsim, 문자.kodlamak(içerik_değer));
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
