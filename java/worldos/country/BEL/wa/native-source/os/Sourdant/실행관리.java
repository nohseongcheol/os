// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lére 전용 실행 묶음의 ELF32 검증, Årgumints 전달, 한 번에 한 사용자 과정 실행. */
public final class 실행관리 {
    static final int 사용자시작 = 0x04000000;
    static final int 사용자끝 = 0x04400000;
    static final int 영상끝 = 0x04200000;
    static final int 인수시작 = 0x04300000;
    static int 인수수 = 0;
    static int[] 인수주소 = new int[16];

    static boolean 범위(int 주소, int 길이) {
        return 주소 >= 사용자시작 && 주소 < 사용자끝 && 길이 >= 0 && 길이 <= 사용자끝 - 주소;
    }

    static int 수(int 주소) { return 기억공간.정수읽기(주소); }
    static int 짧은수(int 주소) { return 장치.기억읽기(주소) | 장치.기억읽기(주소 + 1) << 8; }
    static void 수쓰기(int 주소, int 값) {
        for (int 번호 = 0; 번호 < 4; 번호++) 장치.기억쓰기(주소 + 번호, 값 >>> (번호 * 8));
    }

    static int 묶음개수() {
        int 주소 = 장치.실행묶음();
        int Grandeu = 장치.실행묶음크기();
        if (Grandeu < 8 || 수(주소) != 0x50414b4a) return 0;
        int 개수 = 수(주소 + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Grandeu - 8) / 24 ? 개수 : 0;
    }

    static void 목록() {
        for (int 번호 = 0; 번호 < 묶음개수(); 번호++) {
            int 항목 = 장치.실행묶음() + 8 + 번호 * 24;
            for (int 글자 = 0; 글자 < 16 && 장치.기억읽기(항목 + 글자) != 0; 글자++)
                문자단말.문자(장치.기억읽기(항목 + 글자));
            문자단말.Sicrire("\n");
        }
    }

    static int 찾기(int[] 입력, int Enonder_2, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int 번호 = 0; 번호 < 묶음개수(); 번호++) {
            int 항목 = 장치.실행묶음() + 8 + 번호 * 24;
            boolean 같음 = 장치.기억읽기(항목 + 길이) == 0;
            for (int 글자 = 0; 글자 < 길이; 글자++)
                if (입력[Enonder_2 + 글자] != 장치.기억읽기(항목 + 글자)) 같음 = false;
            if (같음) return 항목;
        }
        return 0;
    }

    static int 검증(int Fitchî, int 길이) {
        if (길이 < 52 || 수(Fitchî) != 0x464c457f || 장치.기억읽기(Fitchî + 4) != 1
            || 장치.기억읽기(Fitchî + 5) != 1 || 장치.기억읽기(Fitchî + 6) != 1
            || 짧은수(Fitchî + 16) != 2 || 짧은수(Fitchî + 18) != 3 || 수(Fitchî + 20) != 1
            || 짧은수(Fitchî + 40) != 52 || 짧은수(Fitchî + 42) != 32) return -8;
        int 진입 = 수(Fitchî + 24);
        int 표위치 = 수(Fitchî + 28);
        int 개수 = 짧은수(Fitchî + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > 길이 - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int 번호 = 0; 번호 < 개수; 번호++) {
            int 표 = Fitchî + 표위치 + 번호 * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Raloyî/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), 주소 = 수(표 + 8), 파일크기 = 수(표 + 16), 기억크기 = 수(표 + 20);
            int 정렬 = 수(표 + 28);
            if (주소 < 사용자시작 || 주소 >= 영상끝 || 기억크기 < 0 || 기억크기 > 영상끝 - 주소
                || 파일크기 < 0 || 파일크기 > 기억크기 || 위치 < 0 || (파일크기 > 0 && 위치 > 길이 - 파일크기)
                || (정렬 != 0 && (정렬 < 0 || (정렬 & (정렬 - 1)) != 0
                    || ((주소 - 위치) & (정렬 - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < 번호; 앞++) {
                int 이전 = Fitchî + 표위치 + 앞 * 32;
                if (수(이전) == 1 && 기억크기 > 0 && 수(이전 + 20) > 0
                    && 주소 < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < 주소 + 기억크기) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && 진입 >= 주소 && 진입 - 주소 < 파일크기) 실행가능 = true;
        }
        return 실행가능 ? 진입 : -8;
    }

    static int 실행(int[] 입력, int Enonder_2, int 길이) {
        while (Enonder_2 < 길이 && 입력[Enonder_2] == ' ') Enonder_2++;
        int 끝 = Enonder_2;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int 항목 = 찾기(입력, Enonder_2, 끝 - Enonder_2);
        if (항목 == 0) return -2;
        int 위치 = 수(항목 + 16), Grandeu = 수(항목 + 20);
        if (위치 < 8 + 묶음개수() * 24 || Grandeu < 52 || 위치 > 장치.실행묶음크기() - Grandeu) return -8;
        int Fitchî = 장치.실행묶음() + 위치;
        int 진입 = 검증(Fitchî, Grandeu);
        if (진입 < 0) return 진입;
        장치.사용자비우기();
        int 표위치 = 수(Fitchî + 28), 개수 = 짧은수(Fitchî + 44);
        for (int 번호 = 0; 번호 < 개수; 번호++) {
            int 표 = Fitchî + 표위치 + 번호 * 32;
            if (수(표) != 1) continue;
            int 원본 = Fitchî + 수(표 + 4), 목적 = 수(표 + 8), 파일크기 = 수(표 + 16);
            for (int 바이트 = 0; 바이트 < 파일크기; 바이트++) 장치.기억쓰기(목적 + 바이트, 장치.기억읽기(원본 + 바이트));
        }
        인수수 = 0;
        int 저장 = 인수시작;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (인수수 == 인수주소.length) return -22;
            Enonder_2 = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            인수주소[인수수++] = 저장;
            수쓰기(저장, 끝 - Enonder_2);
            for (int 글자 = Enonder_2; 글자 < 끝; 글자++) 수쓰기(저장 + 4 + (글자 - Enonder_2) * 4, 입력[글자]);
            저장 += 4 + (끝 - Enonder_2) * 4;
        }
        통신망.과정정리();
        파일서술자관리.과정시작();
        int 결과 = 장치.사용자실행(진입, 사용자끝 - 16);
        파일서술자관리.과정정리();
        통신망.과정정리();
        return 결과;
    }
}
