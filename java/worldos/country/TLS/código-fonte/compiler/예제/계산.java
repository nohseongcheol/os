// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int total_VALOR(int 끝) {
        int resultado = 0;
        for (int ÍNDICE = 1; ÍNDICE <= 끝; ÍNDICE++) resultado += ÍNDICE;
        return resultado;
    }

    public static int iniciar() {
        int[] 값들 = new int[3];
        값들[0] = total_VALOR(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
