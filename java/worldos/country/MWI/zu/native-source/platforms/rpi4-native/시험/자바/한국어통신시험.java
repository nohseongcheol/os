// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 intuba_inani = 연결통신.수신열기(0);
        uxhumano isivakashi_inani = 연결통신.Vula("127.0.0.1", intuba_inani.접속번호());
        uxhumano umnikazi_isivezi = intuba_inani.받기();
        isivakashi_inani.대기시간(200); umnikazi_isivezi.대기시간(200);
        검사.참인지(isivakashi_inani.연결됨() && !isivakashi_inani.닫힘(), "Xhumanisa isimo_inani");
        검사.참인지(umnikazi_isivezi.접속번호() == isivakashi_inani.지역접속번호(), "untanga_inani 접속번호");
        검사.참인지(isivakashi_inani.접속번호() == umnikazi_isivezi.지역접속번호(), "endaweni_umklamo 접속번호");
        입력흐름 입력 = umnikazi_isivezi.입력(); 출력흐름 출력쪽 = isivakashi_inani.출력();
        byte[] umlayezo = 문자.부호화("한글 Stream_inani");
        출력쪽.Bhala(umlayezo, 0, umlayezo.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[umlayezo.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Funda(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Ihele 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.guqulela_imininingwane(받은글), "한글 Stream_inani"), "부분 읽기와 Bhala");
        출력쪽.Bhala(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Funda(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "AMALUNGU_AFANAYO_inani Funda");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Funda();
        검사.참인지(두바이트[1] == 18, "나머지 Funda");
        umnikazi_isivezi.출력().Bhala(255);
        검사.참인지(isivakashi_inani.입력().Funda() == 255, "ukubhala_ngokufihla_inani 없는 한 ibhayithi_inani");
        출력쪽.Vala();
        검사.참인지(isivakashi_inani.닫힘() && 입력.Funda() == -1, "닫기와 Ihele 끝");
        입력.Vala(); 검사.참인지(umnikazi_isivezi.닫힘(), "입력 Stream_inani Vala");
        isivakashi_inani.Vala(); umnikazi_isivezi.Vala();
        intuba_inani.대기시간(15);
        boolean 시간제한 = false;
        try { intuba_inani.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        intuba_inani.Vala(); 검사.참인지(intuba_inani.닫힘(), "수신창구 Vala");
        전문통로 받는곳 = 전문통로.Vula(0), 보내는곳 = 전문통로.Vula(0);
        받는곳.대기시간(200);
        보내는곳.Thumela("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Vala(); 받는곳.Vala();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Vala");
        출력.bhala_umugqa("Isi_Zulu 통신 qiniseka: Xhumanisa 전문 Stream_inani 시간제한 Vala");
    }
}
