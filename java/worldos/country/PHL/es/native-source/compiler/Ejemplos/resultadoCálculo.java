// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class resultadoCálculo {
    static int valorTotal(int terminación) {
        int resultado = 0;
        for (int número = 1; número <= terminación; número++) resultado += número;
        return resultado;
    }

    public static int ponerEnMarcha() {
        int[] valores = new int[3];
        valores[0] = valorTotal(10);
        valores[1] = -7 / 3;
        valores[2] = "한글".length();
        return valores[0] == 55 && valores[1] == -2 && valores[2] == 2 ? 0 : 1;
    }
}
