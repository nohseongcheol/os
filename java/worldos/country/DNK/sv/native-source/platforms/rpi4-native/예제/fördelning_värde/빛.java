// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argument) throws Exception {
        int SUM_värde = 0;
        int nummer = 1;
        while (nummer <= 10) {
            SUM_värde = SUM_värde + nummer;
            nummer = nummer + 1;
        }
        Svenska.eget.utmatningsposition.skriva_nummer(SUM_värde);
        Svenska.eget.filnamn.Skriv("aot.txt", "한글 AOT filnamn 😀");
        Svenska.eget.utmatningsposition.skriva_rad(Svenska.eget.filnamn.Läs("aot.txt"));
    }
}
