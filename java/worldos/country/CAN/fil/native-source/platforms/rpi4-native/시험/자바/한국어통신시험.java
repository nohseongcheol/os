// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_pagbubukod {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        koneksyon bisita_VALUE = 연결통신.buksan("127.0.0.1", port_VALUE.numero_ng_port());
        koneksyon may_ari_tagakilala = port_VALUE.받기();
        bisita_VALUE.TIMEOUT(200); may_ari_tagakilala.TIMEOUT(200);
        검사.참인지(bisita_VALUE.연결됨() && !bisita_VALUE.닫힘(), "CONNECT katayuan_VALUE");
        검사.참인지(may_ari_tagakilala.numero_ng_port() == bisita_VALUE.lokal_numero_ng_port(), "peer_VALUE numero_ng_port");
        검사.참인지(bisita_VALUE.numero_ng_port() == may_ari_tagakilala.lokal_numero_ng_port(), "lokal_lawak numero_ng_port");
        입력흐름 입력 = may_ari_tagakilala.입력(); 출력흐름 출력쪽 = bisita_VALUE.출력();
        byte[] email_8c783e64 = 문자.부호화("한글 Stream_VALUE");
        출력쪽.sumulat(email_8c783e64, 0, email_8c783e64.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[email_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.읽기(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 file 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.i_decrypt_data(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 sumulat");
        출력쪽.sumulat(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        may_ari_tagakilala.출력().sumulat(255);
        검사.참인지(bisita_VALUE.입력().읽기() == 255, "pag_encode_VALUE 없는 한 byte_VALUE");
        출력쪽.isara();
        검사.참인지(bisita_VALUE.닫힘() && 입력.읽기() == -1, "닫기와 file 끝");
        입력.isara(); 검사.참인지(may_ari_tagakilala.닫힘(), "입력 Stream_VALUE isara");
        bisita_VALUE.isara(); may_ari_tagakilala.isara();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (maghintay_TIMEOUT_pagbubukod 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.isara(); 검사.참인지(port_VALUE.닫힘(), "수신창구 isara");
        전문통로 받는곳 = 전문통로.buksan(0), 보내는곳 = 전문통로.buksan(0);
        받는곳.TIMEOUT(200);
        보내는곳.i_email("127.0.0.1", 받는곳.numero_ng_port(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.isara(); 받는곳.isara();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 isara");
        출력.sumulat_linya("한국어 통신 tiyakin_kumpirmahin: CONNECT 전문 Stream_VALUE 시간제한 isara");
    }
}
