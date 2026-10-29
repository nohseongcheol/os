// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.qoşulma;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.giriş_çıxış_istisna;

public class 네트워크예제 {
    public static void İcra_Et() throws giriş_çıxış_istisna {
        // host: python3 Alətlər/예제되돌림.py --tcp-port 9000 --udp-port 9001
        qoşulma Bağlan = qoşulma.Aç("10.0.2.2", 문자.parselləmək_tam_ədəd(실행인수.Mətn(0)));
        try {
            Bağlan.FASİLƏ(700);
            byte[] mesaj = 문자.부호화("JAVA TCP Azerbaijani\n");
            Bağlan.출력().Yazma(mesaj);
            입력흐름 입력 = Bağlan.입력();
            for (int 수 = 0; 수 < 문자.bayt_COUNT(mesaj); 수++) {
                검사.참인지(입력.Oxuma() == (mesaj[수] & 255), "TCP cavab 불일치");
            }
        } finally { Bağlan.Bağla(); }
        전문통로 종단 = 전문통로.Aç(0);
        try {
            종단.FASİLƏ(700);
            종단.göndərmək("10.0.2.2", 문자.parselləmək_tam_ədəd(실행인수.Mətn(1)), "JAVA UDP Azerbaijani");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP Azerbaijani"), "UDP cavab 불일치");
        } finally { 종단.Bağla(); }
        출력.yazmaq_xətt("JAVA 네트워크 yoxlamaq: TCP UDP Azerbaijani");
    }
}
