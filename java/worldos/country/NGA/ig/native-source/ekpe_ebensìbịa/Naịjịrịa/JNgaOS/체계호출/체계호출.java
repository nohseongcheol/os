// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.체계호출;

import Naịjịrịa.JNgaOS.기억공간.ihuakwụkwọ_njikwa;
import Naịjịrịa.JNgaOS.작업.ùsòrò_valuu_6712bde7;
import Naịjịrịa.JNgaOS.작업.배정기;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.실행파일적재기;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.sistèm_ọbọakwụkwo;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.ọbọakwụkwọ_ozi;
import Naịjịrịa.JNgaOS.mkpụrụobī_kọmpùta.ngwaike_valuu;
import Naịjịrịa.JNgaOS.입력.입력관리자;
import Naịjịrịa.JNgaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int ọgụgụ_naanị_ọkọlọtọ = 0;
    public static final int Chọọ_Mbido = 0;
    public static final int 찾기현재 = 1;
    public static final int chọta_ndebà_mèdebe = 2;

    private final sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo;
    private final ihuakwụkwọ_njikwa 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final ngwaike_valuu njìarụ_valuu;
    private final 입력관리자 입력관리;

    public 체계호출(sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo, ihuakwụkwọ_njikwa 쪽관리, 배정기 배정기, ngwaike_valuu njìarụ_valuu, 입력관리자 입력관리) {
        this.sistèm_ọbọakwụkwo = sistèm_ọbọakwụkwo;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.njìarụ_valuu = njìarụ_valuu;
        this.입력관리 = 입력관리;
    }

    public int ùsòrò_ihe_nkọwapụta(ùsòrò_valuu_6712bde7 현재과정) {
        return 현재과정.ihe_nkọwapụta_valuu();
    }

    public int 부모과정식별자(ùsòrò_valuu_6712bde7 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Mepee(ùsòrò_valuu_6712bde7 현재과정, String Aha, int ọkọlọtọ_valuu) {
        if (ọkọlọtọ_valuu != ọgụgụ_naanị_ọkọlọtọ) {
            return -30;
        }
        return 현재과정.파일서술자().Mepee(Aha);
    }

    public int Wepụta_ọzi(ùsòrò_valuu_6712bde7 현재과정, int 서술자, byte[] 받을곳, int Ụhara) {
        if (서술자 == 0) {
            if (Ụhara <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 mmèrème = 입력관리.다음사건();
            if (mmèrème == null || mmèrème.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) mmèrème.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Wepụta_ọzi(서술자, 받을곳, Ụhara);
    }

    public int Chekwaa_ozi(ùsòrò_valuu_6712bde7 현재과정, int 서술자, byte[] datà, int Ụhara) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ụhara < 0 || Ụhara > datà.length) {
            return -22;
        }
        njìarụ_valuu.직렬출력(new String(datà, 0, Ụhara, java.nio.charset.StandardCharsets.UTF_8));
        return Ụhara;
    }

    public int Mechie(ùsòrò_valuu_6712bde7 현재과정, int 서술자) {
        return 현재과정.파일서술자().Mechie(서술자);
    }

    public int 위치옮기기(ùsòrò_valuu_6712bde7 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(ùsòrò_valuu_6712bde7 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(ùsòrò_valuu_6712bde7 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Aha, int usoro_moòdù) {
        ọbọakwụkwọ_ozi Ozi_Sistèm = sistèm_ọbọakwụkwo.Ozi_Sistèm(Aha);
        if (Ozi_Sistèm == null) {
            return -2;
        }
        if ((usoro_moòdù & 1) != 0 && (Ozi_Sistèm.형태() & 0111) == 0) {
            return -13;
        }
        if ((usoro_moòdù & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int ngbanwụ_ndesịta_ēnyemọrụ(String Aha) {
        return "/".equals(Aha) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int òjìàrụ_ihe_nkọwapụta() { return 0; }
    public int kèdịìrè_òjìàrụ_ihe_nkọwapụta() { return 0; }
    public int otu_ihe_nkọwapụta() { return 0; }
    public int kèdịìrè_otu_ihe_nkọwapụta() { return 0; }

    public int hàkọọ_ọbọakwụkwọ(ùsòrò_valuu_6712bde7 현재과정, int 서술자) {
        return 현재과정.파일서술자().Ozi_Sistèm(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Wepụta_ọzi 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(ùsòrò_valuu_6712bde7 현재과정, int 서술자) {
        ọbọakwụkwọ_ozi Ozi_Sistèm = 현재과정.파일서술자().Ozi_Sistèm(서술자);
        return Ozi_Sistèm != null && (Ozi_Sistèm.형태() & 0170000) == 0020000;
    }

    public int ọbọakwụkwọ_njizi(ùsòrò_valuu_6712bde7 현재과정, int 서술자, int Ntiiwu, int 인자) {
        if (Ntiiwu == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Ntiiwu == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Ntiiwu == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Ntiiwu == 3) {
            return 현재과정.파일서술자().Ozi_Sistèm(서술자) == null ? -9 : ọgụgụ_naanị_ọkọlọtọ;
        }
        if (Ntiiwu == 4) {
            return 인자 == ọgụgụ_naanị_ọkọlọtọ ? 0 : -30;
        }
        return -22;
    }

    public int mepụta_ndebà(String Aha, int ikikere_valuu) {
        return -30;
    }

    public ọbọakwụkwọ_ozi 서술자정보(ùsòrò_valuu_6712bde7 현재과정, int 서술자) {
        return 현재과정.파일서술자().Ozi_Sistèm(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JNgaOS", "JNgaOS", "0.1", "Java managed kernel", "i386");
    }

    public ọbọakwụkwọ_ozi ọbọakwụkwọ_ozi(String Aha) {
        return sistèm_ọbọakwụkwo.Ozi_Sistèm(Aha);
    }

    public ùsòrò_valuu_6712bde7 과정복제(ùsòrò_valuu_6712bde7 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(ùsòrò_valuu_6712bde7 부모, int njìmebe_nnwā_ihe_nkọwapụta, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, njìmebe_nnwā_ihe_nkọwapụta, 기다리지않음);
    }

    public int 프로그램끝(ùsòrò_valuu_6712bde7 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
        int 끝쪽 = (새끝 + ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ - 1) / ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
        if (새끝 > 이전끝) {
            for (int indèks = 첫쪽; indèks < 끝쪽; indèks++) {
                int àdreèsì = indèks * ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
                try {
                    쪽관리.바이트읽기(현재과정.àdreèsì_ohere(), àdreèsì);
                } catch (IllegalStateException mmejọ) {
                    쪽관리.gosi_na_maapụ_ihuakwụkwọ(현재과정.àdreèsì_ohere(), àdreèsì, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(ùsòrò_valuu_6712bde7 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int mee_nnyemiwu(ùsòrò_valuu_6712bde7 현재과정, byte[] 실행파일) {
        return mee_nnyemiwu(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int mee_nnyemiwu(ùsòrò_valuu_6712bde7 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.foto foto_valuu;
        try {
            foto_valuu = 적재기.검사(실행파일);
        } catch (IllegalArgumentException mmejọ) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.nkebì_valuu nkebì_valuu : foto_valuu.구역들()) {
            if ((nkebì_valuu.ọkọlọtọ_valuu() & 2) == 0 || nkebì_valuu.Ụhara() == 0) {
                continue;
            }
            int 첫쪽 = nkebì_valuu.àdreèsì() / ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
            int 끝쪽 = (nkebì_valuu.àdreèsì() + nkebì_valuu.Ụhara() + ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ - 1) / ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
            for (int indèks = 첫쪽; indèks < 끝쪽; indèks++) {
                int àdreèsì = indèks * ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ;
                try {
                    쪽관리.바이트읽기(현재과정.àdreèsì_ohere(), àdreèsì);
                    쪽관리.범위개인쓰기(현재과정.àdreèsì_ohere(), àdreèsì, ihuakwụkwọ_njikwa.ụhàrà_ihuakwụkwọ);
                } catch (IllegalStateException mmejọ) {
                    쪽관리.gosi_na_maapụ_ihuakwụkwọ(현재과정.àdreèsì_ohere(), àdreèsì, true);
                }
            }
            for (int indèks = 0; indèks < nkebì_valuu.Ụhara(); indèks++) {
                byte valuu = nkebì_valuu.종류() == 8 ? 0 : 실행파일[nkebì_valuu.파일위치() + indèks];
                쪽관리.dee_baịtị_valuu(현재과정.àdreèsì_ohere(), nkebì_valuu.àdreèsì() + indèks, valuu);
            }
        }
        현재과정.실행문맥설정(foto_valuu.Mbido_àdreèsì(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(ùsòrò_valuu_6712bde7 현재과정, int ọnọdụ_valuu) {
        현재과정.pụọ_app(ọnọdụ_valuu);
    }
}
