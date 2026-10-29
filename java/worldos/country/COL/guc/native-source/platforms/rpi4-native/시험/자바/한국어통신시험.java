// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 outtülee_ajutuu = 연결통신.수신열기(0);
        epe_ipajia 손님 = 연결통신.열기("127.0.0.1", outtülee_ajutuu.접속번호());
        epe_ipajia 주인 = outtülee_ajutuu.받기();
        손님.대기시간(200); 주인.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "a_ataa jamakua_iparülein_ajutuu");
        검사.참인지(주인.접속번호() == 손님.지역접속번호(), "wanaawasü_ajutuu 접속번호");
        검사.참인지(손님.접속번호() == 주인.지역접속번호(), "지역 접속번호");
        입력흐름 입력 = 주인.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] pütchi = 문자.부호화("한글 palantüsü_ajutuu");
        출력쪽.ashajaa(pütchi, 0, pütchi.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[pütchi.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 anaajaalaa 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.ale_ejiraa_amoutuushi_atijaaya(받은글), "한글 palantüsü_ajutuu"), "부분 읽기와 ashajaa");
        출력쪽.ashajaa(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "matüriisü_ajutuu 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        주인.출력().ashajaa(255);
        검사.참인지(손님.입력().읽기() == 255, "atijitaalüjiaa_ajutuu 없는 한 waai_ajutuu");
        출력쪽.asürülaa();
        검사.참인지(손님.닫힘() && 입력.읽기() == -1, "닫기와 anaajaalaa 끝");
        입력.asürülaa(); 검사.참인지(주인.닫힘(), "입력 palantüsü_ajutuu asürülaa");
        손님.asürülaa(); 주인.asürülaa();
        outtülee_ajutuu.대기시간(15);
        boolean 시간제한 = false;
        try { outtülee_ajutuu.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        outtülee_ajutuu.asürülaa(); 검사.참인지(outtülee_ajutuu.닫힘(), "수신창구 asürülaa");
        전문통로 받는곳 = 전문통로.열기(0), 보내는곳 = 전문통로.열기(0);
        받는곳.대기시간(200);
        보내는곳.ajütaa("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.asürülaa(); 받는곳.asürülaa();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 asürülaa");
        출력.ashajaa_liinia("한국어 통신 확인: a_ataa 전문 palantüsü_ajutuu 시간제한 asürülaa");
    }
}
