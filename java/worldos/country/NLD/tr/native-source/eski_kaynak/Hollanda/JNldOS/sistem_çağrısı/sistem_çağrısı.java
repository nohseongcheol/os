// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.sistem_çağrısı;

import Hollanda.JNldOS.Bellek_bölge.sayfa_yönetici;
import Hollanda.JNldOS.작업.işlem_değer;
import Hollanda.JNldOS.작업.Scheduler;
import Hollanda.JNldOS.dosya_sistemi.yürütülebilir_yükleyici;
import Hollanda.JNldOS.dosya_sistemi.dosya_sistemi;
import Hollanda.JNldOS.dosya_sistemi.Dosya_bilgi;
import Hollanda.JNldOS.Çekirdek.donanım_değer;
import Hollanda.JNldOS.artış_değer.artış_yönetici;
import Hollanda.JNldOS.artış_değer.artış_olay;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class sistem_çağrısı {
    public static final int salt_okunur_bayrak = 0;
    public static final int Ara_Start = 0;
    public static final int Ara_geçerli = 1;
    public static final int BUL_girdi_Bitiş = 2;

    private final dosya_sistemi dosya_sistemi;
    private final sayfa_yönetici 쪽관리;
    private final Scheduler Scheduler;
    private final yürütülebilir_yükleyici yükleyici = new yürütülebilir_yükleyici();
    private final donanım_değer cihaz_değer;
    private final artış_yönetici 입력관리;

    public sistem_çağrısı(dosya_sistemi dosya_sistemi, sayfa_yönetici 쪽관리, Scheduler Scheduler, donanım_değer cihaz_değer, artış_yönetici 입력관리) {
        this.dosya_sistemi = dosya_sistemi;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.cihaz_değer = cihaz_değer;
        this.입력관리 = 입력관리;
    }

    public int işlem_tanımlayıcı(işlem_değer geçerli_işlem) {
        return geçerli_işlem.tanımlayıcı_değer();
    }

    public int ana_işlem_tanımlayıcı(işlem_değer geçerli_işlem) {
        return geçerli_işlem.ana_tanımlayıcı();
    }

    public int Aç(işlem_değer geçerli_işlem, String İsim, int bayrak_değer) {
        if (bayrak_değer != salt_okunur_bayrak) {
            return -30;
        }
        return geçerli_işlem.Dosya_tanımlayıcı().Aç(İsim);
    }

    public int Okuma(işlem_değer geçerli_işlem, int tanımlayıcı_girdi, byte[] almak_hedef, int Boyut) {
        if (tanımlayıcı_girdi == 0) {
            if (Boyut <= 0 || almak_hedef.length == 0) {
                return 0;
            }
            artış_olay Olay = 입력관리.Sonraki_olay();
            if (Olay == null || Olay.olay_türü() != artış_olay.Tip_değer.tuş_kapalı) {
                return -11;
            }
            almak_hedef[0] = (byte) Olay.첫째값();
            return 1;
        }
        return geçerli_işlem.Dosya_tanımlayıcı().Okuma(tanımlayıcı_girdi, almak_hedef, Boyut);
    }

    public int Yazma(işlem_değer geçerli_işlem, int tanımlayıcı_girdi, byte[] veri, int Boyut) {
        if (tanımlayıcı_girdi != 1 && tanımlayıcı_girdi != 2) {
            return geçerli_işlem.Dosya_tanımlayıcı().bilgi_teknolojisi_açık(tanımlayıcı_girdi) ? -30 : -9;
        }
        if (Boyut < 0 || Boyut > veri.length) {
            return -22;
        }
        cihaz_değer.직렬출력(new String(veri, 0, Boyut, java.nio.charset.StandardCharsets.UTF_8));
        return Boyut;
    }

    public int Kapat(işlem_değer geçerli_işlem, int tanımlayıcı_girdi) {
        return geçerli_işlem.Dosya_tanımlayıcı().Kapat(tanımlayıcı_girdi);
    }

    public int taşımak_konum(işlem_değer geçerli_işlem, int tanımlayıcı_girdi, int 거리, int işlem_kök) {
        return geçerli_işlem.Dosya_tanımlayıcı().taşımak_konum(tanımlayıcı_girdi, 거리, işlem_kök);
    }

    public int kopya_tanımlayıcı(işlem_değer geçerli_işlem, int tanımlayıcı_girdi) {
        return geçerli_işlem.Dosya_tanımlayıcı().복제서술자(tanımlayıcı_girdi, 0);
    }

    public int 지정서술자복제(işlem_değer geçerli_işlem, int tanımlayıcı_girdi, int 새서술자) {
        return geçerli_işlem.Dosya_tanımlayıcı().지정복제(tanımlayıcı_girdi, 새서술자);
    }

    public int 접근가능(String İsim, int metot_mod) {
        Dosya_bilgi msinfo32_exe = dosya_sistemi.msinfo32_exe(İsim);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metot_mod & 1) != 0 && (msinfo32_exe.şekil_Tip() & 0111) == 0) {
            return -13;
        }
        if ((metot_mod & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int geçiş_Görev_Listesi(String İsim) {
        return "/".equals(İsim) ? 0 : -20;
    }

    public String geçerli_Görev_Listesi(int almak_boyutlandırmak) {
        return almak_boyutlandırmak >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int etkili_UID() { return 0; }
    public int GID() { return 0; }
    public int etkili_GID() { return 0; }

    public int eşitlemek_Dosya(işlem_değer geçerli_işlem, int tanımlayıcı_girdi) {
        return geçerli_işlem.Dosya_tanımlayıcı().msinfo32_exe(tanımlayıcı_girdi) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // geçerli_öğe 파일체계는 Okuma 전용이어서 밀어낼 자료가 없다.
    }

    public boolean bilgi_teknolojisi_Terminal(işlem_değer geçerli_işlem, int tanımlayıcı_girdi) {
        Dosya_bilgi msinfo32_exe = geçerli_işlem.Dosya_tanımlayıcı().msinfo32_exe(tanımlayıcı_girdi);
        return msinfo32_exe != null && (msinfo32_exe.şekil_Tip() & 0170000) == 0020000;
    }

    public int dosya_denetimi(işlem_değer geçerli_işlem, int tanımlayıcı_girdi, int komut, int parametre_bağımsız_değişken) {
        if (komut == 0) {
            return geçerli_işlem.Dosya_tanımlayıcı().복제서술자(tanımlayıcı_girdi, parametre_bağımsız_değişken);
        }
        if (komut == 1) {
            return geçerli_işlem.Dosya_tanımlayıcı().실행시닫기값(tanımlayıcı_girdi);
        }
        if (komut == 2) {
            return geçerli_işlem.Dosya_tanımlayıcı().실행시닫기설정(tanımlayıcı_girdi, (parametre_bağımsız_değişken & 1) != 0);
        }
        if (komut == 3) {
            return geçerli_işlem.Dosya_tanımlayıcı().msinfo32_exe(tanımlayıcı_girdi) == null ? -9 : salt_okunur_bayrak;
        }
        if (komut == 4) {
            return parametre_bağımsız_değişken == salt_okunur_bayrak ? 0 : -30;
        }
        return -22;
    }

    public int açmak_girdi(String İsim, int izin_değer) {
        return -30;
    }

    public Dosya_bilgi tanımlayıcı_bilgi(işlem_değer geçerli_işlem, int tanımlayıcı_girdi) {
        return geçerli_işlem.Dosya_tanımlayıcı().msinfo32_exe(tanımlayıcı_girdi);
    }

    public Sistem_Ayrıntılar Sistem_Ayrıntılar() {
        return new Sistem_Ayrıntılar("JNldOS", "JNldOS", "0.1", "Java managed kernel", "i386");
    }

    public Dosya_bilgi Dosya_bilgi(String İsim) {
        return dosya_sistemi.msinfo32_exe(İsim);
    }

    public işlem_değer kopya_işlem(işlem_değer ana_değer) {
        return Scheduler.kopya_değer(ana_değer);
    }

    public int 자식기다리기(işlem_değer ana_değer, int alt_tanımlayıcı, boolean 기다리지않음) {
        return Scheduler.자식기다리기(ana_değer, alt_tanımlayıcı, 기다리지않음);
    }

    public int program_mola(işlem_değer geçerli_işlem, int 새끝) {
        int Önceki_Bitiş = geçerli_işlem.program_mola();
        if (새끝 == 0) {
            return Önceki_Bitiş;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Önceki_Bitiş / sayfa_yönetici.sayfa_boyutu;
        int 끝쪽 = (새끝 + sayfa_yönetici.sayfa_boyutu - 1) / sayfa_yönetici.sayfa_boyutu;
        if (새끝 > Önceki_Bitiş) {
            for (int Dizin = 첫쪽; Dizin < 끝쪽; Dizin++) {
                int ADRES = Dizin * sayfa_yönetici.sayfa_boyutu;
                try {
                    쪽관리.바이트읽기(geçerli_işlem.adres_alanı(), ADRES);
                } catch (IllegalStateException hata) {
                    쪽관리.MAP_sayfa(geçerli_işlem.adres_alanı(), ADRES, true);
                }
            }
        }
        geçerli_işlem.küme_program_mola(새끝);
        return 새끝;
    }

    public int artış_program_mola(işlem_değer geçerli_işlem, int artış_tutar) {
        int Önceki_Bitiş = geçerli_işlem.program_mola();
        int sonuç = program_mola(geçerli_işlem, Önceki_Bitiş + artış_tutar);
        return sonuç < 0 ? sonuç : Önceki_Bitiş;
    }

    public int yürütmek_komut(işlem_değer geçerli_işlem, byte[] çalıştırılabilir) {
        return yürütmek_komut(geçerli_işlem, çalıştırılabilir, new String[0], new String[0]);
    }

    public int yürütmek_komut(işlem_değer geçerli_işlem, byte[] çalıştırılabilir, String[] parametre_bağımsız_değişken, String[] ortam) {
        yürütülebilir_yükleyici.RESİM RESİM_değer;
        try {
            RESİM_değer = yükleyici.검사(çalıştırılabilir);
        } catch (IllegalArgumentException hata) {
            return -8;
        }
        if (parametre_bağımsız_değişken == null || ortam == null || parametre_bağımsız_değişken.length > 16 || ortam.length > 16) {
            return -7;
        }
        for (yürütülebilir_yükleyici.bölüm_değer_366e0bfa bölüm_değer_366e0bfa : RESİM_değer.구역들()) {
            if ((bölüm_değer_366e0bfa.bayrak_değer() & 2) == 0 || bölüm_değer_366e0bfa.Boyut() == 0) {
                continue;
            }
            int 첫쪽 = bölüm_değer_366e0bfa.ADRES() / sayfa_yönetici.sayfa_boyutu;
            int 끝쪽 = (bölüm_değer_366e0bfa.ADRES() + bölüm_değer_366e0bfa.Boyut() + sayfa_yönetici.sayfa_boyutu - 1) / sayfa_yönetici.sayfa_boyutu;
            for (int Dizin = 첫쪽; Dizin < 끝쪽; Dizin++) {
                int ADRES = Dizin * sayfa_yönetici.sayfa_boyutu;
                try {
                    쪽관리.바이트읽기(geçerli_işlem.adres_alanı(), ADRES);
                    쪽관리.Özel_aralık_yazma(geçerli_işlem.adres_alanı(), ADRES, sayfa_yönetici.sayfa_boyutu);
                } catch (IllegalStateException hata) {
                    쪽관리.MAP_sayfa(geçerli_işlem.adres_alanı(), ADRES, true);
                }
            }
            for (int Dizin = 0; Dizin < bölüm_değer_366e0bfa.Boyut(); Dizin++) {
                byte değer = bölüm_değer_366e0bfa.Tip_değer() == 8 ? 0 : çalıştırılabilir[bölüm_değer_366e0bfa.Dosya_konum() + Dizin];
                쪽관리.yazma_bayt_değer(geçerli_işlem.adres_alanı(), bölüm_değer_366e0bfa.ADRES() + Dizin, değer);
            }
        }
        geçerli_işlem.küme_bağlam(RESİM_değer.Start_ADRES(), parametre_bağımsız_değişken, ortam);
        geçerli_işlem.Dosya_tanımlayıcı().실행시닫기();
        return 0;
    }

    public void çıkış_program(işlem_değer geçerli_işlem, int Durum_değer) {
        geçerli_işlem.Çıkış_program(Durum_değer);
    }
}
