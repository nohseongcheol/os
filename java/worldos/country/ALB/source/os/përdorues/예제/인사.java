// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Ekzekuto() {
        përdorues.Shkrimi("Hello from a separate Java ELF!\n");
        përdorues.Shkrimi(përdorues.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < përdorues.인수개수(); INDEX++) {
            përdorues.Shkrimi("arg: "); përdorues.Shkrimi(përdorues.Argumente(INDEX)); përdorues.Shkrimi("\n");
        }
        return përdorues.실행권한() == 3 ? 0 : 1;
    }
}
