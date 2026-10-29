// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Tafiyar_da() {
        Mai_anfani_da_kwamfuta.Yi_Rubutu("Hello from a separate Java ELF!\n");
        Mai_anfani_da_kwamfuta.Yi_Rubutu(Mai_anfani_da_kwamfuta.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int Indes = 0; Indes < Mai_anfani_da_kwamfuta.인수개수(); Indes++) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("arg: "); Mai_anfani_da_kwamfuta.Yi_Rubutu(Mai_anfani_da_kwamfuta.인수(Indes)); Mai_anfani_da_kwamfuta.Yi_Rubutu("\n");
        }
        return Mai_anfani_da_kwamfuta.실행권한() == 3 ? 0 : 1;
    }
}
