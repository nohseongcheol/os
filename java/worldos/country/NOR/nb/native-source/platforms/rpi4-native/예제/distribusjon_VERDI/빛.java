// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumenter) throws Exception {
        int SUMMER_VERDI = 0;
        int nummer = 1;
        while (nummer <= 10) {
            SUMMER_VERDI = SUMMER_VERDI + nummer;
            nummer = nummer + 1;
        }
        norsk.eget.Utgang.skrive_nummer(SUMMER_VERDI);
        norsk.eget.Fil.Skriv("aot.txt", "한글 AOT Fil 😀");
        norsk.eget.Utgang.skrive_linje(norsk.eget.Fil.Les("aot.txt"));
    }
}
