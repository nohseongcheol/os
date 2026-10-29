// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ungaria.JHunOS.체계호출;

import Ungaria.JHunOS.Memorie_regiune.쪽관리자;
import Ungaria.JHunOS.작업.Proces_VALUE;
import Ungaria.JHunOS.작업.Planificator;
import Ungaria.JHunOS.sistem_de_fișiere.실행파일적재기;
import Ungaria.JHunOS.sistem_de_fișiere.sistem_de_fișiere;
import Ungaria.JHunOS.sistem_de_fișiere.Fișier_info;
import Ungaria.JHunOS.nucleu.하드웨어;
import Ungaria.JHunOS.입력.입력관리자;
import Ungaria.JHunOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int doar_în_citire_fanion = 0;
    public static final int căuta_buta = 0;
    public static final int căuta_curent = 1;
    public static final int FIND_intrare_termina_un_apel = 2;

    private final sistem_de_fișiere sistem_de_fișiere;
    private final 쪽관리자 쪽관리;
    private final Planificator Planificator;
    private final 실행파일적재기 încărcător = new 실행파일적재기();
    private final 하드웨어 mobil_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(sistem_de_fișiere sistem_de_fișiere, 쪽관리자 쪽관리, Planificator Planificator, 하드웨어 mobil_VALUE, 입력관리자 입력관리) {
        this.sistem_de_fișiere = sistem_de_fișiere;
        this.쪽관리 = 쪽관리;
        this.Planificator = Planificator;
        this.mobil_VALUE = mobil_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proces_identificator(Proces_VALUE curent_Proces) {
        return curent_Proces.identificator_VALUE();
    }

    public int părinte_Proces_identificator(Proces_VALUE curent_Proces) {
        return curent_Proces.părinte_identificator();
    }

    public int Deschide(Proces_VALUE curent_Proces, String Nume, int fanion_VALUE) {
        if (fanion_VALUE != doar_în_citire_fanion) {
            return -30;
        }
        return curent_Proces.파일서술자().Deschide(Nume);
    }

    public int Citire(Proces_VALUE curent_Proces, int 서술자, byte[] primi_destinație, int Mărime) {
        if (서술자 == 0) {
            if (Mărime <= 0 || primi_destinație.length == 0) {
                return 0;
            }
            입력사건 Eveniment = 입력관리.Următorul_eveniment();
            if (Eveniment == null || Eveniment.natură_eveniment() != 입력사건.종류.Cheie_nefuncțional) {
                return -11;
            }
            primi_destinație[0] = (byte) Eveniment.첫째값();
            return 1;
        }
        return curent_Proces.파일서술자().Citire(서술자, primi_destinație, Mărime);
    }

    public int Scriere(Proces_VALUE curent_Proces, int 서술자, byte[] date, int Mărime) {
        if (서술자 != 1 && 서술자 != 2) {
            return curent_Proces.파일서술자().sisteme_de_informații_crea(서술자) ? -30 : -9;
        }
        if (Mărime < 0 || Mărime > date.length) {
            return -22;
        }
        mobil_VALUE.직렬출력(new String(date, 0, Mărime, java.nio.charset.StandardCharsets.UTF_8));
        return Mărime;
    }

    public int Închide(Proces_VALUE curent_Proces, int 서술자) {
        return curent_Proces.파일서술자().Închide(서술자);
    }

    public int muta_poziție(Proces_VALUE curent_Proces, int 서술자, int 거리, int Project_rădăcină) {
        return curent_Proces.파일서술자().muta_poziție(서술자, 거리, Project_rădăcină);
    }

    public int 서술자복제(Proces_VALUE curent_Proces, int 서술자) {
        return curent_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE curent_Proces, int 서술자, int 새서술자) {
        return curent_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nume, int metodă_mod) {
        Fișier_info msinfo32_exe = sistem_de_fișiere.msinfo32_exe(Nume);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metodă_mod & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metodă_mod & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_listă_de_activități(String Nume) {
        return "/".equals(Nume) ? 0 : -20;
    }

    public String curent_listă_de_activități(int primi_dimensiona) {
        return primi_dimensiona >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int eficient_UID() { return 0; }
    public int grup_identificator() { return 0; }
    public int eficient_grup_identificator() { return 0; }

    public int sincroniz_Fișier(Proces_VALUE curent_Proces, int 서술자) {
        return curent_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // curent_element 파일체계는 Citire 전용이어서 밀어낼 자료가 없다.
    }

    public boolean sisteme_de_informații_Terminal(Proces_VALUE curent_Proces, int 서술자) {
        Fișier_info msinfo32_exe = curent_Proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fișier_control(Proces_VALUE curent_Proces, int 서술자, int Comandă, int parametru_argument) {
        if (Comandă == 0) {
            return curent_Proces.파일서술자().복제서술자(서술자, parametru_argument);
        }
        if (Comandă == 1) {
            return curent_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (Comandă == 2) {
            return curent_Proces.파일서술자().실행시닫기설정(서술자, (parametru_argument & 1) != 0);
        }
        if (Comandă == 3) {
            return curent_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : doar_în_citire_fanion;
        }
        if (Comandă == 4) {
            return parametru_argument == doar_în_citire_fanion ? 0 : -30;
        }
        return -22;
    }

    public int crea_intrare(String Nume, int permisiune_VALUE) {
        return -30;
    }

    public Fișier_info 서술자정보(Proces_VALUE curent_Proces, int 서술자) {
        return curent_Proces.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Detalii sistem_Detalii() {
        return new sistem_Detalii("JHunOS", "JHunOS", "0.1", "Java managed kernel", "i386");
    }

    public Fișier_info Fișier_info(String Nume) {
        return sistem_de_fișiere.msinfo32_exe(Nume);
    }

    public Proces_VALUE clona_Proces(Proces_VALUE părinte_VALUE) {
        return Planificator.clona_VALUE(părinte_VALUE);
    }

    public int 자식기다리기(Proces_VALUE părinte_VALUE, int copil_identificator, boolean 기다리지않음) {
        return Planificator.자식기다리기(părinte_VALUE, copil_identificator, 기다리지않음);
    }

    public int program_pauză(Proces_VALUE curent_Proces, int 새끝) {
        int Anteriorul_termina_un_apel = curent_Proces.program_pauză();
        if (새끝 == 0) {
            return Anteriorul_termina_un_apel;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Anteriorul_termina_un_apel / 쪽관리자.dimensiune_pagină;
        int 끝쪽 = (새끝 + 쪽관리자.dimensiune_pagină - 1) / 쪽관리자.dimensiune_pagină;
        if (새끝 > Anteriorul_termina_un_apel) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * 쪽관리자.dimensiune_pagină;
                try {
                    쪽관리.바이트읽기(curent_Proces.adresa_SPAȚIU(), adresa);
                } catch (IllegalStateException eroare) {
                    쪽관리.MAP_pagina(curent_Proces.adresa_SPAȚIU(), adresa, true);
                }
            }
        }
        curent_Proces.set_program_pauză(새끝);
        return 새끝;
    }

    public int intrare_în_stoc_program_pauză(Proces_VALUE curent_Proces, int increment_sumă) {
        int Anteriorul_termina_un_apel = curent_Proces.program_pauză();
        int KR = program_pauză(curent_Proces, Anteriorul_termina_un_apel + increment_sumă);
        return KR < 0 ? KR : Anteriorul_termina_un_apel;
    }

    public int executa_comandă(Proces_VALUE curent_Proces, byte[] 실행파일) {
        return executa_comandă(curent_Proces, 실행파일, new String[0], new String[0]);
    }

    public int executa_comandă(Proces_VALUE curent_Proces, byte[] 실행파일, String[] parametru_argument, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = încărcător.검사(실행파일);
        } catch (IllegalArgumentException eroare) {
            return -8;
        }
        if (parametru_argument == null || 환경 == null || parametru_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.secțiune_VALUE secțiune_VALUE : IMAGE_VALUE.구역들()) {
            if ((secțiune_VALUE.fanion_VALUE() & 2) == 0 || secțiune_VALUE.Mărime() == 0) {
                continue;
            }
            int 첫쪽 = secțiune_VALUE.adresa() / 쪽관리자.dimensiune_pagină;
            int 끝쪽 = (secțiune_VALUE.adresa() + secțiune_VALUE.Mărime() + 쪽관리자.dimensiune_pagină - 1) / 쪽관리자.dimensiune_pagină;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adresa = INDEX * 쪽관리자.dimensiune_pagină;
                try {
                    쪽관리.바이트읽기(curent_Proces.adresa_SPAȚIU(), adresa);
                    쪽관리.Privat_zonă_scriere(curent_Proces.adresa_SPAȚIU(), adresa, 쪽관리자.dimensiune_pagină);
                } catch (IllegalStateException eroare) {
                    쪽관리.MAP_pagina(curent_Proces.adresa_SPAȚIU(), adresa, true);
                }
            }
            for (int INDEX = 0; INDEX < secțiune_VALUE.Mărime(); INDEX++) {
                byte VALUE = secțiune_VALUE.종류() == 8 ? 0 : 실행파일[secțiune_VALUE.Fișier_poziție() + INDEX];
                쪽관리.scriere_byte_VALUE(curent_Proces.adresa_SPAȚIU(), secțiune_VALUE.adresa() + INDEX, VALUE);
            }
        }
        curent_Proces.set_executare_context(IMAGE_VALUE.buta_adresa(), parametru_argument, 환경);
        curent_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void ieșire_program(Proces_VALUE curent_Proces, int Stare_VALUE) {
        curent_Proces.ieși_program(Stare_VALUE);
    }
}
