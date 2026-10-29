// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package UGA.JUgaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import UGA.JUgaOS.기억공간.ububiko_Umugenzuzi;
import UGA.JUgaOS.기억공간.paji_Umugenzuzi;
import UGA.JUgaOS.입력.입력사건;
import UGA.JUgaOS.작업.Inzira_agaciro;
import UGA.JUgaOS.체계호출.체계호출;
import UGA.JUgaOS.sisitemu_ya_dosiye.실행파일적재기;
import UGA.JUgaOS.intima.intima;
import UGA.JUgaOS.gucumbikira.호스트하드웨어;
import UGA.JUgaOS.IRQ.IRQ_Umugenzuzi;
import UGA.JUgaOS.서술자.전역서술자표;
import UGA.JUgaOS.Ububiko_igendanwa.고급기술결합장치;
import UGA.JUgaOS.igendanwa_agaciro.igikoresho_ngereka_bisi_Umugenzuzi;
import UGA.JUgaOS.Urusobemiyoboro_Ikirundo.Urusobemiyoboro_Ibikoresho;
import UGA.JUgaOS.Urusobemiyoboro_Ikirundo.Urusobemiyoboro_akugara;
import UGA.JUgaOS.igendanwa_agaciro.isaha;
import UGA.JUgaOS.서술자.umukoro_imimerere_agace;
import UGA.JUgaOS.화면.inyuguti_kwerekana;
import UGA.JUgaOS.sisitemu_ya_dosiye.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 igendanwa_agaciro = new 호스트하드웨어();
        intima intima_agaciro = new intima(igendanwa_agaciro);
        intima_agaciro.ihuriro();

        기억공간시험(intima_agaciro);
        쪽관리시험(intima_agaciro);
        파일과과정시험(intima_agaciro);
        실행파일시험(intima_agaciro);
        입력시험(intima_agaciro);
        하드웨어시험(igendanwa_agaciro);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JUgaOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(intima intima_agaciro) {
        ububiko_Umugenzuzi Umugenzuzi_agaciro = intima_agaciro.기억공간();
        int 첫주소 = Umugenzuzi_agaciro.정렬할당(100, 64);
        gusuzuma((첫주소 & 63) == 0, "gutondeka_agaciro kugenera_Ububiko");
        Umugenzuzi_agaciro.kwandika_bayiti_agaciro(첫주소, (byte) 0x5a);
        gusuzuma(Umugenzuzi_agaciro.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 kwandika");
        int 사용전 = Umugenzuzi_agaciro.사용크기();
        Umugenzuzi_agaciro.kurekura_Ububiko(첫주소);
        gusuzuma(Umugenzuzi_agaciro.사용크기() < 사용전, "기억공간 kurekura_Ububiko");
    }

    private static void 쪽관리시험(intima intima_agaciro) {
        paji_Umugenzuzi Umugenzuzi_agaciro = intima_agaciro.쪽관리();
        paji_Umugenzuzi.aderesi_akanya 부모공간 = Umugenzuzi_agaciro.새주소공간();
        Umugenzuzi_agaciro.ikarita_paji(부모공간, 0x1000, true);
        Umugenzuzi_agaciro.kwandika_bayiti_agaciro(부모공간, 0x1010, (byte) 7);
        paji_Umugenzuzi.aderesi_akanya ishami_akanya = Umugenzuzi_agaciro.쓰기시복사복제(부모공간);
        Umugenzuzi_agaciro.kwandika_bayiti_agaciro(ishami_akanya, 0x1010, (byte) 9);
        gusuzuma(Umugenzuzi_agaciro.바이트읽기(부모공간, 0x1010) == 7, "kwandika 시 kopi_agaciro 부모 격리");
        gusuzuma(Umugenzuzi_agaciro.바이트읽기(ishami_akanya, 0x1010) == 9, "kwandika 시 kopi_agaciro ishami_agaciro_b642f4b4 kwandika");
    }

    private static void 파일과과정시험(intima intima_agaciro) {
        byte[] Ibirimo_agaciro = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        intima_agaciro.sisitemu_ya_dosiye().파일추가("시험", Ibirimo_agaciro);
        Inzira_agaciro 부모 = intima_agaciro.첫과정();
        체계호출 호출 = intima_agaciro.체계호출();
        int 서술자 = 호출.Gufungura(부모, "/시험", 체계호출.soma_gusa_akabendera);
        gusuzuma(서술자 >= 3, "Idosiye Gufungura");

        byte[] 받을곳 = new byte[Ibirimo_agaciro.length];
        gusuzuma(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Ibirimo_agaciro.length, "Idosiye 읽기");
        gusuzuma(Arrays.equals(Ibirimo_agaciro, 받을곳), "Idosiye Ibirimo_agaciro");
        gusuzuma(호출.위치옮기기(부모, 서술자, 0, 체계호출.Gushaka_Itangira) == 0, "Idosiye 위치 kwimura_agaciro");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        gusuzuma(복제서술자 >= 0, "서술자 복제");
        Inzira_agaciro ishami_agaciro_b642f4b4 = 호출.과정복제(부모);
        gusuzuma(ishami_agaciro_b642f4b4.indanga_agaciro() != 부모.indanga_agaciro(), "Inzira_agaciro indanga_agaciro 분리");
        gusuzuma(ishami_agaciro_b642f4b4.부모식별자() == 부모.indanga_agaciro(), "부모 Inzira_agaciro indanga_agaciro");
        gusuzuma(호출.Gufunga(ishami_agaciro_b642f4b4, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "ishami_agaciro_b642f4b4 Gufunga 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        gusuzuma(이전끝 == 0x06000000, "porogaramu_f5044b9b 끝 늘리기");
        gusuzuma(부모.프로그램끝() == 0x06002000, "porogaramu_f5044b9b 끝 반영");
        gusuzuma(ishami_agaciro_b642f4b4.프로그램끝() == 0x06000000, "과정별 porogaramu_f5044b9b 끝 격리");

        ishami_agaciro_b642f4b4.gusohoka_porogaramu(7);
        gusuzuma(호출.자식기다리기(부모, ishami_agaciro_b642f4b4.indanga_agaciro(), false) == (7 << 8), "ishami_agaciro_b642f4b4 gusohoka_porogaramu 기다리기");
        gusuzuma(호출.접근가능("시험", 1) == -13, "gukora_ibwiriza 권한 거부");
        gusuzuma(호출.ukoresha_indanga() == 0 && 호출.itsinda_indanga() == 0, "사용자와 무리 indanga_agaciro");
        gusuzuma("/".equals(호출.현재작업목록(2)) && 호출.guhinduranya_ilisiti_y_imikoro("/") == 0, "현재 작업 icyinjizwa_Urutonde");
        gusuzuma(호출.단말인가(부모, 1), "표준 출력 단말");
        gusuzuma("JUgaOS".equals(호출.체계정보().sisitemu_izina()), "sisitemu_ngengamikorere_agaciro msinfo32_exe");
    }

    private static void 실행파일시험(intima intima_agaciro) {
        byte[] amakurushingiro = new byte[92];
        amakurushingiro[0] = 0x7f;
        amakurushingiro[1] = 'E';
        amakurushingiro[2] = 'L';
        amakurushingiro[3] = 'F';
        amakurushingiro[4] = 1;
        amakurushingiro[5] = 1;
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 24, 0x04001000);
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 32, 52);
        짧은정수쓰기(amakurushingiro, 46, 40);
        짧은정수쓰기(amakurushingiro, 48, 1);
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 56, 8);
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 60, 2);
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 64, 0x04002000);
        kwandika_umubare_wuzuye_agaciro(amakurushingiro, 72, 64);

        실행파일적재기.ishusho ishusho_agaciro = new 실행파일적재기().검사(amakurushingiro);
        gusuzuma(ishusho_agaciro.Itangira_aderesi() == 0x04001000, "ELF ihuriro aderesi");
        gusuzuma(ishusho_agaciro.구역들().size() == 1 && ishusho_agaciro.구역들().get(0).종류() == 8, "ELF 빈 amakurushingiro igice_agaciro");
        int 서술자 = intima_agaciro.체계호출().Gufungura(intima_agaciro.첫과정(), "시험", 체계호출.soma_gusa_akabendera);
        gusuzuma(intima_agaciro.체계호출().dosiye_icunga(intima_agaciro.첫과정(), 서술자, 2, 1) == 0, "gukora_ibwiriza 시 Gufunga Amagenamiterere");
        gusuzuma(intima_agaciro.체계호출().gukora_ibwiriza(intima_agaciro.첫과정(), amakurushingiro, new String[] {"시험", "값"}, new String[] {"Ururimi=Ikinyarwanda"}) == 0, "ELF gukora_ibwiriza ishusho_agaciro 적재");
        gusuzuma(intima_agaciro.첫과정().실행시작주소() == 0x04001000, "gukora_ibwiriza ihuriro aderesi 반영");
        gusuzuma(intima_agaciro.첫과정().실행인자().length == 2 && intima_agaciro.첫과정().환경값().length == 1, "gukora_ibwiriza 인자와 환경");
        gusuzuma(!intima_agaciro.첫과정().파일서술자().열려있음(서술자), "gukora_ibwiriza 시 서술자 Gufunga");
        gusuzuma(intima_agaciro.쪽관리().바이트읽기(intima_agaciro.첫과정().aderesi_akanya(), 0x04002000) == 0, "빈 amakurushingiro igice_agaciro 영 gutangiza");
    }

    private static void 입력시험(intima intima_agaciro) {
        intima_agaciro.입력관리().키누름('가');
        intima_agaciro.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = intima_agaciro.입력관리().다음사건();
        입력사건 둘째사건 = intima_agaciro.입력관리().다음사건();
        gusuzuma(첫사건.사건종류() == 입력사건.종류.키누름, "자판 icyabaye");
        gusuzuma(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 kwimura_agaciro icyabaye");
    }

    private static void 하드웨어시험(호스트하드웨어 igendanwa_agaciro) {
        igendanwa_agaciro.kwandika_poti_bayiti(0x3f8, 0xab);
        gusuzuma(igendanwa_agaciro.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        gusuzuma(igendanwa_agaciro.직렬기록().contains("JUgaOS"), "직렬 kubika_umurongo");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Umugenzuzi Umugenzuzi_agaciro = new IRQ_Umugenzuzi();
        Umugenzuzi_agaciro.등록(0x21, Ububiko_aderesi -> Ububiko_aderesi + 4);
        Umugenzuzi_agaciro.gufungura();
        gusuzuma(Umugenzuzi_agaciro.gucuruza_agaciro(0x21, 100) == 104, "IRQ gucuruza_agaciro");
        Umugenzuzi_agaciro.gufunga();
        gusuzuma(Umugenzuzi_agaciro.gucuruza_agaciro(0x21, 100) == 100, "IRQ gufunga");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.itsinda_agaciro_gasanzweho();
        gusuzuma(서술자표.조각들().size() == 5, "전역 서술자표");
        umukoro_imimerere_agace umukoro_imimerere = new umukoro_imimerere_agace();
        umukoro_imimerere.특권쌓임공간설정(0x10, 0x800000);
        gusuzuma(umukoro_imimerere.영번쌓임조각() == 0x10 && umukoro_imimerere.영번쌓임주소() == 0x800000, "작업 imimerere_agaciro igice_agaciro");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Ububiko_igendanwa = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.igice_ingano];
        byte[] 읽은자료 = new byte[고급기술결합장치.igice_ingano];
        쓸자료[17] = 42;
        Ububiko_igendanwa.kwandika(2, 쓸자료);
        Ububiko_igendanwa.읽기(2, 읽은자료);
        gusuzuma(읽은자료[17] == 42, "ATA igice_agaciro 읽고 kwandika");

        igikoresho_ngereka_bisi_Umugenzuzi igikoresho_ngereka = new igikoresho_ngereka_bisi_Umugenzuzi();
        igikoresho_ngereka.발견(new igikoresho_ngereka_bisi_Umugenzuzi.igendanwa_agaciro(0x1022, 0x2000, 0xc000, 11));
        gusuzuma(igikoresho_ngereka.gushaka_icyinjizwa(0x1022, 0x2000) != null, "주변 igendanwa_agaciro gushaka_icyinjizwa");

        byte[] Ethernet_ikadiri = new byte[34];
        Ethernet_ikadiri[12] = 0x08;
        Ethernet_ikadiri[13] = 0x00;
        Ethernet_ikadiri[14] = 0x45;
        gusuzuma(Urusobemiyoboro_Ibikoresho.이더넷상위규약(Ethernet_ikadiri) == 0x0800, "이더넷 상위 ikibazo_agaciro");
        gusuzuma(Urusobemiyoboro_Ibikoresho.상호통신망규약사판인가(Ethernet_ikadiri, 14), "상호통신망규약 4판");
        gusuzuma(Urusobemiyoboro_Ibikoresho.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kwandika_umubare_wuzuye_agaciro(첫구역, 454, 63);
        kwandika_umubare_wuzuye_agaciro(첫구역, 458, 1024);
        gusuzuma(new 기본분할영역표().읽기(첫구역).size() == 1, "agaciro_gasanzweho 분할 영역표");

        Urusobemiyoboro_akugara akugara_agaciro = new Urusobemiyoboro_akugara();
        int[] 받은수 = new int[1];
        akugara_agaciro.사용자자료단위등록(7, (amakurushingiro, ihuriro, uburebure_agaciro) -> 받은수[0]++);
        byte[] ikadiri_umugerekashakiro = new byte[14 + 20 + 8];
        ikadiri_umugerekashakiro[12] = 0x08;
        ikadiri_umugerekashakiro[13] = 0x00;
        ikadiri_umugerekashakiro[14] = 0x45;
        ikadiri_umugerekashakiro[16] = 0;
        ikadiri_umugerekashakiro[17] = 28;
        ikadiri_umugerekashakiro[23] = 17;
        ikadiri_umugerekashakiro[36] = 0;
        ikadiri_umugerekashakiro[37] = 7;
        gusuzuma(akugara_agaciro.이더넷받기(ikadiri_umugerekashakiro) && 받은수[0] == 1, "ukoresha amakurushingiro ibinyabumwe_agaciro gucuruza_agaciro");
    }

    private static void 화면과시계시험() {
        inyuguti_kwerekana 화면 = new inyuguti_kwerekana();
        화면.출력("가나\n다");
        gusuzuma(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        isaha isaha = new isaha(100);
        for (int umugerekashakiro = 0; umugerekashakiro < 10; umugerekashakiro++) {
            isaha.틱();
        }
        gusuzuma(isaha.지난밀리초() == 100, "isaha 틱 변환");
    }

    private static void kwandika_umubare_wuzuye_agaciro(byte[] amakurushingiro, int 위치, int agaciro) {
        amakurushingiro[위치] = (byte) agaciro;
        amakurushingiro[위치 + 1] = (byte) (agaciro >>> 8);
        amakurushingiro[위치 + 2] = (byte) (agaciro >>> 16);
        amakurushingiro[위치 + 3] = (byte) (agaciro >>> 24);
    }

    private static void 짧은정수쓰기(byte[] amakurushingiro, int 위치, int agaciro) {
        amakurushingiro[위치] = (byte) agaciro;
        amakurushingiro[위치 + 1] = (byte) (agaciro >>> 8);
    }

    private static void gusuzuma(boolean icyangombwa, String Izina) {
        if (!icyangombwa) {
            throw new AssertionError("kudakora_agaciro: " + Izina);
        }
        통과수++;
        System.out.println("통과: " + Izina);
    }
}
