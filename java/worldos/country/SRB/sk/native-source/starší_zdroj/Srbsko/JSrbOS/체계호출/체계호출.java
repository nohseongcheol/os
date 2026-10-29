// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbsko.JSrbOS.체계호출;

import Srbsko.JSrbOS.Pamäť_oblasť.쪽관리자;
import Srbsko.JSrbOS.작업.Proces_VALUE;
import Srbsko.JSrbOS.작업.Plánovač;
import Srbsko.JSrbOS.systém_súborov.spustiteľný_súbor_zavádzací_program;
import Srbsko.JSrbOS.systém_súborov.systém_súborov;
import Srbsko.JSrbOS.systém_súborov.Súbor_informácia;
import Srbsko.JSrbOS.jadro.hardvér_VALUE;
import Srbsko.JSrbOS.vstup_VALUE.입력관리자;
import Srbsko.JSrbOS.vstup_VALUE.vstup_udalosť;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int iba_na_čítanie_príznak = 0;
    public static final int Hľadať_START = 0;
    public static final int Hľadať_v_termíne_splatnosti = 1;
    public static final int FIND_položka_ukončiť_hovor = 2;

    private final systém_súborov systém_súborov;
    private final 쪽관리자 쪽관리;
    private final Plánovač Plánovač;
    private final spustiteľný_súbor_zavádzací_program zavádzací_program = new spustiteľný_súbor_zavádzací_program();
    private final hardvér_VALUE telefón_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(systém_súborov systém_súborov, 쪽관리자 쪽관리, Plánovač Plánovač, hardvér_VALUE telefón_VALUE, 입력관리자 입력관리) {
        this.systém_súborov = systém_súborov;
        this.쪽관리 = 쪽관리;
        this.Plánovač = Plánovač;
        this.telefón_VALUE = telefón_VALUE;
        this.입력관리 = 입력관리;
    }

    public int PID(Proces_VALUE v_termíne_splatnosti_Proces) {
        return v_termíne_splatnosti_Proces.identifikátor_VALUE();
    }

    public int nadradený_PID(Proces_VALUE v_termíne_splatnosti_Proces) {
        return v_termíne_splatnosti_Proces.nadradený_identifikátor();
    }

    public int Otvoriť(Proces_VALUE v_termíne_splatnosti_Proces, String Názov, int príznak_VALUE) {
        if (príznak_VALUE != iba_na_čítanie_príznak) {
            return -30;
        }
        return v_termíne_splatnosti_Proces.파일서술자().Otvoriť(Názov);
    }

    public int Čítanie(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자, byte[] dostať_cieľ, int Veľkosť) {
        if (서술자 == 0) {
            if (Veľkosť <= 0 || dostať_cieľ.length == 0) {
                return 0;
            }
            vstup_udalosť Udalosť = 입력관리.Ďalej_udalosť();
            if (Udalosť == null || Udalosť.druh_udalosti() != vstup_udalosť.종류.키누름) {
                return -11;
            }
            dostať_cieľ[0] = (byte) Udalosť.첫째값();
            return 1;
        }
        return v_termíne_splatnosti_Proces.파일서술자().Čítanie(서술자, dostať_cieľ, Veľkosť);
    }

    public int Zápis(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자, byte[] údaje, int Veľkosť) {
        if (서술자 != 1 && 서술자 != 2) {
            return v_termíne_splatnosti_Proces.파일서술자().Informačné_systémy_otvoriť(서술자) ? -30 : -9;
        }
        if (Veľkosť < 0 || Veľkosť > údaje.length) {
            return -22;
        }
        telefón_VALUE.직렬출력(new String(údaje, 0, Veľkosť, java.nio.charset.StandardCharsets.UTF_8));
        return Veľkosť;
    }

    public int Zatvoriť(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자) {
        return v_termíne_splatnosti_Proces.파일서술자().Zatvoriť(서술자);
    }

    public int premiestniť_pozícia(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자, int 거리, int akcia_koreň) {
        return v_termíne_splatnosti_Proces.파일서술자().premiestniť_pozícia(서술자, 거리, akcia_koreň);
    }

    public int 서술자복제(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자) {
        return v_termíne_splatnosti_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자, int 새서술자) {
        return v_termíne_splatnosti_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Názov, int metóda_MODE) {
        Súbor_informácia Systémové_informácie = systém_súborov.Systémové_informácie(Názov);
        if (Systémové_informácie == null) {
            return -2;
        }
        if ((metóda_MODE & 1) != 0 && (Systémové_informácie.형태() & 0111) == 0) {
            return -13;
        }
        if ((metóda_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_zoznam_úloh(String Názov) {
        return "/".equals(Názov) ? 0 : -20;
    }

    public String v_termíne_splatnosti_zoznam_úloh(int dostať_zmeniť_veľkosť) {
        return dostať_zmeniť_veľkosť >= 2 ? "/" : null;
    }

    public int identifikácia_používateľa() { return 0; }
    public int účinný_identifikácia_používateľa() { return 0; }
    public int Skupina_identifikátor() { return 0; }
    public int účinný_Skupina_identifikátor() { return 0; }

    public int synchronizovať_Súbor(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자) {
        return v_termíne_splatnosti_Proces.파일서술자().Systémové_informácie(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // v_termíne_splatnosti_položka 파일체계는 Čítanie 전용이어서 밀어낼 자료가 없다.
    }

    public boolean Informačné_systémy_Terminál(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자) {
        Súbor_informácia Systémové_informácie = v_termíne_splatnosti_Proces.파일서술자().Systémové_informácie(서술자);
        return Systémové_informácie != null && (Systémové_informácie.형태() & 0170000) == 0020000;
    }

    public int Súbor_riadenie(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자, int Príkaz, int parameter_argument) {
        if (Príkaz == 0) {
            return v_termíne_splatnosti_Proces.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (Príkaz == 1) {
            return v_termíne_splatnosti_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (Príkaz == 2) {
            return v_termíne_splatnosti_Proces.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (Príkaz == 3) {
            return v_termíne_splatnosti_Proces.파일서술자().Systémové_informácie(서술자) == null ? -9 : iba_na_čítanie_príznak;
        }
        if (Príkaz == 4) {
            return parameter_argument == iba_na_čítanie_príznak ? 0 : -30;
        }
        return -22;
    }

    public int Create_položka(String Názov, int povolenie_VALUE) {
        return -30;
    }

    public Súbor_informácia 서술자정보(Proces_VALUE v_termíne_splatnosti_Proces, int 서술자) {
        return v_termíne_splatnosti_Proces.파일서술자().Systémové_informácie(서술자);
    }

    public systém_Podrobnosti systém_Podrobnosti() {
        return new systém_Podrobnosti("JSrbOS", "JSrbOS", "0.1", "Java managed kernel", "i386");
    }

    public Súbor_informácia Súbor_informácia(String Názov) {
        return systém_súborov.Systémové_informácie(Názov);
    }

    public Proces_VALUE klon_Proces(Proces_VALUE nadradený_VALUE) {
        return Plánovač.klon_VALUE(nadradený_VALUE);
    }

    public int 자식기다리기(Proces_VALUE nadradený_VALUE, int dieťa_identifikátor, boolean 기다리지않음) {
        return Plánovač.자식기다리기(nadradený_VALUE, dieťa_identifikátor, 기다리지않음);
    }

    public int program_prerušiť(Proces_VALUE v_termíne_splatnosti_Proces, int 새끝) {
        int 이전끝 = v_termíne_splatnosti_Proces.program_prerušiť();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / 쪽관리자.veľkosť_stránky;
        int 끝쪽 = (새끝 + 쪽관리자.veľkosť_stránky - 1) / 쪽관리자.veľkosť_stránky;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * 쪽관리자.veľkosť_stránky;
                try {
                    쪽관리.바이트읽기(v_termíne_splatnosti_Proces.adresa_priestor(), adresa);
                } catch (IllegalStateException chyba) {
                    쪽관리.MAP_strana(v_termíne_splatnosti_Proces.adresa_priestor(), adresa, true);
                }
            }
        }
        v_termíne_splatnosti_Proces.množina_program_prerušiť(새끝);
        return 새끝;
    }

    public int zvýšenie_program_prerušiť(Proces_VALUE v_termíne_splatnosti_Proces, int prírastok_suma) {
        int 이전끝 = v_termíne_splatnosti_Proces.program_prerušiť();
        int KR = program_prerušiť(v_termíne_splatnosti_Proces, 이전끝 + prírastok_suma);
        return KR < 0 ? KR : 이전끝;
    }

    public int Vykonať_príkaz(Proces_VALUE v_termíne_splatnosti_Proces, byte[] spustiteľný_súbor) {
        return Vykonať_príkaz(v_termíne_splatnosti_Proces, spustiteľný_súbor, new String[0], new String[0]);
    }

    public int Vykonať_príkaz(Proces_VALUE v_termíne_splatnosti_Proces, byte[] spustiteľný_súbor, String[] parameter_argument, String[] 환경) {
        spustiteľný_súbor_zavádzací_program.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = zavádzací_program.검사(spustiteľný_súbor);
        } catch (IllegalArgumentException chyba) {
            return -8;
        }
        if (parameter_argument == null || 환경 == null || parameter_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (spustiteľný_súbor_zavádzací_program.sekcia_VALUE sekcia_VALUE : IMAGE_VALUE.구역들()) {
            if ((sekcia_VALUE.príznak_VALUE() & 2) == 0 || sekcia_VALUE.Veľkosť() == 0) {
                continue;
            }
            int 첫쪽 = sekcia_VALUE.adresa() / 쪽관리자.veľkosť_stránky;
            int 끝쪽 = (sekcia_VALUE.adresa() + sekcia_VALUE.Veľkosť() + 쪽관리자.veľkosť_stránky - 1) / 쪽관리자.veľkosť_stránky;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * 쪽관리자.veľkosť_stránky;
                try {
                    쪽관리.바이트읽기(v_termíne_splatnosti_Proces.adresa_priestor(), adresa);
                    쪽관리.súkromné_rozsah_zapísať(v_termíne_splatnosti_Proces.adresa_priestor(), adresa, 쪽관리자.veľkosť_stránky);
                } catch (IllegalStateException chyba) {
                    쪽관리.MAP_strana(v_termíne_splatnosti_Proces.adresa_priestor(), adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < sekcia_VALUE.Veľkosť(); INDEX++) {
                byte VALUE = sekcia_VALUE.종류() == 8 ? 0 : spustiteľný_súbor[sekcia_VALUE.Súbor_pozícia() + INDEX];
                쪽관리.zapísať_Byte_VALUE(v_termíne_splatnosti_Proces.adresa_priestor(), sekcia_VALUE.adresa() + INDEX, VALUE);
            }
        }
        v_termíne_splatnosti_Proces.실행문맥설정(IMAGE_VALUE.START_adresa(), parameter_argument, 환경);
        v_termíne_splatnosti_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void ukončiť_program(Proces_VALUE v_termíne_splatnosti_Proces, int Stav_VALUE) {
        v_termíne_splatnosti_Proces.Skončiť_program(Stav_VALUE);
    }
}
