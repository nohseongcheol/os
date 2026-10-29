// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 jël_xëyma = 연결통신.수신열기(0);
        jokkalóo gan_xëyma = 연결통신.sos("127.0.0.1", jël_xëyma.접속번호());
        jokkalóo boroom_raññeekaay = jël_xëyma.받기();
        gan_xëyma.대기시간(200); boroom_raññeekaay.대기시간(200);
        검사.참인지(gan_xëyma.연결됨() && !gan_xëyma.닫힘(), "JOKKOO nekkin_xëyma");
        검사.참인지(boroom_raññeekaay.접속번호() == gan_xëyma.지역접속번호(), "Nàttangoo_xëyma 접속번호");
        검사.참인지(gan_xëyma.접속번호() == boroom_raññeekaay.지역접속번호(), "dënnd_nameef 접속번호");
        입력흐름 입력 = boroom_raññeekaay.입력(); 출력흐름 출력쪽 = gan_xëyma.출력();
        byte[] bataaxal = 문자.부호화("한글 dawal_xëyma");
        출력쪽.biir(bataaxal, 0, bataaxal.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[bataaxal.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 bara_denc 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.fecci_mbir(받은글), "한글 dawal_xëyma"), "부분 읽기와 biir");
        출력쪽.biir(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "TABLO_xëyma 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        boroom_raññeekaay.출력().biir(255);
        검사.참인지(gan_xëyma.입력().읽기() == 255, "nëbbin_ci_lim_xëyma 없는 한 okte_xëyma");
        출력쪽.Tej();
        검사.참인지(gan_xëyma.닫힘() && 입력.읽기() == -1, "닫기와 bara_denc 끝");
        입력.Tej(); 검사.참인지(boroom_raññeekaay.닫힘(), "입력 dawal_xëyma Tej");
        gan_xëyma.Tej(); boroom_raññeekaay.Tej();
        jël_xëyma.대기시간(15);
        boolean 시간제한 = false;
        try { jël_xëyma.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        jël_xëyma.Tej(); 검사.참인지(jël_xëyma.닫힘(), "수신창구 Tej");
        전문통로 받는곳 = 전문통로.sos(0), 보내는곳 = 전문통로.sos(0);
        받는곳.대기시간(200);
        보내는곳.Yónnee("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Tej(); 받는곳.Tej();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Tej");
        출력.biir_buum("한국어 통신 luñutu: JOKKOO 전문 dawal_xëyma 시간제한 Tej");
    }
}
