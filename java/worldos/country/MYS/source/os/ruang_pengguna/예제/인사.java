// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Jalan() {
        ruang_pengguna.Tulis("Hello from a separate Java ELF!\n");
        ruang_pengguna.Tulis(ruang_pengguna.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < ruang_pengguna.인수개수(); INDEX++) {
            ruang_pengguna.Tulis("arg: "); ruang_pengguna.Tulis(ruang_pengguna.인수(INDEX)); ruang_pengguna.Tulis("\n");
        }
        return ruang_pengguna.실행권한() == 3 ? 0 : 1;
    }
}
