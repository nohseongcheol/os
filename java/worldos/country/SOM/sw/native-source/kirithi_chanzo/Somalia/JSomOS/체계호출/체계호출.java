// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Somalia.JSomOS.체계호출;

import Somalia.JSomOS.기억공간.ukurasa_msimamizi;
import Somalia.JSomOS.작업.Mchakato_thamani;
import Somalia.JSomOS.작업.배정기;
import Somalia.JSomOS.mfumo_ya_mafaili.실행파일적재기;
import Somalia.JSomOS.mfumo_ya_mafaili.mfumo_ya_mafaili;
import Somalia.JSomOS.mfumo_ya_mafaili.faili_maelezo;
import Somalia.JSomOS.kiini.하드웨어;
import Somalia.JSomOS.입력.입력관리자;
import Somalia.JSomOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int soma_tu_alama = 0;
    public static final int Duhusi_Anza = 0;
    public static final int 찾기현재 = 1;
    public static final int gundua_ingizo_tamatia = 2;

    private final mfumo_ya_mafaili mfumo_ya_mafaili;
    private final ukurasa_msimamizi 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 kifaa_thamani;
    private final 입력관리자 입력관리;

    public 체계호출(mfumo_ya_mafaili mfumo_ya_mafaili, ukurasa_msimamizi 쪽관리, 배정기 배정기, 하드웨어 kifaa_thamani, 입력관리자 입력관리) {
        this.mfumo_ya_mafaili = mfumo_ya_mafaili;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.kifaa_thamani = kifaa_thamani;
        this.입력관리 = 입력관리;
    }

    public int Mchakato_kitambulishi(Mchakato_thamani 현재과정) {
        return 현재과정.kitambulishi_thamani();
    }

    public int 부모과정식별자(Mchakato_thamani 현재과정) {
        return 현재과정.부모식별자();
    }

    public int unda(Mchakato_thamani 현재과정, String Jina, int alama_thamani) {
        if (alama_thamani != soma_tu_alama) {
            return -30;
        }
        return 현재과정.파일서술자().unda(Jina);
    }

    public int 읽기(Mchakato_thamani 현재과정, int 서술자, byte[] 받을곳, int panga_ukubwa) {
        if (서술자 == 0) {
            if (panga_ukubwa <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 tukio = 입력관리.다음사건();
            if (tukio == null || tukio.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) tukio.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, panga_ukubwa);
    }

    public int andika(Mchakato_thamani 현재과정, int 서술자, byte[] data, int panga_ukubwa) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().teknolojia_ya_maelezo_unda(서술자) ? -30 : -9;
        }
        if (panga_ukubwa < 0 || panga_ukubwa > data.length) {
            return -22;
        }
        kifaa_thamani.직렬출력(new String(data, 0, panga_ukubwa, java.nio.charset.StandardCharsets.UTF_8));
        return panga_ukubwa;
    }

    public int funga(Mchakato_thamani 현재과정, int 서술자) {
        return 현재과정.파일서술자().funga(서술자);
    }

    public int 위치옮기기(Mchakato_thamani 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Mchakato_thamani 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Mchakato_thamani 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Jina, int mbinu_hali_tumizi) {
        faili_maelezo msinfo32_exe = mfumo_ya_mafaili.msinfo32_exe(Jina);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((mbinu_hali_tumizi & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((mbinu_hali_tumizi & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int badili_orodha_ya_kazi(String Jina) {
        return "/".equals(Jina) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int mtumiaji_kitambulishi() { return 0; }
    public int fanifu_mtumiaji_kitambulishi() { return 0; }
    public int Kikundi_kitambulishi() { return 0; }
    public int fanifu_Kikundi_kitambulishi() { return 0; }

    public int landanisha_faili(Mchakato_thamani 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Mchakato_thamani 현재과정, int 서술자) {
        faili_maelezo msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int faili_udhibiti(Mchakato_thamani 현재과정, int 서술자, int amri, int parameta_hoja) {
        if (amri == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, parameta_hoja);
        }
        if (amri == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (amri == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (parameta_hoja & 1) != 0);
        }
        if (amri == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : soma_tu_alama;
        }
        if (amri == 4) {
            return parameta_hoja == soma_tu_alama ? 0 : -30;
        }
        return -22;
    }

    public int unda_ingizo(String Jina, int kibali_thamani) {
        return -30;
    }

    public faili_maelezo 서술자정보(Mchakato_thamani 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JSomOS", "JSomOS", "0.1", "Java managed kernel", "i386");
    }

    public faili_maelezo faili_maelezo(String Jina) {
        return mfumo_ya_mafaili.msinfo32_exe(Jina);
    }

    public Mchakato_thamani 과정복제(Mchakato_thamani 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Mchakato_thamani 부모, int mtoto_kitambulishi, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, mtoto_kitambulishi, 기다리지않음);
    }

    public int 프로그램끝(Mchakato_thamani 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / ukurasa_msimamizi.ukubwa_wa_ukurasa;
        int 끝쪽 = (새끝 + ukurasa_msimamizi.ukubwa_wa_ukurasa - 1) / ukurasa_msimamizi.ukubwa_wa_ukurasa;
        if (새끝 > 이전끝) {
            for (int kielezo = 첫쪽; kielezo < 끝쪽; kielezo++) {
                int anwani = kielezo * ukurasa_msimamizi.ukubwa_wa_ukurasa;
                try {
                    쪽관리.바이트읽기(현재과정.anwani_eneo(), anwani);
                } catch (IllegalStateException kosa) {
                    쪽관리.ramani_ukurasa(현재과정.anwani_eneo(), anwani, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Mchakato_thamani 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int tekeleza_amri(Mchakato_thamani 현재과정, byte[] 실행파일) {
        return tekeleza_amri(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int tekeleza_amri(Mchakato_thamani 현재과정, byte[] 실행파일, String[] parameta_hoja, String[] 환경) {
        실행파일적재기.picha picha_thamani;
        try {
            picha_thamani = 적재기.검사(실행파일);
        } catch (IllegalArgumentException kosa) {
            return -8;
        }
        if (parameta_hoja == null || 환경 == null || parameta_hoja.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.sehemu_thamani sehemu_thamani : picha_thamani.구역들()) {
            if ((sehemu_thamani.alama_thamani() & 2) == 0 || sehemu_thamani.panga_ukubwa() == 0) {
                continue;
            }
            int 첫쪽 = sehemu_thamani.anwani() / ukurasa_msimamizi.ukubwa_wa_ukurasa;
            int 끝쪽 = (sehemu_thamani.anwani() + sehemu_thamani.panga_ukubwa() + ukurasa_msimamizi.ukubwa_wa_ukurasa - 1) / ukurasa_msimamizi.ukubwa_wa_ukurasa;
            for (int kielezo = 첫쪽; kielezo < 끝쪽; kielezo++) {
                int anwani = kielezo * ukurasa_msimamizi.ukubwa_wa_ukurasa;
                try {
                    쪽관리.바이트읽기(현재과정.anwani_eneo(), anwani);
                    쪽관리.범위개인쓰기(현재과정.anwani_eneo(), anwani, ukurasa_msimamizi.ukubwa_wa_ukurasa);
                } catch (IllegalStateException kosa) {
                    쪽관리.ramani_ukurasa(현재과정.anwani_eneo(), anwani, true);
                }
            }
            for (int kielezo = 0; kielezo < sehemu_thamani.panga_ukubwa(); kielezo++) {
                byte thamani = sehemu_thamani.종류() == 8 ? 0 : 실행파일[sehemu_thamani.파일위치() + kielezo];
                쪽관리.andika_baiti_thamani(현재과정.anwani_eneo(), sehemu_thamani.anwani() + kielezo, thamani);
            }
        }
        현재과정.실행문맥설정(picha_thamani.Anza_anwani(), parameta_hoja, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Mchakato_thamani 현재과정, int hali_thamani) {
        현재과정.toka_programu(hali_thamani);
    }
}
