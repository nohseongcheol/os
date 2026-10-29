// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumentumok) throws magyar.saját.I_O_kivétel {
        magyar.saját.Kimenet.ír_sor("saját 컴파일러와 magyar kódtár");
        int karakter_DARAB = magyar.saját.문자.kódpont_DARAB("한글😀");
        magyar.saját.Kimenet.ír_szám(karakter_DARAB);
        magyar.saját.Fájl.Írás("한글자료.txt", "saját kernel_ÉRTÉK 안에서 저장한 한글😀");
        magyar.saját.Kimenet.ír_sor(magyar.saját.Fájl.Olvasás("한글자료.txt"));
    }
}
