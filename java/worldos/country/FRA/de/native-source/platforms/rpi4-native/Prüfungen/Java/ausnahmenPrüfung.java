// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ausnahmenPrüfung {
    static int teilenWerte(int n) { return 8 / n; }
    static int abschließenWert() { try { return teilenWerte(0); } finally { System.out.println("abschließenWert"); } }
    public static void main(String[] a) {
        try { abschließenWert(); } catch (ArithmeticException e) { System.out.println("arithmetikWert ausnahme"); }
        try { throw new IllegalArgumentException("잘못된 argumente 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 verweis"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("datenfeldWert beschneiden"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("Ganzzahl beschneiden"); }
        try { Object x = "Text"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("typWert wertUmwandeln"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("Datei ausnahme"); }
        System.out.println("ausnahme prozessWertEintrag istFertig");
    }
}
