// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 저장 akua_ipaa_ajutuu. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] anaajaalaa_taapüla = new int[1024];
    static int 바이트해시(int ajutuu, int atijaaya) { return (ajutuu ^ atijaaya) * 16777619; }
    static void ama_inrüinjiraa_atijaaya() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 512; ee_iyatialujuna++) 저장장치접속.alüjalee_atijaaya[ee_iyatialujuna] = 0;
    }
    static int taapüla_waneepiasü(int 위치) {
        return anaajaalaa_taapüla[위치] | anaajaalaa_taapüla[위치 + 1] << 8 | anaajaalaa_taapüla[위치 + 2] << 16 | anaajaalaa_taapüla[위치 + 3] << 24;
    }
    static void ashajaa_taapüla_waneepiasü(int 위치, int ajutuu) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) anaajaalaa_taapüla[위치 + ee_iyatialujuna] = (ajutuu >>> (ee_iyatialujuna * 8)) & 255;
    }
    static boolean cheeke_taapüla() {
        for (int anaajaalaa = 0; anaajaalaa < 8; anaajaalaa++) {
            int akaliaa_ajutuu = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) 주기억파일체계.이름[칸] = anaajaalaa_taapüla[anaajaalaa * 72 + 칸];
            while (akaliaa_ajutuu < 64 && 주기억파일체계.이름[akaliaa_ajutuu] != 0) akaliaa_ajutuu++;
            if (akaliaa_ajutuu == 0) continue;
            if (!주기억파일체계.이름검사(주기억파일체계.이름, akaliaa_ajutuu)
                || taapüla_waneepiasü(anaajaalaa * 72 + 64) < 0 || taapüla_waneepiasü(anaajaalaa * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < anaajaalaa; 앞++) {
                boolean 같음 = anaajaalaa_taapüla[앞 * 72 + akaliaa_ajutuu] == 0;
                for (int 칸 = 0; 칸 < akaliaa_ajutuu; 칸++) if (anaajaalaa_taapüla[앞 * 72 + 칸] != 주기억파일체계.이름[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int achuwalaa_alüjalee = 1 + 보존본 * 259;
        if (저장장치접속.읽기(achuwalaa_alüjalee) < 0 || 저장장치접속.akatajaa_waneepiasü(0) != 0x4a4b534e) return -1;
        int 세대 = 저장장치접속.akatajaa_waneepiasü(4), 검사합 = 저장장치접속.akatajaa_waneepiasü(8);
        if (세대 < 1 || 저장장치접속.akatajaa_waneepiasü(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int 해시 = 0x811c9dc5;
        for (int alüjalee_ajutuu = 0; alüjalee_ajutuu < 258; alüjalee_ajutuu++) {
            if (저장장치접속.읽기(achuwalaa_alüjalee + 1 + alüjalee_ajutuu) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int ajutuu = 저장장치접속.alüjalee_atijaaya[칸];
                해시 = 바이트해시(해시, ajutuu);
                if (alüjalee_ajutuu < 2) anaajaalaa_taapüla[alüjalee_ajutuu * 512 + 칸] = ajutuu;
            }
        }
        return 해시 == 검사합 && cheeke_taapüla() ? 세대 : -1;
    }
    static int 불러오기(int 보존본) {
        int achuwalaa_alüjalee = 1 + 보존본 * 259;
        for (int alüjalee_ajutuu = 0; alüjalee_ajutuu < 2; alüjalee_ajutuu++) {
            if (저장장치접속.읽기(achuwalaa_alüjalee + 1 + alüjalee_ajutuu) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) anaajaalaa_taapüla[alüjalee_ajutuu * 512 + 칸] = 저장장치접속.alüjalee_atijaaya[칸];
        }
        for (int anaajaalaa = 0; anaajaalaa < 8; anaajaalaa++) {
            for (int 칸 = 0; 칸 < 64; 칸++) 주기억파일체계.이름들[anaajaalaa * 64 + 칸] = anaajaalaa_taapüla[anaajaalaa * 72 + 칸];
            주기억파일체계.크기들[anaajaalaa] = anaajaalaa_taapüla[anaajaalaa * 72] == 0 ? 0 : taapüla_waneepiasü(anaajaalaa * 72 + 64);
            주기억파일체계.허가들[anaajaalaa] = taapüla_waneepiasü(anaajaalaa * 72 + 68) & 511;
            for (int alüjalee_ajutuu = 0; alüjalee_ajutuu < 32; alüjalee_ajutuu++) {
                if (저장장치접속.읽기(achuwalaa_alüjalee + 3 + anaajaalaa * 32 + alüjalee_ajutuu) < 0) return -5;
                int ejepüsee = serulaalü_ajutuu.파일기억() + anaajaalaa * 16384 + alüjalee_ajutuu * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) serulaalü_ajutuu.기억쓰기(ejepüsee + 칸, 저장장치접속.alüjalee_atijaaya[칸]);
            }
        }
        return 0;
    }
    static void 준비() {
        if (저장장치접속.읽기(0) < 0 || 저장장치접속.akatajaa_waneepiasü(0) != 0x54534b4a
            || 저장장치접속.akatajaa_waneepiasü(4) != 0x3145524f || 저장장치접속.akatajaa_waneepiasü(8) != 2048
            || 저장장치접속.akatajaa_waneepiasü(12) != 0x3153464a) {
            문자단말.ashajaa("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        저장장치접속.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.ashajaa("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (불러오기(현재보존본) < 0) {
            문자단말.ashajaa("STORE read failed; halted to preserve files\n"); serulaalü_ajutuu.정지();
        }
        문자단말.ashajaa("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int awanaawajaa() {
        if (!저장장치접속.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, achuwalaa_alüjalee = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 serulaalü_ajutuu 캐시를 비운다.
        ama_inrüinjiraa_atijaaya();
        if (저장장치접속.ashajaa(achuwalaa_alüjalee) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) anaajaalaa_taapüla[칸] = 0;
        for (int anaajaalaa = 0; anaajaalaa < 8; anaajaalaa++) if (주기억파일체계.이름들[anaajaalaa * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) anaajaalaa_taapüla[anaajaalaa * 72 + 칸] = 주기억파일체계.이름들[anaajaalaa * 64 + 칸];
            ashajaa_taapüla_waneepiasü(anaajaalaa * 72 + 64, 주기억파일체계.크기들[anaajaalaa]);
            ashajaa_taapüla_waneepiasü(anaajaalaa * 72 + 68, 주기억파일체계.허가들[anaajaalaa]);
        }
        int 해시 = 0x811c9dc5;
        for (int alüjalee_ajutuu = 0; alüjalee_ajutuu < 258; alüjalee_ajutuu++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int ajutuu = 0;
                if (alüjalee_ajutuu < 2) ajutuu = anaajaalaa_taapüla[alüjalee_ajutuu * 512 + 칸];
                else {
                    int anaajaalaa = (alüjalee_ajutuu - 2) / 32, 위치 = (alüjalee_ajutuu - 2) % 32 * 512 + 칸;
                    if (anaajaalaa_taapüla[anaajaalaa * 72] != 0 && 위치 < 주기억파일체계.크기들[anaajaalaa])
                        ajutuu = serulaalü_ajutuu.기억읽기(serulaalü_ajutuu.파일기억() + anaajaalaa * 16384 + 위치);
                }
                저장장치접속.alüjalee_atijaaya[칸] = ajutuu; 해시 = 바이트해시(해시, ajutuu);
            }
            if (저장장치접속.ashajaa(achuwalaa_alüjalee + 1 + alüjalee_ajutuu) < 0) return -5;
        }
        if (저장장치접속.밀어쓰기() < 0) return -5;
        ama_inrüinjiraa_atijaaya(); 저장장치접속.ashajaa_waneepiasü_ajutuu(0, 0x4a4b534e);
        저장장치접속.ashajaa_waneepiasü_ajutuu(4, 세대번호 + 1); 저장장치접속.ashajaa_waneepiasü_ajutuu(8, 해시);
        저장장치접속.ashajaa_waneepiasü_ajutuu(12, (세대번호 + 1) ^ 해시 ^ 0x4a4b534e);
        if (저장장치접속.ashajaa(achuwalaa_alüjalee) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
