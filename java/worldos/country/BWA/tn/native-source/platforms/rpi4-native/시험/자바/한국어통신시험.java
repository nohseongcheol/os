// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 gorogisetsa_Boleng = 연결통신.수신열기(0);
        Kgolagano moeng_Boleng = 연결통신.bula("127.0.0.1", gorogisetsa_Boleng.접속번호());
        Kgolagano mong_setlhaodi = gorogisetsa_Boleng.받기();
        moeng_Boleng.대기시간(200); mong_setlhaodi.대기시간(200);
        검사.참인지(moeng_Boleng.연결됨() && !moeng_Boleng.닫힘(), "Golaganya kemo_Boleng");
        검사.참인지(mong_setlhaodi.접속번호() == moeng_Boleng.지역접속번호(), "semphato_Boleng 접속번호");
        검사.참인지(moeng_Boleng.접속번호() == mong_setlhaodi.지역접속번호(), "e_e_gaufi_Mothamo 접속번호");
        입력흐름 입력 = mong_setlhaodi.입력(); 출력흐름 출력쪽 = moeng_Boleng.출력();
        byte[] molaetsa = 문자.부호화("한글 moela_Boleng");
        출력쪽.kwala(molaetsa, 0, molaetsa.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[molaetsa.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 faele 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.Sirolola_tshedimosetso(받은글), "한글 moela_Boleng"), "부분 읽기와 kwala");
        출력쪽.kwala(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "setlhopha_Boleng_ed437109 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        mong_setlhaodi.출력().kwala(255);
        검사.참인지(moeng_Boleng.입력().읽기() == 255, "khoutufatso_Boleng 없는 한 baete_Boleng");
        출력쪽.tswala();
        검사.참인지(moeng_Boleng.닫힘() && 입력.읽기() == -1, "닫기와 faele 끝");
        입력.tswala(); 검사.참인지(mong_setlhaodi.닫힘(), "입력 moela_Boleng tswala");
        moeng_Boleng.tswala(); mong_setlhaodi.tswala();
        gorogisetsa_Boleng.대기시간(15);
        boolean 시간제한 = false;
        try { gorogisetsa_Boleng.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        gorogisetsa_Boleng.tswala(); 검사.참인지(gorogisetsa_Boleng.닫힘(), "수신창구 tswala");
        전문통로 받는곳 = 전문통로.bula(0), 보내는곳 = 전문통로.bula(0);
        받는곳.대기시간(200);
        보내는곳.romela("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.tswala(); 받는곳.tswala();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 tswala");
        출력.kwala_Mola("한국어 통신 netefatsa: Golaganya 전문 moela_Boleng 시간제한 tswala");
    }
}
