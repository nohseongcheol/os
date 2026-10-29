// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 kawe_uara = 연결통신.수신열기(0);
        hononga_d584d28a manuhiri_uara = 연결통신.Huaki("127.0.0.1", kawe_uara.접속번호());
        hononga_d584d28a kaipupuri_pūtāutu = kawe_uara.받기();
        manuhiri_uara.KUA_PAU_TE_WĀ(200); kaipupuri_pūtāutu.KUA_PAU_TE_WĀ(200);
        검사.참인지(manuhiri_uara.연결됨() && !manuhiri_uara.닫힘(), "TŪHONO tūnga_uara");
        검사.참인지(kaipupuri_pūtāutu.접속번호() == manuhiri_uara.지역접속번호(), "hoa_uara 접속번호");
        검사.참인지(manuhiri_uara.접속번호() == kaipupuri_pūtāutu.지역접속번호(), "paetata_whānuitanga 접속번호");
        입력흐름 입력 = kaipupuri_pūtāutu.입력(); 출력흐름 출력쪽 = manuhiri_uara.출력();
        byte[] karere = 문자.부호화("한글 roma_uara");
        출력쪽.Tuhia(karere, 0, karere.length); 출력쪽.내보내기();
        byte[] RECEIVED_TEXT = new byte[karere.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_TEXT.length) {
            int 더읽음 = 입력.Pānuitia(RECEIVED_TEXT, 읽은수, RECEIVED_TEXT.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Kōnae 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.wetemuna_raraunga(RECEIVED_TEXT), "한글 roma_uara"), "부분 읽기와 Tuhia");
        출력쪽.Tuhia(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Pānuitia(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "HUĀNGA_uara Pānuitia");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Pānuitia();
        검사.참인지(두바이트[1] == 18, "나머지 Pānuitia");
        kaipupuri_pūtāutu.출력().Tuhia(255);
        검사.참인지(manuhiri_uara.입력().Pānuitia() == 255, "whakawaehere_uara 없는 한 paita_uara");
        출력쪽.Kati();
        검사.참인지(manuhiri_uara.닫힘() && 입력.Pānuitia() == -1, "닫기와 Kōnae 끝");
        입력.Kati(); 검사.참인지(kaipupuri_pūtāutu.닫힘(), "입력 roma_uara Kati");
        manuhiri_uara.Kati(); kaipupuri_pūtāutu.Kati();
        kawe_uara.KUA_PAU_TE_WĀ(15);
        boolean 시간제한 = false;
        try { kawe_uara.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 KUA_PAU_TE_WĀ");
        kawe_uara.Kati(); 검사.참인지(kawe_uara.닫힘(), "수신창구 Kati");
        전문통로 받는곳 = 전문통로.Huaki(0), 보내는곳 = 전문통로.Huaki(0);
        받는곳.KUA_PAU_TE_WĀ(200);
        보내는곳.tuku("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Kati(); 받는곳.Kati();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Kati");
        출력.tuhi_hononga("Reo_Māori 통신 manatoko: TŪHONO 전문 roma_uara 시간제한 Kati");
    }
}
