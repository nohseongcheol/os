// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Gweithredu_2() {
        defnyddiwr.Ysgrifennu("Hello from a separate Java ELF!\n");
        defnyddiwr.Ysgrifennu(defnyddiwr.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < defnyddiwr.인수개수(); INDEX++) {
            defnyddiwr.Ysgrifennu("arg: "); defnyddiwr.Ysgrifennu(defnyddiwr.인수(INDEX)); defnyddiwr.Ysgrifennu("\n");
        }
        return defnyddiwr.실행권한() == 3 ? 0 : 1;
    }
}
