// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Birem. 원본 төзәтү_VALUE/төзү_чыганак эштән_туктау_VALUE 시 기존 파일을 보존한다. */
public final class Хәтер_файл_системасы {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] үлчәмен_үзгәртү_Исемлек = new int[8];
    static int[] ачу_COUNT = new int[8], 허가들 = new int[8];
    static int[] исем = new int[64];
    static int[] төзәтү_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean сыешмау_VALUE = false;
    static int төзәтү_үлчәмен_үзгәртү = 0;

    static boolean чек_исем(int[] символ_VALUE_068c2631, int озынлык_VALUE) {
        if (озынлык_VALUE < 1 || озынлык_VALUE > 63) return false;
        for (int 수 = 0; 수 < озынлык_VALUE; 수++) {
            int VALUE = символ_VALUE_068c2631[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return символ_VALUE_068c2631[0] != '.';
    }

    static int FIND_кертү(int[] символ_VALUE_068c2631, int озынлык_VALUE) {
        if (!чек_исем(символ_VALUE_068c2631, озынлык_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + озынлык_VALUE] == 0;
            for (int оя_кертү = 0; оя_кертү < озынлык_VALUE; оя_кертү++) if (이름들[수 * 64 + оя_кертү] != символ_VALUE_068c2631[оя_кертү]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] символ_VALUE_068c2631, int озынлык_VALUE, int[] мәгълүмат, int үлчәмен_үзгәртү) {
        if (!чек_исем(символ_VALUE_068c2631, озынлык_VALUE) || үлчәмен_үзгәртү < 0 || үлчәмен_үзгәртү > мәгълүмат.length) return -22;
        if (үлчәмен_үзгәртү > 최대크기) return -90;
        int INDEX = FIND_кертү(символ_VALUE_068c2631, озынлык_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && ачу_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int адрес = мобиль_VALUE.файл_Хәтер() + INDEX * 최대크기;
        for (int 수 = 0; 수 < үлчәмен_үзгәртү; 수++) мобиль_VALUE.язу_Хәтер(адрес + 수, мәгълүмат[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < озынлык_VALUE ? символ_VALUE_068c2631[수] : 0;
        үлчәмен_үзгәртү_Исемлек[INDEX] = үлчәмен_үзгәртү;
        return үлчәмен_үзгәртү;
    }

    static void кертү_Исемлек() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int оя_кертү = 0; оя_кертү < 64 && 이름들[수 * 64 + оя_кертү] != 0; оя_кертү++) СМС_Терминал.문자(이름들[수 * 64 + оя_кертү]);
            СМС_Терминал.язу("  "); СМС_Терминал.수쓰기(үлчәмен_үзгәртү_Исемлек[수]); СМС_Терминал.язу("байт_VALUE\n");
        }
        СМС_Терминал.язу(Саклагыч_мобиль_тоташу.사용가능 ? "Birem 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Birem 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void команда(int[] 입력, int эшләтү, int озынлык_VALUE, int Гамәл) {
        while (эшләтү < озынлык_VALUE && 입력[эшләтү] == ' ') эшләтү++;
        int 끝 = озынлык_VALUE;
        while (끝 > эшләтү && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - эшләтү;
        if (수 < 1 || 수 > 63) { СМС_Терминал.язу("올바르지 않은 Birem исем\n"); return; }
        for (int оя_кертү = 0; оя_кертү < 64; оя_кертү++) исем[оя_кертү] = оя_кертү < 수 ? 입력[эшләтү + оя_кертү] : 0;
        int INDEX = FIND_кертү(исем, 수);
        if (INDEX == -22) { СМС_Терминал.язу("올바르지 않은 Birem исем\n"); return; }
        if (Гамәл == 0) {
            편집중 = true; төзәтү_үлчәмен_үзгәртү = 0; сыешмау_VALUE = false;
            СМС_Терминал.язу("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) СМС_Терминал.язу("파일을 찾을 수 없습니다\n");
        else if (Гамәл == 1) {
            int адрес = мобиль_VALUE.файл_Хәтер() + INDEX * 최대크기;
            for (int оя_кертү = 0; оя_кертү < үлчәмен_үзгәртү_Исемлек[INDEX]; оя_кертү++) СМС_Терминал.문자(мобиль_VALUE.기억읽기(адрес + оя_кертү));
            СМС_Терминал.문자(10);
        } else { 이름들[INDEX * 64] = 0; үлчәмен_үзгәртү_Исемлек[INDEX] = 0; СМС_Терминал.язу("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int озынлык_VALUE, String 문구) {
        if (озынлык_VALUE != 문구.length()) return false;
        for (int оя_кертү = 0; оя_кертү < озынлык_VALUE; оя_кертү++) if (입력[оя_кертү] != 문구.charAt(оя_кертү)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int озынлык_VALUE, boolean юл_сыешмау) {
        if (정확(입력, озынлык_VALUE, ".cancel")) {
            편집중 = false; СМС_Терминал.язу("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, озынлык_VALUE, ".save")) {
            편집중 = false;
            if (сыешмау_VALUE) { СМС_Терминал.язу("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && исем[수] != 0) 수++;
            int үлчәм = Store_VALUE(исем, 수, төзәтү_VALUE, төзәтү_үлчәмен_үзгәртү);
            СМС_Терминал.язу(үлчәм >= 0 ? "보존한 байт_VALUE 수: " : "보존 эштән_туктау_VALUE: ");
            СМС_Терминал.수쓰기(үлчәм); СМС_Терминал.문자(10);
        } else if (юл_сыешмау || озынлык_VALUE + 1 > 최대크기 - төзәтү_үлчәмен_үзгәртү) сыешмау_VALUE = true;
        else {
            for (int 수 = 0; 수 < озынлык_VALUE; 수++) төзәтү_VALUE[төзәтү_үлчәмен_үзгәртү++] = 입력[수];
            төзәтү_VALUE[төзәтү_үлчәмен_үзгәртү++] = 10;
        }
    }

    static void 예제(String Birem, String Эчтәлек_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) исем[수] = 수 < Birem.length() ? Birem.charAt(수) : 0;
        for (int 수 = 0; 수 < Эчтәлек_VALUE.length(); 수++) төзәтү_VALUE[수] = Эчтәлек_VALUE.charAt(수);
        Store_VALUE(исем, Birem.length(), төзәтү_VALUE, Эчтәлек_VALUE.length());
    }

    static void Әзерләү() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int төркем_VALUE = мобиль_VALUE.자바파일묶음(), үлчәмен_үзгәртү = мобиль_VALUE.자바파일묶음크기();
        if (үлчәмен_үзгәртү < 8 || 실행관리.수(төркем_VALUE) != 0x464a4b4a) { СМС_Терминал.язу("올바르지 않은 Java Birem төркем_VALUE\n"); return; }
        int элемент_COUNT = 실행관리.수(төркем_VALUE + 4);
        if (элемент_COUNT < 0 || элемент_COUNT > 8 || элемент_COUNT > (үлчәмен_үзгәртү - 8) / 72) { СМС_Терминал.язу("올바르지 않은 Java Birem кертү_Исемлек\n"); return; }
        for (int 수 = 0; 수 < элемент_COUNT; 수++) {
            int кертү_VALUE = төркем_VALUE + 8 + 수 * 72, озынлык_VALUE = 0;
            for (int оя_кертү = 0; оя_кертү < 64; оя_кертү++) исем[оя_кертү] = мобиль_VALUE.기억읽기(кертү_VALUE + оя_кертү);
            while (озынлык_VALUE < 64 && исем[озынлык_VALUE] != 0) озынлык_VALUE++;
            int урнаштыру = 실행관리.수(кертү_VALUE + 64), файл_үлчәмен_үзгәртү = 실행관리.수(кертү_VALUE + 68);
            if (!чек_исем(исем, озынлык_VALUE) || файл_үлчәмен_үзгәртү < 0 || файл_үлчәмен_үзгәртү > 최대크기 || урнаштыру < 8 + элемент_COUNT * 72 || урнаштыру > үлчәмен_үзгәртү - файл_үлчәмен_үзгәртү) {
                СМС_Терминал.язу("올바르지 않은 Java Birem кертү_VALUE\n"); return;
            }
            for (int оя_кертү = 0; оя_кертү < файл_үлчәмен_үзгәртү; оя_кертү++) төзәтү_VALUE[оя_кертү] = мобиль_VALUE.기억읽기(төркем_VALUE + урнаштыру + оя_кертү);
            if (Store_VALUE(исем, озынлык_VALUE, төзәтү_VALUE, файл_үлчәмен_үзгәртү) < 0) { СМС_Терминал.язу("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
