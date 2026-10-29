// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int daw() {
        kiy_jariñoo_internet.biir("Hello from a separate Java ELF!\n");
        kiy_jariñoo_internet.biir(kiy_jariñoo_internet.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int àlluwa_tur = 0; àlluwa_tur < kiy_jariñoo_internet.인수개수(); àlluwa_tur++) {
            kiy_jariñoo_internet.biir("arg: "); kiy_jariñoo_internet.biir(kiy_jariñoo_internet.인수(àlluwa_tur)); kiy_jariñoo_internet.biir("\n");
        }
        return kiy_jariñoo_internet.실행권한() == 3 ? 0 : 1;
    }
}
