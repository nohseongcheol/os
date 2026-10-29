// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** veri_birimi(電文)·Kanal_girdi(通路): 경계를 가진 UDP 자료를 주고받는 uç_nokta. */
public final class veri_birimi_Kanal {
    private final java.net.DatagramSocket Standart_uç_nokta;
    private veri_birimi_Kanal(int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { Standart_uç_nokta = iletişim.Aç(bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static veri_birimi_Kanal Aç(int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { return new veri_birimi_Kanal(bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void göndermek(String ADRES, int bağlantı_noktası_numarası, String veri) throws G_Ç_özel_durum {
        try { iletişim.göndermek(Standart_uç_nokta, ADRES, bağlantı_noktası_numarası, veri);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public String almak() throws G_Ç_özel_durum {
        try { return iletişim.almak(Standart_uç_nokta);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void ZAMANAŞIMI(int 밀리초) throws G_Ç_özel_durum {
        try { iletişim.ZAMANAŞIMI(Standart_uç_nokta, 밀리초);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public int bağlantı_noktası_numarası() { return Standart_uç_nokta.getLocalPort(); }
    public boolean bilgi_teknolojisi_kapalı() { return Standart_uç_nokta.isClosed(); }
    public void Kapat() { iletişim.Kapat(Standart_uç_nokta); }
}
