// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** metinÇıktısı(出力)과 akış_değer: 순서를 보존해 내보내는 바이트의 Kanal_girdi. */
public final class çıkış_akışı {
    private final java.io.OutputStream Standart_akış;
    çıkış_akışı(java.io.OutputStream Standart_akış) { this.Standart_akış = Standart_akış; }
    public void Yazma(int değer) throws G_Ç_özel_durum {
        try { Standart_akış.write(değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void Yazma(byte[] veri) throws G_Ç_özel_durum {
        try { Standart_akış.write(veri);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void Yazma(byte[] veri, int çalıştır, int süre_değer) throws G_Ç_özel_durum {
        try { Standart_akış.write(veri, çalıştır, süre_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void 내보내기() throws G_Ç_özel_durum {
        try { Standart_akış.flush();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public void Kapat() throws G_Ç_özel_durum {
        try { Standart_akış.close();
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
}
