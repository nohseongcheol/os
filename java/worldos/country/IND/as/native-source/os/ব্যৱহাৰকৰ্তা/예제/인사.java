// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int সঞ্চালন() {
        ব্যৱহাৰকৰ্তা.লিখা("Hello from a separate Java ELF!\n");
        ব্যৱহাৰকৰ্তা.লিখা(ব্যৱহাৰকৰ্তা.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ইনডেক্স = 0; ইনডেক্স < ব্যৱহাৰকৰ্তা.인수개수(); ইনডেক্স++) {
            ব্যৱহাৰকৰ্তা.লিখা("arg: "); ব্যৱহাৰকৰ্তা.লিখা(ব্যৱহাৰকৰ্তা.인수(ইনডেক্স)); ব্যৱহাৰকৰ্তা.লিখা("\n");
        }
        return ব্যৱহাৰকৰ্তা.실행권한() == 3 ? 0 : 1;
    }
}
