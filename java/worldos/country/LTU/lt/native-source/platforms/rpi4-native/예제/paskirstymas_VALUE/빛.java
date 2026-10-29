// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumentai) throws Exception {
        int SUM_VALUE = 0;
        int numeris = 1;
        while (numeris <= 10) {
            SUM_VALUE = SUM_VALUE + numeris;
            numeris = numeris + 1;
        }
        Lietuvių.savas.Išvestis.rašymas_numeris(SUM_VALUE);
        Lietuvių.savas.Failas.Rašymas("aot.txt", "한글 AOT Failas 😀");
        Lietuvių.savas.Išvestis.rašymas_eilutė(Lietuvių.savas.Failas.Skaitymas("aot.txt"));
    }
}
