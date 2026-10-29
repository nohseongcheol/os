// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 resde_njaru formaa_njaru. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fiilde_taabal = new int[1024];
    static int 바이트해시(int njaru, int keɓe) { return (njaru ^ keɓe) * 16777619; }
    static void festude_keɓe() {
        for (int joopirdu = 0; joopirdu < 512; joopirdu++) 저장장치접속.taƴre_keɓe[joopirdu] = 0;
    }
    static int 표정수(int 위치) {
        return fiilde_taabal[위치] | fiilde_taabal[위치 + 1] << 8 | fiilde_taabal[위치 + 2] << 16 | fiilde_taabal[위치 + 3] << 24;
    }
    static void 표정수쓰기(int 위치, int njaru) {
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) fiilde_taabal[위치 + joopirdu] = (njaru >>> (joopirdu * 8)) & 255;
    }
    static boolean sek_taabal() {
        for (int fiilde = 0; fiilde < 8; fiilde++) {
            int njuuteendi_njaru = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) teskordu_yuɓɓo_piille.innde[칸] = fiilde_taabal[fiilde * 72 + 칸];
            while (njuuteendi_njaru < 64 && teskordu_yuɓɓo_piille.innde[njuuteendi_njaru] != 0) njuuteendi_njaru++;
            if (njuuteendi_njaru == 0) continue;
            if (!teskordu_yuɓɓo_piille.sek_innde(teskordu_yuɓɓo_piille.innde, njuuteendi_njaru)
                || 표정수(fiilde * 72 + 64) < 0 || 표정수(fiilde * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < fiilde; 앞++) {
                boolean 같음 = fiilde_taabal[앞 * 72 + njuuteendi_njaru] == 0;
                for (int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) if (fiilde_taabal[앞 * 72 + 칸] != teskordu_yuɓɓo_piille.innde[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int huɓɓude_taƴre = 1 + 보존본 * 259;
        if (저장장치접속.읽기(huɓɓude_taƴre) < 0 || 저장장치접속.정수읽기(0) != 0x4a4b534e) return -1;
        int 세대 = 저장장치접속.정수읽기(4), 검사합 = 저장장치접속.정수읽기(8);
        if (세대 < 1 || 저장장치접속.정수읽기(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int 해시 = 0x811c9dc5;
        for (int taƴre_njaru = 0; taƴre_njaru < 258; taƴre_njaru++) {
            if (저장장치접속.읽기(huɓɓude_taƴre + 1 + taƴre_njaru) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int njaru = 저장장치접속.taƴre_keɓe[칸];
                해시 = 바이트해시(해시, njaru);
                if (taƴre_njaru < 2) fiilde_taabal[taƴre_njaru * 512 + 칸] = njaru;
            }
        }
        return 해시 == 검사합 && sek_taabal() ? 세대 : -1;
    }
    static int loowde(int 보존본) {
        int huɓɓude_taƴre = 1 + 보존본 * 259;
        for (int taƴre_njaru = 0; taƴre_njaru < 2; taƴre_njaru++) {
            if (저장장치접속.읽기(huɓɓude_taƴre + 1 + taƴre_njaru) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) fiilde_taabal[taƴre_njaru * 512 + 칸] = 저장장치접속.taƴre_keɓe[칸];
        }
        for (int fiilde = 0; fiilde < 8; fiilde++) {
            for (int 칸 = 0; 칸 < 64; 칸++) teskordu_yuɓɓo_piille.이름들[fiilde * 64 + 칸] = fiilde_taabal[fiilde * 72 + 칸];
            teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] = fiilde_taabal[fiilde * 72] == 0 ? 0 : 표정수(fiilde * 72 + 64);
            teskordu_yuɓɓo_piille.허가들[fiilde] = 표정수(fiilde * 72 + 68) & 511;
            for (int taƴre_njaru = 0; taƴre_njaru < 32; taƴre_njaru++) {
                if (저장장치접속.읽기(huɓɓude_taƴre + 3 + fiilde * 32 + taƴre_njaru) < 0) return -5;
                int ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + fiilde * 16384 + taƴre_njaru * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) kaɓirgal_njaru.winndude_teskordu(ñiiɓirde + 칸, 저장장치접속.taƴre_keɓe[칸]);
            }
        }
        return 0;
    }
    static void Heblu() {
        if (저장장치접속.읽기(0) < 0 || 저장장치접속.정수읽기(0) != 0x54534b4a
            || 저장장치접속.정수읽기(4) != 0x3145524f || 저장장치접속.정수읽기(8) != 2048
            || 저장장치접속.정수읽기(12) != 0x3153464a) {
            문자단말.winndude("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        저장장치접속.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.winndude("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (loowde(현재보존본) < 0) {
            문자단말.winndude("STORE read failed; halted to preserve files\n"); kaɓirgal_njaru.정지();
        }
        문자단말.winndude("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int sanngoɗinde() {
        if (!저장장치접속.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, huɓɓude_taƴre = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 kaɓirgal_njaru 캐시를 비운다.
        festude_keɓe();
        if (저장장치접속.winndude(huɓɓude_taƴre) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) fiilde_taabal[칸] = 0;
        for (int fiilde = 0; fiilde < 8; fiilde++) if (teskordu_yuɓɓo_piille.이름들[fiilde * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) fiilde_taabal[fiilde * 72 + 칸] = teskordu_yuɓɓo_piille.이름들[fiilde * 64 + 칸];
            표정수쓰기(fiilde * 72 + 64, teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde]);
            표정수쓰기(fiilde * 72 + 68, teskordu_yuɓɓo_piille.허가들[fiilde]);
        }
        int 해시 = 0x811c9dc5;
        for (int taƴre_njaru = 0; taƴre_njaru < 258; taƴre_njaru++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int njaru = 0;
                if (taƴre_njaru < 2) njaru = fiilde_taabal[taƴre_njaru * 512 + 칸];
                else {
                    int fiilde = (taƴre_njaru - 2) / 32, 위치 = (taƴre_njaru - 2) % 32 * 512 + 칸;
                    if (fiilde_taabal[fiilde * 72] != 0 && 위치 < teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde])
                        njaru = kaɓirgal_njaru.기억읽기(kaɓirgal_njaru.fiilde_teskordu() + fiilde * 16384 + 위치);
                }
                저장장치접속.taƴre_keɓe[칸] = njaru; 해시 = 바이트해시(해시, njaru);
            }
            if (저장장치접속.winndude(huɓɓude_taƴre + 1 + taƴre_njaru) < 0) return -5;
        }
        if (저장장치접속.밀어쓰기() < 0) return -5;
        festude_keɓe(); 저장장치접속.정수쓰기(0, 0x4a4b534e);
        저장장치접속.정수쓰기(4, 세대번호 + 1); 저장장치접속.정수쓰기(8, 해시);
        저장장치접속.정수쓰기(12, (세대번호 + 1) ^ 해시 ^ 0x4a4b534e);
        if (저장장치접속.winndude(huɓɓude_taƴre) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
