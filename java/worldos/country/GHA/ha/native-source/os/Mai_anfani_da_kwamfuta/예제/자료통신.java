// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int lamba_Daraja(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int 결과 = 0;
        for (int Indes = 0; Indes < SMS.length(); Indes++) {
            int Daraja = SMS.charAt(Indes) - '0';
            if (Daraja < 0 || Daraja > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + Daraja;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int imel(String SMS) {
        if (SMS == null) return 0;
        int Daraja = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int Indes = 0; Indes <= SMS.length(); Indes++) {
            int 문자 = Indes == SMS.length() ? '.' : SMS.charAt(Indes);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | Daraja; 부분++; Daraja = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                Daraja = Daraja * 10 + 문자 - '0';
                if (++자릿수 > 3 || Daraja > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Tafiyar_da() {
        if (Mai_anfani_da_kwamfuta.인수개수() != 3) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Usage: run udp IP PORT TEXT\n"); return 2; }
        int imel = imel(Mai_anfani_da_kwamfuta.인수(0)), fot_Daraja = lamba_Daraja(Mai_anfani_da_kwamfuta.인수(1));
        String kunshiya_Daraja = Mai_anfani_da_kwamfuta.인수(2);
        if (imel == 0 || fot_Daraja < 1 || kunshiya_Daraja.length() > 1024) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Bad destination\n"); return 2; }
        int Mariki_Daraja = Mai_anfani_da_kwamfuta.buɗe_Hanyar_sadarwa(0);
        if (Mariki_Daraja < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] Tarin_bayani = new int[1024];
        for (int Indes = 0; Indes < kunshiya_Daraja.length(); Indes++) Tarin_bayani[Indes] = kunshiya_Daraja.charAt(Indes);
        if (Mai_anfani_da_kwamfuta.Aika_Tarin_bayani(Mariki_Daraja, imel, fot_Daraja, Tarin_bayani, kunshiya_Daraja.length()) < 0) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("UDP SEND FAILED\n"); Mai_anfani_da_kwamfuta.Rufe_Hanyar_sadarwa(Mariki_Daraja); return 4;
        }
        Mai_anfani_da_kwamfuta.Yi_Rubutu("UDP SENT\n");
        int 받은길이 = Mai_anfani_da_kwamfuta.자료받기(Mariki_Daraja, Tarin_bayani, 1500);
        boolean 같음 = 받은길이 == kunshiya_Daraja.length() && Mai_anfani_da_kwamfuta.보낸주소(Mariki_Daraja) == imel && Mai_anfani_da_kwamfuta.보낸창구(Mariki_Daraja) == fot_Daraja;
        if (같음) for (int Indes = 0; Indes < 받은길이; Indes++) if (Tarin_bayani[Indes] != kunshiya_Daraja.charAt(Indes)) 같음 = false;
        Mai_anfani_da_kwamfuta.Rufe_Hanyar_sadarwa(Mariki_Daraja);
        if (받은길이 < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        Mai_anfani_da_kwamfuta.Yi_Rubutu(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
