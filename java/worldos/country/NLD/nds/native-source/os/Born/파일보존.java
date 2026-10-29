// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 저장 형식. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] 파일표 = new int[1024];
    static int 바이트해시(int 값, int 자료) { return (값 ^ 자료) * 16777619; }
    static void 자료비우기() {
        for (int 번호 = 0; 번호 < 512; 번호++) 저장장치접속.구역자료[번호] = 0;
    }
    static int 표정수(int Positschoon) {
        return 파일표[Positschoon] | 파일표[Positschoon + 1] << 8 | 파일표[Positschoon + 2] << 16 | 파일표[Positschoon + 3] << 24;
    }
    static void 표정수쓰기(int Positschoon, int 값) {
        for (int 번호 = 0; 번호 < 4; 번호++) 파일표[Positschoon + 번호] = (값 >>> (번호 * 8)) & 255;
    }
    static boolean 표검사() {
        for (int Datei = 0; Datei < 8; Datei++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) 주기억파일체계.Naam[칸] = 파일표[Datei * 72 + 칸];
            while (길이 < 64 && 주기억파일체계.Naam[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!주기억파일체계.이름검사(주기억파일체계.Naam, 길이)
                || 표정수(Datei * 72 + 64) < 0 || 표정수(Datei * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Datei; 앞++) {
                boolean 같음 = 파일표[앞 * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (파일표[앞 * 72 + 칸] != 주기억파일체계.Naam[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int 시작구역 = 1 + 보존본 * 259;
        if (저장장치접속.Lesen(시작구역) < 0 || 저장장치접속.정수읽기(0) != 0x4a4b534e) return -1;
        int 세대 = 저장장치접속.정수읽기(4), 검사합 = 저장장치접속.정수읽기(8);
        if (세대 < 1 || 저장장치접속.정수읽기(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int 해시 = 0x811c9dc5;
        for (int 구역 = 0; 구역 < 258; 구역++) {
            if (저장장치접속.Lesen(시작구역 + 1 + 구역) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int 값 = 저장장치접속.구역자료[칸];
                해시 = 바이트해시(해시, 값);
                if (구역 < 2) 파일표[구역 * 512 + 칸] = 값;
            }
        }
        return 해시 == 검사합 && 표검사() ? 세대 : -1;
    }
    static int 불러오기(int 보존본) {
        int 시작구역 = 1 + 보존본 * 259;
        for (int 구역 = 0; 구역 < 2; 구역++) {
            if (저장장치접속.Lesen(시작구역 + 1 + 구역) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) 파일표[구역 * 512 + 칸] = 저장장치접속.구역자료[칸];
        }
        for (int Datei = 0; Datei < 8; Datei++) {
            for (int 칸 = 0; 칸 < 64; 칸++) 주기억파일체계.이름들[Datei * 64 + 칸] = 파일표[Datei * 72 + 칸];
            주기억파일체계.크기들[Datei] = 파일표[Datei * 72] == 0 ? 0 : 표정수(Datei * 72 + 64);
            주기억파일체계.허가들[Datei] = 표정수(Datei * 72 + 68) & 511;
            for (int 구역 = 0; 구역 < 32; 구역++) {
                if (저장장치접속.Lesen(시작구역 + 3 + Datei * 32 + 구역) < 0) return -5;
                int 주소 = 장치.파일기억() + Datei * 16384 + 구역 * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) 장치.기억쓰기(주소 + 칸, 저장장치접속.구역자료[칸]);
            }
        }
        return 0;
    }
    static void 준비() {
        if (저장장치접속.Lesen(0) < 0 || 저장장치접속.정수읽기(0) != 0x54534b4a
            || 저장장치접속.정수읽기(4) != 0x3145524f || 저장장치접속.정수읽기(8) != 2048
            || 저장장치접속.정수읽기(12) != 0x3153464a) {
            문자단말.Schrieven("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        저장장치접속.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Schrieven("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (불러오기(현재보존본) < 0) {
            문자단말.Schrieven("STORE read failed; halted to preserve files\n"); 장치.정지();
        }
        문자단말.Schrieven("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int 동기화() {
        if (!저장장치접속.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, 시작구역 = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 장치 캐시를 비운다.
        자료비우기();
        if (저장장치접속.Schrieven(시작구역) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) 파일표[칸] = 0;
        for (int Datei = 0; Datei < 8; Datei++) if (주기억파일체계.이름들[Datei * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) 파일표[Datei * 72 + 칸] = 주기억파일체계.이름들[Datei * 64 + 칸];
            표정수쓰기(Datei * 72 + 64, 주기억파일체계.크기들[Datei]);
            표정수쓰기(Datei * 72 + 68, 주기억파일체계.허가들[Datei]);
        }
        int 해시 = 0x811c9dc5;
        for (int 구역 = 0; 구역 < 258; 구역++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int 값 = 0;
                if (구역 < 2) 값 = 파일표[구역 * 512 + 칸];
                else {
                    int Datei = (구역 - 2) / 32, Positschoon = (구역 - 2) % 32 * 512 + 칸;
                    if (파일표[Datei * 72] != 0 && Positschoon < 주기억파일체계.크기들[Datei])
                        값 = 장치.기억읽기(장치.파일기억() + Datei * 16384 + Positschoon);
                }
                저장장치접속.구역자료[칸] = 값; 해시 = 바이트해시(해시, 값);
            }
            if (저장장치접속.Schrieven(시작구역 + 1 + 구역) < 0) return -5;
        }
        if (저장장치접속.밀어쓰기() < 0) return -5;
        자료비우기(); 저장장치접속.정수쓰기(0, 0x4a4b534e);
        저장장치접속.정수쓰기(4, 세대번호 + 1); 저장장치접속.정수쓰기(8, 해시);
        저장장치접속.정수쓰기(12, (세대번호 + 1) ^ 해시 ^ 0x4a4b534e);
        if (저장장치접속.Schrieven(시작구역) < 0 || 저장장치접속.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
