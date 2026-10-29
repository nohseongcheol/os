// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int నడుపుము() {
        వినియోగదారు.వ్రాయుము("Hello from a separate Java ELF!\n");
        వినియోగదారు.వ్రాయుము(వినియోగదారు.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int సూచీ = 0; సూచీ < వినియోగదారు.인수개수(); సూచీ++) {
            వినియోగదారు.వ్రాయుము("arg: "); వినియోగదారు.వ్రాయుము(వినియోగదారు.인수(సూచీ)); వినియోగదారు.వ్రాయుము("\n");
        }
        return వినియోగదారు.실행권한() == 3 ? 0 : 1;
    }
}
