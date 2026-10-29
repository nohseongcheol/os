// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.체계호출;

import Jungtinė_Karalystė.JGbrOS.atmintis_sritis.쪽관리자;
import Jungtinė_Karalystė.JGbrOS.작업.Procesas_VALUE;
import Jungtinė_Karalystė.JGbrOS.작업.planuotojas;
import Jungtinė_Karalystė.JGbrOS.failų_sistema.실행파일적재기;
import Jungtinė_Karalystė.JGbrOS.failų_sistema.failų_sistema;
import Jungtinė_Karalystė.JGbrOS.failų_sistema.Failas_informacija;
import Jungtinė_Karalystė.JGbrOS.branduolys.aparatūra_VALUE;
import Jungtinė_Karalystė.JGbrOS.입력.입력관리자;
import Jungtinė_Karalystė.JGbrOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int tik_skaitomas_žymė = 0;
    public static final int Ieška_Start = 0;
    public static final int Ieška_dabartinis = 1;
    public static final int FIND_įrašas_baigti_pokalbį = 2;

    private final failų_sistema failų_sistema;
    private final 쪽관리자 쪽관리;
    private final planuotojas planuotojas;
    private final 실행파일적재기 įkelties_programa = new 실행파일적재기();
    private final aparatūra_VALUE įrenginys_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(failų_sistema failų_sistema, 쪽관리자 쪽관리, planuotojas planuotojas, aparatūra_VALUE įrenginys_VALUE, 입력관리자 입력관리) {
        this.failų_sistema = failų_sistema;
        this.쪽관리 = 쪽관리;
        this.planuotojas = planuotojas;
        this.įrenginys_VALUE = įrenginys_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Procesas_identifikatorius(Procesas_VALUE dabartinis_Procesas) {
        return dabartinis_Procesas.identifikatorius_VALUE();
    }

    public int pirminis_Procesas_identifikatorius(Procesas_VALUE dabartinis_Procesas) {
        return dabartinis_Procesas.pirminis_identifikatorius();
    }

    public int Atverti(Procesas_VALUE dabartinis_Procesas, String Pavadinimas_2, int žymė_VALUE) {
        if (žymė_VALUE != tik_skaitomas_žymė) {
            return -30;
        }
        return dabartinis_Procesas.파일서술자().Atverti(Pavadinimas_2);
    }

    public int Skaitymas(Procesas_VALUE dabartinis_Procesas, int 서술자, byte[] gauti_vieta, int Dydis) {
        if (서술자 == 0) {
            if (Dydis <= 0 || gauti_vieta.length == 0) {
                return 0;
            }
            입력사건 Įvykis = 입력관리.toliau_įvykis();
            if (Įvykis == null || Įvykis.įvykio_rūšis() != 입력사건.종류.Raktas_neveikiantis) {
                return -11;
            }
            gauti_vieta[0] = (byte) Įvykis.첫째값();
            return 1;
        }
        return dabartinis_Procesas.파일서술자().Skaitymas(서술자, gauti_vieta, Dydis);
    }

    public int Rašymas(Procesas_VALUE dabartinis_Procesas, int 서술자, byte[] duomenys, int Dydis) {
        if (서술자 != 1 && 서술자 != 2) {
            return dabartinis_Procesas.파일서술자().informacinės_technologijos_kurti(서술자) ? -30 : -9;
        }
        if (Dydis < 0 || Dydis > duomenys.length) {
            return -22;
        }
        įrenginys_VALUE.직렬출력(new String(duomenys, 0, Dydis, java.nio.charset.StandardCharsets.UTF_8));
        return Dydis;
    }

    public int Užverti(Procesas_VALUE dabartinis_Procesas, int 서술자) {
        return dabartinis_Procesas.파일서술자().Užverti(서술자);
    }

    public int judėti_padėtis(Procesas_VALUE dabartinis_Procesas, int 서술자, int 거리, int Project_šaknis) {
        return dabartinis_Procesas.파일서술자().judėti_padėtis(서술자, 거리, Project_šaknis);
    }

    public int 서술자복제(Procesas_VALUE dabartinis_Procesas, int 서술자) {
        return dabartinis_Procesas.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Procesas_VALUE dabartinis_Procesas, int 서술자, int 새서술자) {
        return dabartinis_Procesas.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Pavadinimas_2, int metodas_MODE) {
        Failas_informacija msinfo32_exe = failų_sistema.msinfo32_exe(Pavadinimas_2);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metodas_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metodas_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_užduočių_sąrašas(String Pavadinimas_2) {
        return "/".equals(Pavadinimas_2) ? 0 : -20;
    }

    public String dabartinis_užduočių_sąrašas(int gauti_dydis) {
        return gauti_dydis >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int veiksmingas_UID() { return 0; }
    public int Grupė_identifikatorius() { return 0; }
    public int veiksmingas_Grupė_identifikatorius() { return 0; }

    public int sinchronizuoti_Failas(Procesas_VALUE dabartinis_Procesas, int 서술자) {
        return dabartinis_Procesas.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // dabartinis_prekė 파일체계는 Skaitymas 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informacinės_technologijos_Terminalas(Procesas_VALUE dabartinis_Procesas, int 서술자) {
        Failas_informacija msinfo32_exe = dabartinis_Procesas.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Failas_valdymas(Procesas_VALUE dabartinis_Procesas, int 서술자, int Komanda, int parametras_argumentas) {
        if (Komanda == 0) {
            return dabartinis_Procesas.파일서술자().복제서술자(서술자, parametras_argumentas);
        }
        if (Komanda == 1) {
            return dabartinis_Procesas.파일서술자().실행시닫기값(서술자);
        }
        if (Komanda == 2) {
            return dabartinis_Procesas.파일서술자().실행시닫기설정(서술자, (parametras_argumentas & 1) != 0);
        }
        if (Komanda == 3) {
            return dabartinis_Procesas.파일서술자().msinfo32_exe(서술자) == null ? -9 : tik_skaitomas_žymė;
        }
        if (Komanda == 4) {
            return parametras_argumentas == tik_skaitomas_žymė ? 0 : -30;
        }
        return -22;
    }

    public int kurti_įrašas(String Pavadinimas_2, int teisė_VALUE) {
        return -30;
    }

    public Failas_informacija 서술자정보(Procesas_VALUE dabartinis_Procesas, int 서술자) {
        return dabartinis_Procesas.파일서술자().msinfo32_exe(서술자);
    }

    public sistema_Išsami_informacija sistema_Išsami_informacija() {
        return new sistema_Išsami_informacija("JGbrOS", "JGbrOS", "0.1", "Java managed kernel", "i386");
    }

    public Failas_informacija Failas_informacija(String Pavadinimas_2) {
        return failų_sistema.msinfo32_exe(Pavadinimas_2);
    }

    public Procesas_VALUE klonas_Procesas(Procesas_VALUE pirminis_VALUE) {
        return planuotojas.klonas_VALUE(pirminis_VALUE);
    }

    public int 자식기다리기(Procesas_VALUE pirminis_VALUE, int vaikas_identifikatorius, boolean 기다리지않음) {
        return planuotojas.자식기다리기(pirminis_VALUE, vaikas_identifikatorius, 기다리지않음);
    }

    public int programa_nutraukti(Procesas_VALUE dabartinis_Procesas, int 새끝) {
        int 이전끝 = dabartinis_Procesas.programa_nutraukti();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / 쪽관리자.puslapio_formatas;
        int 끝쪽 = (새끝 + 쪽관리자.puslapio_formatas - 1) / 쪽관리자.puslapio_formatas;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * 쪽관리자.puslapio_formatas;
                try {
                    쪽관리.바이트읽기(dabartinis_Procesas.ADDRESS_erdvė(), ADDRESS);
                } catch (IllegalStateException KLAIDA) {
                    쪽관리.MAP_puslapis(dabartinis_Procesas.ADDRESS_erdvė(), ADDRESS, true);
                }
            }
        }
        dabartinis_Procesas.rinkinys_programa_nutraukti(새끝);
        return 새끝;
    }

    public int padidėjimas_programa_nutraukti(Procesas_VALUE dabartinis_Procesas, int padidinimas_suma) {
        int 이전끝 = dabartinis_Procesas.programa_nutraukti();
        int REZULTATAS = programa_nutraukti(dabartinis_Procesas, 이전끝 + padidinimas_suma);
        return REZULTATAS < 0 ? REZULTATAS : 이전끝;
    }

    public int Vykdyti_komanda(Procesas_VALUE dabartinis_Procesas, byte[] 실행파일) {
        return Vykdyti_komanda(dabartinis_Procesas, 실행파일, new String[0], new String[0]);
    }

    public int Vykdyti_komanda(Procesas_VALUE dabartinis_Procesas, byte[] 실행파일, String[] parametras_argumentas, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = įkelties_programa.검사(실행파일);
        } catch (IllegalArgumentException KLAIDA) {
            return -8;
        }
        if (parametras_argumentas == null || 환경 == null || parametras_argumentas.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.sekcija_VALUE sekcija_VALUE : IMAGE_VALUE.구역들()) {
            if ((sekcija_VALUE.žymė_VALUE() & 2) == 0 || sekcija_VALUE.Dydis() == 0) {
                continue;
            }
            int 첫쪽 = sekcija_VALUE.ADDRESS() / 쪽관리자.puslapio_formatas;
            int 끝쪽 = (sekcija_VALUE.ADDRESS() + sekcija_VALUE.Dydis() + 쪽관리자.puslapio_formatas - 1) / 쪽관리자.puslapio_formatas;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * 쪽관리자.puslapio_formatas;
                try {
                    쪽관리.바이트읽기(dabartinis_Procesas.ADDRESS_erdvė(), ADDRESS);
                    쪽관리.privatus_diapazonas_rašymas(dabartinis_Procesas.ADDRESS_erdvė(), ADDRESS, 쪽관리자.puslapio_formatas);
                } catch (IllegalStateException KLAIDA) {
                    쪽관리.MAP_puslapis(dabartinis_Procesas.ADDRESS_erdvė(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < sekcija_VALUE.Dydis(); INDEX++) {
                byte VALUE = sekcija_VALUE.종류() == 8 ? 0 : 실행파일[sekcija_VALUE.Failas_padėtis() + INDEX];
                쪽관리.rašymas_baitas_VALUE(dabartinis_Procesas.ADDRESS_erdvė(), sekcija_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        dabartinis_Procesas.실행문맥설정(IMAGE_VALUE.Start_ADDRESS(), parametras_argumentas, 환경);
        dabartinis_Procesas.파일서술자().실행시닫기();
        return 0;
    }

    public void išeiti_programa(Procesas_VALUE dabartinis_Procesas, int Būsena_VALUE) {
        dabartinis_Procesas.Baigti_programa_086bb533(Būsena_VALUE);
    }
}
