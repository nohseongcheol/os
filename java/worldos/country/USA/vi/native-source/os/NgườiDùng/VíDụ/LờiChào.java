// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class LờiChào {
    public static int chạy() {
        NgườiDùng.ghi("Hello from a separate Java ELF!\n");
        NgườiDùng.ghi(NgườiDùng.quyềnViệcThựcThi() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int sốHiệu = 0; sốHiệu < NgườiDùng.sốLượngCácĐốiSố(); sốHiệu++) {
            NgườiDùng.ghi("arg: "); NgườiDùng.ghi(NgườiDùng.cácĐốiSố(sốHiệu)); NgườiDùng.ghi("\n");
        }
        return NgườiDùng.quyềnViệcThựcThi() == 3 ? 0 : 1;
    }
}
