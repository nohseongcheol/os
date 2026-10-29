// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.체계호출;

import Italija.JItaOS.pomnilnik_območje.stran_Upravitelj;
import Italija.JItaOS.작업.Proces_VALUE;
import Italija.JItaOS.작업.Načrtovalec;
import Italija.JItaOS.datotečni_sistem.실행파일적재기;
import Italija.JItaOS.datotečni_sistem.datotečni_sistem;
import Italija.JItaOS.datotečni_sistem.Datoteka_informacije;
import Italija.JItaOS.jedro.strojna_oprema_VALUE;
import Italija.JItaOS.입력.입력관리자;
import Italija.JItaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int samo_za_branje_zastavica = 0;
    public static final int Išči_Start = 0;
    public static final int Išči_sprotno = 1;
    public static final int FIND_vnos_končati_klic = 2;

    private final datotečni_sistem datotečni_sistem;
    private final stran_Upravitelj 쪽관리;
    private final Načrtovalec Načrtovalec;
    private final 실행파일적재기 nalagalnik = new 실행파일적재기();
    private final strojna_oprema_VALUE naprava_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(datotečni_sistem datotečni_sistem, stran_Upravitelj 쪽관리, Načrtovalec Načrtovalec, strojna_oprema_VALUE naprava_VALUE, 입력관리자 입력관리) {
        this.datotečni_sistem = datotečni_sistem;
        this.쪽관리 = 쪽관리;
        this.Načrtovalec = Načrtovalec;
        this.naprava_VALUE = naprava_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikator(Proces_VALUE sprotno_Proces) {
        return sprotno_Proces.identifikator_VALUE();
    }

    public int nadrejen_Proces_identifikator(Proces_VALUE sprotno_Proces) {
        return sprotno_Proces.nadrejen_identifikator();
    }

    public int Odpri(Proces_VALUE sprotno_Proces, String Ime, int zastavica_VALUE) {
        if (zastavica_VALUE != samo_za_branje_zastavica) {
            return -30;
        }
        return sprotno_Proces.파일서술자().Odpri(Ime);
    }

    public int Branje(Proces_VALUE sprotno_Proces, int 서술자, byte[] sprejeti_sprejemati_prejeti_prejemati_cilj, int Velikost) {
        if (서술자 == 0) {
            if (Velikost <= 0 || sprejeti_sprejemati_prejeti_prejemati_cilj.length == 0) {
                return 0;
            }
            입력사건 dogodek = 입력관리.Naprej_dogodek();
            if (dogodek == null || dogodek.vrsta_dogodka() != 입력사건.종류.Ključ_ne_deluje) {
                return -11;
            }
            sprejeti_sprejemati_prejeti_prejemati_cilj[0] = (byte) dogodek.첫째값();
            return 1;
        }
        return sprotno_Proces.파일서술자().Branje(서술자, sprejeti_sprejemati_prejeti_prejemati_cilj, Velikost);
    }

    public int Pisanje(Proces_VALUE sprotno_Proces, int 서술자, byte[] podatki, int Velikost) {
        if (서술자 != 1 && 서술자 != 2) {
            return sprotno_Proces.파일서술자().informacijska_tehnologija_odprto(서술자) ? -30 : -9;
        }
        if (Velikost < 0 || Velikost > podatki.length) {
            return -22;
        }
        naprava_VALUE.직렬출력(new String(podatki, 0, Velikost, java.nio.charset.StandardCharsets.UTF_8));
        return Velikost;
    }

    public int Zapri(Proces_VALUE sprotno_Proces, int 서술자) {
        return sprotno_Proces.파일서술자().Zapri(서술자);
    }

    public int premikati_položaj(Proces_VALUE sprotno_Proces, int 서술자, int 거리, int pobuda_koren) {
        return sprotno_Proces.파일서술자().premikati_položaj(서술자, 거리, pobuda_koren);
    }

    public int 서술자복제(Proces_VALUE sprotno_Proces, int 서술자) {
        return sprotno_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE sprotno_Proces, int 서술자, int 새서술자) {
        return sprotno_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ime, int metoda_MODE) {
        Datoteka_informacije msinfo32_exe = datotečni_sistem.msinfo32_exe(Ime);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metoda_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metoda_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_seznam_opravil(String Ime) {
        return "/".equals(Ime) ? 0 : -20;
    }

    public String sprotno_seznam_opravil(int sprejeti_sprejemati_prejeti_prejemati_spremeniti_velikost) {
        return sprejeti_sprejemati_prejeti_prejemati_spremeniti_velikost >= 2 ? "/" : null;
    }

    public int ID_uporabnika() { return 0; }
    public int učinkovito_ID_uporabnika() { return 0; }
    public int Skupina_identifikator() { return 0; }
    public int učinkovito_Skupina_identifikator() { return 0; }

    public int sinhronizirati_Datoteka(Proces_VALUE sprotno_Proces, int 서술자) {
        return sprotno_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // sprotno_element 파일체계는 Branje 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informacijska_tehnologija_Terminal(Proces_VALUE sprotno_Proces, int 서술자) {
        Datoteka_informacije msinfo32_exe = sprotno_Proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Datoteka_nadzor(Proces_VALUE sprotno_Proces, int 서술자, int Ukaz, int parameter_argument) {
        if (Ukaz == 0) {
            return sprotno_Proces.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (Ukaz == 1) {
            return sprotno_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (Ukaz == 2) {
            return sprotno_Proces.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (Ukaz == 3) {
            return sprotno_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : samo_za_branje_zastavica;
        }
        if (Ukaz == 4) {
            return parameter_argument == samo_za_branje_zastavica ? 0 : -30;
        }
        return -22;
    }

    public int Ustvari_vnos(String Ime, int dovoljenje_VALUE) {
        return -30;
    }

    public Datoteka_informacije 서술자정보(Proces_VALUE sprotno_Proces, int 서술자) {
        return sprotno_Proces.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Podrobnosti sistem_Podrobnosti() {
        return new sistem_Podrobnosti("JItaOS", "JItaOS", "0.1", "Java managed kernel", "i386");
    }

    public Datoteka_informacije Datoteka_informacije(String Ime) {
        return datotečni_sistem.msinfo32_exe(Ime);
    }

    public Proces_VALUE klon_Proces(Proces_VALUE nadrejen_VALUE) {
        return Načrtovalec.klon_VALUE(nadrejen_VALUE);
    }

    public int 자식기다리기(Proces_VALUE nadrejen_VALUE, int otrok_identifikator, boolean 기다리지않음) {
        return Načrtovalec.자식기다리기(nadrejen_VALUE, otrok_identifikator, 기다리지않음);
    }

    public int aplikacija_odmor(Proces_VALUE sprotno_Proces, int 새끝) {
        int 이전끝 = sprotno_Proces.aplikacija_odmor();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / stran_Upravitelj.velikost_strani;
        int 끝쪽 = (새끝 + stran_Upravitelj.velikost_strani - 1) / stran_Upravitelj.velikost_strani;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int naslov = INDEX * stran_Upravitelj.velikost_strani;
                try {
                    쪽관리.바이트읽기(sprotno_Proces.naslov_Space(), naslov);
                } catch (IllegalStateException NAPAKA) {
                    쪽관리.MAP_stran(sprotno_Proces.naslov_Space(), naslov, true);
                }
            }
        }
        sprotno_Proces.nabor_aplikacija_odmor(새끝);
        return 새끝;
    }

    public int povečanje_aplikacija_odmor(Proces_VALUE sprotno_Proces, int 증가량) {
        int 이전끝 = sprotno_Proces.aplikacija_odmor();
        int REZULTAT = aplikacija_odmor(sprotno_Proces, 이전끝 + 증가량);
        return REZULTAT < 0 ? REZULTAT : 이전끝;
    }

    public int Izvedi_ukaz(Proces_VALUE sprotno_Proces, byte[] 실행파일) {
        return Izvedi_ukaz(sprotno_Proces, 실행파일, new String[0], new String[0]);
    }

    public int Izvedi_ukaz(Proces_VALUE sprotno_Proces, byte[] 실행파일, String[] parameter_argument, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = nalagalnik.검사(실행파일);
        } catch (IllegalArgumentException NAPAKA) {
            return -8;
        }
        if (parameter_argument == null || 환경 == null || parameter_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.odsek_VALUE odsek_VALUE : IMAGE_VALUE.구역들()) {
            if ((odsek_VALUE.zastavica_VALUE() & 2) == 0 || odsek_VALUE.Velikost() == 0) {
                continue;
            }
            int 첫쪽 = odsek_VALUE.naslov() / stran_Upravitelj.velikost_strani;
            int 끝쪽 = (odsek_VALUE.naslov() + odsek_VALUE.Velikost() + stran_Upravitelj.velikost_strani - 1) / stran_Upravitelj.velikost_strani;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int naslov = INDEX * stran_Upravitelj.velikost_strani;
                try {
                    쪽관리.바이트읽기(sprotno_Proces.naslov_Space(), naslov);
                    쪽관리.zasebno_obseg_pisati(sprotno_Proces.naslov_Space(), naslov, stran_Upravitelj.velikost_strani);
                } catch (IllegalStateException NAPAKA) {
                    쪽관리.MAP_stran(sprotno_Proces.naslov_Space(), naslov, true);
                }
            }
            for (int INDEX = 0; INDEX < odsek_VALUE.Velikost(); INDEX++) {
                byte VALUE = odsek_VALUE.종류() == 8 ? 0 : 실행파일[odsek_VALUE.Datoteka_položaj() + INDEX];
                쪽관리.pisati_bajt_VALUE(sprotno_Proces.naslov_Space(), odsek_VALUE.naslov() + INDEX, VALUE);
            }
        }
        sprotno_Proces.실행문맥설정(IMAGE_VALUE.Start_naslov(), parameter_argument, 환경);
        sprotno_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void izhod_aplikacija(Proces_VALUE sprotno_Proces, int stanje_VALUE) {
        sprotno_Proces.Izhod_aplikacija(stanje_VALUE);
    }
}
