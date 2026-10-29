// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE Format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fichier_Tabell = new int[1024];
    static int 바이트해시(int VALUE, int Daten) { return (VALUE ^ Daten) * 16777619; }
    static void läschen_Daten() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Späicher_Mobil_Verbindung.Beräich_Daten[INDEX] = 0;
    }
    static int Tabell_Ganzzuel(int positionéieren) {
        return Fichier_Tabell[positionéieren] | Fichier_Tabell[positionéieren + 1] << 8 | Fichier_Tabell[positionéieren + 2] << 16 | Fichier_Tabell[positionéieren + 3] << 24;
    }
    static void schreiwen_Tabell_Ganzzuel(int positionéieren, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Fichier_Tabell[positionéieren + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean Scheck_Tabell() {
        for (int Fichier = 0; Fichier < 8; Fichier++) {
            int Längt_VALUE = 0;
            for (int Slot_Agab = 0; Slot_Agab < 64; Slot_Agab++) Späicher_Fichierssystem.Numm[Slot_Agab] = Fichier_Tabell[Fichier * 72 + Slot_Agab];
            while (Längt_VALUE < 64 && Späicher_Fichierssystem.Numm[Längt_VALUE] != 0) Längt_VALUE++;
            if (Längt_VALUE == 0) continue;
            if (!Späicher_Fichierssystem.Scheck_Numm(Späicher_Fichierssystem.Numm, Längt_VALUE)
                || Tabell_Ganzzuel(Fichier * 72 + 64) < 0 || Tabell_Ganzzuel(Fichier * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Fichier; 앞++) {
                boolean 같음 = Fichier_Tabell[앞 * 72 + Längt_VALUE] == 0;
                for (int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) if (Fichier_Tabell[앞 * 72 + Slot_Agab] != Späicher_Fichierssystem.Numm[Slot_Agab]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_Beräich = 1 + 보존본 * 259;
        if (Späicher_Mobil_Verbindung.읽기(Start_Beräich) < 0 || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(0) != 0x4a4b534e) return -1;
        int 세대 = Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(4), 검사합 = Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(8);
        if (세대 < 1 || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int Hash_Fichier = 0x811c9dc5;
        for (int Beräich_VALUE = 0; Beräich_VALUE < 258; Beräich_VALUE++) {
            if (Späicher_Mobil_Verbindung.읽기(Start_Beräich + 1 + Beräich_VALUE) < 0) return -1;
            for (int Slot_Agab = 0; Slot_Agab < 512; Slot_Agab++) {
                int VALUE = Späicher_Mobil_Verbindung.Beräich_Daten[Slot_Agab];
                Hash_Fichier = 바이트해시(Hash_Fichier, VALUE);
                if (Beräich_VALUE < 2) Fichier_Tabell[Beräich_VALUE * 512 + Slot_Agab] = VALUE;
            }
        }
        return Hash_Fichier == 검사합 && Scheck_Tabell() ? 세대 : -1;
    }
    static int Charge(int 보존본) {
        int Start_Beräich = 1 + 보존본 * 259;
        for (int Beräich_VALUE = 0; Beräich_VALUE < 2; Beräich_VALUE++) {
            if (Späicher_Mobil_Verbindung.읽기(Start_Beräich + 1 + Beräich_VALUE) < 0) return -5;
            for (int Slot_Agab = 0; Slot_Agab < 512; Slot_Agab++) Fichier_Tabell[Beräich_VALUE * 512 + Slot_Agab] = Späicher_Mobil_Verbindung.Beräich_Daten[Slot_Agab];
        }
        for (int Fichier = 0; Fichier < 8; Fichier++) {
            for (int Slot_Agab = 0; Slot_Agab < 64; Slot_Agab++) Späicher_Fichierssystem.이름들[Fichier * 64 + Slot_Agab] = Fichier_Tabell[Fichier * 72 + Slot_Agab];
            Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] = Fichier_Tabell[Fichier * 72] == 0 ? 0 : Tabell_Ganzzuel(Fichier * 72 + 64);
            Späicher_Fichierssystem.허가들[Fichier] = Tabell_Ganzzuel(Fichier * 72 + 68) & 511;
            for (int Beräich_VALUE = 0; Beräich_VALUE < 32; Beräich_VALUE++) {
                if (Späicher_Mobil_Verbindung.읽기(Start_Beräich + 3 + Fichier * 32 + Beräich_VALUE) < 0) return -5;
                int Adress = Mobil_VALUE.Fichier_Späicher() + Fichier * 16384 + Beräich_VALUE * 512;
                for (int Slot_Agab = 0; Slot_Agab < 512; Slot_Agab++) Mobil_VALUE.schreiwen_Späicher(Adress + Slot_Agab, Späicher_Mobil_Verbindung.Beräich_Daten[Slot_Agab]);
            }
        }
        return 0;
    }
    static void Préparéieren() {
        if (Späicher_Mobil_Verbindung.읽기(0) < 0 || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(0) != 0x54534b4a
            || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(4) != 0x3145524f || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(8) != 2048
            || Späicher_Mobil_Verbindung.analyséieren_Ganzzuel(12) != 0x3153464a) {
            SMS_Terminal.schreiwen("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Späicher_Mobil_Verbindung.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.schreiwen("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Charge(현재보존본) < 0) {
            SMS_Terminal.schreiwen("STORE read failed; halted to preserve files\n"); Mobil_VALUE.정지();
        }
        SMS_Terminal.schreiwen("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int synchroniséieren() {
        if (!Späicher_Mobil_Verbindung.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Weider_Element = 현재보존본 == 0 ? 1 : 0, Start_Beräich = 1 + Weider_Element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 Mobil_VALUE 캐시를 비운다.
        läschen_Daten();
        if (Späicher_Mobil_Verbindung.schreiwen(Start_Beräich) < 0 || Späicher_Mobil_Verbindung.밀어쓰기() < 0) return -5;
        for (int Slot_Agab = 0; Slot_Agab < 1024; Slot_Agab++) Fichier_Tabell[Slot_Agab] = 0;
        for (int Fichier = 0; Fichier < 8; Fichier++) if (Späicher_Fichierssystem.이름들[Fichier * 64] != 0) {
            for (int Slot_Agab = 0; Slot_Agab < 64; Slot_Agab++) Fichier_Tabell[Fichier * 72 + Slot_Agab] = Späicher_Fichierssystem.이름들[Fichier * 64 + Slot_Agab];
            schreiwen_Tabell_Ganzzuel(Fichier * 72 + 64, Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier]);
            schreiwen_Tabell_Ganzzuel(Fichier * 72 + 68, Späicher_Fichierssystem.허가들[Fichier]);
        }
        int Hash_Fichier = 0x811c9dc5;
        for (int Beräich_VALUE = 0; Beräich_VALUE < 258; Beräich_VALUE++) {
            for (int Slot_Agab = 0; Slot_Agab < 512; Slot_Agab++) {
                int VALUE = 0;
                if (Beräich_VALUE < 2) VALUE = Fichier_Tabell[Beräich_VALUE * 512 + Slot_Agab];
                else {
                    int Fichier = (Beräich_VALUE - 2) / 32, positionéieren = (Beräich_VALUE - 2) % 32 * 512 + Slot_Agab;
                    if (Fichier_Tabell[Fichier * 72] != 0 && positionéieren < Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier])
                        VALUE = Mobil_VALUE.기억읽기(Mobil_VALUE.Fichier_Späicher() + Fichier * 16384 + positionéieren);
                }
                Späicher_Mobil_Verbindung.Beräich_Daten[Slot_Agab] = VALUE; Hash_Fichier = 바이트해시(Hash_Fichier, VALUE);
            }
            if (Späicher_Mobil_Verbindung.schreiwen(Start_Beräich + 1 + Beräich_VALUE) < 0) return -5;
        }
        if (Späicher_Mobil_Verbindung.밀어쓰기() < 0) return -5;
        läschen_Daten(); Späicher_Mobil_Verbindung.schreiwen_Ganzzuel_VALUE(0, 0x4a4b534e);
        Späicher_Mobil_Verbindung.schreiwen_Ganzzuel_VALUE(4, 세대번호 + 1); Späicher_Mobil_Verbindung.schreiwen_Ganzzuel_VALUE(8, Hash_Fichier);
        Späicher_Mobil_Verbindung.schreiwen_Ganzzuel_VALUE(12, (세대번호 + 1) ^ Hash_Fichier ^ 0x4a4b534e);
        if (Späicher_Mobil_Verbindung.schreiwen(Start_Beräich) < 0 || Späicher_Mobil_Verbindung.밀어쓰기() < 0) return -5;
        현재보존본 = Weider_Element; 세대번호++;
        return 0;
    }
}
