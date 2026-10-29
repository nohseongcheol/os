// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class fuenteHangul {
    public static void main(String[] argumentos) throws español.propio.ExcepciónSalidaEntrada {
        español.propio.Salida.escribirLínea("propio 컴파일러와 español biblioteca");
        int númeroElementosCarácter = español.propio.Caracteres.númeroElementosPuntoCódigo("한글😀");
        español.propio.Salida.escribirNúmero(númeroElementosCarácter);
        español.propio.Archivo.escribir("한글자료.txt", "propio valorNúcleo 안에서 저장한 한글😀");
        español.propio.Salida.escribirLínea(español.propio.Archivo.leer("한글자료.txt"));
    }
}
