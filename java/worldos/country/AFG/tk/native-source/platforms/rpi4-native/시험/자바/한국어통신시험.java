// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 port_baha = 연결통신.수신열기(0);
        birikme 손님 = 연결통신.Aç("127.0.0.1", port_baha.접속번호());
        birikme eýe_tanaýjy = port_baha.받기();
        손님.대기시간(200); eýe_tanaýjy.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "Birikme ýagdaý_baha");
        검사.참인지(eýe_tanaýjy.접속번호() == 손님.지역접속번호(), "deň_derejeli_düwün_baha 접속번호");
        검사.참인지(손님.접속번호() == eýe_tanaýjy.지역접속번호(), "ýerli_elýeterli_gor 접속번호");
        입력흐름 입력 = eýe_tanaýjy.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] habar = 문자.부호화("한글 Stream_baha");
        출력쪽.Ýaz(habar, 0, habar.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[habar.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Oka(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Faýl 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.koddan_aç_maglumat(받은글), "한글 Stream_baha"), "부분 읽기와 Ýaz");
        출력쪽.Ýaz(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Oka(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_baha Oka");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Oka();
        검사.참인지(두바이트[1] == 18, "나머지 Oka");
        eýe_tanaýjy.출력().Ýaz(255);
        검사.참인지(손님.입력().Oka() == 255, "kodlaşdyrma_baha 없는 한 baýt_baha");
        출력쪽.Ýap();
        검사.참인지(손님.닫힘() && 입력.Oka() == -1, "닫기와 Faýl 끝");
        입력.Ýap(); 검사.참인지(eýe_tanaýjy.닫힘(), "입력 Stream_baha Ýap");
        손님.Ýap(); eýe_tanaýjy.Ýap();
        port_baha.대기시간(15);
        boolean 시간제한 = false;
        try { port_baha.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        port_baha.Ýap(); 검사.참인지(port_baha.닫힘(), "수신창구 Ýap");
        전문통로 받는곳 = 전문통로.Aç(0), 보내는곳 = 전문통로.Aç(0);
        받는곳.대기시간(200);
        보내는곳.iber("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Ýap(); 받는곳.Ýap();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Ýap");
        출력.ýaz_setir("한국어 통신 barla: Birikme 전문 Stream_baha 시간제한 Ýap");
    }
}
