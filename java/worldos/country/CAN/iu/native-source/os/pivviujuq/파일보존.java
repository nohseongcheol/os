// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 tuqqurli_atuutilik aaqqisurli_atuutilik. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] ini_kipu = new int[1024];
    static int 바이트해시(int atuutilik, int titiqqat) { return (atuutilik ^ titiqqat) * 16777619; }
    static void piijarli_titiqqat() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 512; nalunaiqsimavik++) 저장장치접속.sukuttia_titiqqat[nalunaiqsimavik] = 0;
    }
    static int kipu_naasaut(int 위치) {
        return ini_kipu[위치] | ini_kipu[위치 + 1] << 8 | ini_kipu[위치 + 2] << 16 | ini_kipu[위치 + 3] << 24;
    }
    static void titiraq_kipu_naasaut(int 위치, int atuutilik) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) ini_kipu[위치 + nalunaiqsimavik] = (atuutilik >>> (nalunaiqsimavik * 8)) & 255;
    }
    static boolean qaujigiarli_kipu() {
        for (int ini = 0; ini < 8; ini++) {
            int takininga_atuutilik = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) puigujjaikkut_inikkuvik.atiq[칸] = ini_kipu[ini * 72 + 칸];
            while (takininga_atuutilik < 64 && puigujjaikkut_inikkuvik.atiq[takininga_atuutilik] != 0) takininga_atuutilik++;
            if (takininga_atuutilik == 0) continue;
            if (!puigujjaikkut_inikkuvik.qaujigiarli_atiq(puigujjaikkut_inikkuvik.atiq, takininga_atuutilik)
                || kipu_naasaut(ini * 72 + 64) < 0 || kipu_naasaut(ini * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < ini; 앞++) {
                boolean 같음 = ini_kipu[앞 * 72 + takininga_atuutilik] == 0;
                for (int 칸 = 0; 칸 < takininga_atuutilik; 칸++) if (ini_kipu[앞 * 72 + 칸] != puigujjaikkut_inikkuvik.atiq[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int pigiarli_sukuttia = 1 + 보존본 * 259;
        if (저장장치접속.읽기(pigiarli_sukuttia) < 0 || 저장장치접속.agguqtuut_naasaut(0) != 0x4a4b534e) return -1;
        int 세대 = 저장장치접속.agguqtuut_naasaut(4), 검사합 = 저장장치접속.agguqtuut_naasaut(8);
        if (세대 < 1 || 저장장치접속.agguqtuut_naasaut(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int 해시 = 0x811c9dc5;
        for (int sukuttia_atuutilik = 0; sukuttia_atuutilik < 258; sukuttia_atuutilik++) {
            if (저장장치접속.읽기(pigiarli_sukuttia + 1 + sukuttia_atuutilik) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int atuutilik = 저장장치접속.sukuttia_titiqqat[칸];
                해시 = 바이트해시(해시, atuutilik);
                if (sukuttia_atuutilik < 2) ini_kipu[sukuttia_atuutilik * 512 + 칸] = atuutilik;
            }
        }
        return 해시 == 검사합 && qaujigiarli_kipu() ? 세대 : -1;
    }
    static int puurli(int 보존본) {
        int pigiarli_sukuttia = 1 + 보존본 * 259;
        for (int sukuttia_atuutilik = 0; sukuttia_atuutilik < 2; sukuttia_atuutilik++) {
            if (저장장치접속.읽기(pigiarli_sukuttia + 1 + sukuttia_atuutilik) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) ini_kipu[sukuttia_atuutilik * 512 + 칸] = 저장장치접속.sukuttia_titiqqat[칸];
        }
        for (int ini = 0; ini < 8; ini++) {
            for (int 칸 = 0; 칸 < 64; 칸++) puigujjaikkut_inikkuvik.이름들[ini * 64 + 칸] = ini_kipu[ini * 72 + 칸];
            puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] = ini_kipu[ini * 72] == 0 ? 0 : kipu_naasaut(ini * 72 + 64);
            puigujjaikkut_inikkuvik.허가들[ini] = kipu_naasaut(ini * 72 + 68) & 511;
            for (int sukuttia_atuutilik = 0; sukuttia_atuutilik < 32; sukuttia_atuutilik++) {
                if (저장장치접속.읽기(pigiarli_sukuttia + 3 + ini * 32 + sukuttia_atuutilik) < 0) return -5;
                int turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * 16384 + sukuttia_atuutilik * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(turaarut + 칸, 저장장치접속.sukuttia_titiqqat[칸]);
            }
        }
        return 0;
    }
    static void Parnalli() {
        if (저장장치접속.읽기(0) < 0 || 저장장치접속.agguqtuut_naasaut(0) != 0x54534b4a
            || 저장장치접속.agguqtuut_naasaut(4) != 0x3145524f || 저장장치접속.agguqtuut_naasaut(8) != 2048
            || 저장장치접속.agguqtuut_naasaut(12) != 0x3153464a) {
            문자단말.titiraq("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        저장장치접속.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.titiraq("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (puurli(현재보존본) < 0) {
            문자단말.titiraq("STORE read failed; halted to preserve files\n"); sunakkutaaq_atuutilik.정지();
        }
        문자단말.titiraq("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int asiqqunniqannginniq() {
        if (!저장장치접속.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, pigiarli_sukuttia = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 sunakkutaaq_atuutilik 캐시를 비운다.
        piijarli_titiqqat();
        if (저장장치접속.titiraq(pigiarli_sukuttia) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) ini_kipu[칸] = 0;
        for (int ini = 0; ini < 8; ini++) if (puigujjaikkut_inikkuvik.이름들[ini * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) ini_kipu[ini * 72 + 칸] = puigujjaikkut_inikkuvik.이름들[ini * 64 + 칸];
            titiraq_kipu_naasaut(ini * 72 + 64, puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini]);
            titiraq_kipu_naasaut(ini * 72 + 68, puigujjaikkut_inikkuvik.허가들[ini]);
        }
        int 해시 = 0x811c9dc5;
        for (int sukuttia_atuutilik = 0; sukuttia_atuutilik < 258; sukuttia_atuutilik++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int atuutilik = 0;
                if (sukuttia_atuutilik < 2) atuutilik = ini_kipu[sukuttia_atuutilik * 512 + 칸];
                else {
                    int ini = (sukuttia_atuutilik - 2) / 32, 위치 = (sukuttia_atuutilik - 2) % 32 * 512 + 칸;
                    if (ini_kipu[ini * 72] != 0 && 위치 < puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini])
                        atuutilik = sunakkutaaq_atuutilik.기억읽기(sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * 16384 + 위치);
                }
                저장장치접속.sukuttia_titiqqat[칸] = atuutilik; 해시 = 바이트해시(해시, atuutilik);
            }
            if (저장장치접속.titiraq(pigiarli_sukuttia + 1 + sukuttia_atuutilik) < 0) return -5;
        }
        if (저장장치접속.밀어쓰기() < 0) return -5;
        piijarli_titiqqat(); 저장장치접속.titiraq_naasaut_atuutilik(0, 0x4a4b534e);
        저장장치접속.titiraq_naasaut_atuutilik(4, 세대번호 + 1); 저장장치접속.titiraq_naasaut_atuutilik(8, 해시);
        저장장치접속.titiraq_naasaut_atuutilik(12, (세대번호 + 1) ^ 해시 ^ 0x4a4b534e);
        if (저장장치접속.titiraq(pigiarli_sukuttia) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
