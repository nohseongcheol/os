// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ᎠᎢᏎᏍᏗ() {
        ᎬᏗᏍᎩ.ᎪᏪᎶᏗ("Hello from a separate Java ELF!\n");
        ᎬᏗᏍᎩ.ᎪᏪᎶᏗ(ᎬᏗᏍᎩ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < ᎬᏗᏍᎩ.인수개수(); ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            ᎬᏗᏍᎩ.ᎪᏪᎶᏗ("arg: "); ᎬᏗᏍᎩ.ᎪᏪᎶᏗ(ᎬᏗᏍᎩ.인수(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ)); ᎬᏗᏍᎩ.ᎪᏪᎶᏗ("\n");
        }
        return ᎬᏗᏍᎩ.실행권한() == 3 ? 0 : 1;
    }
}
