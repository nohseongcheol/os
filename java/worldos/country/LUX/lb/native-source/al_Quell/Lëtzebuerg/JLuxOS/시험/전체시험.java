// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Lëtzebuerg.JLuxOS.기억공간.Späicher_Manager;
import Lëtzebuerg.JLuxOS.기억공간.Säit_Manager;
import Lëtzebuerg.JLuxOS.입력.입력사건;
import Lëtzebuerg.JLuxOS.작업.Prozess_VALUE;
import Lëtzebuerg.JLuxOS.체계호출.체계호출;
import Lëtzebuerg.JLuxOS.Fichierssystem.실행파일적재기;
import Lëtzebuerg.JLuxOS.Kernel.Kernel;
import Lëtzebuerg.JLuxOS.Host.호스트하드웨어;
import Lëtzebuerg.JLuxOS.IRQ.IRQ_Manager;
import Lëtzebuerg.JLuxOS.서술자.전역서술자표;
import Lëtzebuerg.JLuxOS.Späicher_Mobil.고급기술결합장치;
import Lëtzebuerg.JLuxOS.Mobil_VALUE.Accessoire_Bus_Manager;
import Lëtzebuerg.JLuxOS.Reseau_Stapel.Reseau_Tools;
import Lëtzebuerg.JLuxOS.Reseau_Stapel.Reseau_Layer;
import Lëtzebuerg.JLuxOS.Mobil_VALUE.Auer;
import Lëtzebuerg.JLuxOS.서술자.To_do_Status_Segment;
import Lëtzebuerg.JLuxOS.화면.Zeechen_Bildschierm;
import Lëtzebuerg.JLuxOS.Fichierssystem.기본분할영역표;

public final class 전체시험 {
    private static int iwwermëttelen_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 Mobil_VALUE = new 호스트하드웨어();
        Kernel Kernel_VALUE = new Kernel(Mobil_VALUE);
        Kernel_VALUE.Laf();

        기억공간시험(Kernel_VALUE);
        쪽관리시험(Kernel_VALUE);
        파일과과정시험(Kernel_VALUE);
        실행파일시험(Kernel_VALUE);
        입력시험(Kernel_VALUE);
        하드웨어시험(Mobil_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JLuxOS 시험 iwwermëttelen_VALUE: " + iwwermëttelen_COUNT);
    }

