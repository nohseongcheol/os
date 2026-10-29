// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Böyüklük/홀수 uzunluq_VALUE 데이터그램으로 faktiki_verilənlər RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Şəbəkə_Loop {
    public static int İcra_Et() {
        if (istifadəçi.인수개수() != 1) { istifadəçi.Yazma("Usage: run stress PORT\n"); return 2; }
        String Mətn = istifadəçi.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Mətn.length(); INDEX++) {
            if (Mətn.charAt(INDEX) < '0' || Mətn.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Mətn.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int tutacaq_VALUE = istifadəçi.açmaq_Şəbəkə(0);
        if (tutacaq_VALUE < 0) return 3;
        int[] verilənlər = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int uzunluq_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) verilənlər[INDEX] = (INDEX + 회차) & 255;
            if (istifadəçi.göndərmək_verilənlər(tutacaq_VALUE, 0x0a000202, port_VALUE, verilənlər, uzunluq_VALUE) != uzunluq_VALUE) return 4;
            if (istifadəçi.자료받기(tutacaq_VALUE, verilənlər, 300) != uzunluq_VALUE) return 5;
            for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) if (verilənlər[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        istifadəçi.bağlamaq_Şəbəkə(tutacaq_VALUE);
        istifadəçi.Yazma("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
