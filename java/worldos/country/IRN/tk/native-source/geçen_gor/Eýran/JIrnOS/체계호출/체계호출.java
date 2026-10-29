// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.체계호출;

import Eýran.JIrnOS.기억공간.sahypa_iş_dolandyryjy;
import Eýran.JIrnOS.작업.Proses_baha;
import Eýran.JIrnOS.작업.배정기;
import Eýran.JIrnOS.faýl_ulgamy.실행파일적재기;
import Eýran.JIrnOS.faýl_ulgamy.faýl_ulgamy;
import Eýran.JIrnOS.faýl_ulgamy.faýl_maglumat;
import Eýran.JIrnOS.ýadro.하드웨어;
import Eýran.JIrnOS.입력.입력관리자;
import Eýran.JIrnOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int diňe_okalýan_alamat_goý = 0;
    public static final int gözle_başlat = 0;
    public static final int 찾기현재 = 1;
    public static final int tap_girizmeklik_tamamla = 2;

    private final faýl_ulgamy faýl_ulgamy;
    private final sahypa_iş_dolandyryjy 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 enjam_baha;
    private final 입력관리자 입력관리;

    public 체계호출(faýl_ulgamy faýl_ulgamy, sahypa_iş_dolandyryjy 쪽관리, 배정기 배정기, 하드웨어 enjam_baha, 입력관리자 입력관리) {
        this.faýl_ulgamy = faýl_ulgamy;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.enjam_baha = enjam_baha;
        this.입력관리 = 입력관리;
    }

    public int Proses_tanaýjy(Proses_baha 현재과정) {
        return 현재과정.tanaýjy_baha();
    }

    public int 부모과정식별자(Proses_baha 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Aç(Proses_baha 현재과정, String Ad, int alamat_goý_baha) {
        if (alamat_goý_baha != diňe_okalýan_alamat_goý) {
            return -30;
        }
        return 현재과정.파일서술자().Aç(Ad);
    }

    public int Oka(Proses_baha 현재과정, int 서술자, byte[] 받을곳, int Ululyk) {
        if (서술자 == 0) {
            if (Ululyk <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 waka = 입력관리.다음사건();
            if (waka == null || waka.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) waka.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Oka(서술자, 받을곳, Ululyk);
    }

    public int Ýaz(Proses_baha 현재과정, int 서술자, byte[] maglumat, int Ululyk) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ululyk < 0 || Ululyk > maglumat.length) {
            return -22;
        }
        enjam_baha.직렬출력(new String(maglumat, 0, Ululyk, java.nio.charset.StandardCharsets.UTF_8));
        return Ululyk;
    }

    public int Ýap(Proses_baha 현재과정, int 서술자) {
        return 현재과정.파일서술자().Ýap(서술자);
    }

    public int 위치옮기기(Proses_baha 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Proses_baha 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_baha 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ad, int usul_reje) {
        faýl_maglumat msinfo32_exe = faýl_ulgamy.msinfo32_exe(Ad);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((usul_reje & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((usul_reje & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int calşyr_meseleleriň_sanawy(String Ad) {
        return "/".equals(Ad) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int ulanyjy_tanaýjy() { return 0; }
    public int netijeli_ulanyjy_tanaýjy() { return 0; }
    public int topar_tanaýjy() { return 0; }
    public int netijeli_topar_tanaýjy() { return 0; }

    public int sinhronlaşdyr_faýl(Proses_baha 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Oka 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Proses_baha 현재과정, int 서술자) {
        faýl_maglumat msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int faýl_dolandyryş(Proses_baha 현재과정, int 서술자, int buýruk, int 인자) {
        if (buýruk == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (buýruk == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (buýruk == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (buýruk == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : diňe_okalýan_alamat_goý;
        }
        if (buýruk == 4) {
            return 인자 == diňe_okalýan_alamat_goý ? 0 : -30;
        }
        return -22;
    }

    public int döretmek_girizmeklik(String Ad, int rugsat_baha) {
        return -30;
    }

    public faýl_maglumat 서술자정보(Proses_baha 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JIrnOS", "JIrnOS", "0.1", "Java managed kernel", "i386");
    }

    public faýl_maglumat faýl_maglumat(String Ad) {
        return faýl_ulgamy.msinfo32_exe(Ad);
    }

    public Proses_baha 과정복제(Proses_baha 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Proses_baha 부모, int çaga_tanaýjy, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, çaga_tanaýjy, 기다리지않음);
    }

    public int 프로그램끝(Proses_baha 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
        int 끝쪽 = (새끝 + sahypa_iş_dolandyryjy.sahypanyň_ölçegi - 1) / sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
        if (새끝 > 이전끝) {
            for (int indeks = 첫쪽; indeks < 끝쪽; indeks++) {
                int salgy = indeks * sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
                try {
                    쪽관리.바이트읽기(현재과정.salgy_ýer(), salgy);
                } catch (IllegalStateException Hata) {
                    쪽관리.kartada_görkez_sahypa(현재과정.salgy_ýer(), salgy, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_baha 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int ýerine_ýetir_buýruk(Proses_baha 현재과정, byte[] 실행파일) {
        return ýerine_ýetir_buýruk(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int ýerine_ýetir_buýruk(Proses_baha 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.surat surat_baha;
        try {
            surat_baha = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Hata) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.bölüm_baha_366e0bfa bölüm_baha_366e0bfa : surat_baha.구역들()) {
            if ((bölüm_baha_366e0bfa.alamat_goý_baha() & 2) == 0 || bölüm_baha_366e0bfa.Ululyk() == 0) {
                continue;
            }
            int 첫쪽 = bölüm_baha_366e0bfa.salgy() / sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
            int 끝쪽 = (bölüm_baha_366e0bfa.salgy() + bölüm_baha_366e0bfa.Ululyk() + sahypa_iş_dolandyryjy.sahypanyň_ölçegi - 1) / sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
            for (int indeks = 첫쪽; indeks < 끝쪽; indeks++) {
                int salgy = indeks * sahypa_iş_dolandyryjy.sahypanyň_ölçegi;
                try {
                    쪽관리.바이트읽기(현재과정.salgy_ýer(), salgy);
                    쪽관리.범위개인쓰기(현재과정.salgy_ýer(), salgy, sahypa_iş_dolandyryjy.sahypanyň_ölçegi);
                } catch (IllegalStateException Hata) {
                    쪽관리.kartada_görkez_sahypa(현재과정.salgy_ýer(), salgy, true);
                }
            }
            for (int indeks = 0; indeks < bölüm_baha_366e0bfa.Ululyk(); indeks++) {
                byte baha = bölüm_baha_366e0bfa.종류() == 8 ? 0 : 실행파일[bölüm_baha_366e0bfa.파일위치() + indeks];
                쪽관리.ýaz_baýt_baha(현재과정.salgy_ýer(), bölüm_baha_366e0bfa.salgy() + indeks, baha);
            }
        }
        현재과정.실행문맥설정(surat_baha.başlat_salgy(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Proses_baha 현재과정, int ýagdaý_baha) {
        현재과정.çyk_programma(ýagdaý_baha);
    }
}
