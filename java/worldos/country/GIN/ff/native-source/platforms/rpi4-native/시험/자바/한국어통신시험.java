// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 poor_njaru = 연결통신.수신열기(0);
        ceŋondiral 손님 = 연결통신.udditde("127.0.0.1", poor_njaru.접속번호());
        ceŋondiral 주인 = poor_njaru.받기();
        손님.대기시간(200); 주인.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "seŋaade ngonka_njaru");
        검사.참인지(주인.접속번호() == 손님.지역접속번호(), "giƴiraaɗo_njaru 접속번호");
        검사.참인지(손님.접속번호() == 주인.지역접속번호(), "nokkuwal_njaajeendi 접속번호");
        입력흐름 입력 = 주인.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] ɓatakuru = 문자.부호화("한글 waraango_njaru");
        출력쪽.winndude(ɓatakuru, 0, ɓatakuru.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[ɓatakuru.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 fiilde 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dokkitde_keɓe(받은글), "한글 waraango_njaru"), "부분 읽기와 winndude");
        출력쪽.winndude(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "배열 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        주인.출력().winndude(255);
        검사.참인지(손님.입력().읽기() == 255, "dokkagol_njaru 없는 한 oktee_njaru");
        출력쪽.uddude();
        검사.참인지(손님.닫힘() && 입력.읽기() == -1, "닫기와 fiilde 끝");
        입력.uddude(); 검사.참인지(주인.닫힘(), "입력 waraango_njaru uddude");
        손님.uddude(); 주인.uddude();
        poor_njaru.대기시간(15);
        boolean 시간제한 = false;
        try { poor_njaru.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        poor_njaru.uddude(); 검사.참인지(poor_njaru.닫힘(), "수신창구 uddude");
        전문통로 받는곳 = 전문통로.udditde(0), 보내는곳 = 전문통로.udditde(0);
        받는곳.대기시간(200);
        보내는곳.neldude("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.uddude(); 받는곳.uddude();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 uddude");
        출력.winndude_diidol("한국어 통신 ƴeewtaade: seŋaade 전문 waraango_njaru 시간제한 uddude");
    }
}
