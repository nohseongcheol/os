// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.체계호출;

import Latvija.JLvaOS.atmiņa_reģions.쪽관리자;
import Latvija.JLvaOS.작업.Process_VALUE;
import Latvija.JLvaOS.작업.plānotājs;
import Latvija.JLvaOS.failu_sistēma.izpildāms_fails_ielādētājs;
import Latvija.JLvaOS.failu_sistēma.failu_sistēma;
import Latvija.JLvaOS.failu_sistēma.Fails_informācija;
import Latvija.JLvaOS.kodols.하드웨어;
import Latvija.JLvaOS.입력.입력관리자;
import Latvija.JLvaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int tikai_lasāms_atzīmēt_ar_karodziņu = 0;
    public static final int Meklēt_Sākt = 0;
    public static final int Meklēt_pašreizējais = 1;
    public static final int FIND_ievade_beigt_zvanu = 2;

    private final failu_sistēma failu_sistēma;
    private final 쪽관리자 쪽관리;
    private final plānotājs plānotājs;
    private final izpildāms_fails_ielādētājs ielādētājs = new izpildāms_fails_ielādētājs();
    private final 하드웨어 ierīce_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(failu_sistēma failu_sistēma, 쪽관리자 쪽관리, plānotājs plānotājs, 하드웨어 ierīce_VALUE, 입력관리자 입력관리) {
        this.failu_sistēma = failu_sistēma;
        this.쪽관리 = 쪽관리;
        this.plānotājs = plānotājs;
        this.ierīce_VALUE = ierīce_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Process_identifikators(Process_VALUE pašreizējais_Process) {
        return pašreizējais_Process.identifikators_VALUE();
    }

    public int vecākobjekts_Process_identifikators(Process_VALUE pašreizējais_Process) {
        return pašreizējais_Process.vecākobjekts_identifikators();
    }

    public int Atvērt(Process_VALUE pašreizējais_Process, String Nosaukums, int atzīmēt_ar_karodziņu_VALUE) {
        if (atzīmēt_ar_karodziņu_VALUE != tikai_lasāms_atzīmēt_ar_karodziņu) {
            return -30;
        }
        return pašreizējais_Process.파일서술자().Atvērt(Nosaukums);
    }

    public int Lasīt(Process_VALUE pašreizējais_Process, int 서술자, byte[] saņemt_mērķis, int Izmērs) {
        if (서술자 == 0) {
            if (Izmērs <= 0 || saņemt_mērķis.length == 0) {
                return 0;
            }
            입력사건 Notikums = 입력관리.Tālāk_notikums();
            if (Notikums == null || Notikums.notikuma_veids() != 입력사건.종류.Atslēga_nedarbojas) {
                return -11;
            }
            saņemt_mērķis[0] = (byte) Notikums.첫째값();
            return 1;
        }
        return pašreizējais_Process.파일서술자().Lasīt(서술자, saņemt_mērķis, Izmērs);
    }

    public int Rakstīt(Process_VALUE pašreizējais_Process, int 서술자, byte[] dati, int Izmērs) {
        if (서술자 != 1 && 서술자 != 2) {
            return pašreizējais_Process.파일서술자().informācijas_tehnoloģija_atvērt(서술자) ? -30 : -9;
        }
        if (Izmērs < 0 || Izmērs > dati.length) {
            return -22;
        }
        ierīce_VALUE.직렬출력(new String(dati, 0, Izmērs, java.nio.charset.StandardCharsets.UTF_8));
        return Izmērs;
    }

    public int Aizvērt(Process_VALUE pašreizējais_Process, int 서술자) {
        return pašreizējais_Process.파일서술자().Aizvērt(서술자);
    }

    public int pārvietot_amats(Process_VALUE pašreizējais_Process, int 서술자, int 거리, int Project_sakne) {
        return pašreizējais_Process.파일서술자().pārvietot_amats(서술자, 거리, Project_sakne);
    }

    public int 서술자복제(Process_VALUE pašreizējais_Process, int 서술자) {
        return pašreizējais_Process.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Process_VALUE pašreizējais_Process, int 서술자, int 새서술자) {
        return pašreizējais_Process.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nosaukums, int metode_MODE) {
        Fails_informācija msinfo32_exe = failu_sistēma.msinfo32_exe(Nosaukums);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metode_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_uzdevumu_saraksts(String Nosaukums) {
        return "/".equals(Nosaukums) ? 0 : -20;
    }

    public String pašreizējais_uzdevumu_saraksts(int saņemt_mainīt_izmērus) {
        return saņemt_mainīt_izmērus >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int efektīvs_UID() { return 0; }
    public int Grupa_identifikators() { return 0; }
    public int efektīvs_Grupa_identifikators() { return 0; }

    public int sinhronizēt_Fails(Process_VALUE pašreizējais_Process, int 서술자) {
        return pašreizējais_Process.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // pašreizējais_krājums 파일체계는 Lasīt 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informācijas_tehnoloģija_Terminālis(Process_VALUE pašreizējais_Process, int 서술자) {
        Fails_informācija msinfo32_exe = pašreizējais_Process.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fails_vadība(Process_VALUE pašreizējais_Process, int 서술자, int Komanda, int parametrs_arg) {
        if (Komanda == 0) {
            return pašreizējais_Process.파일서술자().복제서술자(서술자, parametrs_arg);
        }
        if (Komanda == 1) {
            return pašreizējais_Process.파일서술자().실행시닫기값(서술자);
        }
        if (Komanda == 2) {
            return pašreizējais_Process.파일서술자().실행시닫기설정(서술자, (parametrs_arg & 1) != 0);
        }
        if (Komanda == 3) {
            return pašreizējais_Process.파일서술자().msinfo32_exe(서술자) == null ? -9 : tikai_lasāms_atzīmēt_ar_karodziņu;
        }
        if (Komanda == 4) {
            return parametrs_arg == tikai_lasāms_atzīmēt_ar_karodziņu ? 0 : -30;
        }
        return -22;
    }

    public int atvērt_ievade(String Nosaukums, int atļauja_VALUE) {
        return -30;
    }

    public Fails_informācija 서술자정보(Process_VALUE pašreizējais_Process, int 서술자) {
        return pašreizējais_Process.파일서술자().msinfo32_exe(서술자);
    }

    public sistēma_Detalizēti sistēma_Detalizēti() {
        return new sistēma_Detalizēti("JLvaOS", "JLvaOS", "0.1", "Java managed kernel", "i386");
    }

    public Fails_informācija Fails_informācija(String Nosaukums) {
        return failu_sistēma.msinfo32_exe(Nosaukums);
    }

    public Process_VALUE klons_Process(Process_VALUE vecākobjekts_VALUE) {
        return plānotājs.klons_VALUE(vecākobjekts_VALUE);
    }

    public int 자식기다리기(Process_VALUE vecākobjekts_VALUE, int bērns_identifikators, boolean 기다리지않음) {
        return plānotājs.자식기다리기(vecākobjekts_VALUE, bērns_identifikators, 기다리지않음);
    }

    public int programma_pārtraukt(Process_VALUE pašreizējais_Process, int 새끝) {
        int 이전끝 = pašreizējais_Process.programma_pārtraukt();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / 쪽관리자.lappuses_izmēri;
        int 끝쪽 = (새끝 + 쪽관리자.lappuses_izmēri - 1) / 쪽관리자.lappuses_izmēri;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adrese = INDEX * 쪽관리자.lappuses_izmēri;
                try {
                    쪽관리.바이트읽기(pašreizējais_Process.adrese_telpa(), adrese);
                } catch (IllegalStateException Kļūda) {
                    쪽관리.MAP_lapa(pašreizējais_Process.adrese_telpa(), adrese, true);
                }
            }
        }
        pašreizējais_Process.kopa_programma_pārtraukt(새끝);
        return 새끝;
    }

    public int palielinājums_programma_pārtraukt(Process_VALUE pašreizējais_Process, int palielinājums_summa) {
        int 이전끝 = pašreizējais_Process.programma_pārtraukt();
        int mērs = programma_pārtraukt(pašreizējais_Process, 이전끝 + palielinājums_summa);
        return mērs < 0 ? mērs : 이전끝;
    }

    public int Izpildīt_komanda(Process_VALUE pašreizējais_Process, byte[] izpildāms_fails) {
        return Izpildīt_komanda(pašreizējais_Process, izpildāms_fails, new String[0], new String[0]);
    }

    public int Izpildīt_komanda(Process_VALUE pašreizējais_Process, byte[] izpildāms_fails, String[] parametrs_arg, String[] 환경) {
        izpildāms_fails_ielādētājs.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = ielādētājs.검사(izpildāms_fails);
        } catch (IllegalArgumentException Kļūda) {
            return -8;
        }
        if (parametrs_arg == null || 환경 == null || parametrs_arg.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (izpildāms_fails_ielādētājs.sadaļa_VALUE sadaļa_VALUE : IMAGE_VALUE.구역들()) {
            if ((sadaļa_VALUE.atzīmēt_ar_karodziņu_VALUE() & 2) == 0 || sadaļa_VALUE.Izmērs() == 0) {
                continue;
            }
            int 첫쪽 = sadaļa_VALUE.adrese() / 쪽관리자.lappuses_izmēri;
            int 끝쪽 = (sadaļa_VALUE.adrese() + sadaļa_VALUE.Izmērs() + 쪽관리자.lappuses_izmēri - 1) / 쪽관리자.lappuses_izmēri;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adrese = INDEX * 쪽관리자.lappuses_izmēri;
                try {
                    쪽관리.바이트읽기(pašreizējais_Process.adrese_telpa(), adrese);
                    쪽관리.Privāts_diapazons_rakstīšana(pašreizējais_Process.adrese_telpa(), adrese, 쪽관리자.lappuses_izmēri);
                } catch (IllegalStateException Kļūda) {
                    쪽관리.MAP_lapa(pašreizējais_Process.adrese_telpa(), adrese, true);
                }
            }
            for (int INDEX = 0; INDEX < sadaļa_VALUE.Izmērs(); INDEX++) {
                byte VALUE = sadaļa_VALUE.종류() == 8 ? 0 : izpildāms_fails[sadaļa_VALUE.Fails_amats() + INDEX];
                쪽관리.rakstīšana_byte_VALUE(pašreizējais_Process.adrese_telpa(), sadaļa_VALUE.adrese() + INDEX, VALUE);
            }
        }
        pašreizējais_Process.실행문맥설정(IMAGE_VALUE.Sākt_adrese(), parametrs_arg, 환경);
        pašreizējais_Process.파일서술자().실행시닫기();
        return 0;
    }

    public void iziet_programma(Process_VALUE pašreizējais_Process, int Statuss_VALUE) {
        pašreizējais_Process.Iziet_programma(Statuss_VALUE);
    }
}
