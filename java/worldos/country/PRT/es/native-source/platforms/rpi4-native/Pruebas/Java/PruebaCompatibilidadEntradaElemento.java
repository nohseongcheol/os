// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** No elegir un método auxiliar privado como entrada de código que ya tenga un main estándar. */
public class PruebaCompatibilidadEntradaElemento {
    private static void ponerEnMarcha() { System.out.println("valorAuxiliar Función invocar"); }
    public static void main(String[] argumentos) {
        ponerEnMarcha();
        System.out.println("표준 puntoEntradaElemento retenerValor");
    }
}
