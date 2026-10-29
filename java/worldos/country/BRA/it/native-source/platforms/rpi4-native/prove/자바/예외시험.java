// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("aritmetico_VALORE eccezione"); }
        try { throw new IllegalArgumentException("잘못된 argomenti 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 fonti"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("array_VALORE ritagliare"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("intero ritagliare"); }
        try { Object x = "testo"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("TIPO_VALORE CONVERTI_VALORE"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("file eccezione"); }
        System.out.println("eccezione Processi_VALORE_voce 완료");
    }
}
