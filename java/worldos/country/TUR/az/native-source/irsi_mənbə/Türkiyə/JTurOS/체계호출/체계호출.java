// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.체계호출;

import Türkiyə.JTurOS.기억공간.səhifə_menecer;
import Türkiyə.JTurOS.작업.Proses_VALUE;
import Türkiyə.JTurOS.작업.Planlaşdırıcı;
import Türkiyə.JTurOS.fayl_sistemi.실행파일적재기;
import Türkiyə.JTurOS.fayl_sistemi.fayl_sistemi;
import Türkiyə.JTurOS.fayl_sistemi.fayl_məlumat;
import Türkiyə.JTurOS.nüvə.하드웨어;
import Türkiyə.JTurOS.입력.입력관리자;
import Türkiyə.JTurOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int yalnız_oxunan_bayraq = 0;
    public static final int SEARCH_Başla = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_daxiletmə_bitirmək = 2;

    private final fayl_sistemi fayl_sistemi;
    private final səhifə_menecer 쪽관리;
    private final Planlaşdırıcı Planlaşdırıcı;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 cihaz_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(fayl_sistemi fayl_sistemi, səhifə_menecer 쪽관리, Planlaşdırıcı Planlaşdırıcı, 하드웨어 cihaz_VALUE, 입력관리자 입력관리) {
        this.fayl_sistemi = fayl_sistemi;
        this.쪽관리 = 쪽관리;
        this.Planlaşdırıcı = Planlaşdırıcı;
        this.cihaz_VALUE = cihaz_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proses_identifikator(Proses_VALUE 현재과정) {
        return 현재과정.identifikator_VALUE();
    }

    public int 부모과정식별자(Proses_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Aç(Proses_VALUE 현재과정, String Ad, int bayraq_VALUE) {
        if (bayraq_VALUE != yalnız_oxunan_bayraq) {
            return -30;
        }
        return 현재과정.파일서술자().Aç(Ad);
    }

    public int Oxuma(Proses_VALUE 현재과정, int 서술자, byte[] 받을곳, int Böyüklük) {
        if (서술자 == 0) {
            if (Böyüklük <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 hadisə = 입력관리.Sonrakı_hadisə();
            if (hadisə == null || hadisə.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) hadisə.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Oxuma(서술자, 받을곳, Böyüklük);
    }

    public int Yazma(Proses_VALUE 현재과정, int 서술자, byte[] verilənlər, int Böyüklük) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Böyüklük < 0 || Böyüklük > verilənlər.length) {
            return -22;
        }
        cihaz_VALUE.직렬출력(new String(verilənlər, 0, Böyüklük, java.nio.charset.StandardCharsets.UTF_8));
        return Böyüklük;
    }

    public int Bağla(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Bağla(서술자);
    }

    public int hərəkət_etdir_yerinə_qoymaq(Proses_VALUE 현재과정, int 서술자, int 거리, int Project_kök) {
        return 현재과정.파일서술자().hərəkət_etdir_yerinə_qoymaq(서술자, 거리, Project_kök);
    }

    public int 서술자복제(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ad, int metod_MODE) {
        fayl_məlumat msinfo32_exe = fayl_sistemi.msinfo32_exe(Ad);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metod_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metod_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_tapşırıq_siyahısı(String Ad) {
        return "/".equals(Ad) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int istifadəçi_identifikator() { return 0; }
    public int effektiv_istifadəçi_identifikator() { return 0; }
    public int Qrup_identifikator() { return 0; }
    public int effektiv_Qrup_identifikator() { return 0; }

    public int sinxronlaşdırmaq_fayl(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Oxuma 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Proses_VALUE 현재과정, int 서술자) {
        fayl_məlumat msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fayl_nəzarət(Proses_VALUE 현재과정, int 서술자, int Əmr, int 인자) {
        if (Əmr == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Əmr == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Əmr == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Əmr == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : yalnız_oxunan_bayraq;
        }
        if (Əmr == 4) {
            return 인자 == yalnız_oxunan_bayraq ? 0 : -30;
        }
        return -22;
    }

    public int yarat_daxiletmə(String Ad, int icazə_VALUE) {
        return -30;
    }

    public fayl_məlumat 서술자정보(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JTurOS", "JTurOS", "0.1", "Java managed kernel", "i386");
    }

    public fayl_məlumat fayl_məlumat(String Ad) {
        return fayl_sistemi.msinfo32_exe(Ad);
    }

    public Proses_VALUE 과정복제(Proses_VALUE 부모) {
        return Planlaşdırıcı.복제(부모);
    }

    public int 자식기다리기(Proses_VALUE 부모, int uşaq_identifikator, boolean 기다리지않음) {
        return Planlaşdırıcı.자식기다리기(부모, uşaq_identifikator, 기다리지않음);
    }

    public int 프로그램끝(Proses_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / səhifə_menecer.səhifənin_ölçüsü;
        int 끝쪽 = (새끝 + səhifə_menecer.səhifənin_ölçüsü - 1) / səhifə_menecer.səhifənin_ölçüsü;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ünvan = INDEX * səhifə_menecer.səhifənin_ölçüsü;
                try {
                    쪽관리.바이트읽기(현재과정.ünvan_məkan(), ünvan);
                } catch (IllegalStateException XƏTA) {
                    쪽관리.MAP_səhifə(현재과정.ünvan_məkan(), ünvan, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int ölçü = 프로그램끝(현재과정, 이전끝 + 증가량);
        return ölçü < 0 ? ölçü : 이전끝;
    }

    public int icra_etmək_əmr(Proses_VALUE 현재과정, byte[] 실행파일) {
        return icra_etmək_əmr(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int icra_etmək_əmr(Proses_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException XƏTA) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.bölmə_VALUE_366e0bfa bölmə_VALUE_366e0bfa : IMAGE_VALUE.구역들()) {
            if ((bölmə_VALUE_366e0bfa.bayraq_VALUE() & 2) == 0 || bölmə_VALUE_366e0bfa.Böyüklük() == 0) {
                continue;
            }
            int 첫쪽 = bölmə_VALUE_366e0bfa.ünvan() / səhifə_menecer.səhifənin_ölçüsü;
            int 끝쪽 = (bölmə_VALUE_366e0bfa.ünvan() + bölmə_VALUE_366e0bfa.Böyüklük() + səhifə_menecer.səhifənin_ölçüsü - 1) / səhifə_menecer.səhifənin_ölçüsü;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ünvan = INDEX * səhifə_menecer.səhifənin_ölçüsü;
                try {
                    쪽관리.바이트읽기(현재과정.ünvan_məkan(), ünvan);
                    쪽관리.범위개인쓰기(현재과정.ünvan_məkan(), ünvan, səhifə_menecer.səhifənin_ölçüsü);
                } catch (IllegalStateException XƏTA) {
                    쪽관리.MAP_səhifə(현재과정.ünvan_məkan(), ünvan, true);
                }
            }
            for (int INDEX = 0; INDEX < bölmə_VALUE_366e0bfa.Böyüklük(); INDEX++) {
                byte VALUE = bölmə_VALUE_366e0bfa.종류() == 8 ? 0 : 실행파일[bölmə_VALUE_366e0bfa.fayl_yerinə_qoymaq() + INDEX];
                쪽관리.yazmaq_bayt_VALUE(현재과정.ünvan_məkan(), bölmə_VALUE_366e0bfa.ünvan() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.başlama_ünvanı(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void çıxış_proqram(Proses_VALUE 현재과정, int vəziyyət_VALUE) {
        현재과정.Çıxış_proqram(vəziyyət_VALUE);
    }
}
