// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ଚଳାନ୍ତୁ() {
        ଉପଭୋକ୍ତା.ଲେଖନ୍ତୁ("Hello from a separate Java ELF!\n");
        ଉପଭୋକ୍ତା.ଲେଖନ୍ତୁ(ଉପଭୋକ୍ତା.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ଅନୁକ୍ରମଣିକା = 0; ଅନୁକ୍ରମଣିକା < ଉପଭୋକ୍ତା.인수개수(); ଅନୁକ୍ରମଣିକା++) {
            ଉପଭୋକ୍ତା.ଲେଖନ୍ତୁ("arg: "); ଉପଭୋକ୍ତା.ଲେଖନ୍ତୁ(ଉପଭୋକ୍ତା.인수(ଅନୁକ୍ରମଣିକା)); ଉପଭୋକ୍ତା.ଲେଖନ୍ତୁ("\n");
        }
        return ଉପଭୋକ୍ତା.실행권한() == 3 ? 0 : 1;
    }
}
