// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrayna.JUkrOS.sınamalar;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Ukrayna.JUkrOS.Bellek_bölge.Bellek_yönetici;
import Ukrayna.JUkrOS.Bellek_bölge.sayfa_yönetici;
import Ukrayna.JUkrOS.artış_değer.artış_olay;
import Ukrayna.JUkrOS.작업.işlem_değer;
import Ukrayna.JUkrOS.sistem_çağrısı.sistem_çağrısı;
import Ukrayna.JUkrOS.dosya_sistemi.yürütülebilir_yükleyici;
import Ukrayna.JUkrOS.Çekirdek.Çekirdek;
import Ukrayna.JUkrOS.konak.konak_donanım;
import Ukrayna.JUkrOS.IRQ.IRQ_yönetici;
import Ukrayna.JUkrOS.tanımlayıcı_girdi.GDT;
import Ukrayna.JUkrOS.depolama_aygıtı.고급기술결합장치;
import Ukrayna.JUkrOS.cihaz_değer.donatı_veri_yolu_yönetici;
import Ukrayna.JUkrOS.ağ_Yığın.ağ_Araçlar;
import Ukrayna.JUkrOS.ağ_Yığın.ağ_katmanı;
import Ukrayna.JUkrOS.cihaz_değer.Saat;
import Ukrayna.JUkrOS.tanımlayıcı_girdi.Görev_Durum_segment;
import Ukrayna.JUkrOS.화면.karakter_monitör;
import Ukrayna.JUkrOS.dosya_sistemi.birincil_bölüm_tablo;

public final class 전체시험 {
    private static int geçirmek_BAĞ_DEĞ_SAY;

    private 전체시험() {
    }

    public static void main(String[] parametre_bağımsız_değişken) {
        konak_donanım cihaz_değer = new konak_donanım();
        Çekirdek çekirdek_değer = new Çekirdek(cihaz_değer);
        çekirdek_değer.çalıştır();

        test_Bellek(çekirdek_değer);
        쪽관리시험(çekirdek_değer);
        파일과과정시험(çekirdek_değer);
        실행파일시험(çekirdek_değer);
        test_artış(çekirdek_değer);
        test_donanım(cihaz_değer);
        개입중단과서술자시험();
        test_Depolama_VE_Ağ();
        화면과시계시험();

        System.out.println("JUkrOS sınamalar geçirmek_değer: " + geçirmek_BAĞ_DEĞ_SAY);
    }

    private static void test_Bellek(Çekirdek çekirdek_değer) {
        Bellek_yönetici yönetici_değer = çekirdek_değer.Bellek_bölge();
        int 첫주소 = yönetici_değer.정렬할당(100, 64);
        doğrulamak((첫주소 & 63) == 0, "hizalamak_değer ayırmak_Depolama");
        yönetici_değer.yazma_bayt_değer(첫주소, (byte) 0x5a);
        doğrulamak(yönetici_değer.바이트읽기(첫주소) == (byte) 0x5a, "물리 Bellek_bölge 읽고 Yazma");
        int 사용전 = yönetici_değer.사용크기();
        yönetici_değer.sürüm_Depolama(첫주소);
        doğrulamak(yönetici_değer.사용크기() < 사용전, "Bellek_bölge sürüm_Depolama");
    }

    private static void 쪽관리시험(Çekirdek çekirdek_değer) {
        sayfa_yönetici yönetici_değer = çekirdek_değer.쪽관리();
        sayfa_yönetici.adres_alanı ana_yer = yönetici_değer.새주소공간();
        yönetici_değer.MAP_sayfa(ana_yer, 0x1000, true);
        yönetici_değer.yazma_bayt_değer(ana_yer, 0x1010, (byte) 7);
        sayfa_yönetici.adres_alanı alt_yer = yönetici_değer.쓰기시복사복제(ana_yer);
        yönetici_değer.yazma_bayt_değer(alt_yer, 0x1010, (byte) 9);
        doğrulamak(yönetici_değer.바이트읽기(ana_yer, 0x1010) == 7, "Yazma 시 örnek_değer ana_değer 격리");
        doğrulamak(yönetici_değer.바이트읽기(alt_yer, 0x1010) == 9, "Yazma 시 örnek_değer alt_değer Yazma");
    }

