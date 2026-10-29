// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        ceangal aoigh_VALUE = 연결통신.fosgail("127.0.0.1", port_VALUE.접속번호());
        ceangal sealbhadair_aithnichear = port_VALUE.받기();
        aoigh_VALUE.TIMEOUT(200); sealbhadair_aithnichear.TIMEOUT(200);
        검사.참인지(aoigh_VALUE.연결됨() && !aoigh_VALUE.닫힘(), "CONNECT cor_VALUE");
        검사.참인지(sealbhadair_aithnichear.접속번호() == aoigh_VALUE.지역접속번호(), "seise_VALUE 접속번호");
        검사.참인지(aoigh_VALUE.접속번호() == sealbhadair_aithnichear.지역접속번호(), "ionadail_sgòp 접속번호");
        입력흐름 입력 = sealbhadair_aithnichear.입력(); 출력흐름 출력쪽 = aoigh_VALUE.출력();
        byte[] teachdaireachd = 문자.부호화("한글 sruth_VALUE");
        출력쪽.sgrìobh(teachdaireachd, 0, teachdaireachd.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[teachdaireachd.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.읽기(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 faidhle 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dì_chrioptaich_dàta(RECEIVED_SMS), "한글 sruth_VALUE"), "부분 읽기와 sgrìobh");
        출력쪽.sgrìobh(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        sealbhadair_aithnichear.출력().sgrìobh(255);
        검사.참인지(aoigh_VALUE.입력().읽기() == 255, "còdachadh_VALUE 없는 한 baidht_VALUE");
        출력쪽.dùin();
        검사.참인지(aoigh_VALUE.닫힘() && 입력.읽기() == -1, "닫기와 faidhle 끝");
        입력.dùin(); 검사.참인지(sealbhadair_aithnichear.닫힘(), "입력 sruth_VALUE dùin");
        aoigh_VALUE.dùin(); sealbhadair_aithnichear.dùin();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.dùin(); 검사.참인지(port_VALUE.닫힘(), "수신창구 dùin");
        전문통로 받는곳 = 전문통로.fosgail(0), 보내는곳 = 전문통로.fosgail(0);
        받는곳.TIMEOUT(200);
        보내는곳.cuir("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.dùin(); 받는곳.dùin();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 dùin");
        출력.sgrìobh_loidhne("한국어 통신 dearbh: CONNECT 전문 sruth_VALUE 시간제한 dùin");
    }
}
