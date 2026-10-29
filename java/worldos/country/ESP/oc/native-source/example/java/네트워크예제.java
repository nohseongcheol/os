// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.연결통로;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.Sortida;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void Executar_2() throws 입출력예외 {
        // 호스트: python3 도구/예제되돌림.py --tcp-port 9000 --udp-port 9001
        연결통로 Se_connectar = 연결통로.Dobrir("10.0.2.2", 문자.정수읽기(실행인수.Tèxte(0)));
        try {
            Se_connectar.대기시간(700);
            byte[] 보낼글 = 문자.부호화("JAVA TCP oc\n");
            Se_connectar.Sortida().Escritura(보낼글);
            입력흐름 입력 = Se_connectar.입력();
            for (int 수 = 0; 수 < 문자.바이트수(보낼글); 수++) {
                검사.참인지(입력.Lectura() == (보낼글[수] & 255), "TCP 응답 불일치");
            }
        } finally { Se_connectar.Tampar(); }
        전문통로 종단 = 전문통로.Dobrir(0);
        try {
            종단.대기시간(700);
            종단.보내기("10.0.2.2", 문자.정수읽기(실행인수.Tèxte(1)), "JAVA UDP oc");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP oc"), "UDP 응답 불일치");
        } finally { 종단.Tampar(); }
        Sortida.줄쓰기("JAVA 네트워크 확인: TCP UDP oc");
    }
}
