// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] argumentit) throws suomi.oma.I_O_poikkeus {
        suomi.oma.tulostuspaikka.kirjoitus_rivi("oma 컴파일러와 suomi kirjasto");
        int merkki_LASKE = suomi.oma.문자.koodipiste_LASKE("한글😀");
        suomi.oma.tulostuspaikka.kirjoitus_numero(merkki_LASKE);
        suomi.oma.tiedoston_nimi.Kirjoitus("한글자료.txt", "oma ydin_ARVO 안에서 저장한 한글😀");
        suomi.oma.tulostuspaikka.kirjoitus_rivi(suomi.oma.tiedoston_nimi.Luku("한글자료.txt"));
    }
}
