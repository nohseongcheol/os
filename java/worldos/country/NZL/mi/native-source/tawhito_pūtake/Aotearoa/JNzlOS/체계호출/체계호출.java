// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.체계호출;

import Aotearoa.JNzlOS.기억공간.whārangi_pouwhakahaere;
import Aotearoa.JNzlOS.작업.Hātepe_uara;
import Aotearoa.JNzlOS.작업.Pūwhakahōtaka;
import Aotearoa.JNzlOS.pūnaha_kōnae.실행파일적재기;
import Aotearoa.JNzlOS.pūnaha_kōnae.pūnaha_kōnae;
import Aotearoa.JNzlOS.pūnaha_kōnae.kōnae_mōhiohio;
import Aotearoa.JNzlOS.kākano.하드웨어;
import Aotearoa.JNzlOS.입력.입력관리자;
import Aotearoa.JNzlOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int pānui_anake_kara = 0;
    public static final int Rapu_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_tāurunga_mutu = 2;

    private final pūnaha_kōnae pūnaha_kōnae;
    private final whārangi_pouwhakahaere 쪽관리;
    private final Pūwhakahōtaka Pūwhakahōtaka;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 pūkoro_uara;
    private final 입력관리자 입력관리;

    public 체계호출(pūnaha_kōnae pūnaha_kōnae, whārangi_pouwhakahaere 쪽관리, Pūwhakahōtaka Pūwhakahōtaka, 하드웨어 pūkoro_uara, 입력관리자 입력관리) {
        this.pūnaha_kōnae = pūnaha_kōnae;
        this.쪽관리 = 쪽관리;
        this.Pūwhakahōtaka = Pūwhakahōtaka;
        this.pūkoro_uara = pūkoro_uara;
        this.입력관리 = 입력관리;
    }

    public int Hātepe_pūtāutu(Hātepe_uara 현재과정) {
        return 현재과정.pūtāutu_uara();
    }

    public int 부모과정식별자(Hātepe_uara 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Huaki(Hātepe_uara 현재과정, String Ingoa, int kara_uara) {
        if (kara_uara != pānui_anake_kara) {
            return -30;
        }
        return 현재과정.파일서술자().Huaki(Ingoa);
    }

    public int Pānuitia(Hātepe_uara 현재과정, int 서술자, byte[] 받을곳, int rahi) {
        if (서술자 == 0) {
            if (rahi <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 hui = 입력관리.Panuku_hui();
            if (hui == null || hui.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) hui.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Pānuitia(서술자, 받을곳, rahi);
    }

    public int Tuhia(Hātepe_uara 현재과정, int 서술자, byte[] raraunga, int rahi) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (rahi < 0 || rahi > raraunga.length) {
            return -22;
        }
        pūkoro_uara.직렬출력(new String(raraunga, 0, rahi, java.nio.charset.StandardCharsets.UTF_8));
        return rahi;
    }

    public int Kati(Hātepe_uara 현재과정, int 서술자) {
        return 현재과정.파일서술자().Kati(서술자);
    }

    public int nuku_tūranga(Hātepe_uara 현재과정, int 서술자, int 거리, int whakaatu_pūtake) {
        return 현재과정.파일서술자().nuku_tūranga(서술자, 거리, whakaatu_pūtake);
    }

    public int 서술자복제(Hātepe_uara 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Hātepe_uara 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ingoa, int aratuka_MODE) {
        kōnae_mōhiohio msinfo32_exe = pūnaha_kōnae.msinfo32_exe(Ingoa);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((aratuka_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((aratuka_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_rārangi_tūmahi(String Ingoa) {
        return "/".equals(Ingoa) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int kaiwhakamahi_pūtāutu() { return 0; }
    public int Whaipānga_kaiwhakamahi_pūtāutu() { return 0; }
    public int rōpū_pūtāutu() { return 0; }
    public int Whaipānga_rōpū_pūtāutu() { return 0; }

    public int tukutahi_kōnae(Hātepe_uara 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Pānuitia 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Hātepe_uara 현재과정, int 서술자) {
        kōnae_mōhiohio msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int kōnae_mana(Hātepe_uara 현재과정, int 서술자, int tono, int 인자) {
        if (tono == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (tono == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (tono == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (tono == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : pānui_anake_kara;
        }
        if (tono == 4) {
            return 인자 == pānui_anake_kara ? 0 : -30;
        }
        return -22;
    }

    public int Waihanga_tāurunga(String Ingoa, int mana_uru_uara) {
        return -30;
    }

    public kōnae_mōhiohio 서술자정보(Hātepe_uara 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JNzlOS", "JNzlOS", "0.1", "Java managed kernel", "i386");
    }

    public kōnae_mōhiohio kōnae_mōhiohio(String Ingoa) {
        return pūnaha_kōnae.msinfo32_exe(Ingoa);
    }

    public Hātepe_uara 과정복제(Hātepe_uara 부모) {
        return Pūwhakahōtaka.복제(부모);
    }

    public int 자식기다리기(Hātepe_uara 부모, int tamaiti_pūtāutu, boolean 기다리지않음) {
        return Pūwhakahōtaka.자식기다리기(부모, tamaiti_pūtāutu, 기다리지않음);
    }

    public int 프로그램끝(Hātepe_uara 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / whārangi_pouwhakahaere.rahinga_whārangi;
        int 끝쪽 = (새끝 + whārangi_pouwhakahaere.rahinga_whārangi - 1) / whārangi_pouwhakahaere.rahinga_whārangi;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * whārangi_pouwhakahaere.rahinga_whārangi;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_wāhi(), ADDRESS);
                } catch (IllegalStateException Pōhēhē) {
                    쪽관리.MAPI_whārangi(현재과정.ADDRESS_wāhi(), ADDRESS, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Hātepe_uara 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int mēhua = 프로그램끝(현재과정, 이전끝 + 증가량);
        return mēhua < 0 ? mēhua : 이전끝;
    }

    public int kawe_tono(Hātepe_uara 현재과정, byte[] 실행파일) {
        return kawe_tono(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int kawe_tono(Hātepe_uara 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_uara;
        try {
            IMAGE_uara = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Pōhēhē) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.wāhanga_uara wāhanga_uara : IMAGE_uara.구역들()) {
            if ((wāhanga_uara.kara_uara() & 2) == 0 || wāhanga_uara.rahi() == 0) {
                continue;
            }
            int 첫쪽 = wāhanga_uara.ADDRESS() / whārangi_pouwhakahaere.rahinga_whārangi;
            int 끝쪽 = (wāhanga_uara.ADDRESS() + wāhanga_uara.rahi() + whārangi_pouwhakahaere.rahinga_whārangi - 1) / whārangi_pouwhakahaere.rahinga_whārangi;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * whārangi_pouwhakahaere.rahinga_whārangi;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_wāhi(), ADDRESS);
                    쪽관리.범위개인쓰기(현재과정.ADDRESS_wāhi(), ADDRESS, whārangi_pouwhakahaere.rahinga_whārangi);
                } catch (IllegalStateException Pōhēhē) {
                    쪽관리.MAPI_whārangi(현재과정.ADDRESS_wāhi(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < wāhanga_uara.rahi(); INDEX++) {
                byte uara = wāhanga_uara.종류() == 8 ? 0 : 실행파일[wāhanga_uara.kōnae_tūranga() + INDEX];
                쪽관리.tuhi_paita_uara(현재과정.ADDRESS_wāhi(), wāhanga_uara.ADDRESS() + INDEX, uara);
            }
        }
        현재과정.실행문맥설정(IMAGE_uara.Start_ADDRESS(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void wehe_kaupapa(Hātepe_uara 현재과정, int tūnga_uara) {
        현재과정.Putaatu_kaupapa(tūnga_uara);
    }
}