    private static void 파일과과정시험(Çekirdek çekirdek_değer) {
        byte[] içerik_değer = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        çekirdek_değer.dosya_sistemi().Ekleme_Dosya("sınamalar", içerik_değer);
        işlem_değer ana_değer = çekirdek_değer.첫과정();
        sistem_çağrısı 호출 = çekirdek_değer.sistem_çağrısı();
        int tanımlayıcı_girdi = 호출.Aç(ana_değer, "/sınamalar", sistem_çağrısı.salt_okunur_bayrak);
        doğrulamak(tanımlayıcı_girdi >= 3, "dosya Aç");

        byte[] almak_hedef = new byte[içerik_değer.length];
        doğrulamak(호출.Okuma(ana_değer, tanımlayıcı_girdi, almak_hedef, almak_hedef.length) == içerik_değer.length, "dosya Okuma");
        doğrulamak(Arrays.equals(içerik_değer, almak_hedef), "dosya içerik_değer");
        doğrulamak(호출.taşımak_konum(ana_değer, tanımlayıcı_girdi, 0, sistem_çağrısı.Ara_Start) == 0, "dosya konum taşımak_değer_83b651b8");

        int 복제서술자 = 호출.kopya_tanımlayıcı(ana_değer, tanımlayıcı_girdi);
        doğrulamak(복제서술자 >= 0, "tanımlayıcı_girdi kopya_değer");
        işlem_değer alt_değer = 호출.kopya_işlem(ana_değer);
        doğrulamak(alt_değer.tanımlayıcı_değer() != ana_değer.tanımlayıcı_değer(), "işlem_değer tanımlayıcı_değer 분리");
        doğrulamak(alt_değer.ana_tanımlayıcı() == ana_değer.tanımlayıcı_değer(), "ana_değer işlem_değer tanımlayıcı_değer");
        doğrulamak(호출.Kapat(alt_değer, tanımlayıcı_girdi) == 0 && ana_değer.Dosya_tanımlayıcı().bilgi_teknolojisi_açık(tanımlayıcı_girdi), "alt_değer Kapat 격리");

        int Önceki_Bitiş = 호출.artış_program_mola(ana_değer, 8192);
        doğrulamak(Önceki_Bitiş == 0x06000000, "program_f5044b9b 끝 늘리기");
        doğrulamak(ana_değer.program_mola() == 0x06002000, "program_f5044b9b 끝 반영");
        doğrulamak(alt_değer.program_mola() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        alt_değer.Çıkış_program(7);
        doğrulamak(호출.자식기다리기(ana_değer, alt_değer.tanımlayıcı_değer(), false) == (7 << 8), "alt_değer Çıkış_program 기다리기");
        doğrulamak(호출.접근가능("sınamalar", 1) == -13, "yürütmek_komut izin_değer reddetmek_değer");
        doğrulamak(호출.UID() == 0 && 호출.GID() == 0, "사용자와 무리 tanımlayıcı_değer");
        doğrulamak("/".equals(호출.geçerli_Görev_Listesi(2)) && 호출.geçiş_Görev_Listesi("/") == 0, "geçerli_öğe 작업 girdi_Liste");
        doğrulamak(호출.bilgi_teknolojisi_Terminal(ana_değer, 1), "표준 metinÇıktısı 단말");
        doğrulamak("JUkrOS".equals(호출.Sistem_Ayrıntılar().Sistem_ad()), "işletim_sistemi_değer msinfo32_exe");
    }

    private static void 실행파일시험(Çekirdek çekirdek_değer) {
        byte[] veri = new byte[92];
        veri[0] = 0x7f;
        veri[1] = 'E';
        veri[2] = 'L';
        veri[3] = 'F';
        veri[4] = 1;
        veri[5] = 1;
        yazma_bilgi_değer(veri, 24, 0x04001000);
        yazma_bilgi_değer(veri, 32, 52);
        짧은정수쓰기(veri, 46, 40);
        짧은정수쓰기(veri, 48, 1);
        yazma_bilgi_değer(veri, 56, 8);
        yazma_bilgi_değer(veri, 60, 2);
        yazma_bilgi_değer(veri, 64, 0x04002000);
        yazma_bilgi_değer(veri, 72, 64);

        yürütülebilir_yükleyici.RESİM RESİM_değer = new yürütülebilir_yükleyici().검사(veri);
        doğrulamak(RESİM_değer.Start_ADRES() == 0x04001000, "ELF çalıştır ADRES");
        doğrulamak(RESİM_değer.구역들().size() == 1 && RESİM_değer.구역들().get(0).Tip_değer() == 8, "ELF 빈 veri bölüm_değer_366e0bfa");
        int tanımlayıcı_girdi = çekirdek_değer.sistem_çağrısı().Aç(çekirdek_değer.첫과정(), "sınamalar", sistem_çağrısı.salt_okunur_bayrak);
        doğrulamak(çekirdek_değer.sistem_çağrısı().dosya_denetimi(çekirdek_değer.첫과정(), tanımlayıcı_girdi, 2, 1) == 0, "yürütmek_komut 시 Kapat Ayarlar");
        doğrulamak(çekirdek_değer.sistem_çağrısı().yürütmek_komut(çekirdek_değer.첫과정(), veri, new String[] {"sınamalar", "값"}, new String[] {"Dil=Türkçe"}) == 0, "ELF yürütmek_komut RESİM_değer 적재");
        doğrulamak(çekirdek_değer.첫과정().yürütme_Start_ADRES() == 0x04001000, "yürütmek_komut çalıştır ADRES 반영");
        doğrulamak(çekirdek_değer.첫과정().yürütme_bağımsız_değişken().length == 2 && çekirdek_değer.첫과정().ortam_değer().length == 1, "yürütmek_komut 인자와 ortam");
        doğrulamak(!çekirdek_değer.첫과정().Dosya_tanımlayıcı().bilgi_teknolojisi_açık(tanımlayıcı_girdi), "yürütmek_komut 시 tanımlayıcı_girdi Kapat");
        doğrulamak(çekirdek_değer.쪽관리().바이트읽기(çekirdek_değer.첫과정().adres_alanı(), 0x04002000) == 0, "빈 veri bölüm_değer_366e0bfa sıfır_işlenen başlat");
    }

    private static void test_artış(Çekirdek çekirdek_değer) {
        çekirdek_değer.입력관리().tuş_kapalı('가');
        çekirdek_değer.입력관리().쥐이동(3, -2);
        artış_olay 첫사건 = çekirdek_değer.입력관리().Sonraki_olay();
        artış_olay SANİYE_olay = çekirdek_değer.입력관리().Sonraki_olay();
        doğrulamak(첫사건.olay_türü() == artış_olay.Tip_değer.tuş_kapalı, "자판 Olay");
        doğrulamak(SANİYE_olay.첫째값() == 3 && SANİYE_olay.SANİYE_değer() == -2, "쥐 taşımak_değer_83b651b8 Olay");
    }

    private static void test_donanım(konak_donanım cihaz_değer) {
        cihaz_değer.yazma_taşımak_bayt(0x3f8, 0xab);
        doğrulamak(cihaz_değer.포트바이트읽기(0x3f8) == 0xab, "donanım_taşımak G_Ç sınır_değer");
        doğrulamak(cihaz_değer.직렬기록().contains("JUkrOS"), "직렬 LOG_KAYIT");
    }

    private static void 개입중단과서술자시험() {
        IRQ_yönetici yönetici_değer = new IRQ_yönetici();
        yönetici_değer.yazmaç_girdi(0x21, Depolama_ADRES -> Depolama_ADRES + 4);
        yönetici_değer.açmak();
        doğrulamak(yönetici_değer.dağıtmak_değer(0x21, 100) == 104, "IRQ dağıtmak_değer");
        yönetici_değer.devre_dışı_bırakmak();
        doğrulamak(yönetici_değer.dağıtmak_değer(0x21, 100) == 100, "IRQ devre_dışı_bırakmak");

        GDT tanımlayıcı_tablo = new GDT();
        tanımlayıcı_tablo.küme_varsayılan_değer();
        doğrulamak(tanımlayıcı_tablo.조각들().size() == 5, "전역 tanımlayıcı_tablo");
        Görev_Durum_segment Görev_Durum = new Görev_Durum_segment();
        Görev_Durum.특권쌓임공간설정(0x10, 0x800000);
        doğrulamak(Görev_Durum.Yığın_sıfır_blok() == 0x10 && Görev_Durum.Yığın_sıfır_ADRES() == 0x800000, "작업 Durum_değer bölüm_değer_366e0bfa");
    }

    private static void test_Depolama_VE_Ağ() {
        고급기술결합장치 depolama_aygıtı = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.bölüm_boyutlandırmak];
        byte[] 읽은자료 = new byte[고급기술결합장치.bölüm_boyutlandırmak];
        쓸자료[17] = 42;
        depolama_aygıtı.Yazma(2, 쓸자료);
        depolama_aygıtı.Okuma(2, 읽은자료);
        doğrulamak(읽은자료[17] == 42, "ATA bölüm_değer_366e0bfa 읽고 Yazma");

        donatı_veri_yolu_yönetici donatı = new donatı_veri_yolu_yönetici();
        donatı.발견(new donatı_veri_yolu_yönetici.cihaz_değer(0x1022, 0x2000, 0xc000, 11));
        doğrulamak(donatı.BUL_girdi(0x1022, 0x2000) != null, "주변 cihaz_değer BUL_girdi");

        byte[] Ethernet_kare = new byte[34];
        Ethernet_kare[12] = 0x08;
        Ethernet_kare[13] = 0x00;
        Ethernet_kare[14] = 0x45;
        doğrulamak(ağ_Araçlar.Ethernet_BÜYÜKHARF_protokol(Ethernet_kare) == 0x0800, "이더넷 상위 sözleşme_değeri");
        doğrulamak(ağ_Araçlar.bilgi_teknolojisi_FFF_4_protokol(Ethernet_kare, 14), "상호통신망규약 4판");
        doğrulamak(ağ_Araçlar.bulut_sağlama_toplamı(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 sağlama_toplamı");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        yazma_bilgi_değer(첫구역, 454, 63);
        yazma_bilgi_değer(첫구역, 458, 1024);
        doğrulamak(new birincil_bölüm_tablo().Okuma(첫구역).size() == 1, "varsayılan_değer 분할 영역표");

        ağ_katmanı katman_değer_e65604ef = new ağ_katmanı();
        int[] GETİRİ_BAĞ_DEĞ_SAY = new int[1];
        katman_değer_e65604ef.yazmaç_kullanıcı_veri_ders(7, (veri, çalıştır, süre_değer) -> GETİRİ_BAĞ_DEĞ_SAY[0]++);
        byte[] kare_Dizin = new byte[14 + 20 + 8];
        kare_Dizin[12] = 0x08;
        kare_Dizin[13] = 0x00;
        kare_Dizin[14] = 0x45;
        kare_Dizin[16] = 0;
        kare_Dizin[17] = 28;
        kare_Dizin[23] = 17;
        kare_Dizin[36] = 0;
        kare_Dizin[37] = 7;
        doğrulamak(katman_değer_e65604ef.almak_Ethernet(kare_Dizin) && GETİRİ_BAĞ_DEĞ_SAY[0] == 1, "kullanıcı_alanı veri ders_değer dağıtmak_değer");
    }

    private static void 화면과시계시험() {
        karakter_monitör 화면 = new karakter_monitör();
        화면.metinÇıktısı("가나\n다");
        doğrulamak(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 metinÇıktısı");
        Saat Saat = new Saat(100);
        for (int Dizin = 0; Dizin < 10; Dizin++) {
            Saat.tık_değer_a516cff0();
        }
        doğrulamak(Saat.지난밀리초() == 100, "Saat tık_değer_a516cff0 ÇEVİR_değer");
    }

    private static void yazma_bilgi_değer(byte[] veri, int konum, int değer) {
        veri[konum] = (byte) değer;
        veri[konum + 1] = (byte) (değer >>> 8);
        veri[konum + 2] = (byte) (değer >>> 16);
        veri[konum + 3] = (byte) (değer >>> 24);
    }

    private static void 짧은정수쓰기(byte[] veri, int konum, int değer) {
        veri[konum] = (byte) değer;
        veri[konum + 1] = (byte) (değer >>> 8);
    }

    private static void doğrulamak(boolean koşul, String İsim) {
        if (!koşul) {
            throw new AssertionError("hata_değer: " + İsim);
        }
        geçirmek_BAĞ_DEĞ_SAY++;
        System.out.println("geçirmek_değer: " + İsim);
    }
}
