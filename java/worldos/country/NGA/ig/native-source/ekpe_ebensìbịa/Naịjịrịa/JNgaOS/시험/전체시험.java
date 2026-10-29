// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Naịjịrịa.JNgaOS.기억공간.memọrị_njikwa;
import Naịjịrịa.JNgaOS.기억공간.ihuakwụkwọ_njikwa;
import Naịjịrịa.JNgaOS.입력.입력사건;
import Naịjịrịa.JNgaOS.작업.ùsòrò_valuu_6712bde7;
import Naịjịrịa.JNgaOS.체계호출.체계호출;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.실행파일적재기;
import Naịjịrịa.JNgaOS.mkpụrụobī_kọmpùta.mkpụrụobī_kọmpùta;
import Naịjịrịa.JNgaOS.usu.usu_ngwaike;
import Naịjịrịa.JNgaOS.IRQ.IRQ_njikwa;
import Naịjịrịa.JNgaOS.서술자.전역서술자표;
import Naịjịrịa.JNgaOS.Nchekwa_njìarụ.고급기술결합장치;
import Naịjịrịa.JNgaOS.njìarụ_valuu.ngwakọmpụtà_bọọs_njikwa;
import Naịjịrịa.JNgaOS.Netwọọkụ_ikpo.Netwọọkụ_Ngwaọrụ;
import Naịjịrịa.JNgaOS.Netwọọkụ_ikpo.Netwọọkụ_òkpùkpù;
import Naịjịrịa.JNgaOS.njìarụ_valuu.elekere;
import Naịjịrịa.JNgaOS.서술자.ọrụ_ọnọdụ_mwezuga;
import Naịjịrịa.JNgaOS.화면.mkpụrụedemede_gosịpụta;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        usu_ngwaike njìarụ_valuu = new usu_ngwaike();
        mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu = new mkpụrụobī_kọmpùta(njìarụ_valuu);
        mkpụrụobī_kọmpùta_valuu.Bido();

        기억공간시험(mkpụrụobī_kọmpùta_valuu);
        쪽관리시험(mkpụrụobī_kọmpùta_valuu);
        파일과과정시험(mkpụrụobī_kọmpùta_valuu);
        실행파일시험(mkpụrụobī_kọmpùta_valuu);
        입력시험(mkpụrụobī_kọmpùta_valuu);
        하드웨어시험(njìarụ_valuu);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNgaOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu) {
        memọrị_njikwa njikwa_valuu = mkpụrụobī_kọmpùta_valuu.기억공간();
        int 첫주소 = njikwa_valuu.정렬할당(100, 64);
        nkwàdo_eziokwū((첫주소 & 63) == 0, "hàkọma_valuu kepụta_Nchekwa");
        njikwa_valuu.dee_baịtị_valuu(첫주소, (byte) 0x5a);
        nkwàdo_eziokwū(njikwa_valuu.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Chekwaa_ozi");
        int 사용전 = njikwa_valuu.사용크기();
        njikwa_valuu.bupute_Nchekwa(첫주소);
        nkwàdo_eziokwū(njikwa_valuu.사용크기() < 사용전, "기억공간 bupute_Nchekwa");
    }

    private static void 쪽관리시험(mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu) {
        ihuakwụkwọ_njikwa njikwa_valuu = mkpụrụobī_kọmpùta_valuu.쪽관리();
        ihuakwụkwọ_njikwa.àdreèsì_ohere 부모공간 = njikwa_valuu.새주소공간();
        njikwa_valuu.gosi_na_maapụ_ihuakwụkwọ(부모공간, 0x1000, true);
        njikwa_valuu.dee_baịtị_valuu(부모공간, 0x1010, (byte) 7);
        ihuakwụkwọ_njikwa.àdreèsì_ohere njìmebe_nnwā_ohere = njikwa_valuu.쓰기시복사복제(부모공간);
        njikwa_valuu.dee_baịtị_valuu(njìmebe_nnwā_ohere, 0x1010, (byte) 9);
        nkwàdo_eziokwū(njikwa_valuu.바이트읽기(부모공간, 0x1010) == 7, "Chekwaa_ozi 시 ṅomie_valuu 부모 격리");
        nkwàdo_eziokwū(njikwa_valuu.바이트읽기(njìmebe_nnwā_ohere, 0x1010) == 9, "Chekwaa_ozi 시 ṅomie_valuu njìmebe_nnwā_valuu Chekwaa_ozi");
    }

    private static void 파일과과정시험(mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu) {
        byte[] ndịnà_valuu = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        mkpụrụobī_kọmpùta_valuu.sistèm_ọbọakwụkwo().파일추가("시험", ndịnà_valuu);
        ùsòrò_valuu_6712bde7 부모 = mkpụrụobī_kọmpùta_valuu.첫과정();
        체계호출 호출 = mkpụrụobī_kọmpùta_valuu.체계호출();
        int 서술자 = 호출.Mepee(부모, "/시험", 체계호출.ọgụgụ_naanị_ọkọlọtọ);
        nkwàdo_eziokwū(서술자 >= 3, "Faịlụ Mepee");

        byte[] 받을곳 = new byte[ndịnà_valuu.length];
        nkwàdo_eziokwū(호출.Wepụta_ọzi(부모, 서술자, 받을곳, 받을곳.length) == ndịnà_valuu.length, "Faịlụ Wepụta_ọzi");
        nkwàdo_eziokwū(Arrays.equals(ndịnà_valuu, 받을곳), "Faịlụ ndịnà_valuu");
        nkwàdo_eziokwū(호출.위치옮기기(부모, 서술자, 0, 체계호출.Chọọ_Mbido) == 0, "Faịlụ 위치 gàa_valuu");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        nkwàdo_eziokwū(복제서술자 >= 0, "서술자 복제");
        ùsòrò_valuu_6712bde7 njìmebe_nnwā_valuu = 호출.과정복제(부모);
        nkwàdo_eziokwū(njìmebe_nnwā_valuu.ihe_nkọwapụta_valuu() != 부모.ihe_nkọwapụta_valuu(), "ùsòrò_valuu_6712bde7 ihe_nkọwapụta_valuu 분리");
        nkwàdo_eziokwū(njìmebe_nnwā_valuu.부모식별자() == 부모.ihe_nkọwapụta_valuu(), "부모 ùsòrò_valuu_6712bde7 ihe_nkọwapụta_valuu");
        nkwàdo_eziokwū(호출.Mechie(njìmebe_nnwā_valuu, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "njìmebe_nnwā_valuu Mechie 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        nkwàdo_eziokwū(이전끝 == 0x06000000, "app_f5044b9b 끝 늘리기");
        nkwàdo_eziokwū(부모.프로그램끝() == 0x06002000, "app_f5044b9b 끝 반영");
        nkwàdo_eziokwū(njìmebe_nnwā_valuu.프로그램끝() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        njìmebe_nnwā_valuu.pụọ_app(7);
        nkwàdo_eziokwū(호출.자식기다리기(부모, njìmebe_nnwā_valuu.ihe_nkọwapụta_valuu(), false) == (7 << 8), "njìmebe_nnwā_valuu pụọ_app 기다리기");
        nkwàdo_eziokwū(호출.접근가능("시험", 1) == -13, "mee_nnyemiwu ikikere_valuu 거부");
        nkwàdo_eziokwū(호출.òjìàrụ_ihe_nkọwapụta() == 0 && 호출.otu_ihe_nkọwapụta() == 0, "사용자와 무리 ihe_nkọwapụta_valuu");
        nkwàdo_eziokwū("/".equals(호출.현재작업목록(2)) && 호출.ngbanwụ_ndesịta_ēnyemọrụ("/") == 0, "현재 작업 ndebà_ndepụta");
        nkwàdo_eziokwū(호출.단말인가(부모, 1), "표준 출력 단말");
        nkwàdo_eziokwū("JNgaOS".equals(호출.체계정보().sistèm_akara_ahà()), "OS_valuu Ozi_Sistèm");
    }

    private static void 실행파일시험(mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu) {
        byte[] datà = new byte[92];
        datà[0] = 0x7f;
        datà[1] = 'E';
        datà[2] = 'L';
        datà[3] = 'F';
        datà[4] = 1;
        datà[5] = 1;
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 24, 0x04001000);
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 32, 52);
        짧은정수쓰기(datà, 46, 40);
        짧은정수쓰기(datà, 48, 1);
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 56, 8);
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 60, 2);
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 64, 0x04002000);
        dee_ọnụọgụ_nzùrùòkè_valuu(datà, 72, 64);

        실행파일적재기.foto foto_valuu = new 실행파일적재기().검사(datà);
        nkwàdo_eziokwū(foto_valuu.Mbido_àdreèsì() == 0x04001000, "ELF Bido àdreèsì");
        nkwàdo_eziokwū(foto_valuu.구역들().size() == 1 && foto_valuu.구역들().get(0).종류() == 8, "ELF 빈 datà nkebì_valuu");
        int 서술자 = mkpụrụobī_kọmpùta_valuu.체계호출().Mepee(mkpụrụobī_kọmpùta_valuu.첫과정(), "시험", 체계호출.ọgụgụ_naanị_ọkọlọtọ);
        nkwàdo_eziokwū(mkpụrụobī_kọmpùta_valuu.체계호출().ọbọakwụkwọ_njizi(mkpụrụobī_kọmpùta_valuu.첫과정(), 서술자, 2, 1) == 0, "mee_nnyemiwu 시 Mechie Mwube");
        nkwàdo_eziokwū(mkpụrụobī_kọmpùta_valuu.체계호출().mee_nnyemiwu(mkpụrụobī_kọmpùta_valuu.첫과정(), datà, new String[] {"시험", "값"}, new String[] {"Asụsụ=한국어"}) == 0, "ELF mee_nnyemiwu foto_valuu 적재");
        nkwàdo_eziokwū(mkpụrụobī_kọmpùta_valuu.첫과정().실행시작주소() == 0x04001000, "mee_nnyemiwu Bido àdreèsì 반영");
        nkwàdo_eziokwū(mkpụrụobī_kọmpùta_valuu.첫과정().실행인자().length == 2 && mkpụrụobī_kọmpùta_valuu.첫과정().환경값().length == 1, "mee_nnyemiwu 인자와 환경");
        nkwàdo_eziokwū(!mkpụrụobī_kọmpùta_valuu.첫과정().파일서술자().열려있음(서술자), "mee_nnyemiwu 시 서술자 Mechie");
        nkwàdo_eziokwū(mkpụrụobī_kọmpùta_valuu.쪽관리().바이트읽기(mkpụrụobī_kọmpùta_valuu.첫과정().àdreèsì_ohere(), 0x04002000) == 0, "빈 datà nkebì_valuu 영 kwàdo_mmàlite");
    }

    private static void 입력시험(mkpụrụobī_kọmpùta mkpụrụobī_kọmpùta_valuu) {
        mkpụrụobī_kọmpùta_valuu.입력관리().키누름('가');
        mkpụrụobī_kọmpùta_valuu.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = mkpụrụobī_kọmpùta_valuu.입력관리().다음사건();
        입력사건 둘째사건 = mkpụrụobī_kọmpùta_valuu.입력관리().다음사건();
        nkwàdo_eziokwū(첫사건.사건종류() == 입력사건.종류.키누름, "자판 mmèrème");
        nkwàdo_eziokwū(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 gàa_valuu mmèrème");
    }

    private static void 하드웨어시험(usu_ngwaike njìarụ_valuu) {
        njìarụ_valuu.dee_pọọt_baịtị(0x3f8, 0xab);
        nkwàdo_eziokwū(njìarụ_valuu.포트바이트읽기(0x3f8) == 0xab, "ngwaike_pọọt I_O 경계");
        nkwàdo_eziokwū(njìarụ_valuu.직렬기록().contains("JNgaOS"), "직렬 ndekọ_NDEKỌ");
    }

    private static void 개입중단과서술자시험() {
        IRQ_njikwa njikwa_valuu = new IRQ_njikwa();
        njikwa_valuu.등록(0x21, Nchekwa_àdreèsì -> Nchekwa_àdreèsì + 4);
        njikwa_valuu.gbanye();
        nkwàdo_eziokwū(njikwa_valuu.kesaa_valuu(0x21, 100) == 104, "IRQ kesaa_valuu");
        njikwa_valuu.mwepụ̀_ike();
        nkwàdo_eziokwū(njikwa_valuu.kesaa_valuu(0x21, 100) == 100, "IRQ mwepụ̀_ike");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.Seti_Ngwa_ihe_dịadị();
        nkwàdo_eziokwū(서술자표.조각들().size() == 5, "전역 서술자표");
        ọrụ_ọnọdụ_mwezuga ọrụ_ọnọdụ = new ọrụ_ọnọdụ_mwezuga();
        ọrụ_ọnọdụ.특권쌓임공간설정(0x10, 0x800000);
        nkwàdo_eziokwū(ọrụ_ọnọdụ.영번쌓임조각() == 0x10 && ọrụ_ọnọdụ.영번쌓임주소() == 0x800000, "작업 ọnọdụ_valuu nkebì_valuu");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Nchekwa_njìarụ = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.nkebì_ụha];
        byte[] 읽은자료 = new byte[고급기술결합장치.nkebì_ụha];
        쓸자료[17] = 42;
        Nchekwa_njìarụ.Chekwaa_ozi(2, 쓸자료);
        Nchekwa_njìarụ.Wepụta_ọzi(2, 읽은자료);
        nkwàdo_eziokwū(읽은자료[17] == 42, "ATA nkebì_valuu 읽고 Chekwaa_ozi");

        ngwakọmpụtà_bọọs_njikwa ngwakọmpụtà = new ngwakọmpụtà_bọọs_njikwa();
        ngwakọmpụtà.발견(new ngwakọmpụtà_bọọs_njikwa.njìarụ_valuu(0x1022, 0x2000, 0xc000, 11));
        nkwàdo_eziokwū(ngwakọmpụtà.chọta_ndebà(0x1022, 0x2000) != null, "주변 njìarụ_valuu chọta_ndebà");

        byte[] Etāneèt_okpokoro = new byte[34];
        Etāneèt_okpokoro[12] = 0x08;
        Etāneèt_okpokoro[13] = 0x00;
        Etāneèt_okpokoro[14] = 0x45;
        nkwàdo_eziokwū(Netwọọkụ_Ngwaọrụ.이더넷상위규약(Etāneèt_okpokoro) == 0x0800, "이더넷 상위 ngō_valuu");
        nkwàdo_eziokwū(Netwọọkụ_Ngwaọrụ.상호통신망규약사판인가(Etāneèt_okpokoro, 14), "상호통신망규약 4판");
        nkwàdo_eziokwū(Netwọọkụ_Ngwaọrụ.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        dee_ọnụọgụ_nzùrùòkè_valuu(첫구역, 454, 63);
        dee_ọnụọgụ_nzùrùòkè_valuu(첫구역, 458, 1024);
        nkwàdo_eziokwū(new 기본분할영역표().Wepụta_ọzi(첫구역).size() == 1, "Ngwa_ihe_dịadị 분할 영역표");

        Netwọọkụ_òkpùkpù òkpùkpù_valuu = new Netwọọkụ_òkpùkpù();
        int[] 받은수 = new int[1];
        òkpùkpù_valuu.사용자자료단위등록(7, (datà, Bido, ogologo_valuu) -> 받은수[0]++);
        byte[] okpokoro_indèks = new byte[14 + 20 + 8];
        okpokoro_indèks[12] = 0x08;
        okpokoro_indèks[13] = 0x00;
        okpokoro_indèks[14] = 0x45;
        okpokoro_indèks[16] = 0;
        okpokoro_indèks[17] = 28;
        okpokoro_indèks[23] = 17;
        okpokoro_indèks[36] = 0;
        okpokoro_indèks[37] = 7;
        nkwàdo_eziokwū(òkpùkpù_valuu.이더넷받기(okpokoro_indèks) && 받은수[0] == 1, "òjìàrụ datà ihe_ọmụmụ_valuu kesaa_valuu");
    }

    private static void 화면과시계시험() {
        mkpụrụedemede_gosịpụta 화면 = new mkpụrụedemede_gosịpụta();
        화면.출력("가나\n다");
        nkwàdo_eziokwū(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        elekere elekere = new elekere(100);
        for (int indèks = 0; indèks < 10; indèks++) {
            elekere.틱();
        }
        nkwàdo_eziokwū(elekere.지난밀리초() == 100, "elekere 틱 변환");
    }

    private static void dee_ọnụọgụ_nzùrùòkè_valuu(byte[] datà, int 위치, int valuu) {
        datà[위치] = (byte) valuu;
        datà[위치 + 1] = (byte) (valuu >>> 8);
        datà[위치 + 2] = (byte) (valuu >>> 16);
        datà[위치 + 3] = (byte) (valuu >>> 24);
    }

    private static void 짧은정수쓰기(byte[] datà, int 위치, int valuu) {
        datà[위치] = (byte) valuu;
        datà[위치 + 1] = (byte) (valuu >>> 8);
    }

    private static void nkwàdo_eziokwū(boolean ọnọdụ, String Aha) {
        if (!ọnọdụ) {
            throw new AssertionError("ọdịdà_valuu: " + Aha);
        }
        통과수++;
        System.out.println("통과: " + Aha);
    }
}
