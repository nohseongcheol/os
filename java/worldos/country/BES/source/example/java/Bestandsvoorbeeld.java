// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Bestandsvoorbeeld {
    public static void starten() throws Nederlands.Eigen.I_O_uitzondering {
        Nederlands.Eigen.bestand.Schrijven("java.txt", "JAVA bestand: Nederlands 😀\n");
        Nederlands.Eigen.tekstuitvoer.Schrijven(Nederlands.Eigen.bestand.Lezen("java.txt"));
    }
}
