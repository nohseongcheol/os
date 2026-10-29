// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Éire.JIrlOS.기억공간.Cuimhne_bainisteoir;
import Éire.JIrlOS.기억공간.leathanach_bainisteoir;
import Éire.JIrlOS.입력.입력사건;
import Éire.JIrlOS.작업.Próiseas_VALUE;
import Éire.JIrlOS.체계호출.체계호출;
import Éire.JIrlOS.córas_comhad.실행파일적재기;
import Éire.JIrlOS.eithne.eithne;
import Éire.JIrlOS.óstach.호스트하드웨어;
import Éire.JIrlOS.IRQ.IRQ_bainisteoir;
import Éire.JIrlOS.서술자.전역서술자표;
import Éire.JIrlOS.Stóras_gléas.고급기술결합장치;
import Éire.JIrlOS.gléas_VALUE.oiriúint_bus_bainisteoir;
import Éire.JIrlOS.Líonra_Cruach.Líonra_Uirlisí;
import Éire.JIrlOS.Líonra_Cruach.Líonra_sraith;
import Éire.JIrlOS.gléas_VALUE.Clog;
import Éire.JIrlOS.서술자.tasc_staid_deighleán;
import Éire.JIrlOS.화면.carachtar_taispeáin;
import Éire.JIrlOS.córas_comhad.기본분할영역표;

public final class 전체시험 {
    private static int seol_ar_aghaidh_COUNT;

    private 전체시험() {
    }

