// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
import java.net.*;
public final class cxn_taşıma {
    private cxn_taşıma() {}
    public static cxn Aç(String ADRES, int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { return cxn.Aç(ADRES, bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static almak_taşımak 수신열기(int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { return almak_taşımak.Aç(bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static Socket Bağlan(String ADRES, int taşımak_değer) throws G_Ç_özel_durum {
        try { return new Socket(ADRES, taşımak_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static ServerSocket dinlemek_uç_nokta(int taşımak_değer) throws G_Ç_özel_durum {
        try { return new ServerSocket(taşımak_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static Socket almak(ServerSocket sunucu_değer) throws G_Ç_özel_durum {
        try { return sunucu_değer.accept();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
