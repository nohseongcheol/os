// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ක්_රියාත්මක_කරන්න_2() {
        පරිශීලක.ලිවීම("Hello from a separate Java ELF!\n");
        පරිශීලක.ලිවීම(පරිශීලක.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int සූචිය = 0; සූචිය < පරිශීලක.인수개수(); සූචිය++) {
            පරිශීලක.ලිවීම("arg: "); පරිශීලක.ලිවීම(පරිශීලක.විස්තාරක(සූචිය)); පරිශීලක.ලිවීම("\n");
        }
        return පරිශීලක.실행권한() == 3 ? 0 : 1;
    }
}
