// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ચલાવો_2() {
        ઉપયોગકર્તા.લખો("Hello from a separate Java ELF!\n");
        ઉપયોગકર્તા.લખો(ઉપયોગકર્તા.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int અનુક્રમણિકા = 0; અનુક્રમણિકા < ઉપયોગકર્તા.인수개수(); અનુક્રમણિકા++) {
            ઉપયોગકર્તા.લખો("arg: "); ઉપયોગકર્તા.લખો(ઉપયોગકર્તા.દલીલો(અનુક્રમણિકા)); ઉપયોગકર્તા.લખો("\n");
        }
        return ઉપયોગકર્તા.실행권한() == 3 ? 0 : 1;
    }
}
