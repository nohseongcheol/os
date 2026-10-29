// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumenti) throws Exception {
        int SUM_VALUE = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_VALUE = SUM_VALUE + 수;
            수 = 수 + 1;
        }
        hrvatski.vlastiti.Izlaz.수쓰기(SUM_VALUE);
        hrvatski.vlastiti.Datoteka.Zapisuj("aot.txt", "한글 AOT Datoteka 😀");
        hrvatski.vlastiti.Izlaz.zapisivanje_red(hrvatski.vlastiti.Datoteka.Čitaj("aot.txt"));
    }
}
