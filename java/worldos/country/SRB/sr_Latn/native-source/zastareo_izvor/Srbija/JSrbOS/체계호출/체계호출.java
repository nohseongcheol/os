// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.체계호출;

import Srbija.JSrbOS.Memorija_oblast.stranica_menadžer;
import Srbija.JSrbOS.작업.Proces_VALUE;
import Srbija.JSrbOS.작업.Planer;
import Srbija.JSrbOS.sistem_datoteka.실행파일적재기;
import Srbija.JSrbOS.sistem_datoteka.sistem_datoteka;
import Srbija.JSrbOS.sistem_datoteka.Datoteka_informacije;
import Srbija.JSrbOS.jezgro.하드웨어;
import Srbija.JSrbOS.입력.입력관리자;
import Srbija.JSrbOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int samo_za_čitanje_zastavica = 0;
    public static final int SEARCH_START = 0;
    public static final int SEARCH_aktuelno = 1;
    public static final int FIND_stavka_završiti_razgovor = 2;

    private final sistem_datoteka sistem_datoteka;
    private final stranica_menadžer 쪽관리;
    private final Planer Planer;
    private final 실행파일적재기 rutina_za_punjenje = new 실행파일적재기();
    private final 하드웨어 uređaj_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(sistem_datoteka sistem_datoteka, stranica_menadžer 쪽관리, Planer Planer, 하드웨어 uređaj_VALUE, 입력관리자 입력관리) {
        this.sistem_datoteka = sistem_datoteka;
        this.쪽관리 = 쪽관리;
        this.Planer = Planer;
        this.uređaj_VALUE = uređaj_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikator(Proces_VALUE aktuelno_Proces) {
        return aktuelno_Proces.identifikator_VALUE();
    }

    public int nadređen_Proces_identifikator(Proces_VALUE aktuelno_Proces) {
        return aktuelno_Proces.nadređen_identifikator();
    }

    public int otvoren(Proces_VALUE aktuelno_Proces, String ime, int zastavica_VALUE) {
        if (zastavica_VALUE != samo_za_čitanje_zastavica) {
            return -30;
        }
        return aktuelno_Proces.파일서술자().otvoren(ime);
    }

    public int 읽기(Proces_VALUE aktuelno_Proces, int 서술자, byte[] primiti_odredište, int promeniti_veličinu) {
        if (서술자 == 0) {
            if (promeniti_veličinu <= 0 || primiti_odredište.length == 0) {
                return 0;
            }
            입력사건 događaj = 입력관리.Dalje_događaj();
            if (događaj == null || događaj.vrsta_događaja() != 입력사건.종류.Ključ_van_funkcije) {
                return -11;
            }
            primiti_odredište[0] = (byte) događaj.첫째값();
            return 1;
        }
        return aktuelno_Proces.파일서술자().읽기(서술자, primiti_odredište, promeniti_veličinu);
    }

    public int 쓰기(Proces_VALUE aktuelno_Proces, int 서술자, byte[] podaci, int promeniti_veličinu) {
        if (서술자 != 1 && 서술자 != 2) {
            return aktuelno_Proces.파일서술자().informatičko_odeljenje_otvoren(서술자) ? -30 : -9;
        }
        if (promeniti_veličinu < 0 || promeniti_veličinu > podaci.length) {
            return -22;
        }
        uređaj_VALUE.직렬출력(new String(podaci, 0, promeniti_veličinu, java.nio.charset.StandardCharsets.UTF_8));
        return promeniti_veličinu;
    }

    public int Zatvori(Proces_VALUE aktuelno_Proces, int 서술자) {
        return aktuelno_Proces.파일서술자().Zatvori(서술자);
    }

    public int premestiti_pozicija(Proces_VALUE aktuelno_Proces, int 서술자, int 거리, int radnja_koren) {
        return aktuelno_Proces.파일서술자().premestiti_pozicija(서술자, 거리, radnja_koren);
    }

    public int 서술자복제(Proces_VALUE aktuelno_Proces, int 서술자) {
        return aktuelno_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE aktuelno_Proces, int 서술자, int 새서술자) {
        return aktuelno_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String ime, int metod_MODE) {
        Datoteka_informacije msinfo32_exe = sistem_datoteka.msinfo32_exe(ime);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metod_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metod_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_lista_zadataka(String ime) {
        return "/".equals(ime) ? 0 : -20;
    }

    public String aktuelno_lista_zadataka(int primiti_promeniti_veličinu) {
        return primiti_promeniti_veličinu >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int efikasan_UID() { return 0; }
    public int Grupa_identifikator() { return 0; }
    public int efikasan_Grupa_identifikator() { return 0; }

    public int sinhronizovati_Datoteka(Proces_VALUE aktuelno_Proces, int 서술자) {
        return aktuelno_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // aktuelno_stavka 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informatičko_odeljenje_Terminal(Proces_VALUE aktuelno_Proces, int 서술자) {
        Datoteka_informacije msinfo32_exe = aktuelno_Proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Datoteka_kontrola(Proces_VALUE aktuelno_Proces, int 서술자, int komanda, int parametar_argument) {
        if (komanda == 0) {
            return aktuelno_Proces.파일서술자().복제서술자(서술자, parametar_argument);
        }
        if (komanda == 1) {
            return aktuelno_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (komanda == 2) {
            return aktuelno_Proces.파일서술자().실행시닫기설정(서술자, (parametar_argument & 1) != 0);
        }
        if (komanda == 3) {
            return aktuelno_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : samo_za_čitanje_zastavica;
        }
        if (komanda == 4) {
            return parametar_argument == samo_za_čitanje_zastavica ? 0 : -30;
        }
        return -22;
    }

    public int Create_stavka(String ime, int dozvola_VALUE) {
        return -30;
    }

    public Datoteka_informacije 서술자정보(Proces_VALUE aktuelno_Proces, int 서술자) {
        return aktuelno_Proces.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Detalji sistem_Detalji() {
        return new sistem_Detalji("JSrbOS", "JSrbOS", "0.1", "Java managed kernel", "i386");
    }

    public Datoteka_informacije Datoteka_informacije(String ime) {
        return sistem_datoteka.msinfo32_exe(ime);
    }

    public Proces_VALUE klon_Proces(Proces_VALUE nadređen_VALUE) {
        return Planer.klon_VALUE(nadređen_VALUE);
    }

    public int 자식기다리기(Proces_VALUE nadređen_VALUE, int dete_identifikator, boolean 기다리지않음) {
        return Planer.자식기다리기(nadređen_VALUE, dete_identifikator, 기다리지않음);
    }

    public int program_pauza(Proces_VALUE aktuelno_Proces, int 새끝) {
        int 이전끝 = aktuelno_Proces.program_pauza();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / stranica_menadžer.veličina_stranice;
        int 끝쪽 = (새끝 + stranica_menadžer.veličina_stranice - 1) / stranica_menadžer.veličina_stranice;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * stranica_menadžer.veličina_stranice;
                try {
                    쪽관리.바이트읽기(aktuelno_Proces.adresa_prostor(), adresa);
                } catch (IllegalStateException greška) {
                    쪽관리.MAP_stranica(aktuelno_Proces.adresa_prostor(), adresa, true);
                }
            }
        }
        aktuelno_Proces.skup_program_pauza(새끝);
        return 새끝;
    }

    public int povećanje_program_pauza(Proces_VALUE aktuelno_Proces, int 증가량) {
        int 이전끝 = aktuelno_Proces.program_pauza();
        int KR = program_pauza(aktuelno_Proces, 이전끝 + 증가량);
        return KR < 0 ? KR : 이전끝;
    }

    public int Izvrši_komanda(Proces_VALUE aktuelno_Proces, byte[] 실행파일) {
        return Izvrši_komanda(aktuelno_Proces, 실행파일, new String[0], new String[0]);
    }

    public int Izvrši_komanda(Proces_VALUE aktuelno_Proces, byte[] 실행파일, String[] parametar_argument, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = rutina_za_punjenje.검사(실행파일);
        } catch (IllegalArgumentException greška) {
            return -8;
        }
        if (parametar_argument == null || 환경 == null || parametar_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.odeljak_VALUE odeljak_VALUE : IMAGE_VALUE.구역들()) {
            if ((odeljak_VALUE.zastavica_VALUE() & 2) == 0 || odeljak_VALUE.promeniti_veličinu() == 0) {
                continue;
            }
            int 첫쪽 = odeljak_VALUE.adresa() / stranica_menadžer.veličina_stranice;
            int 끝쪽 = (odeljak_VALUE.adresa() + odeljak_VALUE.promeniti_veličinu() + stranica_menadžer.veličina_stranice - 1) / stranica_menadžer.veličina_stranice;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * stranica_menadžer.veličina_stranice;
                try {
                    쪽관리.바이트읽기(aktuelno_Proces.adresa_prostor(), adresa);
                    쪽관리.범위개인쓰기(aktuelno_Proces.adresa_prostor(), adresa, stranica_menadžer.veličina_stranice);
                } catch (IllegalStateException greška) {
                    쪽관리.MAP_stranica(aktuelno_Proces.adresa_prostor(), adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < odeljak_VALUE.promeniti_veličinu(); INDEX++) {
                byte VALUE = odeljak_VALUE.종류() == 8 ? 0 : 실행파일[odeljak_VALUE.Datoteka_pozicija() + INDEX];
                쪽관리.바이트쓰기(aktuelno_Proces.adresa_prostor(), odeljak_VALUE.adresa() + INDEX, VALUE);
            }
        }
        aktuelno_Proces.실행문맥설정(IMAGE_VALUE.START_adresa(), parametar_argument, 환경);
        aktuelno_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void Napusti_program(Proces_VALUE aktuelno_Proces, int Status_VALUE) {
        aktuelno_Proces.Izađi_program(Status_VALUE);
    }
}
