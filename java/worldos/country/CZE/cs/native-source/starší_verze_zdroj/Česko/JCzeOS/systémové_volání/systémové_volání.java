// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systémové_volání;

import Česko.JCzeOS.Paměť_oblast.stránka_Správce;
import Česko.JCzeOS.작업.Proces_HODNOTA;
import Česko.JCzeOS.작업.Plánovač;
import Česko.JCzeOS.systém_souborů.spustitelný_zavaděč;
import Česko.JCzeOS.systém_souborů.systém_souborů;
import Česko.JCzeOS.systém_souborů.Soubor_informace;
import Česko.JCzeOS.jádro.hardware_HODNOTA;
import Česko.JCzeOS.vstup_HODNOTA.vstup_Správce;
import Česko.JCzeOS.vstup_HODNOTA.vstup_událost;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class systémové_volání {
    public static final int jen_pro_čtení_příznak = 0;
    public static final int HLEDAT_START = 0;
    public static final int HLEDAT_dobrá = 1;
    public static final int NAJÍT_položka_konec = 2;

    private final systém_souborů systém_souborů;
    private final stránka_Správce 쪽관리;
    private final Plánovač Plánovač;
    private final spustitelný_zavaděč zavaděč = new spustitelný_zavaděč();
    private final hardware_HODNOTA mobilní_HODNOTA;
    private final vstup_Správce 입력관리;

    public systémové_volání(systém_souborů systém_souborů, stránka_Správce 쪽관리, Plánovač Plánovač, hardware_HODNOTA mobilní_HODNOTA, vstup_Správce 입력관리) {
        this.systém_souborů = systém_souborů;
        this.쪽관리 = 쪽관리;
        this.Plánovač = Plánovač;
        this.mobilní_HODNOTA = mobilní_HODNOTA;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikátor(Proces_HODNOTA dobrá_Proces) {
        return dobrá_Proces.identifikátor_HODNOTA();
    }

    public int nadřazený_Proces_identifikátor(Proces_HODNOTA dobrá_Proces) {
        return dobrá_Proces.nadřazený_identifikátor();
    }

    public int Otevřít(Proces_HODNOTA dobrá_Proces, String Název, int příznak_HODNOTA) {
        if (příznak_HODNOTA != jen_pro_čtení_příznak) {
            return -30;
        }
        return dobrá_Proces.Soubor_popisovač().Otevřít(Název);
    }

    public int Čtení(Proces_HODNOTA dobrá_Proces, int popisovač_položka, byte[] dostat_cíl, int Velikost) {
        if (popisovač_položka == 0) {
            if (Velikost <= 0 || dostat_cíl.length == 0) {
                return 0;
            }
            vstup_událost Události = 입력관리.Další_událost();
            if (Události == null || Události.událost_Druh() != vstup_událost.Druh_HODNOTA.Klíč_mimo_provoz) {
                return -11;
            }
            dostat_cíl[0] = (byte) Události.첫째값();
            return 1;
        }
        return dobrá_Proces.Soubor_popisovač().Čtení(popisovač_položka, dostat_cíl, Velikost);
    }

    public int Zápis(Proces_HODNOTA dobrá_Proces, int popisovač_položka, byte[] data, int Velikost) {
        if (popisovač_položka != 1 && popisovač_položka != 2) {
            return dobrá_Proces.Soubor_popisovač().informační_systémy_otevřít(popisovač_položka) ? -30 : -9;
        }
        if (Velikost < 0 || Velikost > data.length) {
            return -22;
        }
        mobilní_HODNOTA.직렬출력(new String(data, 0, Velikost, java.nio.charset.StandardCharsets.UTF_8));
        return Velikost;
    }

    public int Zavřené(Proces_HODNOTA dobrá_Proces, int popisovač_položka) {
        return dobrá_Proces.Soubor_popisovač().Zavřené(popisovač_položka);
    }

    public int přesunout_pozice(Proces_HODNOTA dobrá_Proces, int popisovač_položka, int 거리, int akce_kořen) {
        return dobrá_Proces.Soubor_popisovač().přesunout_pozice(popisovač_položka, 거리, akce_kořen);
    }

    public int duplikát_popisovač(Proces_HODNOTA dobrá_Proces, int popisovač_položka) {
        return dobrá_Proces.Soubor_popisovač().복제서술자(popisovač_položka, 0);
    }

    public int 지정서술자복제(Proces_HODNOTA dobrá_Proces, int popisovač_položka, int 새서술자) {
        return dobrá_Proces.Soubor_popisovač().지정복제(popisovač_položka, 새서술자);
    }

    public int 접근가능(String Název, int metoda_MODE) {
        Soubor_informace Informace_o_systému = systém_souborů.Informace_o_systému(Název);
        if (Informace_o_systému == null) {
            return -2;
        }
        if ((metoda_MODE & 1) != 0 && (Informace_o_systému.tvar_Druh() & 0111) == 0) {
            return -13;
        }
        if ((metoda_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_Seznam_úkolů(String Název) {
        return "/".equals(Název) ? 0 : -20;
    }

    public String dobrá_Seznam_úkolů(int dostat_změnit_velikost) {
        return dostat_změnit_velikost >= 2 ? "/" : null;
    }

    public int ID_uživatele() { return 0; }
    public int efektivní_ID_uživatele() { return 0; }
    public int ID_skupiny() { return 0; }
    public int efektivní_ID_skupiny() { return 0; }

    public int synchronizovat_Soubor(Proces_HODNOTA dobrá_Proces, int popisovač_položka) {
        return dobrá_Proces.Soubor_popisovač().Informace_o_systému(popisovač_položka) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // dobrá_zboží 파일체계는 Čtení 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informační_systémy_Terminál(Proces_HODNOTA dobrá_Proces, int popisovač_položka) {
        Soubor_informace Informace_o_systému = dobrá_Proces.Soubor_popisovač().Informace_o_systému(popisovač_položka);
        return Informace_o_systému != null && (Informace_o_systému.tvar_Druh() & 0170000) == 0020000;
    }

    public int řízení_souboru(Proces_HODNOTA dobrá_Proces, int popisovač_položka, int příkaz, int parametr_argument) {
        if (příkaz == 0) {
            return dobrá_Proces.Soubor_popisovač().복제서술자(popisovač_položka, parametr_argument);
        }
        if (příkaz == 1) {
            return dobrá_Proces.Soubor_popisovač().실행시닫기값(popisovač_položka);
        }
        if (příkaz == 2) {
            return dobrá_Proces.Soubor_popisovač().실행시닫기설정(popisovač_položka, (parametr_argument & 1) != 0);
        }
        if (příkaz == 3) {
            return dobrá_Proces.Soubor_popisovač().Informace_o_systému(popisovač_položka) == null ? -9 : jen_pro_čtení_příznak;
        }
        if (příkaz == 4) {
            return parametr_argument == jen_pro_čtení_příznak ? 0 : -30;
        }
        return -22;
    }

    public int Create_položka(String Název, int oprávnění_HODNOTA) {
        return -30;
    }

    public Soubor_informace popisovač_informace(Proces_HODNOTA dobrá_Proces, int popisovač_položka) {
        return dobrá_Proces.Soubor_popisovač().Informace_o_systému(popisovač_položka);
    }

    public Systém_Podrobnosti Systém_Podrobnosti() {
        return new Systém_Podrobnosti("JCzeOS", "JCzeOS", "0.1", "Java managed kernel", "i386");
    }

    public Soubor_informace Soubor_informace(String Název) {
        return systém_souborů.Informace_o_systému(Název);
    }

    public Proces_HODNOTA klon_Proces(Proces_HODNOTA nadřazený_HODNOTA) {
        return Plánovač.klon_HODNOTA(nadřazený_HODNOTA);
    }

    public int 자식기다리기(Proces_HODNOTA nadřazený_HODNOTA, int dítě_identifikátor, boolean 기다리지않음) {
        return Plánovač.자식기다리기(nadřazený_HODNOTA, dítě_identifikátor, 기다리지않음);
    }

    public int program_přerušení(Proces_HODNOTA dobrá_Proces, int 새끝) {
        int Předchozí_konec = dobrá_Proces.program_přerušení();
        if (새끝 == 0) {
            return Předchozí_konec;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Předchozí_konec / stránka_Správce.velikost_stránky;
        int 끝쪽 = (새끝 + stránka_Správce.velikost_stránky - 1) / stránka_Správce.velikost_stránky;
        if (새끝 > Předchozí_konec) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adresa = INDEX * stránka_Správce.velikost_stránky;
                try {
                    쪽관리.바이트읽기(dobrá_Proces.adresní_prostor(), Adresa);
                } catch (IllegalStateException chyba) {
                    쪽관리.MAP_stránka(dobrá_Proces.adresní_prostor(), Adresa, true);
                }
            }
        }
        dobrá_Proces.sada_program_přerušení(새끝);
        return 새끝;
    }

    public int zvýšení_program_přerušení(Proces_HODNOTA dobrá_Proces, int 증가량) {
        int Předchozí_konec = dobrá_Proces.program_přerušení();
        int VÝSLEDEK = program_přerušení(dobrá_Proces, Předchozí_konec + 증가량);
        return VÝSLEDEK < 0 ? VÝSLEDEK : Předchozí_konec;
    }

    public int Provést_příkaz(Proces_HODNOTA dobrá_Proces, byte[] spustitelný_soubor) {
        return Provést_příkaz(dobrá_Proces, spustitelný_soubor, new String[0], new String[0]);
    }

    public int Provést_příkaz(Proces_HODNOTA dobrá_Proces, byte[] spustitelný_soubor, String[] parametr_argument, String[] prostředí_5d36e09c) {
        spustitelný_zavaděč.image image_HODNOTA;
        try {
            image_HODNOTA = zavaděč.검사(spustitelný_soubor);
        } catch (IllegalArgumentException chyba) {
            return -8;
        }
        if (parametr_argument == null || prostředí_5d36e09c == null || parametr_argument.length > 16 || prostředí_5d36e09c.length > 16) {
            return -7;
        }
        for (spustitelný_zavaděč.oddíl_HODNOTA_366e0bfa oddíl_HODNOTA_366e0bfa : image_HODNOTA.구역들()) {
            if ((oddíl_HODNOTA_366e0bfa.příznak_HODNOTA() & 2) == 0 || oddíl_HODNOTA_366e0bfa.Velikost() == 0) {
                continue;
            }
            int 첫쪽 = oddíl_HODNOTA_366e0bfa.Adresa() / stránka_Správce.velikost_stránky;
            int 끝쪽 = (oddíl_HODNOTA_366e0bfa.Adresa() + oddíl_HODNOTA_366e0bfa.Velikost() + stránka_Správce.velikost_stránky - 1) / stránka_Správce.velikost_stránky;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adresa = INDEX * stránka_Správce.velikost_stránky;
                try {
                    쪽관리.바이트읽기(dobrá_Proces.adresní_prostor(), Adresa);
                    쪽관리.soukromý_oblast_zápis(dobrá_Proces.adresní_prostor(), Adresa, stránka_Správce.velikost_stránky);
                } catch (IllegalStateException chyba) {
                    쪽관리.MAP_stránka(dobrá_Proces.adresní_prostor(), Adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < oddíl_HODNOTA_366e0bfa.Velikost(); INDEX++) {
                byte HODNOTA = oddíl_HODNOTA_366e0bfa.Druh_HODNOTA() == 8 ? 0 : spustitelný_soubor[oddíl_HODNOTA_366e0bfa.Soubor_pozice() + INDEX];
                쪽관리.zápis_bajt_HODNOTA(dobrá_Proces.adresní_prostor(), oddíl_HODNOTA_366e0bfa.Adresa() + INDEX, HODNOTA);
            }
        }
        dobrá_Proces.sada_kontext(image_HODNOTA.START_ODKAZ(), parametr_argument, prostředí_5d36e09c);
        dobrá_Proces.Soubor_popisovač().실행시닫기();
        return 0;
    }

    public void ukončit_program(Proces_HODNOTA dobrá_Proces, int Stav_HODNOTA) {
        dobrá_Proces.Konec_program(Stav_HODNOTA);
    }
}
