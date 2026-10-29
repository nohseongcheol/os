// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** artış_değer(入力)과 akış_değer: 순서대로 들어오는 바이트를 읽는 Kanal_girdi. */
public final class giriş_akışı {
    private final java.io.InputStream Standart_akış;
    giriş_akışı(java.io.InputStream Standart_akış) { this.Standart_akış = Standart_akış; }
    public int Okuma() throws G_Ç_özel_durum {
        try { return Standart_akış.read();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public int Okuma(byte[] veri) throws G_Ç_özel_durum {
        try { return Standart_akış.read(veri);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public int Okuma(byte[] veri, int çalıştır, int süre_değer) throws G_Ç_özel_durum {
        try { return Standart_akış.read(veri, çalıştır, süre_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void Kapat() throws G_Ç_özel_durum {
        try { Standart_akış.close();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
