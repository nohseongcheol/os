// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Выканаць() {
        карыстальнік.Запіс("Hello from a separate Java ELF!\n");
        карыстальнік.Запіс(карыстальнік.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int індэкс = 0; індэкс < карыстальнік.인수개수(); індэкс++) {
            карыстальнік.Запіс("arg: "); карыстальнік.Запіс(карыстальнік.인수(індэкс)); карыстальнік.Запіс("\n");
        }
        return карыстальнік.실행권한() == 3 ? 0 : 1;
    }
}
