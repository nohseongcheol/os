// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class PrimjerDatoteke {
    public static void Pokreni() throws hrvatski.vlastiti.U_I_iznimka {
        hrvatski.vlastiti.Datoteka.Zapisuj("java.txt", "JAVA Datoteka: hrvatski 😀\n");
        hrvatski.vlastiti.Izlaz.Zapisuj(hrvatski.vlastiti.Datoteka.Čitaj("java.txt"));
    }
}
