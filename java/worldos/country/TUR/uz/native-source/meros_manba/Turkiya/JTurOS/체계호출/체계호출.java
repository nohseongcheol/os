// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkiya.JTurOS.체계호출;

import Turkiya.JTurOS.기억공간.sahifa_menejer;
import Turkiya.JTurOS.작업.Jarayon_VALUE;
import Turkiya.JTurOS.작업.Jadval_tuzuvchi;
import Turkiya.JTurOS.fayllar_tizimi.실행파일적재기;
import Turkiya.JTurOS.fayllar_tizimi.fayllar_tizimi;
import Turkiya.JTurOS.fayllar_tizimi.fayl_ma_lumot;
import Turkiya.JTurOS.o_zak.하드웨어;
import Turkiya.JTurOS.입력.입력관리자;
import Turkiya.JTurOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int faqat_o_qish_uchun_bayroq = 0;
    public static final int Izlash_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_kiritish_to_xtatmoq = 2;

    private final fayllar_tizimi fayllar_tizimi;
    private final sahifa_menejer 쪽관리;
    private final Jadval_tuzuvchi Jadval_tuzuvchi;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 qurilma_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(fayllar_tizimi fayllar_tizimi, sahifa_menejer 쪽관리, Jadval_tuzuvchi Jadval_tuzuvchi, 하드웨어 qurilma_VALUE, 입력관리자 입력관리) {
        this.fayllar_tizimi = fayllar_tizimi;
        this.쪽관리 = 쪽관리;
        this.Jadval_tuzuvchi = Jadval_tuzuvchi;
        this.qurilma_VALUE = qurilma_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Jarayon_identifikator(Jarayon_VALUE 현재과정) {
        return 현재과정.identifikator_VALUE();
    }

    public int 부모과정식별자(Jarayon_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Ochish(Jarayon_VALUE 현재과정, String Nomi, int bayroq_VALUE) {
        if (bayroq_VALUE != faqat_o_qish_uchun_bayroq) {
            return -30;
        }
        return 현재과정.파일서술자().Ochish(Nomi);
    }

    public int Oʻqish(Jarayon_VALUE 현재과정, int 서술자, byte[] 받을곳, int Hajmi) {
        if (서술자 == 0) {
            if (Hajmi <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 hodisa = 입력관리.Keyingi_hodisa();
            if (hodisa == null || hodisa.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) hodisa.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Oʻqish(서술자, 받을곳, Hajmi);
    }

    public int Yozish(Jarayon_VALUE 현재과정, int 서술자, byte[] ma_lumotlar, int Hajmi) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Hajmi < 0 || Hajmi > ma_lumotlar.length) {
            return -22;
        }
        qurilma_VALUE.직렬출력(new String(ma_lumotlar, 0, Hajmi, java.nio.charset.StandardCharsets.UTF_8));
        return Hajmi;
    }

    public int Yopish(Jarayon_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Yopish(서술자);
    }

    public int ko_chirmoq_holat(Jarayon_VALUE 현재과정, int 서술자, int 거리, int Project_ildiz) {
        return 현재과정.파일서술자().ko_chirmoq_holat(서술자, 거리, Project_ildiz);
    }

    public int 서술자복제(Jarayon_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Jarayon_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nomi, int uslub_MODE) {
        fayl_ma_lumot msinfo32_exe = fayllar_tizimi.msinfo32_exe(Nomi);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((uslub_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((uslub_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_vazifalar_ro_yxati(String Nomi) {
        return "/".equals(Nomi) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int foydalanuvchi_identifikator() { return 0; }
    public int samarali_foydalanuvchi_identifikator() { return 0; }
    public int Guruh_identifikator() { return 0; }
    public int samarali_Guruh_identifikator() { return 0; }

    public int sinxronlashtirish_fayl(Jarayon_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Oʻqish 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Jarayon_VALUE 현재과정, int 서술자) {
        fayl_ma_lumot msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fayl_boshqaruv(Jarayon_VALUE 현재과정, int 서술자, int Buyruq, int 인자) {
        if (Buyruq == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Buyruq == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Buyruq == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Buyruq == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : faqat_o_qish_uchun_bayroq;
        }
        if (Buyruq == 4) {
            return 인자 == faqat_o_qish_uchun_bayroq ? 0 : -30;
        }
        return -22;
    }

    public int Yaratish_kiritish(String Nomi, int ruxsat_VALUE_a9fa0dfa) {
        return -30;
    }

    public fayl_ma_lumot 서술자정보(Jarayon_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JTurOS", "JTurOS", "0.1", "Java managed kernel", "i386");
    }

    public fayl_ma_lumot fayl_ma_lumot(String Nomi) {
        return fayllar_tizimi.msinfo32_exe(Nomi);
    }

    public Jarayon_VALUE 과정복제(Jarayon_VALUE 부모) {
        return Jadval_tuzuvchi.복제(부모);
    }

    public int 자식기다리기(Jarayon_VALUE 부모, int farzand_identifikator, boolean 기다리지않음) {
        return Jadval_tuzuvchi.자식기다리기(부모, farzand_identifikator, 기다리지않음);
    }

    public int 프로그램끝(Jarayon_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / sahifa_menejer.sahifa_o_lchami;
        int 끝쪽 = (새끝 + sahifa_menejer.sahifa_o_lchami - 1) / sahifa_menejer.sahifa_o_lchami;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int manzil = INDEX * sahifa_menejer.sahifa_o_lchami;
                try {
                    쪽관리.바이트읽기(현재과정.manzil_joy(), manzil);
                } catch (IllegalStateException Xato) {
                    쪽관리.MAP_sahifa(현재과정.manzil_joy(), manzil, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Jarayon_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int o_lchov = 프로그램끝(현재과정, 이전끝 + 증가량);
        return o_lchov < 0 ? o_lchov : 이전끝;
    }

    public int bajarmoq_buyruq(Jarayon_VALUE 현재과정, byte[] 실행파일) {
        return bajarmoq_buyruq(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int bajarmoq_buyruq(Jarayon_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.rasm rasm_VALUE;
        try {
            rasm_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Xato) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.bo_lim_VALUE_366e0bfa bo_lim_VALUE_366e0bfa : rasm_VALUE.구역들()) {
            if ((bo_lim_VALUE_366e0bfa.bayroq_VALUE() & 2) == 0 || bo_lim_VALUE_366e0bfa.Hajmi() == 0) {
                continue;
            }
            int 첫쪽 = bo_lim_VALUE_366e0bfa.manzil() / sahifa_menejer.sahifa_o_lchami;
            int 끝쪽 = (bo_lim_VALUE_366e0bfa.manzil() + bo_lim_VALUE_366e0bfa.Hajmi() + sahifa_menejer.sahifa_o_lchami - 1) / sahifa_menejer.sahifa_o_lchami;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int manzil = INDEX * sahifa_menejer.sahifa_o_lchami;
                try {
                    쪽관리.바이트읽기(현재과정.manzil_joy(), manzil);
                    쪽관리.범위개인쓰기(현재과정.manzil_joy(), manzil, sahifa_menejer.sahifa_o_lchami);
                } catch (IllegalStateException Xato) {
                    쪽관리.MAP_sahifa(현재과정.manzil_joy(), manzil, true);
                }
            }
            for (int INDEX = 0; INDEX < bo_lim_VALUE_366e0bfa.Hajmi(); INDEX++) {
                byte VALUE = bo_lim_VALUE_366e0bfa.종류() == 8 ? 0 : 실행파일[bo_lim_VALUE_366e0bfa.fayl_holat_2aa21a9a() + INDEX];
                쪽관리.yozmoq_bayt_VALUE(현재과정.manzil_joy(), bo_lim_VALUE_366e0bfa.manzil() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(rasm_VALUE.Start_manzil(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void tugatish_ilova(Jarayon_VALUE 현재과정, int holat_VALUE_e10195a1) {
        현재과정.Chiqish_ilova(holat_VALUE_e10195a1);
    }
}
