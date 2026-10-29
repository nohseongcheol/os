// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 파일. 원본 편집/컴파일 실패 시 기존 파일을 보존한다. */
public final class 주기억파일체계 {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] 크기들 = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] mbiekolo = new int[64];
    static int[] 편집 = new int[최대크기];
    static boolean 편집중 = false;
    static boolean 넘침 = false;
    static int 편집크기 = 0;

    static boolean 이름검사(int[] 글자, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int 수 = 0; 수 < 길이; 수++) {
            int 값 = 글자[수];
            if (!(값 >= 'a' && 값 <= 'z') && !(값 >= 'A' && 값 <= 'Z')
                && !(값 >= '0' && 값 <= '9') && 값 != '_' && 값 != '-' && 값 != '.') return false;
        }
        return 글자[0] != '.';
    }

    static int 찾기(int[] 글자, int 길이) {
        if (!이름검사(글자, 길이)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[수 * 64 + 칸] != 글자[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int 저장(int[] 글자, int 길이, int[] 자료, int 크기) {
        if (!이름검사(글자, 길이) || 크기 < 0 || 크기 > 자료.length) return -22;
        if (크기 > 최대크기) return -90;
        int 번호 = 찾기(글자, 길이);
        if (번호 == -2) {
            for (int 수 = 0; 수 < 8 && 번호 < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) 번호 = 수;
            if (번호 >= 0) 허가들[번호] = 438;
        }
        if (번호 < 0) return -28;
        int 주소 = 장치.파일기억() + 번호 * 최대크기;
        for (int 수 = 0; 수 < 크기; 수++) 장치.기억쓰기(주소 + 수, 자료[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[번호 * 64 + 수] = 수 < 길이 ? 글자[수] : 0;
        크기들[번호] = 크기;
        return 크기;
    }

    static void 목록() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) 문자단말.문자(이름들[수 * 64 + 칸]);
            문자단말.쓰기("  "); 문자단말.수쓰기(크기들[수]); 문자단말.쓰기("바이트\n");
        }
        문자단말.쓰기(저장장치접속.사용가능 ? "파일 8칸, 파일당 16384바이트; sync로 저장 장치에 보존\n"
            : "임시 파일 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void 명령(int[] 입력, int 시작, int 길이, int 동작) {
        while (시작 < 길이 && 입력[시작] == ' ') 시작++;
        int 끝 = 길이;
        while (끝 > 시작 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - 시작;
        if (수 < 1 || 수 > 63) { 문자단말.쓰기("올바르지 않은 파일 mbiekolo\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) mbiekolo[칸] = 칸 < 수 ? 입력[시작 + 칸] : 0;
        int 번호 = 찾기(mbiekolo, 수);
        if (번호 == -22) { 문자단말.쓰기("올바르지 않은 파일 mbiekolo\n"); return; }
        if (동작 == 0) {
            편집중 = true; 편집크기 = 0; 넘침 = false;
            문자단말.쓰기("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (번호 < 0) 문자단말.쓰기("파일을 찾을 수 없습니다\n");
        else if (동작 == 1) {
            int 주소 = 장치.파일기억() + 번호 * 최대크기;
            for (int 칸 = 0; 칸 < 크기들[번호]; 칸++) 문자단말.문자(장치.기억읽기(주소 + 칸));
            문자단말.문자(10);
        } else { 이름들[번호 * 64] = 0; 크기들[번호] = 0; 문자단말.쓰기("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int 길이, boolean 줄넘침) {
        if (정확(입력, 길이, ".cancel")) {
            편집중 = false; 문자단말.쓰기("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, 길이, ".save")) {
            편집중 = false;
            if (넘침) { 문자단말.쓰기("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && mbiekolo[수] != 0) 수++;
            int 결과 = 저장(mbiekolo, 수, 편집, 편집크기);
            문자단말.쓰기(결과 >= 0 ? "보존한 바이트 수: " : "보존 실패: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (줄넘침 || 길이 + 1 > 최대크기 - 편집크기) 넘침 = true;
        else {
            for (int 수 = 0; 수 < 길이; 수++) 편집[편집크기++] = 입력[수];
            편집[편집크기++] = 10;
        }
    }

    static void 예제(String 파일, String 내용) {
        for (int 수 = 0; 수 < 64; 수++) mbiekolo[수] = 수 < 파일.length() ? 파일.charAt(수) : 0;
        for (int 수 = 0; 수 < 내용.length(); 수++) 편집[수] = 내용.charAt(수);
        저장(mbiekolo, 파일.length(), 편집, 내용.length());
    }

    static void 준비() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int 묶음 = 장치.자바파일묶음(), 크기 = 장치.자바파일묶음크기();
        if (크기 < 8 || 실행관리.수(묶음) != 0x464a4b4a) { 문자단말.쓰기("올바르지 않은 Java 파일 묶음\n"); return; }
        int 개수 = 실행관리.수(묶음 + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (크기 - 8) / 72) { 문자단말.쓰기("올바르지 않은 Java 파일 목록\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int 항목 = 묶음 + 8 + 수 * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) mbiekolo[칸] = 장치.기억읽기(항목 + 칸);
            while (길이 < 64 && mbiekolo[길이] != 0) 길이++;
            int 위치 = 실행관리.수(항목 + 64), 파일크기 = 실행관리.수(항목 + 68);
            if (!이름검사(mbiekolo, 길이) || 파일크기 < 0 || 파일크기 > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > 크기 - 파일크기) {
                문자단말.쓰기("올바르지 않은 Java 파일 항목\n"); return;
            }
            for (int 칸 = 0; 칸 < 파일크기; 칸++) 편집[칸] = 장치.기억읽기(묶음 + 위치 + 칸);
            if (저장(mbiekolo, 길이, 편집, 파일크기) < 0) { 문자단말.쓰기("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
