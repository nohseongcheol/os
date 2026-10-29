// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int നടപ്പിലാക്കുക() {
        ഉപയോക്താവ്.എഴുത്തു്("Hello from a separate Java ELF!\n");
        ഉപയോക്താവ്.എഴുത്തു്(ഉപയോക്താവ്.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int സൂചിക = 0; സൂചിക < ഉപയോക്താവ്.인수개수(); സൂചിക++) {
            ഉപയോക്താവ്.എഴുത്തു്("arg: "); ഉപയോക്താവ്.എഴുത്തു്(ഉപയോക്താവ്.인수(സൂചിക)); ഉപയോക്താവ്.എഴുത്തു്("\n");
        }
        return ഉപയോക്താവ്.실행권한() == 3 ? 0 : 1;
    }
}
