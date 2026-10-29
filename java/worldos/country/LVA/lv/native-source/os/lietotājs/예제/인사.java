// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Palaist() {
        lietotājs.Rakstīt("Hello from a separate Java ELF!\n");
        lietotājs.Rakstīt(lietotājs.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < lietotājs.인수개수(); INDEX++) {
            lietotājs.Rakstīt("arg: "); lietotājs.Rakstīt(lietotājs.Parametri(INDEX)); lietotājs.Rakstīt("\n");
        }
        return lietotājs.실행권한() == 3 ? 0 : 1;
    }
}
