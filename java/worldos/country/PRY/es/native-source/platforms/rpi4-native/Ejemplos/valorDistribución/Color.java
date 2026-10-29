// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Color {
    public static void main(String[] argumentos) throws Exception {
        int valorTotalSuma = 0;
        int númeroValor = 1;
        while (númeroValor <= 10) {
            valorTotalSuma = valorTotalSuma + númeroValor;
            númeroValor = númeroValor + 1;
        }
        español.propio.Salida.escribirNúmero(valorTotalSuma);
        español.propio.Archivo.escribir("aot.txt", "한글 AOT Archivo 😀");
        español.propio.Salida.escribirLínea(español.propio.Archivo.leer("aot.txt"));
    }
}
