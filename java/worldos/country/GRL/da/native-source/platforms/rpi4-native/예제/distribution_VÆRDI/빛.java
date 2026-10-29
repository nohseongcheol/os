// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumenter) throws Exception {
        int SUM_VÆRDI = 0;
        int tal = 1;
        while (tal <= 10) {
            SUM_VÆRDI = SUM_VÆRDI + tal;
            tal = tal + 1;
        }
        Dansk.eget.Udgang.skrive_tal(SUM_VÆRDI);
        Dansk.eget.Fil.Skrive("aot.txt", "한글 AOT Fil 😀");
        Dansk.eget.Udgang.skrive_linje(Dansk.eget.Fil.Læse("aot.txt"));
    }
}
