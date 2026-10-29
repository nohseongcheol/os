// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class pruebaExcepciones {
    static int valoresDividir(int n) { return 8 / n; }
    static int valorFinalizar() { try { return valoresDividir(0); } finally { System.out.println("valorFinalizar"); } }
    public static void main(String[] a) {
        try { valorFinalizar(); } catch (ArithmeticException e) { System.out.println("valorAritmética excepción"); }
        try { throw new IllegalArgumentException("잘못된 argumentos 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 referencia"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("valorArreglo recortar"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("EnteroValor recortar"); }
        try { Object x = "texto"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("valorTipo convertirValor"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("Archivo excepción"); }
        System.out.println("excepción entradaElementoValorProceso esTerminado");
    }
}
