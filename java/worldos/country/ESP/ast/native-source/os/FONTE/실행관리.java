// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Llectura 전용 실행 묶음의 ELF32 검증, Argumentu 전달, 한 번에 한 사용자 과정 실행. */
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
        int Tamañu = 장치.실행묶음크기();
        if (Tamañu < 8 || 수(주소) != 0x50414b4a) return 0;
        int 개수 = 수(주소 + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Tamañu - 8) / 24 ? 개수 : 0;
    }

    static void 목록() {
        for (int 번호 = 0; 번호 < 묶음개수(); 번호++) {
            int 항목 = 장치.실행묶음() + 8 + 번호 * 24;
            for (int 글자 = 0; 글자 < 16 && 장치.기억읽기(항목 + 글자) != 0; 글자++)
                문자단말.문자(장치.기억읽기(항목 + 글자));
            문자단말.Escritura("\n");
        }
    }

    static int 찾기(int[] 입력, int Executar_2, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int 번호 = 0; 번호 < 묶음개수(); 번호++) {
            int 항목 = 장치.실행묶음() + 8 + 번호 * 24;
            boolean 같음 = 장치.기억읽기(항목 + 길이) == 0;
            for (int 글자 = 0; 글자 < 길이; 글자++)
                if (입력[Executar_2 + 글자] != 장치.기억읽기(항목 + 글자)) 같음 = false;
            if (같음) return 항목;
        }
        return 0;
    }

    static int 검증(int Ficheru, int 길이) {
        if (길이 < 52 || 수(Ficheru) != 0x464c457f || 장치.기억읽기(Ficheru + 4) != 1
            || 장치.기억읽기(Ficheru + 5) != 1 || 장치.기억읽기(Ficheru + 6) != 1
            || 짧은수(Ficheru + 16) != 2 || 짧은수(Ficheru + 18) != 3 || 수(Ficheru + 20) != 1
            || 짧은수(Ficheru + 40) != 52 || 짧은수(Ficheru + 42) != 32) return -8;
        int 진입 = 수(Ficheru + 24);
        int 표위치 = 수(Ficheru + 28);
        int 개수 = 짧은수(Ficheru + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > 길이 - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int 번호 = 0; 번호 < 개수; 번호++) {
            int 표 = Ficheru + 표위치 + 번호 * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Coneutar/해석기 미지원
            if (종류 != 1) continue;
            int Posición = 수(표 + 4), 주소 = 수(표 + 8), 파일크기 = 수(표 + 16), 기억크기 = 수(표 + 20);
            int 정렬 = 수(표 + 28);
            if (주소 < 사용자시작 || 주소 >= 영상끝 || 기억크기 < 0 || 기억크기 > 영상끝 - 주소
                || 파일크기 < 0 || 파일크기 > 기억크기 || Posición < 0 || (파일크기 > 0 && Posición > 길이 - 파일크기)
                || (정렬 != 0 && (정렬 < 0 || (정렬 & (정렬 - 1)) != 0
                    || ((주소 - Posición) & (정렬 - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < 번호; 앞++) {
                int 이전 = Ficheru + 표위치 + 앞 * 32;
                if (수(이전) == 1 && 기억크기 > 0 && 수(이전 + 20) > 0
                    && 주소 < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < 주소 + 기억크기) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && 진입 >= 주소 && 진입 - 주소 < 파일크기) 실행가능 = true;
        }
        return 실행가능 ? 진입 : -8;
    }

    static int 실행(int[] 입력, int Executar_2, int 길이) {
        while (Executar_2 < 길이 && 입력[Executar_2] == ' ') Executar_2++;
        int 끝 = Executar_2;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int 항목 = 찾기(입력, Executar_2, 끝 - Executar_2);
        if (항목 == 0) return -2;
        int Posición = 수(항목 + 16), Tamañu = 수(항목 + 20);
        if (Posición < 8 + 묶음개수() * 24 || Tamañu < 52 || Posición > 장치.실행묶음크기() - Tamañu) return -8;
        int Ficheru = 장치.실행묶음() + Posición;
        int 진입 = 검증(Ficheru, Tamañu);
        if (진입 < 0) return 진입;
        장치.사용자비우기();
        int 표위치 = 수(Ficheru + 28), 개수 = 짧은수(Ficheru + 44);
        for (int 번호 = 0; 번호 < 개수; 번호++) {
            int 표 = Ficheru + 표위치 + 번호 * 32;
            if (수(표) != 1) continue;
            int 원본 = Ficheru + 수(표 + 4), 목적 = 수(표 + 8), 파일크기 = 수(표 + 16);
            for (int 바이트 = 0; 바이트 < 파일크기; 바이트++) 장치.기억쓰기(목적 + 바이트, 장치.기억읽기(원본 + 바이트));
        }
        인수수 = 0;
        int 저장 = 인수시작;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (인수수 == 인수주소.length) return -22;
            Executar_2 = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            인수주소[인수수++] = 저장;
            수쓰기(저장, 끝 - Executar_2);
            for (int 글자 = Executar_2; 글자 < 끝; 글자++) 수쓰기(저장 + 4 + (글자 - Executar_2) * 4, 입력[글자]);
            저장 += 4 + (끝 - Executar_2) * 4;
        }
        통신망.과정정리();
        파일서술자관리.과정시작();
        int 결과 = 장치.사용자실행(진입, 사용자끝 - 16);
        파일서술자관리.과정정리();
        통신망.과정정리();
        return 결과;
    }
}
