// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.ᎫᏓᎸᎢ;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void ᎠᎢᏎᏍᏗ() throws 입출력예외 {
        // ᎠᏁᏢᏍᎩ: python3 도구/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ᎫᏓᎸᎢ ᎫᏓᎳ = ᎫᏓᎸᎢ.ᎯᏍᏚᎢ("10.0.2.2", 문자.정수읽기(실행인수.ᎠᎪᎵᏰᏗ(0)));
        try {
            ᎫᏓᎳ.대기시간(700);
            byte[] ᎠᎪᎵᏰᏗ_8c783e64 = 문자.부호화("JAVA TCP chr\n");
            ᎫᏓᎳ.출력().ᎪᏪᎶᏗ(ᎠᎪᎵᏰᏗ_8c783e64);
            입력흐름 입력 = ᎫᏓᎳ.입력();
            for (int 수 = 0; 수 < 문자.바이트수(ᎠᎪᎵᏰᏗ_8c783e64); 수++) {
                검사.참인지(입력.읽기() == (ᎠᎪᎵᏰᏗ_8c783e64[수] & 255), "TCP 응답 불일치");
            }
        } finally { ᎫᏓᎳ.ᎯᏍᏚᎲᎦ(); }
        전문통로 종단 = 전문통로.ᎯᏍᏚᎢ(0);
        try {
            종단.대기시간(700);
            종단.ᏫᎦᏅᏗ("10.0.2.2", 문자.정수읽기(실행인수.ᎠᎪᎵᏰᏗ(1)), "JAVA UDP chr");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP chr"), "UDP 응답 불일치");
        } finally { 종단.ᎯᏍᏚᎲᎦ(); }
        출력.ᎪᏪᎶᏗ_ᏚᏓᏅᏅᎢ("JAVA 네트워크 ᎰᎯᏳᏓ: TCP UDP chr");
    }
}
