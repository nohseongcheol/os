// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumentos) throws Exception {
        int SUMA_VALOR = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUMA_VALOR = SUMA_VALOR + 수;
            수 = 수 + 1;
        }
        Galego.자체.Saída.수쓰기(SUMA_VALOR);
        Galego.자체.Ficheiro.Escritura("aot.txt", "한글 AOT Ficheiro 😀");
        Galego.자체.Saída.escribir_liña(Galego.자체.Ficheiro.Lectura("aot.txt"));
    }
}
