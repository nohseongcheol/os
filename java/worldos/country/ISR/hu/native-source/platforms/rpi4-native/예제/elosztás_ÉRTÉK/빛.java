// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumentumok) throws Exception {
        int SUM_ÉRTÉK = 0;
        int szám = 1;
        while (szám <= 10) {
            SUM_ÉRTÉK = SUM_ÉRTÉK + szám;
            szám = szám + 1;
        }
        magyar.saját.Kimenet.ír_szám(SUM_ÉRTÉK);
        magyar.saját.Fájl.Írás("aot.txt", "한글 AOT Fájl 😀");
        magyar.saját.Kimenet.ír_sor(magyar.saját.Fájl.Olvasás("aot.txt"));
    }
}
