// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.Öz.cxn;
import Türkçe.Öz.실행인수;
import Türkçe.Öz.veri_birimi_Kanal;
import Türkçe.Öz.문자;
import Türkçe.Öz.metinÇıktısı;
import Türkçe.Öz.검사;
import Türkçe.Öz.giriş_akışı;
import Türkçe.Öz.G_Ç_özel_durum;

public class AğÖrneği {
    public static void çalıştır() throws G_Ç_özel_durum {
        // konak: python3 araçlar/예제되돌림.py --tcp-port 9000 --udp-port 9001
        cxn Bağlan = cxn.Aç("10.0.2.2", 문자.ayrıştırmak_bilgi(실행인수.metin(0)));
        try {
            Bağlan.ZAMANAŞIMI(700);
            byte[] belge = 문자.kodlamak("JAVA TCP tr\n");
            Bağlan.metinÇıktısı().Yazma(belge);
            giriş_akışı artış_değer = Bağlan.artış_değer();
            for (int 수 = 0; 수 < 문자.bayt_BAĞ_DEĞ_SAY(belge); 수++) {
                검사.참인지(artış_değer.Okuma() == (belge[수] & 255), "TCP yanıt 불일치");
            }
        } finally { Bağlan.Kapat(); }
        veri_birimi_Kanal uç_nokta = veri_birimi_Kanal.Aç(0);
        try {
            uç_nokta.ZAMANAŞIMI(700);
            uç_nokta.göndermek("10.0.2.2", 문자.ayrıştırmak_bilgi(실행인수.metin(1)), "JAVA UDP tr");
            검사.참인지(문자.같음(uç_nokta.almak(), "JAVA UDP tr"), "UDP yanıt 불일치");
        } finally { uç_nokta.Kapat(); }
        metinÇıktısı.yazma_hat("JAVA 네트워크 doğrulamak: TCP UDP tr");
    }
}
