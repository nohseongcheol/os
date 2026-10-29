// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 pọọt_valuu = 연결통신.수신열기(0);
        njikọ 손님 = 연결통신.Mepee("127.0.0.1", pọọt_valuu.접속번호());
        njikọ nwe_ihe_nkọwapụta = pọọt_valuu.받기();
        손님.대기시간(200); nwe_ihe_nkọwapụta.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "Banye ọnọdụ_valuu");
        검사.참인지(nwe_ihe_nkọwapụta.접속번호() == 손님.지역접속번호(), "ibè_valuu 접속번호");
        검사.참인지(손님.접속번호() == nwe_ihe_nkọwapụta.지역접속번호(), "otù_ebe_ọgba 접속번호");
        입력흐름 입력 = nwe_ihe_nkọwapụta.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] ozi = 문자.부호화("한글 agịrị_valuu");
        출력쪽.Chekwaa_ozi(ozi, 0, ozi.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[ozi.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Wepụta_ọzi(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Faịlụ 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.tụghee_edenzizo_datà(받은글), "한글 agịrị_valuu"), "부분 읽기와 Chekwaa_ozi");
        출력쪽.Chekwaa_ozi(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Wepụta_ọzi(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MKPOKỌTA_valuu Wepụta_ọzi");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Wepụta_ọzi();
        검사.참인지(두바이트[1] == 18, "나머지 Wepụta_ọzi");
        nwe_ihe_nkọwapụta.출력().Chekwaa_ozi(255);
        검사.참인지(손님.입력().Wepụta_ọzi() == 255, "ntinye_koòdù_valuu 없는 한 baịtị_valuu");
        출력쪽.Mechie();
        검사.참인지(손님.닫힘() && 입력.Wepụta_ọzi() == -1, "닫기와 Faịlụ 끝");
        입력.Mechie(); 검사.참인지(nwe_ihe_nkọwapụta.닫힘(), "입력 agịrị_valuu Mechie");
        손님.Mechie(); nwe_ihe_nkọwapụta.Mechie();
        pọọt_valuu.대기시간(15);
        boolean 시간제한 = false;
        try { pọọt_valuu.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        pọọt_valuu.Mechie(); 검사.참인지(pọọt_valuu.닫힘(), "수신창구 Mechie");
        전문통로 받는곳 = 전문통로.Mepee(0), 보내는곳 = 전문통로.Mepee(0);
        받는곳.대기시간(200);
        보내는곳.zìga("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Mechie(); 받는곳.Mechie();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Mechie");
        출력.dee_ahịrī("한국어 통신 nkwàdo_eziokwū: Banye 전문 agịrị_valuu 시간제한 Mechie");
    }
}
