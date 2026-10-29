// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int تشغيل() {
        فضاء_المستخدم.كتابة("Hello from a separate Java ELF!\n");
        فضاء_المستخدم.كتابة(فضاء_المستخدم.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int فهرس = 0; فهرس < فضاء_المستخدم.인수개수(); فهرس++) {
            فضاء_المستخدم.كتابة("arg: "); فضاء_المستخدم.كتابة(فضاء_المستخدم.وسائط(فهرس)); فضاء_المستخدم.كتابة("\n");
        }
        return فضاء_المستخدم.실행권한() == 3 ? 0 : 1;
    }
}
