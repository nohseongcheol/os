// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Parametri) throws Exception {
        int SUM_VALUE = 0;
        int numurs = 1;
        while (numurs <= 10) {
            SUM_VALUE = SUM_VALUE + numurs;
            numurs = numurs + 1;
        }
        Latviešu.savs.Izvade.rakstīšana_numurs(SUM_VALUE);
        Latviešu.savs.Fails.Rakstīt("aot.txt", "한글 AOT Fails 😀");
        Latviešu.savs.Izvade.rakstīšana_līnija(Latviešu.savs.Fails.Lasīt("aot.txt"));
    }
}
