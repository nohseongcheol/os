// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumendid) throws Exception {
        int SUM_VALUE = 0;
        int number = 1;
        while (number <= 10) {
            SUM_VALUE = SUM_VALUE + number;
            number = number + 1;
        }
        Eesti.oma.Väljund.kirjutamine_number(SUM_VALUE);
        Eesti.oma.Fail.Kirjutamine("aot.txt", "한글 AOT Fail 😀");
        Eesti.oma.Väljund.kirjutamine_liin(Eesti.oma.Fail.Lugemine("aot.txt"));
    }
}