    private static void 기억공간시험(Kernel Kernel_VALUE) {
        Späicher_Manager Manager_VALUE = Kernel_VALUE.기억공간();
        int 첫주소 = Manager_VALUE.정렬할당(100, 64);
        verifizéieren((첫주소 & 63) == 0, "alignéieren_VALUE zouweisen_Späicher");
        Manager_VALUE.schreiwen_Byte_VALUE(첫주소, (byte) 0x5a);
        verifizéieren(Manager_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 schreiwen");
        int 사용전 = Manager_VALUE.사용크기();
        Manager_VALUE.Versioun_Späicher(첫주소);
        verifizéieren(Manager_VALUE.사용크기() < 사용전, "기억공간 Versioun_Späicher");
    }

    private static void 쪽관리시험(Kernel Kernel_VALUE) {
        Säit_Manager Manager_VALUE = Kernel_VALUE.쪽관리();
        Säit_Manager.Adress_Plaz 부모공간 = Manager_VALUE.새주소공간();
        Manager_VALUE.MAP_Säit(부모공간, 0x1000, true);
        Manager_VALUE.schreiwen_Byte_VALUE(부모공간, 0x1010, (byte) 7);
        Säit_Manager.Adress_Plaz Kand_Plaz = Manager_VALUE.쓰기시복사복제(부모공간);
        Manager_VALUE.schreiwen_Byte_VALUE(Kand_Plaz, 0x1010, (byte) 9);
        verifizéieren(Manager_VALUE.바이트읽기(부모공간, 0x1010) == 7, "schreiwen 시 Instanz_VALUE 부모 격리");
        verifizéieren(Manager_VALUE.바이트읽기(Kand_Plaz, 0x1010) == 9, "schreiwen 시 Instanz_VALUE Kand_VALUE schreiwen");
    }

    private static void 파일과과정시험(Kernel Kernel_VALUE) {
        byte[] Inhalt_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        Kernel_VALUE.Fichierssystem().파일추가("시험", Inhalt_VALUE);
        Prozess_VALUE 부모 = Kernel_VALUE.첫과정();
        체계호출 호출 = Kernel_VALUE.체계호출();
        int 서술자 = 호출.ariichten(부모, "/시험", 체계호출.schreifgeschützt_kennzeechnen);
        verifizéieren(서술자 >= 3, "Fichier ariichten");

        byte[] 받을곳 = new byte[Inhalt_VALUE.length];
        verifizéieren(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Inhalt_VALUE.length, "Fichier 읽기");
        verifizéieren(Arrays.equals(Inhalt_VALUE, 받을곳), "Fichier Inhalt_VALUE");
        verifizéieren(호출.verréckelen_positionéieren(부모, 서술자, 0, 체계호출.Sich_Start) == 0, "Fichier positionéieren verréckelen_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        verifizéieren(복제서술자 >= 0, "서술자 복제");
        Prozess_VALUE Kand_VALUE = 호출.과정복제(부모);
        verifizéieren(Kand_VALUE.Identifikateur_VALUE() != 부모.Identifikateur_VALUE(), "Prozess_VALUE Identifikateur_VALUE 분리");
        verifizéieren(Kand_VALUE.부모식별자() == 부모.Identifikateur_VALUE(), "부모 Prozess_VALUE Identifikateur_VALUE");
        verifizéieren(호출.Clôture(Kand_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "Kand_VALUE Clôture 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        verifizéieren(이전끝 == 0x06000000, "App_f5044b9b 끝 늘리기");
        verifizéieren(부모.프로그램끝() == 0x06002000, "App_f5044b9b 끝 반영");
        verifizéieren(Kand_VALUE.프로그램끝() == 0x06000000, "과정별 App_f5044b9b 끝 격리");

        Kand_VALUE.Schluss_App(7);
        verifizéieren(호출.자식기다리기(부모, Kand_VALUE.Identifikateur_VALUE(), false) == (7 << 8), "Kand_VALUE Schluss_App 기다리기");
        verifizéieren(호출.접근가능("시험", 1) == -13, "ausféieren_Befeel Geneemegung_VALUE 거부");
        verifizéieren(호출.Benotzer_Identifikateur() == 0 && 호출.Grupp_Identifikateur() == 0, "사용자와 무리 Identifikateur_VALUE");
        verifizéieren("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_Aufgabelëscht("/") == 0, "현재 작업 Agab_Lëscht");
        verifizéieren(호출.단말인가(부모, 1), "표준 출력 단말");
        verifizéieren("JLuxOS".equals(호출.체계정보().System_Numm()), "Betribssystem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(Kernel Kernel_VALUE) {
        byte[] Daten = new byte[92];
        Daten[0] = 0x7f;
        Daten[1] = 'E';
        Daten[2] = 'L';
        Daten[3] = 'F';
        Daten[4] = 1;
        Daten[5] = 1;
        schreiwen_Ganzzuel_VALUE(Daten, 24, 0x04001000);
        schreiwen_Ganzzuel_VALUE(Daten, 32, 52);
        짧은정수쓰기(Daten, 46, 40);
        짧은정수쓰기(Daten, 48, 1);
        schreiwen_Ganzzuel_VALUE(Daten, 56, 8);
        schreiwen_Ganzzuel_VALUE(Daten, 60, 2);
        schreiwen_Ganzzuel_VALUE(Daten, 64, 0x04002000);
        schreiwen_Ganzzuel_VALUE(Daten, 72, 64);

        실행파일적재기.Bild Bild_VALUE = new 실행파일적재기().검사(Daten);
        verifizéieren(Bild_VALUE.Start_Adress() == 0x04001000, "ELF Laf Adress");
        verifizéieren(Bild_VALUE.구역들().size() == 1 && Bild_VALUE.구역들().get(0).종류() == 8, "ELF 빈 Daten Beräich_VALUE");
        int 서술자 = Kernel_VALUE.체계호출().ariichten(Kernel_VALUE.첫과정(), "시험", 체계호출.schreifgeschützt_kennzeechnen);
        verifizéieren(Kernel_VALUE.체계호출().Fichier_Kontroll(Kernel_VALUE.첫과정(), 서술자, 2, 1) == 0, "ausféieren_Befeel 시 Clôture Astellungen");
        verifizéieren(Kernel_VALUE.체계호출().ausféieren_Befeel(Kernel_VALUE.첫과정(), Daten, new String[] {"시험", "값"}, new String[] {"Sprooch=한국어"}) == 0, "ELF ausféieren_Befeel Bild_VALUE 적재");
        verifizéieren(Kernel_VALUE.첫과정().실행시작주소() == 0x04001000, "ausféieren_Befeel Laf Adress 반영");
        verifizéieren(Kernel_VALUE.첫과정().실행인자().length == 2 && Kernel_VALUE.첫과정().환경값().length == 1, "ausféieren_Befeel 인자와 환경");
        verifizéieren(!Kernel_VALUE.첫과정().파일서술자().열려있음(서술자), "ausféieren_Befeel 시 서술자 Clôture");
        verifizéieren(Kernel_VALUE.쪽관리().바이트읽기(Kernel_VALUE.첫과정().Adress_Plaz(), 0x04002000) == 0, "빈 Daten Beräich_VALUE 영 initialiséieren");
    }

    private static void 입력시험(Kernel Kernel_VALUE) {
        Kernel_VALUE.입력관리().키누름('가');
        Kernel_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = Kernel_VALUE.입력관리().Weider_Evenement();
        입력사건 SECOND_Evenement = Kernel_VALUE.입력관리().Weider_Evenement();
        verifizéieren(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Evenement");
        verifizéieren(SECOND_Evenement.첫째값() == 3 && SECOND_Evenement.SECOND_VALUE() == -2, "쥐 verréckelen_VALUE Evenement");
    }

    private static void 하드웨어시험(호스트하드웨어 Mobil_VALUE) {
        Mobil_VALUE.schreiwen_Port_Byte(0x3f8, 0xab);
        verifizéieren(Mobil_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        verifizéieren(Mobil_VALUE.직렬기록().contains("JLuxOS"), "직렬 LOG_Rei");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Manager Manager_VALUE = new IRQ_Manager();
        Manager_VALUE.registréieren_Agab(0x21, Späicher_Adress -> Späicher_Adress + 4);
        Manager_VALUE.aschalten();
        verifizéieren(Manager_VALUE.verdeelen_VALUE(0x21, 100) == 104, "IRQ verdeelen_VALUE");
        Manager_VALUE.desaktivéieren();
        verifizéieren(Manager_VALUE.verdeelen_VALUE(0x21, 100) == 100, "IRQ desaktivéieren");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.Saz_Standardwäert();
        verifizéieren(서술자표.조각들().size() == 5, "전역 서술자표");
        To_do_Status_Segment To_do_Status = new To_do_Status_Segment();
        To_do_Status.특권쌓임공간설정(0x10, 0x800000);
        verifizéieren(To_do_Status.영번쌓임조각() == 0x10 && To_do_Status.영번쌓임주소() == 0x800000, "작업 Status_VALUE Beräich_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Späicher_Mobil = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.Beräich_d_Gréisst_veränneren];
        byte[] 읽은자료 = new byte[고급기술결합장치.Beräich_d_Gréisst_veränneren];
        쓸자료[17] = 42;
        Späicher_Mobil.schreiwen(2, 쓸자료);
        Späicher_Mobil.읽기(2, 읽은자료);
        verifizéieren(읽은자료[17] == 42, "ATA Beräich_VALUE 읽고 schreiwen");

        Accessoire_Bus_Manager Accessoire = new Accessoire_Bus_Manager();
        Accessoire.발견(new Accessoire_Bus_Manager.Mobil_VALUE(0x1022, 0x2000, 0xc000, 11));
        verifizéieren(Accessoire.FIND_Agab(0x1022, 0x2000) != null, "주변 Mobil_VALUE FIND_Agab");

        byte[] Ethernet_Rumm = new byte[34];
        Ethernet_Rumm[12] = 0x08;
        Ethernet_Rumm[13] = 0x00;
        Ethernet_Rumm[14] = 0x45;
        verifizéieren(Reseau_Tools.Ethernet_UPPER_Protokoll(Ethernet_Rumm) == 0x0800, "이더넷 상위 Job_VALUE");
        verifizéieren(Reseau_Tools.상호통신망규약사판인가(Ethernet_Rumm, 14), "상호통신망규약 4판");
        verifizéieren(Reseau_Tools.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        schreiwen_Ganzzuel_VALUE(첫구역, 454, 63);
        schreiwen_Ganzzuel_VALUE(첫구역, 458, 1024);
        verifizéieren(new 기본분할영역표().읽기(첫구역).size() == 1, "Standardwäert 분할 영역표");

        Reseau_Layer Layer_VALUE = new Reseau_Layer();
        int[] RECEIVED_COUNT = new int[1];
        Layer_VALUE.registréieren_Benotzer_Daten_Lektioun(7, (Daten, Laf, Längt_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] Rumm_INDEX = new byte[14 + 20 + 8];
        Rumm_INDEX[12] = 0x08;
        Rumm_INDEX[13] = 0x00;
        Rumm_INDEX[14] = 0x45;
        Rumm_INDEX[16] = 0;
        Rumm_INDEX[17] = 28;
        Rumm_INDEX[23] = 17;
        Rumm_INDEX[36] = 0;
        Rumm_INDEX[37] = 7;
        verifizéieren(Layer_VALUE.이더넷받기(Rumm_INDEX) && RECEIVED_COUNT[0] == 1, "Benotzer Daten Lektioun_VALUE verdeelen_VALUE");
    }

    private static void 화면과시계시험() {
        Zeechen_Bildschierm 화면 = new Zeechen_Bildschierm();
        화면.출력("가나\n다");
        verifizéieren(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Auer Auer = new Auer(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Auer.틱();
        }
        verifizéieren(Auer.지난밀리초() == 100, "Auer 틱 CONVERT_VALUE");
    }

    private static void schreiwen_Ganzzuel_VALUE(byte[] Daten, int positionéieren, int VALUE) {
        Daten[positionéieren] = (byte) VALUE;
        Daten[positionéieren + 1] = (byte) (VALUE >>> 8);
        Daten[positionéieren + 2] = (byte) (VALUE >>> 16);
        Daten[positionéieren + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] Daten, int positionéieren, int VALUE) {
        Daten[positionéieren] = (byte) VALUE;
        Daten[positionéieren + 1] = (byte) (VALUE >>> 8);
    }

    private static void verifizéieren(boolean Bedéngung, String Numm) {
        if (!Bedéngung) {
            throw new AssertionError("Feeler_VALUE: " + Numm);
        }
        iwwermëttelen_COUNT++;
        System.out.println("iwwermëttelen_VALUE: " + Numm);
    }
}
