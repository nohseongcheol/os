// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.muunganisho;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_T_vighairi;

public class 네트워크예제 {
    public static void endesha() throws I_T_vighairi {
        // mwenyeji: python3 Zana/예제되돌림.py --tcp-port 9000 --udp-port 9001
        muunganisho UNGANISHA = muunganisho.unda("10.0.2.2", 문자.changanua_namba_kamili(실행인수.SMS(0)));
        try {
            UNGANISHA.대기시간(700);
            byte[] ujumbe = 문자.부호화("JAVA TCP sw\n");
            UNGANISHA.출력().andika(ujumbe);
            입력흐름 입력 = UNGANISHA.입력();
            for (int 수 = 0; 수 < 문자.바이트수(ujumbe); 수++) {
                검사.참인지(입력.읽기() == (ujumbe[수] & 255), "TCP jibu 불일치");
            }
        } finally { UNGANISHA.funga(); }
        전문통로 종단 = 전문통로.unda(0);
        try {
            종단.대기시간(700);
            종단.tuma("10.0.2.2", 문자.changanua_namba_kamili(실행인수.SMS(1)), "JAVA UDP sw");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP sw"), "UDP jibu 불일치");
        } finally { 종단.funga(); }
        출력.andika_laini("JAVA 네트워크 thibitisha: TCP UDP sw");
    }
}
