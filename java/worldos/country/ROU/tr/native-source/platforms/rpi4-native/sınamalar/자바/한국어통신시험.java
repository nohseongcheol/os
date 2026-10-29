// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.Öz.*;

/** 동일 바이트코드를 OpenJDK와 Öz JVM에서 실행하는 iletişim 계약 sınamalar. */
public class 한국어통신시험 {
    public static void main(String[] bağımsız_değişkenler) throws G_Ç_özel_durum {
        almak_taşımak taşımak_değer = cxn_taşıma.수신열기(0);
        cxn konuk_değer = cxn_taşıma.Aç("127.0.0.1", taşımak_değer.bağlantı_noktası_numarası());
        cxn sahip_tanımlayıcı = taşımak_değer.almak();
        konuk_değer.ZAMANAŞIMI(200); sahip_tanımlayıcı.ZAMANAŞIMI(200);
        검사.참인지(konuk_değer.연결됨() && !konuk_değer.bilgi_teknolojisi_kapalı(), "Bağlan Durum_değer");
        검사.참인지(sahip_tanımlayıcı.bağlantı_noktası_numarası() == konuk_değer.yerel_bağlantı_noktası_numarası(), "eş_değer bağlantı_noktası_numarası");
        검사.참인지(konuk_değer.bağlantı_noktası_numarası() == sahip_tanımlayıcı.yerel_bağlantı_noktası_numarası(), "yerel_Scope bağlantı_noktası_numarası");
        giriş_akışı artış_değer = sahip_tanımlayıcı.artış_değer(); çıkış_akışı çıktı_sayfa = konuk_değer.metinÇıktısı();
        byte[] belge = 문자.kodlamak("한글 akış_değer");
        çıktı_sayfa.Yazma(belge, 0, belge.length); çıktı_sayfa.내보내기();
        byte[] GETİRİ_SMS = new byte[belge.length];
        int 읽은수 = 0;
        while (읽은수 < GETİRİ_SMS.length) {
            int 더읽음 = artış_değer.Okuma(GETİRİ_SMS, 읽은수, GETİRİ_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 dosya 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.şifre_çözmek_veri(GETİRİ_SMS), "한글 akış_değer"), "부분 읽기와 Yazma");
        çıktı_sayfa.Yazma(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = artış_değer.Okuma(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "DİZİ_değer Okuma");
        if (첫읽기 == 1) 두바이트[1] = (byte)artış_değer.Okuma();
        검사.참인지(두바이트[1] == 18, "나머지 Okuma");
        sahip_tanımlayıcı.metinÇıktısı().Yazma(255);
        검사.참인지(konuk_değer.artış_değer().Okuma() == 255, "kodlama_değer 없는 한 bayt_değer");
        çıktı_sayfa.Kapat();
        검사.참인지(konuk_değer.bilgi_teknolojisi_kapalı() && artış_değer.Okuma() == -1, "닫기와 dosya 끝");
        artış_değer.Kapat(); 검사.참인지(sahip_tanımlayıcı.bilgi_teknolojisi_kapalı(), "artış_değer akış_değer Kapat");
        konuk_değer.Kapat(); sahip_tanımlayıcı.Kapat();
        taşımak_değer.ZAMANAŞIMI(15);
        boolean yürütme_ZAMANAŞIMI = false;
        try { taşımak_değer.almak(); } catch (bekle_ZAMANAŞIMI_özel_durum 예상한오류) { yürütme_ZAMANAŞIMI = true; }
        검사.참인지(yürütme_ZAMANAŞIMI, "almak_değer ZAMANAŞIMI");
        taşımak_değer.Kapat(); 검사.참인지(taşımak_değer.bilgi_teknolojisi_kapalı(), "almak_taşımak Kapat");
        veri_birimi_Kanal 받는곳 = veri_birimi_Kanal.Aç(0), 보내는곳 = veri_birimi_Kanal.Aç(0);
        받는곳.ZAMANAŞIMI(200);
        보내는곳.göndermek("127.0.0.1", 받는곳.bağlantı_noktası_numarası(), "veri_birimi 한글");
        검사.참인지(문자.같음(받는곳.almak(), "veri_birimi 한글"), "veri_birimi 송수신");
        보내는곳.Kapat(); 받는곳.Kapat();
        검사.참인지(보내는곳.bilgi_teknolojisi_kapalı() && 받는곳.bilgi_teknolojisi_kapalı(), "veri_birimi Kapat");
        metinÇıktısı.yazma_hat("Türkçe iletişim doğrulamak: Bağlan veri_birimi akış_değer yürütme_ZAMANAŞIMI Kapat");
    }
}
