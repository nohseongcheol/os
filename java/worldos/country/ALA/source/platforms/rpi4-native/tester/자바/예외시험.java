// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("산술 fel_31f743d2"); }
        try { throw new IllegalArgumentException("잘못된 argument 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 referens"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("MATRIS_värde klipp"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("heltal klipp"); }
        try { Object x = "text"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("Typ_värde KONVERTERA_värde"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("filnamn fel_31f743d2"); }
        System.out.println("fel_31f743d2 Process_värde_post 완료");
    }
}
