// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int চালনা() {
        ব্যবহারকারী.লেখা("Hello from a separate Java ELF!\n");
        ব্যবহারকারী.লেখা(ব্যবহারকারী.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int সূচি = 0; সূচি < ব্যবহারকারী.인수개수(); সূচি++) {
            ব্যবহারকারী.লেখা("arg: "); ব্যবহারকারী.লেখা(ব্যবহারকারী.আর্গুমেন্ট_তালিকা(সূচি)); ব্যবহারকারী.লেখা("\n");
        }
        return ব্যবহারকারী.실행권한() == 3 ? 0 : 1;
    }
}
