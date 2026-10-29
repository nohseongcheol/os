// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.체계호출;

import an_Ríocht_Aontaithe.JGbrOS.기억공간.leathanach_bainisteoir;
import an_Ríocht_Aontaithe.JGbrOS.작업.Próiseas_VALUE;
import an_Ríocht_Aontaithe.JGbrOS.작업.Sceidealóir;
import an_Ríocht_Aontaithe.JGbrOS.córas_comhad.실행파일적재기;
import an_Ríocht_Aontaithe.JGbrOS.córas_comhad.córas_comhad;
import an_Ríocht_Aontaithe.JGbrOS.córas_comhad.comhad_faisnéis;
import an_Ríocht_Aontaithe.JGbrOS.eithne.하드웨어;
import an_Ríocht_Aontaithe.JGbrOS.입력.입력관리자;
import an_Ríocht_Aontaithe.JGbrOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int inléite_amháin_bratach = 0;
    public static final int SEARCH_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_iontráil_cuir_deireadh_le = 2;

    private final córas_comhad córas_comhad;
    private final leathanach_bainisteoir 쪽관리;
    private final Sceidealóir Sceidealóir;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 gléas_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(córas_comhad córas_comhad, leathanach_bainisteoir 쪽관리, Sceidealóir Sceidealóir, 하드웨어 gléas_VALUE, 입력관리자 입력관리) {
        this.córas_comhad = córas_comhad;
        this.쪽관리 = 쪽관리;
        this.Sceidealóir = Sceidealóir;
        this.gléas_VALUE = gléas_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Próiseas_aitheantóir(Próiseas_VALUE 현재과정) {
        return 현재과정.aitheantóir_VALUE();
    }

    public int 부모과정식별자(Próiseas_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Oscail(Próiseas_VALUE 현재과정, String Ainm, int bratach_VALUE) {
        if (bratach_VALUE != inléite_amháin_bratach) {
            return -30;
        }
        return 현재과정.파일서술자().Oscail(Ainm);
    }

    public int Léigh(Próiseas_VALUE 현재과정, int 서술자, byte[] 받을곳, int Méid) {
        if (서술자 == 0) {
            if (Méid <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 ócáid = 입력관리.Ar_aghaidh_ócáid();
            if (ócáid == null || ócáid.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) ócáid.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Léigh(서술자, 받을곳, Méid);
    }

    public int Scríobh(Próiseas_VALUE 현재과정, int 서술자, byte[] sonraí, int Méid) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().teicneolaíocht_faisnéise_oscail(서술자) ? -30 : -9;
        }
        if (Méid < 0 || Méid > sonraí.length) {
            return -22;
        }
        gléas_VALUE.직렬출력(new String(sonraí, 0, Méid, java.nio.charset.StandardCharsets.UTF_8));
        return Méid;
    }

    public int Dún(Próiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Dún(서술자);
    }

    public int bog_suíomh(Próiseas_VALUE 현재과정, int 서술자, int 거리, int teilgean_fréamh) {
        return 현재과정.파일서술자().bog_suíomh(서술자, 거리, teilgean_fréamh);
    }

    public int 서술자복제(Próiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Próiseas_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ainm, int modh_mód) {
        comhad_faisnéis msinfo32_exe = córas_comhad.msinfo32_exe(Ainm);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((modh_mód & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((modh_mód & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_liosta_tascanna(String Ainm) {
        return "/".equals(Ainm) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int úsáideoir_aitheantóir() { return 0; }
    public int éifeachtach_úsáideoir_aitheantóir() { return 0; }
    public int Grúpa_aitheantóir() { return 0; }
    public int éifeachtach_Grúpa_aitheantóir() { return 0; }

    public int sioncronaigh_comhad(Próiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Léigh 전용이어서 밀어낼 자료가 없다.
    }

    public boolean teicneolaíocht_faisnéise_Teirminéal(Próiseas_VALUE 현재과정, int 서술자) {
        comhad_faisnéis msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int comhad_rialú(Próiseas_VALUE 현재과정, int 서술자, int Ordú, int paraiméadar_argóint) {
        if (Ordú == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, paraiméadar_argóint);
        }
        if (Ordú == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Ordú == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (paraiméadar_argóint & 1) != 0);
        }
        if (Ordú == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : inléite_amháin_bratach;
        }
        if (Ordú == 4) {
            return paraiméadar_argóint == inléite_amháin_bratach ? 0 : -30;
        }
        return -22;
    }

    public int Create_iontráil(String Ainm, int cead_VALUE) {
        return -30;
    }

    public comhad_faisnéis 서술자정보(Próiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JGbrOS", "JGbrOS", "0.1", "Java managed kernel", "i386");
    }

    public comhad_faisnéis comhad_faisnéis(String Ainm) {
        return córas_comhad.msinfo32_exe(Ainm);
    }

    public Próiseas_VALUE 과정복제(Próiseas_VALUE 부모) {
        return Sceidealóir.복제(부모);
    }

    public int 자식기다리기(Próiseas_VALUE 부모, int leanbh_aitheantóir, boolean 기다리지않음) {
        return Sceidealóir.자식기다리기(부모, leanbh_aitheantóir, 기다리지않음);
    }

    public int 프로그램끝(Próiseas_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / leathanach_bainisteoir.méid_leathanaigh;
        int 끝쪽 = (새끝 + leathanach_bainisteoir.méid_leathanaigh - 1) / leathanach_bainisteoir.méid_leathanaigh;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * leathanach_bainisteoir.méid_leathanaigh;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_spás(), ADDRESS);
                } catch (IllegalStateException ERREÁID) {
                    쪽관리.MAPÁIL_leathanach(현재과정.ADDRESS_spás(), ADDRESS, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Próiseas_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int tomhas = 프로그램끝(현재과정, 이전끝 + 증가량);
        return tomhas < 0 ? tomhas : 이전끝;
    }

    public int Rith_ordú(Próiseas_VALUE 현재과정, byte[] 실행파일) {
        return Rith_ordú(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int Rith_ordú(Próiseas_VALUE 현재과정, byte[] 실행파일, String[] paraiméadar_argóint, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException ERREÁID) {
            return -8;
        }
        if (paraiméadar_argóint == null || 환경 == null || paraiméadar_argóint.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.rannán_VALUE rannán_VALUE : IMAGE_VALUE.구역들()) {
            if ((rannán_VALUE.bratach_VALUE() & 2) == 0 || rannán_VALUE.Méid() == 0) {
                continue;
            }
            int 첫쪽 = rannán_VALUE.ADDRESS() / leathanach_bainisteoir.méid_leathanaigh;
            int 끝쪽 = (rannán_VALUE.ADDRESS() + rannán_VALUE.Méid() + leathanach_bainisteoir.méid_leathanaigh - 1) / leathanach_bainisteoir.méid_leathanaigh;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * leathanach_bainisteoir.méid_leathanaigh;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_spás(), ADDRESS);
                    쪽관리.범위개인쓰기(현재과정.ADDRESS_spás(), ADDRESS, leathanach_bainisteoir.méid_leathanaigh);
                } catch (IllegalStateException ERREÁID) {
                    쪽관리.MAPÁIL_leathanach(현재과정.ADDRESS_spás(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < rannán_VALUE.Méid(); INDEX++) {
                byte VALUE = rannán_VALUE.종류() == 8 ? 0 : 실행파일[rannán_VALUE.comhad_suíomh() + INDEX];
                쪽관리.scríobh_beart_VALUE(현재과정.ADDRESS_spás(), rannán_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.seoladh_tosaithe(), paraiméadar_argóint, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void scoir_clár_55b3a1cd(Próiseas_VALUE 현재과정, int staid_VALUE) {
        현재과정.scoir_clár(staid_VALUE);
    }
}
