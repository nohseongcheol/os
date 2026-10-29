// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** almak_değer(受信)·taşımak_değer(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class almak_taşımak {
    private final java.net.ServerSocket Standart_taşımak;
    private almak_taşımak(int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { Standart_taşımak = new java.net.ServerSocket(bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static almak_taşımak Aç(int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try { return new almak_taşımak(bağlantı_noktası_numarası);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public cxn almak() throws G_Ç_özel_durum {
        try { return new cxn(Standart_taşımak.accept());
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public int bağlantı_noktası_numarası() { return Standart_taşımak.getLocalPort(); }
    public void ZAMANAŞIMI(int 밀리초) throws G_Ç_özel_durum {
        try { Standart_taşımak.setSoTimeout(밀리초);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public boolean bilgi_teknolojisi_kapalı() { return Standart_taşımak.isClosed(); }
    public void Kapat() throws G_Ç_özel_durum {
        try { Standart_taşımak.close();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
