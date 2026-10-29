// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int SUMA_VALOR = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUMA_VALOR = SUMA_VALOR + 수;
            수 = 수 + 1;
        }
        Català.propi.Sortida.수쓰기(SUMA_VALOR);
        Català.propi.Fitxer.Escriptura("aot.txt", "한글 AOT Fitxer 😀");
        Català.propi.Sortida.escriure_línia(Català.propi.Fitxer.Lectura("aot.txt"));
    }
}
