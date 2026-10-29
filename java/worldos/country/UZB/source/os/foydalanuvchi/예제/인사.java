// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Bajarish() {
        foydalanuvchi.Yozish("Hello from a separate Java ELF!\n");
        foydalanuvchi.Yozish(foydalanuvchi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < foydalanuvchi.인수개수(); INDEX++) {
            foydalanuvchi.Yozish("arg: "); foydalanuvchi.Yozish(foydalanuvchi.인수(INDEX)); foydalanuvchi.Yozish("\n");
        }
        return foydalanuvchi.실행권한() == 3 ? 0 : 1;
    }
}
