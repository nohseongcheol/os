// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int totale_VALORE(int 끝) {
        int risultato = 0;
        for (int INDICE = 1; INDICE <= 끝; INDICE++) risultato += INDICE;
        return risultato;
    }

    public static int avvia() {
        int[] 값들 = new int[3];
        값들[0] = totale_VALORE(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
