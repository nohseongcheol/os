// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ແລ່ນ() {
        ຜູ້ໃຊ້.ຂຽນ("Hello from a separate Java ELF!\n");
        ຜູ້ໃຊ້.ຂຽນ(ຜູ້ໃຊ້.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ດັດຊະນີ = 0; ດັດຊະນີ < ຜູ້ໃຊ້.인수개수(); ດັດຊະນີ++) {
            ຜູ້ໃຊ້.ຂຽນ("arg: "); ຜູ້ໃຊ້.ຂຽນ(ຜູ້ໃຊ້.인수(ດັດຊະນີ)); ຜູ້ໃຊ້.ຂຽນ("\n");
        }
        return ຜູ້ໃຊ້.실행권한() == 3 ? 0 : 1;
    }
}
