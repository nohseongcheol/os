// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** fiili_veri Java sözleşme_değeri 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_test {
    static int 횟수 = 0;
    static void doğrulamak(boolean değer) { if (!değer) throw new AssertionError("case " + 횟수); 횟수++; }
    static int sağlama_toplamı(int[] değer, int çalıştır, int süre_değer, int başlangıç_durumu) {
        int SUM_değer = başlangıç_durumu;
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) SUM_değer += değer[çalıştır + Dizin] << ((Dizin & 1) == 0 ? 8 : 0);
        SUM_değer = (SUM_değer & 65535) + (SUM_değer >>> 16);
        SUM_değer = (SUM_değer & 65535) + (SUM_değer >>> 16);
        return ~SUM_değer & 65535;
    }
    static void Hazırlan(int süre_değer) {
        ağ_Yığın.TEMİZ_işlem();
        doğrulamak(ağ_Yığın.Aç(5000) == 3);
        int[] kare_Dizin = ağ_Yığın.artış_kare;
        Arrays.fill(kare_Dizin, 0);
        for (int Dizin = 0; Dizin < 6; Dizin++) kare_Dizin[Dizin] = ağ_sürücü.cihaz_ADRES[Dizin];
        ağ_Yığın.넣기16(kare_Dizin, 12, 0x0800);
        kare_Dizin[14] = 0x45; kare_Dizin[22] = 64; kare_Dizin[23] = 17;
        ağ_Yığın.넣기16(kare_Dizin, 16, 28 + süre_değer);
        ağ_Yığın.넣기32(kare_Dizin, 26, 0x0a000202); ağ_Yığın.넣기32(kare_Dizin, 30, ağ_Yığın.내주소);
        ağ_Yığın.넣기16(kare_Dizin, 34, 4321); ağ_Yığın.넣기16(kare_Dizin, 36, 5000); ağ_Yığın.넣기16(kare_Dizin, 38, süre_değer + 8);
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) kare_Dizin[42 + Dizin] = Dizin & 255;
        küme_sağlama_toplamı(süre_değer);
    }
    static void küme_sağlama_toplamı(int süre_değer) {
        int[] kare_Dizin = ağ_Yığın.artış_kare;
        ağ_Yığın.넣기16(kare_Dizin, 24, 0); ağ_Yığın.넣기16(kare_Dizin, 40, 0);
        ağ_Yığın.넣기16(kare_Dizin, 24, sağlama_toplamı(kare_Dizin, 14, 20, 0));
        int başlangıç_durumu = ağ_Yığın.가상머리합(ağ_Yığın.bilgi_32(kare_Dizin, 26), ağ_Yığın.내주소, süre_değer + 8);
        int SUM_değer = sağlama_toplamı(kare_Dizin, 34, süre_değer + 8, başlangıç_durumu);
        ağ_Yığın.넣기16(kare_Dizin, 40, SUM_değer == 0 ? 65535 : SUM_değer);
    }
    static void reddetmek_değer(int süre_değer) { ağ_Yığın.işlem_kare(süre_değer); doğrulamak(ağ_Yığın.GETİRİ_süre[0] == -1); }
    public static void main(String[] bağımsız_değişkenler) {
        for (int süre_değer : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Hazırlan(süre_değer); ağ_Yığın.işlem_kare(süre_değer + 42);
            doğrulamak(ağ_Yığın.GETİRİ_süre[0] == süre_değer);
            doğrulamak(ağ_Yığın.GETİRİ_ADRES[0] == 0x0a000202 && ağ_Yığın.GETİRİ_bağlantı_noktası_numarası[0] == 4321);
            for (int Dizin = 0; Dizin < süre_değer; Dizin++) doğrulamak(ağ_Yığın.GETİRİ_veri[Dizin] == (Dizin & 255));
        }
        for (int süre_değer = 0; süre_değer < 42; süre_değer++) { Hazırlan(0); reddetmek_değer(süre_değer); }
        Hazırlan(1025); reddetmek_değer(1067);
        Hazırlan(2); ağ_Yığın.artış_kare[24] ^= 1; reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[42] ^= 1; reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.넣기16(ağ_Yığın.artış_kare, 38, 7); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.넣기16(ağ_Yığın.artış_kare, 38, 65535); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[14] = 0x4f; reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[14] = 0x44; reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[20] = 0x20; küme_sağlama_toplamı(2); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[21] = 1; küme_sağlama_toplamı(2); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[33] = 99; küme_sağlama_toplamı(2); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[0] ^= 1; reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.artış_kare[23] = 6; küme_sağlama_toplamı(2); reddetmek_değer(44);
        Hazırlan(2); ağ_Yığın.넣기16(ağ_Yığın.artış_kare, 40, 0); ağ_Yığın.işlem_kare(44); doğrulamak(ağ_Yığın.GETİRİ_süre[0] == 2);
        int[] sonuç = new int[4];
        doğrulamak(ağ_Yığın.almak(3, sonuç, 1, 0) == -90);
        doğrulamak(ağ_Yığın.almak(3, sonuç, 4, 0) == -11);
        Hazırlan(2); ağ_Yığın.işlem_kare(44); int atmak_değer = ağ_Yığın.폐기수;
        ağ_Yığın.işlem_kare(44); doğrulamak(ağ_Yığın.폐기수 == atmak_değer + 1);
        ağ_Yığın.TEMİZ_işlem(); doğrulamak(ağ_Yığın.Aç(5000) == 3);
        doğrulamak(ağ_Yığın.Aç(5000) == -98); doğrulamak(ağ_Yığın.Aç(0) == 4);
        doğrulamak(ağ_Yığın.Aç(0) == 5); doğrulamak(ağ_Yığın.Aç(0) == 6); doğrulamak(ağ_Yığın.Aç(0) == -24);
        doğrulamak(ağ_Yığın.Kapat(4) == 0); doğrulamak(ağ_Yığın.Kapat(4) == -9);
        ağ_Yığın.찾은주소 = ağ_Yığın.ağ_geçidi_değer;
        doğrulamak(ağ_Yığın.göndermek(3, ağ_Yığın.ağ_geçidi_değer, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = ağ_sürücü.en_son_değer;
        doğrulamak(sağlama_toplamı(보냄, 14, 20, 0) == 0);
        doğrulamak(sağlama_toplamı(보냄, 34, 11, ağ_Yığın.가상머리합(ağ_Yığın.내주소, ağ_Yığın.ağ_geçidi_değer, 11)) == 0);
        doğrulamak(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
