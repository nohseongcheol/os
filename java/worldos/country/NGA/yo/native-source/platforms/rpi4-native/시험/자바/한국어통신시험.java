// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 ojú_iye = 연결통신.수신열기(0);
        Ìsomọ́ àlejò_iye = 연결통신.Ṣi("127.0.0.1", ojú_iye.접속번호());
        Ìsomọ́ Oníǹkan_Àfidámọ̀ = ojú_iye.받기();
        àlejò_iye.대기시간(200); Oníǹkan_Àfidámọ̀.대기시간(200);
        검사.참인지(àlejò_iye.연결됨() && !àlejò_iye.닫힘(), "Darapọ̀ ipò_iye");
        검사.참인지(Oníǹkan_Àfidámọ̀.접속번호() == àlejò_iye.지역접속번호(), "ọ̀gbà_iye 접속번호");
        검사.참인지(àlejò_iye.접속번호() == Oníǹkan_Àfidámọ̀.지역접속번호(), "agbègbè_sàkání 접속번호");
        입력흐름 입력 = Oníǹkan_Àfidámọ̀.입력(); 출력흐름 출력쪽 = àlejò_iye.출력();
        byte[] iṣé = 문자.부호화("한글 Stream_iye");
        출력쪽.Kọ(iṣé, 0, iṣé.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[iṣé.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Kàá(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fáìlì 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.ṣàtúpalẹ̀_àrokò_détà(받은글), "한글 Stream_iye"), "부분 읽기와 Kọ");
        출력쪽.Kọ(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Kàá(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ÀRÉÈ_iye Kàá");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Kàá();
        검사.참인지(두바이트[1] == 18, "나머지 Kàá");
        Oníǹkan_Àfidámọ̀.출력().Kọ(255);
        검사.참인지(àlejò_iye.입력().Kàá() == 255, "pípàrokò_iye 없는 한 báìtì_iye");
        출력쪽.Ti();
        검사.참인지(àlejò_iye.닫힘() && 입력.Kàá() == -1, "닫기와 Fáìlì 끝");
        입력.Ti(); 검사.참인지(Oníǹkan_Àfidámọ̀.닫힘(), "입력 Stream_iye Ti");
        àlejò_iye.Ti(); Oníǹkan_Àfidámọ̀.Ti();
        ojú_iye.대기시간(15);
        boolean 시간제한 = false;
        try { ojú_iye.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        ojú_iye.Ti(); 검사.참인지(ojú_iye.닫힘(), "수신창구 Ti");
        전문통로 받는곳 = 전문통로.Ṣi(0), 보내는곳 = 전문통로.Ṣi(0);
        받는곳.대기시간(200);
        보내는곳.í_meèlì("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Ti(); 받는곳.Ti();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Ti");
        출력.kọ_ìlà("한국어 통신 ridájú: Darapọ̀ 전문 Stream_iye 시간제한 Ti");
    }
}
