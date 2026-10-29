// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** Bağlan(連結)·Kanal_girdi(通路): 상대와 이어진 TCP bayt_değer 흐름의 uç_nokta. */
public final class cxn {
    private final java.net.Socket Standart_kitaplık_köprü;
    cxn(java.net.Socket Standart_kitaplık_köprü) { this.Standart_kitaplık_köprü = Standart_kitaplık_köprü; }
    public static cxn Aç(String ADRES, int bağlantı_noktası_numarası) throws G_Ç_özel_durum {
        try {
            return new cxn(new java.net.Socket(ADRES, bağlantı_noktası_numarası));
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public giriş_akışı artış_değer() throws G_Ç_özel_durum {
        try { return new giriş_akışı(Standart_kitaplık_köprü.getInputStream());
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public çıkış_akışı metinÇıktısı() throws G_Ç_özel_durum {
        try { return new çıkış_akışı(Standart_kitaplık_köprü.getOutputStream());
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void ZAMANAŞIMI(int 밀리초) throws G_Ç_özel_durum {
        try { Standart_kitaplık_köprü.setSoTimeout(밀리초);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public int bağlantı_noktası_numarası() { return Standart_kitaplık_köprü.getPort(); }
    public int yerel_bağlantı_noktası_numarası() { return Standart_kitaplık_köprü.getLocalPort(); }
    public boolean bilgi_teknolojisi_kapalı() { return Standart_kitaplık_köprü.isClosed(); }
    public boolean 연결됨() { return Standart_kitaplık_köprü.isConnected(); }
    public void Kapat() throws G_Ç_özel_durum {
        try { Standart_kitaplık_köprü.close();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
