// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Standardausgabe des eigenständigen Kernels. UTF-16-Surrogatpaare werden über UART als UTF-8 gesendet. */
public final class Ausgabe {
    private Ausgabe() {}
    public static void schreiben(String Text) { System.out.print(Text); }
    public static void zeileSchreiben(String Text) { System.out.println(Text); }
    public static void nummerSchreiben(int Zahl) { System.out.println(Zahl); }
}