    public static void main(String[] paraiméadar_argóint) {
        호스트하드웨어 gléas_VALUE = new 호스트하드웨어();
        eithne eithne_VALUE = new eithne(gléas_VALUE);
        eithne_VALUE.Rith_2();

        기억공간시험(eithne_VALUE);
        쪽관리시험(eithne_VALUE);
        파일과과정시험(eithne_VALUE);
        실행파일시험(eithne_VALUE);
        입력시험(eithne_VALUE);
        하드웨어시험(gléas_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JIrlOS 시험 seol_ar_aghaidh_VALUE: " + seol_ar_aghaidh_COUNT);
    }

    private static void 기억공간시험(eithne eithne_VALUE) {
        Cuimhne_bainisteoir bainisteoir_VALUE = eithne_VALUE.기억공간();
        int 첫주소 = bainisteoir_VALUE.정렬할당(100, 64);
        fíoraigh((첫주소 & 63) == 0, "ailínigh_VALUE leithdháil_Stóras");
        bainisteoir_VALUE.scríobh_beart_VALUE(첫주소, (byte) 0x5a);
        fíoraigh(bainisteoir_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Scríobh");
        int 사용전 = bainisteoir_VALUE.사용크기();
        bainisteoir_VALUE.leagan_Stóras(첫주소);
        fíoraigh(bainisteoir_VALUE.사용크기() < 사용전, "기억공간 leagan_Stóras");
    }

    private static void 쪽관리시험(eithne eithne_VALUE) {
        leathanach_bainisteoir bainisteoir_VALUE = eithne_VALUE.쪽관리();
        leathanach_bainisteoir.ADDRESS_spás 부모공간 = bainisteoir_VALUE.새주소공간();
        bainisteoir_VALUE.MAPÁIL_leathanach(부모공간, 0x1000, true);
        bainisteoir_VALUE.scríobh_beart_VALUE(부모공간, 0x1010, (byte) 7);
        leathanach_bainisteoir.ADDRESS_spás leanbh_spás = bainisteoir_VALUE.쓰기시복사복제(부모공간);
        bainisteoir_VALUE.scríobh_beart_VALUE(leanbh_spás, 0x1010, (byte) 9);
        fíoraigh(bainisteoir_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Scríobh 시 ásc_VALUE 부모 격리");
        fíoraigh(bainisteoir_VALUE.바이트읽기(leanbh_spás, 0x1010) == 9, "Scríobh 시 ásc_VALUE leanbh_VALUE Scríobh");
    }

    private static void 파일과과정시험(eithne eithne_VALUE) {
        byte[] Inneachar_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        eithne_VALUE.córas_comhad().파일추가("시험", Inneachar_VALUE);
        Próiseas_VALUE 부모 = eithne_VALUE.첫과정();
        체계호출 호출 = eithne_VALUE.체계호출();
        int 서술자 = 호출.Oscail(부모, "/시험", 체계호출.inléite_amháin_bratach);
        fíoraigh(서술자 >= 3, "Comhad Oscail");

        byte[] 받을곳 = new byte[Inneachar_VALUE.length];
        fíoraigh(호출.Léigh(부모, 서술자, 받을곳, 받을곳.length) == Inneachar_VALUE.length, "Comhad Léigh");
        fíoraigh(Arrays.equals(Inneachar_VALUE, 받을곳), "Comhad Inneachar_VALUE");
        fíoraigh(호출.bog_suíomh(부모, 서술자, 0, 체계호출.SEARCH_Start) == 0, "Comhad suíomh bog_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        fíoraigh(복제서술자 >= 0, "서술자 복제");
        Próiseas_VALUE leanbh_VALUE = 호출.과정복제(부모);
        fíoraigh(leanbh_VALUE.aitheantóir_VALUE() != 부모.aitheantóir_VALUE(), "Próiseas_VALUE aitheantóir_VALUE 분리");
        fíoraigh(leanbh_VALUE.부모식별자() == 부모.aitheantóir_VALUE(), "부모 Próiseas_VALUE aitheantóir_VALUE");
        fíoraigh(호출.Dún(leanbh_VALUE, 서술자) == 0 && 부모.파일서술자().teicneolaíocht_faisnéise_oscail(서술자), "leanbh_VALUE Dún 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        fíoraigh(이전끝 == 0x06000000, "clár_f5044b9b 끝 늘리기");
        fíoraigh(부모.프로그램끝() == 0x06002000, "clár_f5044b9b 끝 반영");
        fíoraigh(leanbh_VALUE.프로그램끝() == 0x06000000, "과정별 clár_f5044b9b 끝 격리");

        leanbh_VALUE.scoir_clár(7);
        fíoraigh(호출.자식기다리기(부모, leanbh_VALUE.aitheantóir_VALUE(), false) == (7 << 8), "leanbh_VALUE scoir_clár 기다리기");
        fíoraigh(호출.접근가능("시험", 1) == -13, "Rith_ordú cead_VALUE diúltaigh_VALUE");
        fíoraigh(호출.úsáideoir_aitheantóir() == 0 && 호출.Grúpa_aitheantóir() == 0, "사용자와 무리 aitheantóir_VALUE");
        fíoraigh("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_liosta_tascanna("/") == 0, "현재 작업 iontráil_Liosta");
        fíoraigh(호출.teicneolaíocht_faisnéise_Teirminéal(부모, 1), "표준 Aschur 단말");
        fíoraigh("JIrlOS".equals(호출.체계정보().córas_ainm()), "córas_oibriúcháin_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(eithne eithne_VALUE) {
        byte[] sonraí = new byte[92];
        sonraí[0] = 0x7f;
        sonraí[1] = 'E';
        sonraí[2] = 'L';
        sonraí[3] = 'F';
        sonraí[4] = 1;
        sonraí[5] = 1;
        scríobh_slánuimhir_VALUE(sonraí, 24, 0x04001000);
        scríobh_slánuimhir_VALUE(sonraí, 32, 52);
        짧은정수쓰기(sonraí, 46, 40);
        짧은정수쓰기(sonraí, 48, 1);
        scríobh_slánuimhir_VALUE(sonraí, 56, 8);
        scríobh_slánuimhir_VALUE(sonraí, 60, 2);
        scríobh_slánuimhir_VALUE(sonraí, 64, 0x04002000);
        scríobh_slánuimhir_VALUE(sonraí, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(sonraí);
        fíoraigh(IMAGE_VALUE.seoladh_tosaithe() == 0x04001000, "ELF Rith_2 ADDRESS");
        fíoraigh(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 sonraí rannán_VALUE");
        int 서술자 = eithne_VALUE.체계호출().Oscail(eithne_VALUE.첫과정(), "시험", 체계호출.inléite_amháin_bratach);
        fíoraigh(eithne_VALUE.체계호출().comhad_rialú(eithne_VALUE.첫과정(), 서술자, 2, 1) == 0, "Rith_ordú 시 Dún Socruithe");
        fíoraigh(eithne_VALUE.체계호출().Rith_ordú(eithne_VALUE.첫과정(), sonraí, new String[] {"시험", "값"}, new String[] {"Teanga=Gaeilge"}) == 0, "ELF Rith_ordú IMAGE_VALUE 적재");
        fíoraigh(eithne_VALUE.첫과정().실행시작주소() == 0x04001000, "Rith_ordú Rith_2 ADDRESS 반영");
        fíoraigh(eithne_VALUE.첫과정().실행인자().length == 2 && eithne_VALUE.첫과정().환경값().length == 1, "Rith_ordú 인자와 환경");
        fíoraigh(!eithne_VALUE.첫과정().파일서술자().teicneolaíocht_faisnéise_oscail(서술자), "Rith_ordú 시 서술자 Dún");
        fíoraigh(eithne_VALUE.쪽관리().바이트읽기(eithne_VALUE.첫과정().ADDRESS_spás(), 0x04002000) == 0, "빈 sonraí rannán_VALUE 영 túsaigh");
    }

    private static void 입력시험(eithne eithne_VALUE) {
        eithne_VALUE.입력관리().키누름('가');
        eithne_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = eithne_VALUE.입력관리().Ar_aghaidh_ócáid();
        입력사건 SECOND_ócáid = eithne_VALUE.입력관리().Ar_aghaidh_ócáid();
        fíoraigh(첫사건.사건종류() == 입력사건.종류.키누름, "자판 ócáid");
        fíoraigh(SECOND_ócáid.첫째값() == 3 && SECOND_ócáid.SECOND_VALUE() == -2, "쥐 bog_VALUE ócáid");
    }

    private static void 하드웨어시험(호스트하드웨어 gléas_VALUE) {
        gléas_VALUE.scríobh_port_beart(0x3f8, 0xab);
        fíoraigh(gléas_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        fíoraigh(gléas_VALUE.직렬기록().contains("JIrlOS"), "직렬 LOG_ró");
    }

    private static void 개입중단과서술자시험() {
        IRQ_bainisteoir bainisteoir_VALUE = new IRQ_bainisteoir();
        bainisteoir_VALUE.cláraigh_iontráil(0x21, Stóras_ADDRESS -> Stóras_ADDRESS + 4);
        bainisteoir_VALUE.cas_air();
        fíoraigh(bainisteoir_VALUE.dáileadh_VALUE(0x21, 100) == 104, "IRQ dáileadh_VALUE");
        bainisteoir_VALUE.díghníomhachtaigh();
        fíoraigh(bainisteoir_VALUE.dáileadh_VALUE(0x21, 100) == 100, "IRQ díghníomhachtaigh");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.tacar_luach_réamhshocraithe();
        fíoraigh(서술자표.조각들().size() == 5, "전역 서술자표");
        tasc_staid_deighleán tasc_staid = new tasc_staid_deighleán();
        tasc_staid.특권쌓임공간설정(0x10, 0x800000);
        fíoraigh(tasc_staid.영번쌓임조각() == 0x10 && tasc_staid.영번쌓임주소() == 0x800000, "작업 staid_VALUE rannán_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Stóras_gléas = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.rannán_socraigh_méid];
        byte[] 읽은자료 = new byte[고급기술결합장치.rannán_socraigh_méid];
        쓸자료[17] = 42;
        Stóras_gléas.Scríobh(2, 쓸자료);
        Stóras_gléas.Léigh(2, 읽은자료);
        fíoraigh(읽은자료[17] == 42, "ATA rannán_VALUE 읽고 Scríobh");

        oiriúint_bus_bainisteoir oiriúint = new oiriúint_bus_bainisteoir();
        oiriúint.발견(new oiriúint_bus_bainisteoir.gléas_VALUE(0x1022, 0x2000, 0xc000, 11));
        fíoraigh(oiriúint.FIND_iontráil(0x1022, 0x2000) != null, "주변 gléas_VALUE FIND_iontráil");

        byte[] Ethernet_fráma = new byte[34];
        Ethernet_fráma[12] = 0x08;
        Ethernet_fráma[13] = 0x00;
        Ethernet_fráma[14] = 0x45;
        fíoraigh(Líonra_Uirlisí.Ethernet_UPPER_prótacal(Ethernet_fráma) == 0x0800, "이더넷 상위 cás_VALUE");
        fíoraigh(Líonra_Uirlisí.상호통신망규약사판인가(Ethernet_fráma, 14), "상호통신망규약 4판");
        fíoraigh(Líonra_Uirlisí.néal_suim_seiceála(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 suim_seiceála");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        scríobh_slánuimhir_VALUE(첫구역, 454, 63);
        scríobh_slánuimhir_VALUE(첫구역, 458, 1024);
        fíoraigh(new 기본분할영역표().Léigh(첫구역).size() == 1, "luach_réamhshocraithe 분할 영역표");

        Líonra_sraith sraith_VALUE = new Líonra_sraith();
        int[] RECEIVED_COUNT = new int[1];
        sraith_VALUE.cláraigh_úsáideoir_sonraí_aonaid(7, (sonraí, Rith_2, fad_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] fráma_INDEX = new byte[14 + 20 + 8];
        fráma_INDEX[12] = 0x08;
        fráma_INDEX[13] = 0x00;
        fráma_INDEX[14] = 0x45;
        fráma_INDEX[16] = 0;
        fráma_INDEX[17] = 28;
        fráma_INDEX[23] = 17;
        fráma_INDEX[36] = 0;
        fráma_INDEX[37] = 7;
        fíoraigh(sraith_VALUE.이더넷받기(fráma_INDEX) && RECEIVED_COUNT[0] == 1, "úsáideoir sonraí aonaid_VALUE dáileadh_VALUE");
    }

    private static void 화면과시계시험() {
        carachtar_taispeáin 화면 = new carachtar_taispeáin();
        화면.Aschur("가나\n다");
        fíoraigh(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Aschur");
        Clog Clog = new Clog(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Clog.틱();
        }
        fíoraigh(Clog.지난밀리초() == 100, "Clog 틱 CONVERT_VALUE");
    }

    private static void scríobh_slánuimhir_VALUE(byte[] sonraí, int suíomh, int VALUE) {
        sonraí[suíomh] = (byte) VALUE;
        sonraí[suíomh + 1] = (byte) (VALUE >>> 8);
        sonraí[suíomh + 2] = (byte) (VALUE >>> 16);
        sonraí[suíomh + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] sonraí, int suíomh, int VALUE) {
        sonraí[suíomh] = (byte) VALUE;
        sonraí[suíomh + 1] = (byte) (VALUE >>> 8);
    }

    private static void fíoraigh(boolean coinníoll, String Ainm) {
        if (!coinníoll) {
            throw new AssertionError("teip_VALUE: " + Ainm);
        }
        seol_ar_aghaidh_COUNT++;
        System.out.println("seol_ar_aghaidh_VALUE: " + Ainm);
    }
}
