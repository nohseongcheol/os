// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mayotte.JMytOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Mayotte.JMytOS.기억공간.kumbukumbu_msimamizi;
import Mayotte.JMytOS.기억공간.ukurasa_msimamizi;
import Mayotte.JMytOS.입력.입력사건;
import Mayotte.JMytOS.작업.Mchakato_thamani;
import Mayotte.JMytOS.체계호출.체계호출;
import Mayotte.JMytOS.mfumo_ya_mafaili.실행파일적재기;
import Mayotte.JMytOS.kiini.kiini;
import Mayotte.JMytOS.mwenyeji.호스트하드웨어;
import Mayotte.JMytOS.IRQ.IRQ_msimamizi;
import Mayotte.JMytOS.서술자.전역서술자표;
import Mayotte.JMytOS.Hifadhi_kifaa.고급기술결합장치;
import Mayotte.JMytOS.kifaa_thamani.kipembezo_basi_msimamizi;
import Mayotte.JMytOS.Mtandao_Mpororo.Mtandao_Zana;
import Mayotte.JMytOS.Mtandao_Mpororo.Mtandao_tabaka;
import Mayotte.JMytOS.kifaa_thamani.saa;
import Mayotte.JMytOS.서술자.kazi_hali_sehemu;
import Mayotte.JMytOS.화면.kibambo_onyesha;
import Mayotte.JMytOS.mfumo_ya_mafaili.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] parameta_hoja) {
        호스트하드웨어 kifaa_thamani = new 호스트하드웨어();
        kiini kiini_thamani_0611a8a8 = new kiini(kifaa_thamani);
        kiini_thamani_0611a8a8.endesha();

        기억공간시험(kiini_thamani_0611a8a8);
        쪽관리시험(kiini_thamani_0611a8a8);
        파일과과정시험(kiini_thamani_0611a8a8);
        실행파일시험(kiini_thamani_0611a8a8);
        입력시험(kiini_thamani_0611a8a8);
        하드웨어시험(kifaa_thamani);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JMytOS 시험 pitisha_thamani: " + 통과수);
    }

    private static void 기억공간시험(kiini kiini_thamani_0611a8a8) {
        kumbukumbu_msimamizi msimamizi_thamani = kiini_thamani_0611a8a8.기억공간();
        int 첫주소 = msimamizi_thamani.정렬할당(100, 64);
        thibitisha((첫주소 & 63) == 0, "pangilia_thamani tengea_Hifadhi");
        msimamizi_thamani.andika_baiti_thamani(첫주소, (byte) 0x5a);
        thibitisha(msimamizi_thamani.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 andika");
        int 사용전 = msimamizi_thamani.사용크기();
        msimamizi_thamani.toleo_Hifadhi(첫주소);
        thibitisha(msimamizi_thamani.사용크기() < 사용전, "기억공간 toleo_Hifadhi");
    }

    private static void 쪽관리시험(kiini kiini_thamani_0611a8a8) {
        ukurasa_msimamizi msimamizi_thamani = kiini_thamani_0611a8a8.쪽관리();
        ukurasa_msimamizi.anwani_eneo 부모공간 = msimamizi_thamani.새주소공간();
        msimamizi_thamani.ramani_ukurasa(부모공간, 0x1000, true);
        msimamizi_thamani.andika_baiti_thamani(부모공간, 0x1010, (byte) 7);
        ukurasa_msimamizi.anwani_eneo mtoto_eneo = msimamizi_thamani.쓰기시복사복제(부모공간);
        msimamizi_thamani.andika_baiti_thamani(mtoto_eneo, 0x1010, (byte) 9);
        thibitisha(msimamizi_thamani.바이트읽기(부모공간, 0x1010) == 7, "andika 시 mfano_thamani 부모 격리");
        thibitisha(msimamizi_thamani.바이트읽기(mtoto_eneo, 0x1010) == 9, "andika 시 mfano_thamani mtoto_thamani andika");
    }

    private static void 파일과과정시험(kiini kiini_thamani_0611a8a8) {
        byte[] maudhui_thamani = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kiini_thamani_0611a8a8.mfumo_ya_mafaili().파일추가("시험", maudhui_thamani);
        Mchakato_thamani 부모 = kiini_thamani_0611a8a8.첫과정();
        체계호출 호출 = kiini_thamani_0611a8a8.체계호출();
        int 서술자 = 호출.unda(부모, "/시험", 체계호출.soma_tu_alama);
        thibitisha(서술자 >= 3, "faili unda");

        byte[] 받을곳 = new byte[maudhui_thamani.length];
        thibitisha(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == maudhui_thamani.length, "faili 읽기");
        thibitisha(Arrays.equals(maudhui_thamani, 받을곳), "faili maudhui_thamani");
        thibitisha(호출.위치옮기기(부모, 서술자, 0, 체계호출.Duhusi_Anza) == 0, "faili 위치 hamisha_thamani");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        thibitisha(복제서술자 >= 0, "서술자 복제");
        Mchakato_thamani mtoto_thamani = 호출.과정복제(부모);
        thibitisha(mtoto_thamani.kitambulishi_thamani() != 부모.kitambulishi_thamani(), "Mchakato_thamani kitambulishi_thamani 분리");
        thibitisha(mtoto_thamani.부모식별자() == 부모.kitambulishi_thamani(), "부모 Mchakato_thamani kitambulishi_thamani");
        thibitisha(호출.funga(mtoto_thamani, 서술자) == 0 && 부모.파일서술자().teknolojia_ya_maelezo_unda(서술자), "mtoto_thamani funga 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        thibitisha(이전끝 == 0x06000000, "programu_f5044b9b 끝 늘리기");
        thibitisha(부모.프로그램끝() == 0x06002000, "programu_f5044b9b 끝 반영");
        thibitisha(mtoto_thamani.프로그램끝() == 0x06000000, "과정별 programu_f5044b9b 끝 격리");

        mtoto_thamani.toka_programu(7);
        thibitisha(호출.자식기다리기(부모, mtoto_thamani.kitambulishi_thamani(), false) == (7 << 8), "mtoto_thamani toka_programu 기다리기");
        thibitisha(호출.접근가능("시험", 1) == -13, "tekeleza_amri kibali_thamani kataa_thamani");
        thibitisha(호출.mtumiaji_kitambulishi() == 0 && 호출.Kikundi_kitambulishi() == 0, "사용자와 무리 kitambulishi_thamani");
        thibitisha("/".equals(호출.현재작업목록(2)) && 호출.badili_orodha_ya_kazi("/") == 0, "현재 작업 ingizo_Orodha");
        thibitisha(호출.단말인가(부모, 1), "표준 출력 단말");
        thibitisha("JMytOS".equals(호출.체계정보().mfumo_jina()), "mfumo_endeshi_thamani msinfo32_exe");
    }

    private static void 실행파일시험(kiini kiini_thamani_0611a8a8) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        andika_namba_kamili_thamani(data, 24, 0x04001000);
        andika_namba_kamili_thamani(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        andika_namba_kamili_thamani(data, 56, 8);
        andika_namba_kamili_thamani(data, 60, 2);
        andika_namba_kamili_thamani(data, 64, 0x04002000);
        andika_namba_kamili_thamani(data, 72, 64);

        실행파일적재기.picha picha_thamani = new 실행파일적재기().검사(data);
        thibitisha(picha_thamani.Anza_anwani() == 0x04001000, "ELF endesha anwani");
        thibitisha(picha_thamani.구역들().size() == 1 && picha_thamani.구역들().get(0).종류() == 8, "ELF 빈 data sehemu_thamani");
        int 서술자 = kiini_thamani_0611a8a8.체계호출().unda(kiini_thamani_0611a8a8.첫과정(), "시험", 체계호출.soma_tu_alama);
        thibitisha(kiini_thamani_0611a8a8.체계호출().faili_udhibiti(kiini_thamani_0611a8a8.첫과정(), 서술자, 2, 1) == 0, "tekeleza_amri 시 funga Mipangilio");
        thibitisha(kiini_thamani_0611a8a8.체계호출().tekeleza_amri(kiini_thamani_0611a8a8.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Lugha=한국어"}) == 0, "ELF tekeleza_amri picha_thamani 적재");
        thibitisha(kiini_thamani_0611a8a8.첫과정().실행시작주소() == 0x04001000, "tekeleza_amri endesha anwani 반영");
        thibitisha(kiini_thamani_0611a8a8.첫과정().실행인자().length == 2 && kiini_thamani_0611a8a8.첫과정().환경값().length == 1, "tekeleza_amri 인자와 환경");
        thibitisha(!kiini_thamani_0611a8a8.첫과정().파일서술자().teknolojia_ya_maelezo_unda(서술자), "tekeleza_amri 시 서술자 funga");
        thibitisha(kiini_thamani_0611a8a8.쪽관리().바이트읽기(kiini_thamani_0611a8a8.첫과정().anwani_eneo(), 0x04002000) == 0, "빈 data sehemu_thamani 영 anzilisha");
    }

    private static void 입력시험(kiini kiini_thamani_0611a8a8) {
        kiini_thamani_0611a8a8.입력관리().키누름('가');
        kiini_thamani_0611a8a8.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kiini_thamani_0611a8a8.입력관리().다음사건();
        입력사건 둘째사건 = kiini_thamani_0611a8a8.입력관리().다음사건();
        thibitisha(첫사건.사건종류() == 입력사건.종류.키누름, "자판 tukio");
        thibitisha(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 hamisha_thamani tukio");
    }

    private static void 하드웨어시험(호스트하드웨어 kifaa_thamani) {
        kifaa_thamani.andika_kituo_baiti(0x3f8, 0xab);
        thibitisha(kifaa_thamani.포트바이트읽기(0x3f8) == 0xab, "포트 I_T 경계");
        thibitisha(kifaa_thamani.직렬기록().contains("JMytOS"), "직렬 batli_REKODI");
    }

    private static void 개입중단과서술자시험() {
        IRQ_msimamizi msimamizi_thamani = new IRQ_msimamizi();
        msimamizi_thamani.sajili_ingizo(0x21, Hifadhi_anwani -> Hifadhi_anwani + 4);
        msimamizi_thamani.washa();
        thibitisha(msimamizi_thamani.sambaza_thamani(0x21, 100) == 104, "IRQ sambaza_thamani");
        msimamizi_thamani.lemaza();
        thibitisha(msimamizi_thamani.sambaza_thamani(0x21, 100) == 100, "IRQ lemaza");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.seti_hali_ya_chaguo_msingi();
        thibitisha(서술자표.조각들().size() == 5, "전역 서술자표");
        kazi_hali_sehemu kazi_hali = new kazi_hali_sehemu();
        kazi_hali.특권쌓임공간설정(0x10, 0x800000);
        thibitisha(kazi_hali.영번쌓임조각() == 0x10 && kazi_hali.영번쌓임주소() == 0x800000, "작업 hali_thamani sehemu_thamani");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Hifadhi_kifaa = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sehemu_panga_ukubwa];
        byte[] 읽은자료 = new byte[고급기술결합장치.sehemu_panga_ukubwa];
        쓸자료[17] = 42;
        Hifadhi_kifaa.andika(2, 쓸자료);
        Hifadhi_kifaa.읽기(2, 읽은자료);
        thibitisha(읽은자료[17] == 42, "ATA sehemu_thamani 읽고 andika");

        kipembezo_basi_msimamizi kipembezo = new kipembezo_basi_msimamizi();
        kipembezo.발견(new kipembezo_basi_msimamizi.kifaa_thamani(0x1022, 0x2000, 0xc000, 11));
        thibitisha(kipembezo.gundua_ingizo(0x1022, 0x2000) != null, "주변 kifaa_thamani gundua_ingizo");

        byte[] Ethaneti_fremu = new byte[34];
        Ethaneti_fremu[12] = 0x08;
        Ethaneti_fremu[13] = 0x00;
        Ethaneti_fremu[14] = 0x45;
        thibitisha(Mtandao_Zana.이더넷상위규약(Ethaneti_fremu) == 0x0800, "이더넷 상위 Kazi_thamani");
        thibitisha(Mtandao_Zana.상호통신망규약사판인가(Ethaneti_fremu, 14), "상호통신망규약 4판");
        thibitisha(Mtandao_Zana.wingu_jumla(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 jumla");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        andika_namba_kamili_thamani(첫구역, 454, 63);
        andika_namba_kamili_thamani(첫구역, 458, 1024);
        thibitisha(new 기본분할영역표().읽기(첫구역).size() == 1, "hali_ya_chaguo_msingi 분할 영역표");

        Mtandao_tabaka tabaka_thamani = new Mtandao_tabaka();
        int[] 받은수 = new int[1];
        tabaka_thamani.sajili_mtumiaji_data_funzo(7, (data, endesha, urefu_thamani) -> 받은수[0]++);
        byte[] fremu_kielezo = new byte[14 + 20 + 8];
        fremu_kielezo[12] = 0x08;
        fremu_kielezo[13] = 0x00;
        fremu_kielezo[14] = 0x45;
        fremu_kielezo[16] = 0;
        fremu_kielezo[17] = 28;
        fremu_kielezo[23] = 17;
        fremu_kielezo[36] = 0;
        fremu_kielezo[37] = 7;
        thibitisha(tabaka_thamani.이더넷받기(fremu_kielezo) && 받은수[0] == 1, "mtumiaji data funzo_thamani sambaza_thamani");
    }

    private static void 화면과시계시험() {
        kibambo_onyesha 화면 = new kibambo_onyesha();
        화면.출력("가나\n다");
        thibitisha(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        saa saa = new saa(100);
        for (int kielezo = 0; kielezo < 10; kielezo++) {
            saa.틱();
        }
        thibitisha(saa.지난밀리초() == 100, "saa 틱 변환");
    }

    private static void andika_namba_kamili_thamani(byte[] data, int 위치, int thamani) {
        data[위치] = (byte) thamani;
        data[위치 + 1] = (byte) (thamani >>> 8);
        data[위치 + 2] = (byte) (thamani >>> 16);
        data[위치 + 3] = (byte) (thamani >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int 위치, int thamani) {
        data[위치] = (byte) thamani;
        data[위치 + 1] = (byte) (thamani >>> 8);
    }

    private static void thibitisha(boolean sharti, String Jina) {
        if (!sharti) {
            throw new AssertionError("kushindwa_thamani: " + Jina);
        }
        통과수++;
        System.out.println("pitisha_thamani: " + Jina);
    }
}
