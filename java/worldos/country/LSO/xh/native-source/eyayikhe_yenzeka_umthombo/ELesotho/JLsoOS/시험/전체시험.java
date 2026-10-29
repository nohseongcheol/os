// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import ELesotho.JLsoOS.기억공간.imemori_umphathi;
import ELesotho.JLsoOS.기억공간.ikhasi_umphathi;
import ELesotho.JLsoOS.입력.입력사건;
import ELesotho.JLsoOS.작업.Inkqubo_ixabiso;
import ELesotho.JLsoOS.체계호출.체계호출;
import ELesotho.JLsoOS.uhlobo_loseto_lwefayile.실행파일적재기;
import ELesotho.JLsoOS.ikheneli.ikheneli;
import ELesotho.JLsoOS.umsingathi.호스트하드웨어;
import ELesotho.JLsoOS.i_IRQ.i_IRQ_umphathi;
import ELesotho.JLsoOS.서술자.전역서술자표;
import ELesotho.JLsoOS.Ugcino_isixhobo.고급기술결합장치;
import ELesotho.JLsoOS.isixhobo_ixabiso.isixhobo_isihambisi_lwazi_umphathi;
import ELesotho.JLsoOS.Inethiwekhi_fumba.Inethiwekhi_Izixhobo;
import ELesotho.JLsoOS.Inethiwekhi_fumba.Inethiwekhi_ileya;
import ELesotho.JLsoOS.isixhobo_ixabiso.iwotshi;
import ELesotho.JLsoOS.서술자.umsebenzi_imo_isahlulo;
import ELesotho.JLsoOS.화면.ikharakhtha_bonisa;
import ELesotho.JLsoOS.uhlobo_loseto_lwefayile.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 isixhobo_ixabiso = new 호스트하드웨어();
        ikheneli ikheneli_ixabiso = new ikheneli(isixhobo_ixabiso);
        ikheneli_ixabiso.Phumeza();

        기억공간시험(ikheneli_ixabiso);
        쪽관리시험(ikheneli_ixabiso);
        파일과과정시험(ikheneli_ixabiso);
        실행파일시험(ikheneli_ixabiso);
        입력시험(ikheneli_ixabiso);
        하드웨어시험(isixhobo_ixabiso);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JLsoOS 시험 dlulisela_ixabiso: " + 통과수);
    }

    private static void 기억공간시험(ikheneli ikheneli_ixabiso) {
        imemori_umphathi umphathi_ixabiso = ikheneli_ixabiso.기억공간();
        int 첫주소 = umphathi_ixabiso.정렬할당(100, 64);
        ngqinisisa((첫주소 & 63) == 0, "lungelelanisa_ixabiso yabela_Ugcino");
        umphathi_ixabiso.bhala_ibhayithi_ixabiso(첫주소, (byte) 0x5a);
        ngqinisisa(umphathi_ixabiso.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Bhala");
        int 사용전 = umphathi_ixabiso.사용크기();
        umphathi_ixabiso.vulela_Ugcino(첫주소);
        ngqinisisa(umphathi_ixabiso.사용크기() < 사용전, "기억공간 vulela_Ugcino");
    }

    private static void 쪽관리시험(ikheneli ikheneli_ixabiso) {
        ikhasi_umphathi umphathi_ixabiso = ikheneli_ixabiso.쪽관리();
        ikhasi_umphathi.idilesi_isithuba 부모공간 = umphathi_ixabiso.새주소공간();
        umphathi_ixabiso.beka_emephini_ikhasi(부모공간, 0x1000, true);
        umphathi_ixabiso.bhala_ibhayithi_ixabiso(부모공간, 0x1010, (byte) 7);
        ikhasi_umphathi.idilesi_isithuba umntwana_isithuba = umphathi_ixabiso.쓰기시복사복제(부모공간);
        umphathi_ixabiso.bhala_ibhayithi_ixabiso(umntwana_isithuba, 0x1010, (byte) 9);
        ngqinisisa(umphathi_ixabiso.바이트읽기(부모공간, 0x1010) == 7, "Bhala 시 kopa_ixabiso 부모 격리");
        ngqinisisa(umphathi_ixabiso.바이트읽기(umntwana_isithuba, 0x1010) == 9, "Bhala 시 kopa_ixabiso umntwana_ixabiso Bhala");
    }

    private static void 파일과과정시험(ikheneli ikheneli_ixabiso) {
        byte[] Isiqulatho_ixabiso = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        ikheneli_ixabiso.uhlobo_loseto_lwefayile().파일추가("시험", Isiqulatho_ixabiso);
        Inkqubo_ixabiso 부모 = ikheneli_ixabiso.첫과정();
        체계호출 호출 = ikheneli_ixabiso.체계호출();
        int 서술자 = 호출.Vula(부모, "/시험", 체계호출.efundwayo_kuphela_iflegi);
        ngqinisisa(서술자 >= 3, "iFayili Vula");

        byte[] 받을곳 = new byte[Isiqulatho_ixabiso.length];
        ngqinisisa(호출.Funda(부모, 서술자, 받을곳, 받을곳.length) == Isiqulatho_ixabiso.length, "iFayili Funda");
        ngqinisisa(Arrays.equals(Isiqulatho_ixabiso, 받을곳), "iFayili Isiqulatho_ixabiso");
        ngqinisisa(호출.위치옮기기(부모, 서술자, 0, 체계호출.Khangela_qala) == 0, "iFayili 위치 fudusa_ixabiso");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        ngqinisisa(복제서술자 >= 0, "서술자 복제");
        Inkqubo_ixabiso umntwana_ixabiso = 호출.과정복제(부모);
        ngqinisisa(umntwana_ixabiso.isalathisi_ixabiso() != 부모.isalathisi_ixabiso(), "Inkqubo_ixabiso isalathisi_ixabiso 분리");
        ngqinisisa(umntwana_ixabiso.부모식별자() == 부모.isalathisi_ixabiso(), "부모 Inkqubo_ixabiso isalathisi_ixabiso");
        ngqinisisa(호출.Vala(umntwana_ixabiso, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "umntwana_ixabiso Vala 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        ngqinisisa(이전끝 == 0x06000000, "inkqubo_f5044b9b 끝 늘리기");
        ngqinisisa(부모.프로그램끝() == 0x06002000, "inkqubo_f5044b9b 끝 반영");
        ngqinisisa(umntwana_ixabiso.프로그램끝() == 0x06000000, "과정별 inkqubo_f5044b9b 끝 격리");

        umntwana_ixabiso.phuma_inkqubo(7);
        ngqinisisa(호출.자식기다리기(부모, umntwana_ixabiso.isalathisi_ixabiso(), false) == (7 << 8), "umntwana_ixabiso phuma_inkqubo 기다리기");
        ngqinisisa(호출.접근가능("시험", 1) == -13, "ukwenza_umyalelo imvume_ixabiso 거부");
        ngqinisisa(호출.umsebenzisi_isalathisi() == 0 && 호출.iqela_isalathisi() == 0, "사용자와 무리 isalathisi_ixabiso");
        ngqinisisa("/".equals(호출.현재작업목록(2)) && 호출.tshintshela_uluhlu_lwemisebenzi("/") == 0, "현재 작업 ufako_nkcukacha_uludwe");
        ngqinisisa(호출.단말인가(부모, 1), "표준 출력 단말");
        ngqinisisa("JLsoOS".equals(호출.체계정보().inkqubo_igama()), "Indlela_yokusebenza_ixabiso i_msinfo32_exe");
    }

    private static void 실행파일시험(ikheneli ikheneli_ixabiso) {
        byte[] iingcombolo = new byte[92];
        iingcombolo[0] = 0x7f;
        iingcombolo[1] = 'E';
        iingcombolo[2] = 'L';
        iingcombolo[3] = 'F';
        iingcombolo[4] = 1;
        iingcombolo[5] = 1;
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 24, 0x04001000);
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 32, 52);
        짧은정수쓰기(iingcombolo, 46, 40);
        짧은정수쓰기(iingcombolo, 48, 1);
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 56, 8);
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 60, 2);
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 64, 0x04002000);
        bhala_inani_elipheleleyo_ixabiso(iingcombolo, 72, 64);

        실행파일적재기.umfanekiso umfanekiso_ixabiso = new 실행파일적재기().검사(iingcombolo);
        ngqinisisa(umfanekiso_ixabiso.qala_idilesi() == 0x04001000, "ELF Phumeza idilesi");
        ngqinisisa(umfanekiso_ixabiso.구역들().size() == 1 && umfanekiso_ixabiso.구역들().get(0).종류() == 8, "ELF 빈 iingcombolo icandelo_ixabiso");
        int 서술자 = ikheneli_ixabiso.체계호출().Vula(ikheneli_ixabiso.첫과정(), "시험", 체계호출.efundwayo_kuphela_iflegi);
        ngqinisisa(ikheneli_ixabiso.체계호출().ifayile_isilawuli(ikheneli_ixabiso.첫과정(), 서술자, 2, 1) == 0, "ukwenza_umyalelo 시 Vala Imimiselo");
        ngqinisisa(ikheneli_ixabiso.체계호출().ukwenza_umyalelo(ikheneli_ixabiso.첫과정(), iingcombolo, new String[] {"시험", "값"}, new String[] {"Ulwimi=isiXhosa"}) == 0, "ELF ukwenza_umyalelo umfanekiso_ixabiso 적재");
        ngqinisisa(ikheneli_ixabiso.첫과정().실행시작주소() == 0x04001000, "ukwenza_umyalelo Phumeza idilesi 반영");
        ngqinisisa(ikheneli_ixabiso.첫과정().실행인자().length == 2 && ikheneli_ixabiso.첫과정().환경값().length == 1, "ukwenza_umyalelo 인자와 환경");
        ngqinisisa(!ikheneli_ixabiso.첫과정().파일서술자().열려있음(서술자), "ukwenza_umyalelo 시 서술자 Vala");
        ngqinisisa(ikheneli_ixabiso.쪽관리().바이트읽기(ikheneli_ixabiso.첫과정().idilesi_isithuba(), 0x04002000) == 0, "빈 iingcombolo icandelo_ixabiso 영 qalisa_umsebenzi");
    }

    private static void 입력시험(ikheneli ikheneli_ixabiso) {
        ikheneli_ixabiso.입력관리().키누름('가');
        ikheneli_ixabiso.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = ikheneli_ixabiso.입력관리().다음사건();
        입력사건 둘째사건 = ikheneli_ixabiso.입력관리().다음사건();
        ngqinisisa(첫사건.사건종류() == 입력사건.종류.키누름, "자판 umcimbi");
        ngqinisisa(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 fudusa_ixabiso umcimbi");
    }

    private static void 하드웨어시험(호스트하드웨어 isixhobo_ixabiso) {
        isixhobo_ixabiso.bhala_iphothi_ibhayithi(0x3f8, 0xab);
        ngqinisisa(isixhobo_ixabiso.포트바이트읽기(0x3f8) == 0xab, "포트 i_I_O 경계");
        ngqinisisa(isixhobo_ixabiso.직렬기록().contains("JLsoOS"), "직렬 ilog_umqolo");
    }

    private static void 개입중단과서술자시험() {
        i_IRQ_umphathi umphathi_ixabiso = new i_IRQ_umphathi();
        umphathi_ixabiso.bhalisa_ufako_nkcukacha(0x21, Ugcino_idilesi -> Ugcino_idilesi + 4);
        umphathi_ixabiso.ukuvula();
        ngqinisisa(umphathi_ixabiso.sasaza_ixabiso(0x21, 100) == 104, "i_IRQ sasaza_ixabiso");
        umphathi_ixabiso.yenza_ingasebenzi();
        ngqinisisa(umphathi_ixabiso.sasaza_ixabiso(0x21, 100) == 100, "i_IRQ yenza_ingasebenzi");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.isethi_ixabiso_elisisiseko();
        ngqinisisa(서술자표.조각들().size() == 5, "전역 서술자표");
        umsebenzi_imo_isahlulo umsebenzi_imo = new umsebenzi_imo_isahlulo();
        umsebenzi_imo.특권쌓임공간설정(0x10, 0x800000);
        ngqinisisa(umsebenzi_imo.영번쌓임조각() == 0x10 && umsebenzi_imo.영번쌓임주소() == 0x800000, "작업 imo_ixabiso icandelo_ixabiso");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Ugcino_isixhobo = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.icandelo_isayizi];
        byte[] 읽은자료 = new byte[고급기술결합장치.icandelo_isayizi];
        쓸자료[17] = 42;
        Ugcino_isixhobo.Bhala(2, 쓸자료);
        Ugcino_isixhobo.Funda(2, 읽은자료);
        ngqinisisa(읽은자료[17] == 42, "ATA icandelo_ixabiso 읽고 Bhala");

        isixhobo_isihambisi_lwazi_umphathi isixhobo = new isixhobo_isihambisi_lwazi_umphathi();
        isixhobo.발견(new isixhobo_isihambisi_lwazi_umphathi.isixhobo_ixabiso(0x1022, 0x2000, 0xc000, 11));
        ngqinisisa(isixhobo.fumana_ufako_nkcukacha(0x1022, 0x2000) != null, "주변 isixhobo_ixabiso fumana_ufako_nkcukacha");

        byte[] i_Ithanethi_ifreyim = new byte[34];
        i_Ithanethi_ifreyim[12] = 0x08;
        i_Ithanethi_ifreyim[13] = 0x00;
        i_Ithanethi_ifreyim[14] = 0x45;
        ngqinisisa(Inethiwekhi_Izixhobo.이더넷상위규약(i_Ithanethi_ifreyim) == 0x0800, "이더넷 상위 isiganeko_ixabiso");
        ngqinisisa(Inethiwekhi_Izixhobo.상호통신망규약사판인가(i_Ithanethi_ifreyim, 14), "상호통신망규약 4판");
        ngqinisisa(Inethiwekhi_Izixhobo.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        bhala_inani_elipheleleyo_ixabiso(첫구역, 454, 63);
        bhala_inani_elipheleleyo_ixabiso(첫구역, 458, 1024);
        ngqinisisa(new 기본분할영역표().Funda(첫구역).size() == 1, "ixabiso_elisisiseko 분할 영역표");

        Inethiwekhi_ileya ileya_ixabiso = new Inethiwekhi_ileya();
        int[] 받은수 = new int[1];
        ileya_ixabiso.bhalisa_umsebenzisi_iingcombolo_isifundo(7, (iingcombolo, Phumeza, ubude_ixabiso) -> 받은수[0]++);
        byte[] ifreyim_indeksa = new byte[14 + 20 + 8];
        ifreyim_indeksa[12] = 0x08;
        ifreyim_indeksa[13] = 0x00;
        ifreyim_indeksa[14] = 0x45;
        ifreyim_indeksa[16] = 0;
        ifreyim_indeksa[17] = 28;
        ifreyim_indeksa[23] = 17;
        ifreyim_indeksa[36] = 0;
        ifreyim_indeksa[37] = 7;
        ngqinisisa(ileya_ixabiso.이더넷받기(ifreyim_indeksa) && 받은수[0] == 1, "umsebenzisi iingcombolo isifundo_ixabiso sasaza_ixabiso");
    }

    private static void 화면과시계시험() {
        ikharakhtha_bonisa 화면 = new ikharakhtha_bonisa();
        화면.출력("가나\n다");
        ngqinisisa(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        iwotshi iwotshi = new iwotshi(100);
        for (int indeksa = 0; indeksa < 10; indeksa++) {
            iwotshi.틱();
        }
        ngqinisisa(iwotshi.지난밀리초() == 100, "iwotshi 틱 변환");
    }

    private static void bhala_inani_elipheleleyo_ixabiso(byte[] iingcombolo, int 위치, int ixabiso) {
        iingcombolo[위치] = (byte) ixabiso;
        iingcombolo[위치 + 1] = (byte) (ixabiso >>> 8);
        iingcombolo[위치 + 2] = (byte) (ixabiso >>> 16);
        iingcombolo[위치 + 3] = (byte) (ixabiso >>> 24);
    }

    private static void 짧은정수쓰기(byte[] iingcombolo, int 위치, int ixabiso) {
        iingcombolo[위치] = (byte) ixabiso;
        iingcombolo[위치 + 1] = (byte) (ixabiso >>> 8);
    }

    private static void ngqinisisa(boolean imo, String Igama) {
        if (!imo) {
            throw new AssertionError("ukungaphumeleli_ixabiso: " + Igama);
        }
        통과수++;
        System.out.println("dlulisela_ixabiso: " + Igama);
    }
}
