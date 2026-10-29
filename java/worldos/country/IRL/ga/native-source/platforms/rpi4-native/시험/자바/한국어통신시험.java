// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argóintí) throws I_O_eisceacht {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        nasc aoi_VALUE = 연결통신.Oscail("127.0.0.1", port_VALUE.uimhir_phoirt());
        nasc úinéir_aitheantóir = port_VALUE.받기();
        aoi_VALUE.TIMEOUT(200); úinéir_aitheantóir.TIMEOUT(200);
        검사.참인지(aoi_VALUE.연결됨() && !aoi_VALUE.닫힘(), "Nasc staid_VALUE");
        검사.참인지(úinéir_aitheantóir.uimhir_phoirt() == aoi_VALUE.logánta_uimhir_phoirt(), "piara_VALUE uimhir_phoirt");
        검사.참인지(aoi_VALUE.uimhir_phoirt() == úinéir_aitheantóir.logánta_uimhir_phoirt(), "logánta_scóip uimhir_phoirt");
        입력흐름 입력 = úinéir_aitheantóir.입력(); 출력흐름 출력쪽 = aoi_VALUE.Aschur();
        byte[] teachtaireacht = 문자.부호화("한글 sruth_VALUE");
        출력쪽.Scríobh(teachtaireacht, 0, teachtaireacht.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[teachtaireacht.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Léigh(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Comhad 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.díchriptigh_sonraí(RECEIVED_SMS), "한글 sruth_VALUE"), "부분 읽기와 Scríobh");
        출력쪽.Scríobh(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Léigh(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Léigh");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Léigh();
        검사.참인지(두바이트[1] == 18, "나머지 Léigh");
        úinéir_aitheantóir.Aschur().Scríobh(255);
        검사.참인지(aoi_VALUE.입력().Léigh() == 255, "ionchódú_VALUE 없는 한 beart_VALUE");
        출력쪽.Dún();
        검사.참인지(aoi_VALUE.닫힘() && 입력.Léigh() == -1, "닫기와 Comhad 끝");
        입력.Dún(); 검사.참인지(úinéir_aitheantóir.닫힘(), "입력 sruth_VALUE Dún");
        aoi_VALUE.Dún(); úinéir_aitheantóir.Dún();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.Dún(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Dún");
        전문통로 받는곳 = 전문통로.Oscail(0), 보내는곳 = 전문통로.Oscail(0);
        받는곳.TIMEOUT(200);
        보내는곳.seol("127.0.0.1", 받는곳.uimhir_phoirt(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Dún(); 받는곳.Dún();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Dún");
        Aschur.scríobh_líne("Gaeilge 통신 fíoraigh: Nasc 전문 sruth_VALUE 시간제한 Dún");
    }
}
