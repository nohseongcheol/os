// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.체계호출;

import Bosna_i_Hercegovina.JBihOS.기억공간.stranica_menadžer;
import Bosna_i_Hercegovina.JBihOS.작업.proces_VALUE;
import Bosna_i_Hercegovina.JBihOS.작업.Planer;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.실행파일적재기;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.fajl_sistem;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.fajl_informacija;
import Bosna_i_Hercegovina.JBihOS.jezgro.hardver_VALUE;
import Bosna_i_Hercegovina.JBihOS.입력.입력관리자;
import Bosna_i_Hercegovina.JBihOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int samo_za_čitanje_zastavica = 0;
    public static final int Traži_START = 0;
    public static final int Traži_trenutno = 1;
    public static final int FIND_unos_završiti = 2;

    private final fajl_sistem fajl_sistem;
    private final stranica_menadžer 쪽관리;
    private final Planer Planer;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final hardver_VALUE uređaj_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(fajl_sistem fajl_sistem, stranica_menadžer 쪽관리, Planer Planer, hardver_VALUE uređaj_VALUE, 입력관리자 입력관리) {
        this.fajl_sistem = fajl_sistem;
        this.쪽관리 = 쪽관리;
        this.Planer = Planer;
        this.uređaj_VALUE = uređaj_VALUE;
        this.입력관리 = 입력관리;
    }

    public int proces_identifikator(proces_VALUE trenutno_proces) {
        return trenutno_proces.identifikator_VALUE();
    }

    public int roditelj_proces_identifikator(proces_VALUE trenutno_proces) {
        return trenutno_proces.roditelj_identifikator();
    }

    public int Otvori(proces_VALUE trenutno_proces, String Naziv, int zastavica_VALUE) {
        if (zastavica_VALUE != samo_za_čitanje_zastavica) {
            return -30;
        }
        return trenutno_proces.파일서술자().Otvori(Naziv);
    }

    public int Čitaj(proces_VALUE trenutno_proces, int 서술자, byte[] 받을곳, int Veličina) {
        if (서술자 == 0) {
            if (Veličina <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 događaj = 입력관리.Dalje_događaj();
            if (događaj == null || događaj.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) događaj.첫째값();
            return 1;
        }
        return trenutno_proces.파일서술자().Čitaj(서술자, 받을곳, Veličina);
    }

    public int Piši(proces_VALUE trenutno_proces, int 서술자, byte[] podaci, int Veličina) {
        if (서술자 != 1 && 서술자 != 2) {
            return trenutno_proces.파일서술자().odjel_za_informacijske_tehnologije_kreirati(서술자) ? -30 : -9;
        }
        if (Veličina < 0 || Veličina > podaci.length) {
            return -22;
        }
        uređaj_VALUE.직렬출력(new String(podaci, 0, Veličina, java.nio.charset.StandardCharsets.UTF_8));
        return Veličina;
    }

    public int Zatvori(proces_VALUE trenutno_proces, int 서술자) {
        return trenutno_proces.파일서술자().Zatvori(서술자);
    }

    public int pomaći_položaj(proces_VALUE trenutno_proces, int 서술자, int 거리, int projicirati_koijen) {
        return trenutno_proces.파일서술자().pomaći_položaj(서술자, 거리, projicirati_koijen);
    }

    public int 서술자복제(proces_VALUE trenutno_proces, int 서술자) {
        return trenutno_proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(proces_VALUE trenutno_proces, int 서술자, int 새서술자) {
        return trenutno_proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Naziv, int metoda_mod) {
        fajl_informacija msinfo32_exe = fajl_sistem.msinfo32_exe(Naziv);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metoda_mod & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metoda_mod & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_spisak_zadataka(String Naziv) {
        return "/".equals(Naziv) ? 0 : -20;
    }

    public String trenutno_spisak_zadataka(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int korisnik_identifikator() { return 0; }
    public int djelotvoran_korisnik_identifikator() { return 0; }
    public int Grupa_identifikator() { return 0; }
    public int djelotvoran_Grupa_identifikator() { return 0; }

    public int sinhronizirati_fajl(proces_VALUE trenutno_proces, int 서술자) {
        return trenutno_proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // trenutno_stavka 파일체계는 Čitaj 전용이어서 밀어낼 자료가 없다.
    }

    public boolean odjel_za_informacijske_tehnologije_Terminal(proces_VALUE trenutno_proces, int 서술자) {
        fajl_informacija msinfo32_exe = trenutno_proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fajl_kontrola(proces_VALUE trenutno_proces, int 서술자, int Naredba, int parametar_argument) {
        if (Naredba == 0) {
            return trenutno_proces.파일서술자().복제서술자(서술자, parametar_argument);
        }
        if (Naredba == 1) {
            return trenutno_proces.파일서술자().실행시닫기값(서술자);
        }
        if (Naredba == 2) {
            return trenutno_proces.파일서술자().실행시닫기설정(서술자, (parametar_argument & 1) != 0);
        }
        if (Naredba == 3) {
            return trenutno_proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : samo_za_čitanje_zastavica;
        }
        if (Naredba == 4) {
            return parametar_argument == samo_za_čitanje_zastavica ? 0 : -30;
        }
        return -22;
    }

    public int Create_unos(String Naziv, int dozvola_VALUE) {
        return -30;
    }

    public fajl_informacija 서술자정보(proces_VALUE trenutno_proces, int 서술자) {
        return trenutno_proces.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Detalji sistem_Detalji() {
        return new sistem_Detalji("JBihOS", "JBihOS", "0.1", "Java managed kernel", "i386");
    }

    public fajl_informacija fajl_informacija(String Naziv) {
        return fajl_sistem.msinfo32_exe(Naziv);
    }

    public proces_VALUE 과정복제(proces_VALUE roditelj_VALUE) {
        return Planer.복제(roditelj_VALUE);
    }

    public int 자식기다리기(proces_VALUE roditelj_VALUE, int dijete_identifikator, boolean 기다리지않음) {
        return Planer.자식기다리기(roditelj_VALUE, dijete_identifikator, 기다리지않음);
    }

    public int 프로그램끝(proces_VALUE trenutno_proces, int 새끝) {
        int 이전끝 = trenutno_proces.프로그램끝();
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
                    쪽관리.바이트읽기(trenutno_proces.adresa_prostor(), adresa);
                } catch (IllegalStateException GRESKA) {
                    쪽관리.MAP_stranica(trenutno_proces.adresa_prostor(), adresa, true);
                }
            }
        }
        trenutno_proces.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(proces_VALUE trenutno_proces, int 증가량) {
        int 이전끝 = trenutno_proces.프로그램끝();
        int mjera = 프로그램끝(trenutno_proces, 이전끝 + 증가량);
        return mjera < 0 ? mjera : 이전끝;
    }

    public int Izvrši_komanda(proces_VALUE trenutno_proces, byte[] 실행파일) {
        return Izvrši_komanda(trenutno_proces, 실행파일, new String[0], new String[0]);
    }

    public int Izvrši_komanda(proces_VALUE trenutno_proces, byte[] 실행파일, String[] parametar_argument, String[] operativno_okruženje) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException GRESKA) {
            return -8;
        }
        if (parametar_argument == null || operativno_okruženje == null || parametar_argument.length > 16 || operativno_okruženje.length > 16) {
            return -7;
        }
        for (실행파일적재기.sekcija_VALUE sekcija_VALUE : IMAGE_VALUE.구역들()) {
            if ((sekcija_VALUE.zastavica_VALUE() & 2) == 0 || sekcija_VALUE.Veličina() == 0) {
                continue;
            }
            int 첫쪽 = sekcija_VALUE.adresa() / stranica_menadžer.veličina_stranice;
            int 끝쪽 = (sekcija_VALUE.adresa() + sekcija_VALUE.Veličina() + stranica_menadžer.veličina_stranice - 1) / stranica_menadžer.veličina_stranice;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * stranica_menadžer.veličina_stranice;
                try {
                    쪽관리.바이트읽기(trenutno_proces.adresa_prostor(), adresa);
                    쪽관리.범위개인쓰기(trenutno_proces.adresa_prostor(), adresa, stranica_menadžer.veličina_stranice);
                } catch (IllegalStateException GRESKA) {
                    쪽관리.MAP_stranica(trenutno_proces.adresa_prostor(), adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < sekcija_VALUE.Veličina(); INDEX++) {
                byte VALUE = sekcija_VALUE.종류() == 8 ? 0 : 실행파일[sekcija_VALUE.fajl_položaj() + INDEX];
                쪽관리.pisati_bajt_VALUE(trenutno_proces.adresa_prostor(), sekcija_VALUE.adresa() + INDEX, VALUE);
            }
        }
        trenutno_proces.실행문맥설정(IMAGE_VALUE.početna_adresa(), parametar_argument, operativno_okruženje);
        trenutno_proces.파일서술자().실행시닫기();
        return 0;
    }

    public void izađi_program(proces_VALUE trenutno_proces, int stanje_VALUE) {
        trenutno_proces.izaći_program(stanje_VALUE);
    }
}
