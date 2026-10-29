// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 үлчәмен_үзгәртү/홀수 озынлык_VALUE 데이터그램으로 фактик_мәгълүмат RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Челтәр_Loop {
    public static int эшләтү() {
        if (кулланучы.인수개수() != 1) { кулланучы.язу("Usage: run stress PORT\n"); return 2; }
        String Mäten = кулланучы.인수(0);
        int порт_VALUE = 0;
        for (int INDEX = 0; INDEX < Mäten.length(); INDEX++) {
            if (Mäten.charAt(INDEX) < '0' || Mäten.charAt(INDEX) > '9' || порт_VALUE > 6553) return 2;
            порт_VALUE = порт_VALUE * 10 + Mäten.charAt(INDEX) - '0';
        }
        if (порт_VALUE < 1 || порт_VALUE > 65535) return 2;
        int дескриптор_VALUE = кулланучы.ачу_Челтәр(0);
        if (дескриптор_VALUE < 0) return 3;
        int[] мәгълүмат = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int озынлык_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX++) мәгълүмат[INDEX] = (INDEX + 회차) & 255;
            if (кулланучы.җибәрү_мәгълүмат(дескриптор_VALUE, 0x0a000202, порт_VALUE, мәгълүмат, озынлык_VALUE) != озынлык_VALUE) return 4;
            if (кулланучы.자료받기(дескриптор_VALUE, мәгълүмат, 300) != озынлык_VALUE) return 5;
            for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX++) if (мәгълүмат[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        кулланучы.чик_Челтәр(дескриптор_VALUE);
        кулланучы.язу("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
