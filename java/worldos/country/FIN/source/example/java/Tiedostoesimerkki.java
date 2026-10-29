// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Tiedostoesimerkki {
    public static void Suorita_2() throws suomi.oma.I_O_poikkeus {
        suomi.oma.tiedoston_nimi.Kirjoitus("java.txt", "JAVA tiedoston_nimi: suomi 😀\n");
        suomi.oma.tulostuspaikka.Kirjoitus(suomi.oma.tiedoston_nimi.Luku("java.txt"));
    }
}
