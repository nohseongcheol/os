// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class testExceptions {
    static int valeursDiviser(int n) { return 8 / n; }
    static int valeurFinaliser() { try { return valeursDiviser(0); } finally { System.out.println("valeurFinaliser"); } }
    public static void main(String[] a) {
        try { valeurFinaliser(); } catch (ArithmeticException e) { System.out.println("valeurArithmétique exception"); }
        try { throw new IllegalArgumentException("잘못된 arguments 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 référence"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("valeurTableau rogner"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("Entier rogner"); }
        try { Object x = "texte"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("valeurType convertirValeur"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("Fichier exception"); }
        System.out.println("exception entréeÉlémentValeurProcessus estTerminé");
    }
}
