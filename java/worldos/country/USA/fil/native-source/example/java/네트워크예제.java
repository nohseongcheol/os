// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.koneksyon;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_O_pagbubukod;

public class 네트워크예제 {
    public static void run() throws I_O_pagbubukod {
        // host: python3 Mga_Tool/예제되돌림.py --tcp-port 9000 --udp-port 9001
        koneksyon CONNECT = koneksyon.buksan("10.0.2.2", 문자.mag_parse_integer_buong_numero(실행인수.SMS(0)));
        try {
            CONNECT.TIMEOUT(700);
            byte[] email_8c783e64 = 문자.부호화("JAVA TCP fil\n");
            CONNECT.출력().sumulat(email_8c783e64);
            입력흐름 입력 = CONNECT.입력();
            for (int 수 = 0; 수 < 문자.byte_COUNT(email_8c783e64); 수++) {
                검사.참인지(입력.읽기() == (email_8c783e64[수] & 255), "TCP tumugon 불일치");
            }
        } finally { CONNECT.isara(); }
        전문통로 종단 = 전문통로.buksan(0);
        try {
            종단.TIMEOUT(700);
            종단.i_email("10.0.2.2", 문자.mag_parse_integer_buong_numero(실행인수.SMS(1)), "JAVA UDP fil");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP fil"), "UDP tumugon 불일치");
        } finally { 종단.isara(); }
        출력.sumulat_linya("JAVA 네트워크 tiyakin_kumpirmahin: TCP UDP fil");
    }
}
