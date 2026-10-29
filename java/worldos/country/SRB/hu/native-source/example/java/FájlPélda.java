// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class FájlPélda {
    public static void Futtatás() throws magyar.saját.I_O_kivétel {
        magyar.saját.Fájl.Írás("java.txt", "JAVA Fájl: hu 😀\n");
        magyar.saját.Kimenet.Írás(magyar.saját.Fájl.Olvasás("java.txt"));
    }
}
