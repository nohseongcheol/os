// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] argument) throws Svenska.eget.indata_utleverans_fel {
        Svenska.eget.utmatningsposition.skriva_rad("eget 컴파일러와 Svenska bibliotek");
        int tecken_ANTAL = Svenska.eget.문자.kodpunkt_ANTAL("한글😀");
        Svenska.eget.utmatningsposition.skriva_nummer(tecken_ANTAL);
        Svenska.eget.filnamn.Skriv("한글자료.txt", "eget kärna_värde 안에서 저장한 한글😀");
        Svenska.eget.utmatningsposition.skriva_rad(Svenska.eget.filnamn.Läs("한글자료.txt"));
    }
}
