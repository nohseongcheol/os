// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iMalawi.JMwiOS.체계호출;

import iMalawi.JMwiOS.기억공간.ikhasi_imeneja;
import iMalawi.JMwiOS.작업.Inqubo_inani;
import iMalawi.JMwiOS.작업.배정기;
import iMalawi.JMwiOS.isistimu_yefayela.실행파일적재기;
import iMalawi.JMwiOS.isistimu_yefayela.isistimu_yefayela;
import iMalawi.JMwiOS.isistimu_yefayela.ifayela_ulwazi;
import iMalawi.JMwiOS.ikhenela.하드웨어;
import iMalawi.JMwiOS.입력.입력관리자;
import iMalawi.JMwiOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int fundwayo_kuphela_iflegi = 0;
    public static final int Bheka_qala = 0;
    public static final int 찾기현재 = 1;
    public static final int thola_okufakwayo_yekisa = 2;

    private final isistimu_yefayela isistimu_yefayela;
    private final ikhasi_imeneja 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 idivayisi_inani;
    private final 입력관리자 입력관리;

    public 체계호출(isistimu_yefayela isistimu_yefayela, ikhasi_imeneja 쪽관리, 배정기 배정기, 하드웨어 idivayisi_inani, 입력관리자 입력관리) {
        this.isistimu_yefayela = isistimu_yefayela;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.idivayisi_inani = idivayisi_inani;
        this.입력관리 = 입력관리;
    }

    public int Inqubo_isivezi(Inqubo_inani 현재과정) {
        return 현재과정.isivezi_inani();
    }

    public int 부모과정식별자(Inqubo_inani 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Vula(Inqubo_inani 현재과정, String Igama, int iflegi_inani) {
        if (iflegi_inani != fundwayo_kuphela_iflegi) {
            return -30;
        }
        return 현재과정.파일서술자().Vula(Igama);
    }

    public int Funda(Inqubo_inani 현재과정, int 서술자, byte[] 받을곳, int Ubungako) {
        if (서술자 == 0) {
            if (Ubungako <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 isigameko = 입력관리.다음사건();
            if (isigameko == null || isigameko.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) isigameko.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Funda(서술자, 받을곳, Ubungako);
    }

    public int Bhala(Inqubo_inani 현재과정, int 서술자, byte[] imininingwane, int Ubungako) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ubungako < 0 || Ubungako > imininingwane.length) {
            return -22;
        }
        idivayisi_inani.직렬출력(new String(imininingwane, 0, Ubungako, java.nio.charset.StandardCharsets.UTF_8));
        return Ubungako;
    }

    public int Vala(Inqubo_inani 현재과정, int 서술자) {
        return 현재과정.파일서술자().Vala(서술자);
    }

    public int 위치옮기기(Inqubo_inani 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Inqubo_inani 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Inqubo_inani 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Igama, int indlela_inqubo) {
        ifayela_ulwazi I_msinfo32_exe = isistimu_yefayela.I_msinfo32_exe(Igama);
        if (I_msinfo32_exe == null) {
            return -2;
        }
        if ((indlela_inqubo & 1) != 0 && (I_msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((indlela_inqubo & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int guqulela_kokunye_uhlu_lwemisebenzi(String Igama) {
        return "/".equals(Igama) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int umsebenzisi_isivezi() { return 0; }
    public int lungisayo_kufanelekayo_umsebenzisi_isivezi() { return 0; }
    public int iqoqo_isivezi() { return 0; }
    public int lungisayo_kufanelekayo_iqoqo_isivezi() { return 0; }

    public int i_sync_ifayela(Inqubo_inani 현재과정, int 서술자) {
        return 현재과정.파일서술자().I_msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Funda 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Inqubo_inani 현재과정, int 서술자) {
        ifayela_ulwazi I_msinfo32_exe = 현재과정.파일서술자().I_msinfo32_exe(서술자);
        return I_msinfo32_exe != null && (I_msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int ifayela_isilawuli(Inqubo_inani 현재과정, int 서술자, int Umlayelo, int 인자) {
        if (Umlayelo == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Umlayelo == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Umlayelo == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Umlayelo == 3) {
            return 현재과정.파일서술자().I_msinfo32_exe(서술자) == null ? -9 : fundwayo_kuphela_iflegi;
        }
        if (Umlayelo == 4) {
            return 인자 == fundwayo_kuphela_iflegi ? 0 : -30;
        }
        return -22;
    }

    public int yakha_okufakwayo(String Igama, int imvume_inani) {
        return -30;
    }

    public ifayela_ulwazi 서술자정보(Inqubo_inani 현재과정, int 서술자) {
        return 현재과정.파일서술자().I_msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JMwiOS", "JMwiOS", "0.1", "Java managed kernel", "i386");
    }

    public ifayela_ulwazi ifayela_ulwazi(String Igama) {
        return isistimu_yefayela.I_msinfo32_exe(Igama);
    }

    public Inqubo_inani 과정복제(Inqubo_inani 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Inqubo_inani 부모, int ingane_isivezi, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, ingane_isivezi, 기다리지않음);
    }

    public int 프로그램끝(Inqubo_inani 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / ikhasi_imeneja.ubungako_bekhasi;
        int 끝쪽 = (새끝 + ikhasi_imeneja.ubungako_bekhasi - 1) / ikhasi_imeneja.ubungako_bekhasi;
        if (새끝 > 이전끝) {
            for (int thola_inkomba = 첫쪽; thola_inkomba < 끝쪽; thola_inkomba++) {
                int ikheli = thola_inkomba * ikhasi_imeneja.ubungako_bekhasi;
                try {
                    쪽관리.바이트읽기(현재과정.ikheli_indawo(), ikheli);
                } catch (IllegalStateException Iphutha) {
                    쪽관리.faka_kumephu_ikhasi(현재과정.ikheli_indawo(), ikheli, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Inqubo_inani 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int yenza_umyalo(Inqubo_inani 현재과정, byte[] 실행파일) {
        return yenza_umyalo(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int yenza_umyalo(Inqubo_inani 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.isithombe isithombe_inani;
        try {
            isithombe_inani = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Iphutha) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.isigaba_inani isigaba_inani : isithombe_inani.구역들()) {
            if ((isigaba_inani.iflegi_inani() & 2) == 0 || isigaba_inani.Ubungako() == 0) {
                continue;
            }
            int 첫쪽 = isigaba_inani.ikheli() / ikhasi_imeneja.ubungako_bekhasi;
            int 끝쪽 = (isigaba_inani.ikheli() + isigaba_inani.Ubungako() + ikhasi_imeneja.ubungako_bekhasi - 1) / ikhasi_imeneja.ubungako_bekhasi;
            for (int thola_inkomba = 첫쪽; thola_inkomba < 끝쪽; thola_inkomba++) {
                int ikheli = thola_inkomba * ikhasi_imeneja.ubungako_bekhasi;
                try {
                    쪽관리.바이트읽기(현재과정.ikheli_indawo(), ikheli);
                    쪽관리.범위개인쓰기(현재과정.ikheli_indawo(), ikheli, ikhasi_imeneja.ubungako_bekhasi);
                } catch (IllegalStateException Iphutha) {
                    쪽관리.faka_kumephu_ikhasi(현재과정.ikheli_indawo(), ikheli, true);
                }
            }
            for (int thola_inkomba = 0; thola_inkomba < isigaba_inani.Ubungako(); thola_inkomba++) {
                byte inani = isigaba_inani.종류() == 8 ? 0 : 실행파일[isigaba_inani.파일위치() + thola_inkomba];
                쪽관리.bhala_ibhayithi_inani(현재과정.ikheli_indawo(), isigaba_inani.ikheli() + thola_inkomba, inani);
            }
        }
        현재과정.실행문맥설정(isithombe_inani.qala_ikheli(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Inqubo_inani 현재과정, int isimo_inani) {
        현재과정.phuma_i_app(isimo_inani);
    }
}
