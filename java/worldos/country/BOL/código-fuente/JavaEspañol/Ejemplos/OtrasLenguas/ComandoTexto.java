// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.Java.Caracteres;

/** Pequeña entrada Java cuyos resultados pueden leer otros lenguajes desde la salida estándar. */
public final class ComandoTexto {
    public static void main(String[] argumentos) {
        if (argumentos.length != 1) {
            System.err.println("사용법: ComandoTexto Cadena");
            System.exit(2);
        }
        System.out.println(Caracteres.númeroElementosPuntoCódigo(argumentos[0]));
    }
}
