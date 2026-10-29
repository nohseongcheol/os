// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.체계호출;

import EMzantsi_Afrika.JZafOS.기억공간.ikhasi_umphathi;
import EMzantsi_Afrika.JZafOS.작업.Inkqubo_ixabiso;
import EMzantsi_Afrika.JZafOS.작업.배정기;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.실행파일적재기;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.uhlobo_loseto_lwefayile;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.ifayile_ingcaciso;
import EMzantsi_Afrika.JZafOS.ikheneli.하드웨어;
import EMzantsi_Afrika.JZafOS.입력.입력관리자;
import EMzantsi_Afrika.JZafOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int efundwayo_kuphela_iflegi = 0;
    public static final int Khangela_qala = 0;
    public static final int 찾기현재 = 1;
    public static final int fumana_ufako_nkcukacha_phela = 2;

    private final uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile;
    private final ikhasi_umphathi 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 isixhobo_ixabiso;
    private final 입력관리자 입력관리;

    public 체계호출(uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile, ikhasi_umphathi 쪽관리, 배정기 배정기, 하드웨어 isixhobo_ixabiso, 입력관리자 입력관리) {
        this.uhlobo_loseto_lwefayile = uhlobo_loseto_lwefayile;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.isixhobo_ixabiso = isixhobo_ixabiso;
        this.입력관리 = 입력관리;
    }

    public int Inkqubo_isalathisi(Inkqubo_ixabiso 현재과정) {
        return 현재과정.isalathisi_ixabiso();
    }

    public int 부모과정식별자(Inkqubo_ixabiso 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Vula(Inkqubo_ixabiso 현재과정, String Igama, int iflegi_ixabiso) {
        if (iflegi_ixabiso != efundwayo_kuphela_iflegi) {
            return -30;
        }
        return 현재과정.파일서술자().Vula(Igama);
    }

    public int Funda(Inkqubo_ixabiso 현재과정, int 서술자, byte[] 받을곳, int Ubukhulu) {
        if (서술자 == 0) {
            if (Ubukhulu <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 umcimbi = 입력관리.다음사건();
            if (umcimbi == null || umcimbi.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) umcimbi.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Funda(서술자, 받을곳, Ubukhulu);
    }

    public int Bhala(Inkqubo_ixabiso 현재과정, int 서술자, byte[] iingcombolo, int Ubukhulu) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ubukhulu < 0 || Ubukhulu > iingcombolo.length) {
            return -22;
        }
        isixhobo_ixabiso.직렬출력(new String(iingcombolo, 0, Ubukhulu, java.nio.charset.StandardCharsets.UTF_8));
        return Ubukhulu;
    }

    public int Vala(Inkqubo_ixabiso 현재과정, int 서술자) {
        return 현재과정.파일서술자().Vala(서술자);
    }

    public int 위치옮기기(Inkqubo_ixabiso 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Inkqubo_ixabiso 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Inkqubo_ixabiso 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Igama, int imethodi_imo) {
        ifayile_ingcaciso i_msinfo32_exe = uhlobo_loseto_lwefayile.i_msinfo32_exe(Igama);
        if (i_msinfo32_exe == null) {
            return -2;
        }
        if ((imethodi_imo & 1) != 0 && (i_msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((imethodi_imo & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int tshintshela_uluhlu_lwemisebenzi(String Igama) {
        return "/".equals(Igama) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int umsebenzisi_isalathisi() { return 0; }
    public int elungileyo_umsebenzisi_isalathisi() { return 0; }
    public int iqela_isalathisi() { return 0; }
    public int elungileyo_iqela_isalathisi() { return 0; }

    public int ngqamanisa_ifayile(Inkqubo_ixabiso 현재과정, int 서술자) {
        return 현재과정.파일서술자().i_msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Funda 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Inkqubo_ixabiso 현재과정, int 서술자) {
        ifayile_ingcaciso i_msinfo32_exe = 현재과정.파일서술자().i_msinfo32_exe(서술자);
        return i_msinfo32_exe != null && (i_msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int ifayile_isilawuli(Inkqubo_ixabiso 현재과정, int 서술자, int Umyalelo, int 인자) {
        if (Umyalelo == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Umyalelo == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Umyalelo == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Umyalelo == 3) {
            return 현재과정.파일서술자().i_msinfo32_exe(서술자) == null ? -9 : efundwayo_kuphela_iflegi;
        }
        if (Umyalelo == 4) {
            return 인자 == efundwayo_kuphela_iflegi ? 0 : -30;
        }
        return -22;
    }

    public int yila_ufako_nkcukacha(String Igama, int imvume_ixabiso) {
        return -30;
    }

    public ifayile_ingcaciso 서술자정보(Inkqubo_ixabiso 현재과정, int 서술자) {
        return 현재과정.파일서술자().i_msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JZafOS", "JZafOS", "0.1", "Java managed kernel", "i386");
    }

    public ifayile_ingcaciso ifayile_ingcaciso(String Igama) {
        return uhlobo_loseto_lwefayile.i_msinfo32_exe(Igama);
    }

    public Inkqubo_ixabiso 과정복제(Inkqubo_ixabiso 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Inkqubo_ixabiso 부모, int umntwana_isalathisi, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, umntwana_isalathisi, 기다리지않음);
    }

    public int 프로그램끝(Inkqubo_ixabiso 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / ikhasi_umphathi.ubungakanani_bekhasi;
        int 끝쪽 = (새끝 + ikhasi_umphathi.ubungakanani_bekhasi - 1) / ikhasi_umphathi.ubungakanani_bekhasi;
        if (새끝 > 이전끝) {
            for (int indeksa = 첫쪽; indeksa < 끝쪽; indeksa++) {
                int idilesi = indeksa * ikhasi_umphathi.ubungakanani_bekhasi;
                try {
                    쪽관리.바이트읽기(현재과정.idilesi_isithuba(), idilesi);
                } catch (IllegalStateException Impazamo) {
                    쪽관리.beka_emephini_ikhasi(현재과정.idilesi_isithuba(), idilesi, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Inkqubo_ixabiso 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int ukwenza_umyalelo(Inkqubo_ixabiso 현재과정, byte[] 실행파일) {
        return ukwenza_umyalelo(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int ukwenza_umyalelo(Inkqubo_ixabiso 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.umfanekiso umfanekiso_ixabiso;
        try {
            umfanekiso_ixabiso = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Impazamo) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.icandelo_ixabiso icandelo_ixabiso : umfanekiso_ixabiso.구역들()) {
            if ((icandelo_ixabiso.iflegi_ixabiso() & 2) == 0 || icandelo_ixabiso.Ubukhulu() == 0) {
                continue;
            }
            int 첫쪽 = icandelo_ixabiso.idilesi() / ikhasi_umphathi.ubungakanani_bekhasi;
            int 끝쪽 = (icandelo_ixabiso.idilesi() + icandelo_ixabiso.Ubukhulu() + ikhasi_umphathi.ubungakanani_bekhasi - 1) / ikhasi_umphathi.ubungakanani_bekhasi;
            for (int indeksa = 첫쪽; indeksa < 끝쪽; indeksa++) {
                int idilesi = indeksa * ikhasi_umphathi.ubungakanani_bekhasi;
                try {
                    쪽관리.바이트읽기(현재과정.idilesi_isithuba(), idilesi);
                    쪽관리.범위개인쓰기(현재과정.idilesi_isithuba(), idilesi, ikhasi_umphathi.ubungakanani_bekhasi);
                } catch (IllegalStateException Impazamo) {
                    쪽관리.beka_emephini_ikhasi(현재과정.idilesi_isithuba(), idilesi, true);
                }
            }
            for (int indeksa = 0; indeksa < icandelo_ixabiso.Ubukhulu(); indeksa++) {
                byte ixabiso = icandelo_ixabiso.종류() == 8 ? 0 : 실행파일[icandelo_ixabiso.파일위치() + indeksa];
                쪽관리.bhala_ibhayithi_ixabiso(현재과정.idilesi_isithuba(), icandelo_ixabiso.idilesi() + indeksa, ixabiso);
            }
        }
        현재과정.실행문맥설정(umfanekiso_ixabiso.qala_idilesi(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Inkqubo_ixabiso 현재과정, int imo_ixabiso) {
        현재과정.phuma_inkqubo(imo_ixabiso);
    }
}
