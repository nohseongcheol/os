// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumente) throws Exception {
        int SUM_VALUE = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_VALUE = SUM_VALUE + 수;
            수 = 수 + 1;
        }
        Română.propriu.Rezultat.수쓰기(SUM_VALUE);
        Română.propriu.Fișier.Scriere("aot.txt", "한글 AOT Fișier 😀");
        Română.propriu.Rezultat.scriere_linie(Română.propriu.Fișier.Citire("aot.txt"));
    }
}
