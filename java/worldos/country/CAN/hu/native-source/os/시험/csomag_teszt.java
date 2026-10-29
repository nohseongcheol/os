// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** tényleges_adat Java szerződés_értéke 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class csomag_teszt {
    static int 횟수 = 0;
    static void igazol(boolean ÉRTÉK) { if (!ÉRTÉK) throw new AssertionError("case " + 횟수); 횟수++; }
    static int ellenőrzőösszeg(int[] ÉRTÉK, int Futtatás, int hossz_ÉRTÉK, int kiinduló_állapot) {
        int SUM_ÉRTÉK = kiinduló_állapot;
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) SUM_ÉRTÉK += ÉRTÉK[Futtatás + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_ÉRTÉK = (SUM_ÉRTÉK & 65535) + (SUM_ÉRTÉK >>> 16);
        SUM_ÉRTÉK = (SUM_ÉRTÉK & 65535) + (SUM_ÉRTÉK >>> 16);
        return ~SUM_ÉRTÉK & 65535;
    }
    static void Előkészítés(int hossz_ÉRTÉK) {
        hálózat_Sor.TISZTÍT_folyamat();
        igazol(hálózat_Sor.Megnyitás(5000) == 3);
        int[] doboz_INDEX = hálózat_Sor.bevitel_doboz;
        Arrays.fill(doboz_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) doboz_INDEX[INDEX] = hálózat_eszközillesztő.mobil_CÍM[INDEX];
        hálózat_Sor.넣기16(doboz_INDEX, 12, 0x0800);
        doboz_INDEX[14] = 0x45; doboz_INDEX[22] = 64; doboz_INDEX[23] = 17;
        hálózat_Sor.넣기16(doboz_INDEX, 16, 28 + hossz_ÉRTÉK);
        hálózat_Sor.넣기32(doboz_INDEX, 26, 0x0a000202); hálózat_Sor.넣기32(doboz_INDEX, 30, hálózat_Sor.내주소);
        hálózat_Sor.넣기16(doboz_INDEX, 34, 4321); hálózat_Sor.넣기16(doboz_INDEX, 36, 5000); hálózat_Sor.넣기16(doboz_INDEX, 38, hossz_ÉRTÉK + 8);
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) doboz_INDEX[42 + INDEX] = INDEX & 255;
        halmaz_ellenőrzőösszeg(hossz_ÉRTÉK);
    }
    static void halmaz_ellenőrzőösszeg(int hossz_ÉRTÉK) {
        int[] doboz_INDEX = hálózat_Sor.bevitel_doboz;
        hálózat_Sor.넣기16(doboz_INDEX, 24, 0); hálózat_Sor.넣기16(doboz_INDEX, 40, 0);
        hálózat_Sor.넣기16(doboz_INDEX, 24, ellenőrzőösszeg(doboz_INDEX, 14, 20, 0));
        int kiinduló_állapot = hálózat_Sor.가상머리합(hálózat_Sor.egész_szám_32(doboz_INDEX, 26), hálózat_Sor.내주소, hossz_ÉRTÉK + 8);
        int SUM_ÉRTÉK = ellenőrzőösszeg(doboz_INDEX, 34, hossz_ÉRTÉK + 8, kiinduló_állapot);
        hálózat_Sor.넣기16(doboz_INDEX, 40, SUM_ÉRTÉK == 0 ? 65535 : SUM_ÉRTÉK);
    }
    static void elutasít_ÉRTÉK(int hossz_ÉRTÉK) { hálózat_Sor.folyamat_doboz(hossz_ÉRTÉK); igazol(hálózat_Sor.KAPOTT_hossz[0] == -1); }
    public static void main(String[] Argumentumok) {
        for (int hossz_ÉRTÉK : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Előkészítés(hossz_ÉRTÉK); hálózat_Sor.folyamat_doboz(hossz_ÉRTÉK + 42);
            igazol(hálózat_Sor.KAPOTT_hossz[0] == hossz_ÉRTÉK);
            igazol(hálózat_Sor.KAPOTT_CÍM[0] == 0x0a000202 && hálózat_Sor.KAPOTT_portszám[0] == 4321);
            for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) igazol(hálózat_Sor.KAPOTT_adat[INDEX] == (INDEX & 255));
        }
        for (int hossz_ÉRTÉK = 0; hossz_ÉRTÉK < 42; hossz_ÉRTÉK++) { Előkészítés(0); elutasít_ÉRTÉK(hossz_ÉRTÉK); }
        Előkészítés(1025); elutasít_ÉRTÉK(1067);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[24] ^= 1; elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[42] ^= 1; elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.넣기16(hálózat_Sor.bevitel_doboz, 38, 7); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.넣기16(hálózat_Sor.bevitel_doboz, 38, 65535); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[14] = 0x4f; elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[14] = 0x44; elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[20] = 0x20; halmaz_ellenőrzőösszeg(2); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[21] = 1; halmaz_ellenőrzőösszeg(2); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[33] = 99; halmaz_ellenőrzőösszeg(2); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[0] ^= 1; elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.bevitel_doboz[23] = 6; halmaz_ellenőrzőösszeg(2); elutasít_ÉRTÉK(44);
        Előkészítés(2); hálózat_Sor.넣기16(hálózat_Sor.bevitel_doboz, 40, 0); hálózat_Sor.folyamat_doboz(44); igazol(hálózat_Sor.KAPOTT_hossz[0] == 2);
        int[] KR = new int[4];
        igazol(hálózat_Sor.fogad(3, KR, 1, 0) == -90);
        igazol(hálózat_Sor.fogad(3, KR, 4, 0) == -11);
        Előkészítés(2); hálózat_Sor.folyamat_doboz(44); int elvet_ÉRTÉK = hálózat_Sor.폐기수;
        hálózat_Sor.folyamat_doboz(44); igazol(hálózat_Sor.폐기수 == elvet_ÉRTÉK + 1);
        hálózat_Sor.TISZTÍT_folyamat(); igazol(hálózat_Sor.Megnyitás(5000) == 3);
        igazol(hálózat_Sor.Megnyitás(5000) == -98); igazol(hálózat_Sor.Megnyitás(0) == 4);
        igazol(hálózat_Sor.Megnyitás(0) == 5); igazol(hálózat_Sor.Megnyitás(0) == 6); igazol(hálózat_Sor.Megnyitás(0) == -24);
        igazol(hálózat_Sor.Bezárás(4) == 0); igazol(hálózat_Sor.Bezárás(4) == -9);
        hálózat_Sor.찾은주소 = hálózat_Sor.átjáró_ÉRTÉK;
        igazol(hálózat_Sor.küld(3, hálózat_Sor.átjáró_ÉRTÉK, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = hálózat_eszközillesztő.aktuális_ÉRTÉK;
        igazol(ellenőrzőösszeg(보냄, 14, 20, 0) == 0);
        igazol(ellenőrzőösszeg(보냄, 34, 11, hálózat_Sor.가상머리합(hálózat_Sor.내주소, hálózat_Sor.átjáró_ÉRTÉK, 11)) == 0);
        igazol(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
