// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Gruß {
    static int werteHinzufügen(int ersterOrdnungszahl, int zweiterOrdnungszahl) { return ersterOrdnungszahl + zweiterOrdnungszahl; }
    public static void main(String[] argumente) {
        int gesamtwertWert = werteHinzufügen(20, 22);
        System.out.println("안녕하세요 · gesamtwertWert=" + gesamtwertWert);
    }
}
