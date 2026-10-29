// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 poti_agaciro = 연결통신.수신열기(0);
        kwihuza 손님 = 연결통신.Gufungura("127.0.0.1", poti_agaciro.접속번호());
        kwihuza nyirayo_indanga = poti_agaciro.받기();
        손님.대기시간(200); nyirayo_indanga.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "Guhuza imimerere_agaciro");
        검사.참인지(nyirayo_indanga.접속번호() == 손님.지역접속번호(), "Mugenzi_agaciro 접속번호");
        검사.참인지(손님.접속번호() == nyirayo_indanga.지역접속번호(), "mu_gace_urwego 접속번호");
        입력흐름 입력 = nyirayo_indanga.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] ubutumwa = 문자.부호화("한글 Stream_agaciro");
        출력쪽.kwandika(ubutumwa, 0, ubutumwa.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[ubutumwa.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Idosiye 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.gusobanura_amakurushingiro(받은글), "한글 Stream_agaciro"), "부분 읽기와 kwandika");
        출력쪽.kwandika(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_agaciro 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        nyirayo_indanga.출력().kwandika(255);
        검사.참인지(손님.입력().읽기() == 255, "gusobeka_agaciro 없는 한 bayiti_agaciro");
        출력쪽.Gufunga();
        검사.참인지(손님.닫힘() && 입력.읽기() == -1, "닫기와 Idosiye 끝");
        입력.Gufunga(); 검사.참인지(nyirayo_indanga.닫힘(), "입력 Stream_agaciro Gufunga");
        손님.Gufunga(); nyirayo_indanga.Gufunga();
        poti_agaciro.대기시간(15);
        boolean 시간제한 = false;
        try { poti_agaciro.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        poti_agaciro.Gufunga(); 검사.참인지(poti_agaciro.닫힘(), "수신창구 Gufunga");
        전문통로 받는곳 = 전문통로.Gufungura(0), 보내는곳 = 전문통로.Gufungura(0);
        받는곳.대기시간(200);
        보내는곳.kohereza("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Gufunga(); 받는곳.Gufunga();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Gufunga");
        출력.kwandika_umurongo("Ikinyarwanda 통신 gusuzuma: Guhuza 전문 Stream_agaciro 시간제한 Gufunga");
    }
}
