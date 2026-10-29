// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.체계호출;

import Italija.JItaOS.Memorija_regije.dojaviti_Upravitelj;
import Italija.JItaOS.작업.Proces_VALUE;
import Italija.JItaOS.작업.Alat_za_zakazivanje;
import Italija.JItaOS.datotečni_sustav.실행파일적재기;
import Italija.JItaOS.datotečni_sustav.datotečni_sustav;
import Italija.JItaOS.datotečni_sustav.Datoteka_informacija;
import Italija.JItaOS.jezgra_sustava.하드웨어;
import Italija.JItaOS.입력.입력관리자;
import Italija.JItaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int samo_za_čitanje_zastavica = 0;
    public static final int Traži_START = 0;
    public static final int Traži_redovno = 1;
    public static final int FIND_unos_završiti_razgovor = 2;

    private final datotečni_sustav datotečni_sustav;
    private final dojaviti_Upravitelj 쪽관리;
    private final Alat_za_zakazivanje Alat_za_zakazivanje;
    private final 실행파일적재기 učitavač = new 실행파일적재기();
    private final 하드웨어 uređaj_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(datotečni_sustav datotečni_sustav, dojaviti_Upravitelj 쪽관리, Alat_za_zakazivanje Alat_za_zakazivanje, 하드웨어 uređaj_VALUE, 입력관리자 입력관리) {
        this.datotečni_sustav = datotečni_sustav;
        this.쪽관리 = 쪽관리;
        this.Alat_za_zakazivanje = Alat_za_zakazivanje;
        this.uređaj_VALUE = uređaj_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikator(Proces_VALUE redovno_Proces) {
        return redovno_Proces.identifikator_VALUE();
    }

    public int roditeljski_Proces_identifikator(Proces_VALUE redovno_Proces) {
        return redovno_Proces.roditeljski_identifikator();
    }

    public int Otvori(Proces_VALUE redovno_Proces, String Ime, int zastavica_VALUE) {
        if (zastavica_VALUE != samo_za_čitanje_zastavica) {
            return -30;
        }
        return redovno_Proces.파일서술자().Otvori(Ime);
    }

    public int Čitaj(Proces_VALUE redovno_Proces, int 서술자, byte[] primiti_odredište, int Veličina) {
        if (서술자 == 0) {
            if (Veličina <= 0 || primiti_odredište.length == 0) {
                return 0;
            }
            입력사건 Događaj = 입력관리.Dalje_događaj();
            if (Događaj == null || Događaj.vrsta_događaja() != 입력사건.종류.Ključ_izvan_funkcije) {
                return -11;
            }
            primiti_odredište[0] = (byte) Događaj.첫째값();
            return 1;
        }
        return redovno_Proces.파일서술자().Čitaj(서술자, primiti_odredište, Veličina);
    }

    public int Zapisuj(Proces_VALUE redovno_Proces, int 서술자, byte[] podaci, int Veličina) {
        if (서술자 != 1 && 서술자 != 2) {
            return redovno_Proces.파일서술자().odjel_informacijske_tehnologije_otvoreno(서술자) ? -30 : -9;
        }
        if (Veličina < 0 || Veličina > podaci.length) {
            return -22;
        }
        uređaj_VALUE.직렬출력(new String(podaci, 0, Veličina, java.nio.charset.StandardCharsets.UTF_8));
        return Veličina;
    }

    public int Zatvori(Proces_VALUE redovno_Proces, int 서술자) {
        return redovno_Proces.파일서술자().Zatvori(서술자);
    }

    public int pomicati_se_položaj(Proces_VALUE redovno_Proces, int 서술자, int 거리, int akcija_korijen) {
        return redovno_Proces.파일서술자().pomicati_se_položaj(서술자, 거리, akcija_korijen);
    }

    public int 서술자복제(Proces_VALUE redovno_Proces, int 서술자) {
        return redovno_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE redovno_Proces, int 서술자, int 새서술자) {
        return redovno_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ime, int postupak_MODE) {
        Datoteka_informacija Podaci_o_sustavu = datotečni_sustav.Podaci_o_sustavu(Ime);
        if (Podaci_o_sustavu == null) {
            return -2;
        }
        if ((postupak_MODE & 1) != 0 && (Podaci_o_sustavu.형태() & 0111) == 0) {
            return -13;
        }
        if ((postupak_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_popis_zadataka(String Ime) {
        return "/".equals(Ime) ? 0 : -20;
    }

    public String redovno_popis_zadataka(int primiti_promijeniti_veličinu) {
        return primiti_promijeniti_veličinu >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int učinkovito_UID() { return 0; }
    public int Grupa_identifikator() { return 0; }
    public int učinkovito_Grupa_identifikator() { return 0; }

    public int sinkronizacija_Datoteka(Proces_VALUE redovno_Proces, int 서술자) {
        return redovno_Proces.파일서술자().Podaci_o_sustavu(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // redovno_artikl 파일체계는 Čitaj 전용이어서 밀어낼 자료가 없다.
    }

    public boolean odjel_informacijske_tehnologije_Terminal(Proces_VALUE redovno_Proces, int 서술자) {
        Datoteka_informacija Podaci_o_sustavu = redovno_Proces.파일서술자().Podaci_o_sustavu(서술자);
        return Podaci_o_sustavu != null && (Podaci_o_sustavu.형태() & 0170000) == 0020000;
    }

    public int Datoteka_kontrola(Proces_VALUE redovno_Proces, int 서술자, int Naredba, int parametar_argument) {
        if (Naredba == 0) {
            return redovno_Proces.파일서술자().복제서술자(서술자, parametar_argument);
        }
        if (Naredba == 1) {
            return redovno_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (Naredba == 2) {
            return redovno_Proces.파일서술자().실행시닫기설정(서술자, (parametar_argument & 1) != 0);
        }
        if (Naredba == 3) {
            return redovno_Proces.파일서술자().Podaci_o_sustavu(서술자) == null ? -9 : samo_za_čitanje_zastavica;
        }
        if (Naredba == 4) {
            return parametar_argument == samo_za_čitanje_zastavica ? 0 : -30;
        }
        return -22;
    }

    public int Create_unos(String Ime, int dozvola_VALUE) {
        return -30;
    }

    public Datoteka_informacija 서술자정보(Proces_VALUE redovno_Proces, int 서술자) {
        return redovno_Proces.파일서술자().Podaci_o_sustavu(서술자);
    }

    public sustav_Pojedinosti sustav_Pojedinosti() {
        return new sustav_Pojedinosti("JItaOS", "JItaOS", "0.1", "Java managed kernel", "i386");
    }

    public Datoteka_informacija Datoteka_informacija(String Ime) {
        return datotečni_sustav.Podaci_o_sustavu(Ime);
    }

    public Proces_VALUE klon_Proces(Proces_VALUE roditeljski_VALUE) {
        return Alat_za_zakazivanje.klon_VALUE(roditeljski_VALUE);
    }

    public int 자식기다리기(Proces_VALUE roditeljski_VALUE, int dijete_identifikator, boolean 기다리지않음) {
        return Alat_za_zakazivanje.자식기다리기(roditeljski_VALUE, dijete_identifikator, 기다리지않음);
    }

    public int program_pauza(Proces_VALUE redovno_Proces, int 새끝) {
        int 이전끝 = redovno_Proces.program_pauza();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / dojaviti_Upravitelj.veličina_stranice;
        int 끝쪽 = (새끝 + dojaviti_Upravitelj.veličina_stranice - 1) / dojaviti_Upravitelj.veličina_stranice;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * dojaviti_Upravitelj.veličina_stranice;
                try {
                    쪽관리.바이트읽기(redovno_Proces.adresa_Space(), adresa);
                } catch (IllegalStateException GREŠKA) {
                    쪽관리.MAP_dojaviti(redovno_Proces.adresa_Space(), adresa, true);
                }
            }
        }
        redovno_Proces.skup_program_pauza(새끝);
        return 새끝;
    }

    public int povećanje_program_pauza(Proces_VALUE redovno_Proces, int inkrement_iznos) {
        int 이전끝 = redovno_Proces.program_pauza();
        int REZULTAT = program_pauza(redovno_Proces, 이전끝 + inkrement_iznos);
        return REZULTAT < 0 ? REZULTAT : 이전끝;
    }

    public int Izvrši_naredba(Proces_VALUE redovno_Proces, byte[] 실행파일) {
        return Izvrši_naredba(redovno_Proces, 실행파일, new String[0], new String[0]);
    }

    public int Izvrši_naredba(Proces_VALUE redovno_Proces, byte[] 실행파일, String[] parametar_argument, String[] okruženje) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = učitavač.검사(실행파일);
        } catch (IllegalArgumentException GREŠKA) {
            return -8;
        }
        if (parametar_argument == null || okruženje == null || parametar_argument.length > 16 || okruženje.length > 16) {
            return -7;
        }
        for (실행파일적재기.sekcija_VALUE sekcija_VALUE : IMAGE_VALUE.구역들()) {
            if ((sekcija_VALUE.zastavica_VALUE() & 2) == 0 || sekcija_VALUE.Veličina() == 0) {
                continue;
            }
            int 첫쪽 = sekcija_VALUE.adresa() / dojaviti_Upravitelj.veličina_stranice;
            int 끝쪽 = (sekcija_VALUE.adresa() + sekcija_VALUE.Veličina() + dojaviti_Upravitelj.veličina_stranice - 1) / dojaviti_Upravitelj.veličina_stranice;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * dojaviti_Upravitelj.veličina_stranice;
                try {
                    쪽관리.바이트읽기(redovno_Proces.adresa_Space(), adresa);
                    쪽관리.privatan_raspon_zapisivanje(redovno_Proces.adresa_Space(), adresa, dojaviti_Upravitelj.veličina_stranice);
                } catch (IllegalStateException GREŠKA) {
                    쪽관리.MAP_dojaviti(redovno_Proces.adresa_Space(), adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < sekcija_VALUE.Veličina(); INDEX++) {
                byte VALUE = sekcija_VALUE.종류() == 8 ? 0 : 실행파일[sekcija_VALUE.Datoteka_položaj() + INDEX];
                쪽관리.zapisivanje_bajt_VALUE(redovno_Proces.adresa_Space(), sekcija_VALUE.adresa() + INDEX, VALUE);
            }
        }
        redovno_Proces.실행문맥설정(IMAGE_VALUE.START_adresa(), parametar_argument, okruženje);
        redovno_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void izlaz_program(Proces_VALUE redovno_Proces, int Stanje_VALUE) {
        redovno_Proces.Izlaz_program(Stanje_VALUE);
    }
}
