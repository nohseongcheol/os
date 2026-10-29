// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumenti) throws hrvatski.vlastiti.U_I_iznimka {
        hrvatski.vlastiti.Izlaz.zapisivanje_red("vlastiti 컴파일러와 hrvatski biblioteka");
        int znak_COUNT = hrvatski.vlastiti.문자.točka_koda_COUNT("한글😀");
        hrvatski.vlastiti.Izlaz.수쓰기(znak_COUNT);
        hrvatski.vlastiti.Datoteka.Zapisuj("한글자료.txt", "vlastiti jezgra_sustava_VALUE 안에서 저장한 한글😀");
        hrvatski.vlastiti.Izlaz.zapisivanje_red(hrvatski.vlastiti.Datoteka.Čitaj("한글자료.txt"));
    }
}
