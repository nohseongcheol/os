// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** iletişim(通信): IPv4 UDP veri_birimi. dış_değer 주소는 rakam_değer 주소를 사용한다. */
public final class iletişim {
    private iletişim() {}
    public static DatagramSocket Aç(int taşımak_değer) throws G_Ç_özel_durum {
        try { return new DatagramSocket(taşımak_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void göndermek(DatagramSocket uç_nokta, int taşımak_değer, String içerik_değer) throws G_Ç_özel_durum {
        try {
        göndermek(uç_nokta, "127.0.0.1", taşımak_değer, içerik_değer);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void göndermek(DatagramSocket uç_nokta, String ADRES, int taşımak_değer, String içerik_değer) throws G_Ç_özel_durum {
        try {
        byte[] bayt_değer = 문자.kodlamak(içerik_değer);
        uç_nokta.send(new DatagramPacket(bayt_değer, bayt_değer.length, InetAddress.getByName(ADRES), taşımak_değer));
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static String almak(DatagramSocket uç_nokta) throws G_Ç_özel_durum {
        try {
        byte[] bayt_değer = new byte[512]; DatagramPacket veri_birimi = new DatagramPacket(bayt_değer, bayt_değer.length); uç_nokta.receive(veri_birimi);
        byte[] sonuç = new byte[veri_birimi.getLength()]; System.arraycopy(bayt_değer, 0, sonuç, 0, sonuç.length); return 문자.şifre_çözmek_veri(sonuç);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void ZAMANAŞIMI(DatagramSocket uç_nokta, int 밀리초) throws G_Ç_özel_durum {
        try { uç_nokta.setSoTimeout(밀리초);
        } catch (java.io.IOException hata) { throw ÇEVİR_özel_durum.G_Ç(hata); }
        catch (RuntimeException hata) { throw ÇEVİR_özel_durum.yürütmek_komut(hata); }
    }
    public static void Kapat(DatagramSocket uç_nokta) { uç_nokta.close(); }
}
