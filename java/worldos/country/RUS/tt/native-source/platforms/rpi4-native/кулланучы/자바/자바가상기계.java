// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Birem/스택/Белешмәлекләр/тармак 경계를 үтәргә_команда 중 검사한다. */
public final class 자바가상기계 {
    static int[] Birem = new int[16 * 16384], 임시파일 = new int[16384], файл_исем_СМС = new int[512];
    static int[] константа_тәг = new int[8192], 상가 = new int[8192], константа_SECOND_VALUE = new int[8192], юл_Белешмәлекләр = new int[8192];
    static int[] ысул_исем_СМС = new int[512], ысул_TYPE = new int[512], ысул_керү = new int[512], ысул_биләүче = new int[512];
    static int[] ысул_Start = new int[512], ысул_тәмамлау = new int[512], ысул_Стәк = new int[512], 함수지역 = new int[512];
    static int[] ысул_аргумент_COUNT = new int[512], ысул_аргумент_TYPE = new int[8192], ысул_кайтару = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] локаль_VALUE = new int[16384], локаль_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] кадр_ысул = new int[128], кадр_урнаштыру = new int[128], кадр_Стәк = new int[128], кадр_инструкция = new int[128], инициализацияләү_кадр = new int[128];
    static int[] класс_Билгеләмә_исем = new int[16], класс_Билгеләмә_үлчәмен_үзгәртү = new int[16], 종부모 = new int[16], класс_Билгеләмә_халәт = new int[16], класс_оя_COUNT = new int[16], инициализацияләү_класс_Билгеләмә = new int[16];
    static int[] класс_интерфейс = new int[16 * 16], класс_интерфейс_COUNT = new int[16];
    static int[] оя_исем = new int[512], оя_TYPE = new int[512], оя_биләүче = new int[512], оя_хокук_бирү = new int[512], оя_урнаштыру = new int[512], оя_мәгълүмат = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], МАССИВ_элемент = new int[32768], Store_бөтен_сан = new int[256];
    static int үлчәмен_үзгәртү, 읽기위치, ысул_COUNT, класс_исем, кадр_INDEX = -1, 힙끝 = 1, кайтару_TYPE;
    static int класс_Билгеләмә_COUNT, оя_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, дисплей_COUNT, туплама_COUNT;
    static int 현재가닥, агым_COUNT = 1, кертү_класс_Билгеләмә;
    static int[] агым_кадр = new int[4], агым_халәт = new int[4], агым_объект = new int[4], агым_максат_кыйммәт = new int[4], 가닥대기 = new int[4];
    static boolean Хата, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], класс_агым = new int[16];

    static void эштән_туктау_VALUE(String Word_СМС) {
        if (Хата) return;
        int категория_CODE = 0;
        if (자바도구.같음(Word_СМС, "ArithmeticException: / by zero")) категория_CODE = 4;
        if (자바도구.같음(Word_СМС, "NullPointerException") || 자바도구.같음(Word_СМС, "null or invalid array")) категория_CODE = 5;
        if (자바도구.같음(Word_СМС, "ArrayIndexOutOfBoundsException")) категория_CODE = 7;
        if (자바도구.같음(Word_СМС, "StringIndexOutOfBoundsException")) категория_CODE = 8;
        if (자바도구.같음(Word_СМС, "NumberFormatException")) категория_CODE = 10;
        if (자바도구.같음(Word_СМС, "FileNotFoundException: file open failed")) категория_CODE = 12;
        if (자바도구.같음(Word_СМС, "IOException: stream closed") || 자바도구.같음(Word_СМС, "IOException: read failed") || 자바도구.같음(Word_СМС, "IOException: write failed")) категория_CODE = 11;
        if (자바도구.같음(Word_СМС, "ClassCastException")) категория_CODE = 14;
        if (자바도구.같음(Word_СМС, "NegativeArraySizeException")) категория_CODE = 15;
        if (категория_CODE != 0 && кадр_INDEX >= 0) { 예외던짐(категория_CODE, Word_СМС); return; }
        кулланучы.язу("JVM error: "); кулланучы.язу(Word_СМС); кулланучы.язу_символ_VALUE(10); Хата = true;
    }
    static boolean клип(int эшләтү, int озынлык_VALUE) {
        if (эшләтү < 0 || эшләтү >= Birem.length || озынлык_VALUE < 0) return false;
        int класс_Билгеләмә = эшләтү / 16384;
        return эшләтү % 16384 <= класс_Билгеләмә_үлчәмен_үзгәртү[класс_Билгеләмә] && озынлык_VALUE <= класс_Билгеләмә_үлчәмен_үзгәртү[класс_Билгеләмә] - эшләтү % 16384;
    }
    static int байт_VALUE() {
        if (!клип(읽기위치, 1)) { эштән_туктау_VALUE("truncated class file"); return 0; }
        return Birem[읽기위치++];
    }
    static int 짧은수() { return байт_VALUE() << 8 | байт_VALUE(); }
    static int бөтен_сан() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int озынлык_VALUE) { if (!клип(읽기위치, озынлык_VALUE)) эштән_туктау_VALUE("invalid attribute size"); else 읽기위치 += озынлык_VALUE; }
    static boolean чек_константа(int 수, int 종류) {
        if (수 <= 0 || 수 >= константа_тәг.length || константа_тәг[수] != 종류) { эштән_туктау_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int эшләтү, int озынлык_VALUE, String Word_СМС) {
        if (!клип(эшләтү, озынлык_VALUE)) return false;
        int 읽는자리 = эшләтү, 끝 = эшләтү + озынлык_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_СМС.length(); Loop_INDEX++) {
            int символ_коды = Word_СМС.charAt(Loop_INDEX);
            if (символ_коды > 0 && символ_коды < 128) { if (읽는자리 >= 끝 || Birem[읽는자리++] != символ_коды) return false; }
            else if (символ_коды < 2048) {
                if (읽는자리 + 2 > 끝 || Birem[읽는자리++] != (192 | (символ_коды >> 6)) || Birem[읽는자리++] != (128 | (символ_коды & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Birem[읽는자리++] != (224 | (символ_коды >> 12)) || Birem[읽는자리++] != (128 | ((символ_коды >> 6) & 63)) || Birem[읽는자리++] != (128 | (символ_коды & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_СМС(int константа_VALUE, String Word_СМС) { return чек_константа(константа_VALUE, 1) && 구간(상가[константа_VALUE], константа_SECOND_VALUE[константа_VALUE], Word_СМС); }
    static boolean 같은말(int 가, int 나) {
        if (!чек_константа(가, 1) || !чек_константа(나, 1) || константа_SECOND_VALUE[가] != константа_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < константа_SECOND_VALUE[가]; 수++) if (Birem[상가[가] + 수] != Birem[상가[나] + 수]) return false;
        return true;
    }
    static int класс_исем_СМС(int 수) { return чек_константа(수, 7) && чек_константа(상가[수], 1) ? 상가[수] : 0; }
    static int Белешмәлекләр_исем(int 수) { return чек_константа(수, 12) && чек_константа(상가[수], 1) ? 상가[수] : 0; }
    static int Белешмәлекләр_TYPE(int 수) { return чек_константа(수, 12) && чек_константа(константа_SECOND_VALUE[수], 1) ? константа_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean Буш_TYPE) {
        if (읽기위치 >= 끝) { эштән_туктау_VALUE("invalid descriptor"); return 0; }
        int VALUE = байт_VALUE();
        if (VALUE == 'V' && Буш_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int эшләтү = 읽기위치;
            while (읽기위치 < 끝 && Birem[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == эшләтү) эштән_туктау_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        эштән_туктау_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int ФУНКЦИЯ_VALUE) {
        int 이전 = 읽기위치, 수 = ысул_TYPE[ФУНКЦИЯ_VALUE];
        if (!чек_константа(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + константа_SECOND_VALUE[수];
        if (байт_VALUE() != '(') эштән_туктау_VALUE("invalid method descriptor");
        int элемент_COUNT = 0;
        while (!Хата && 읽기위치 < 끝 && Birem[읽기위치] != ')') {
            if (элемент_COUNT == 16) { эштән_туктау_VALUE("too many method arguments"); break; }
            ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + элемент_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || байт_VALUE() != ')') эштән_туктау_VALUE("invalid method descriptor");
        ысул_кайтару[ФУНКЦИЯ_VALUE] = 서술형(끝, true); ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE] = элемент_COUNT;
        if (읽기위치 != 끝) эштән_туктау_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return ысул_биләүче[кадр_ысул[кадр_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int элемент_COUNT = 짧은수();
        for (int 수 = 0; 수 < элемент_COUNT && !Хата; 수++) { чек_константа(상번호(), 1); 건너(бөтен_сан()); }
    }
    static int команда_озынлык(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int урнаштыру_бөтен_сан(int 읽는자리) {
        if (!клип(읽는자리, 4)) { эштән_туктау_VALUE("truncated bytecode operand"); return 0; }
        return Birem[읽는자리] << 24 | Birem[읽는자리 + 1] << 16 | Birem[읽는자리 + 2] << 8 | Birem[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int эшләтү, int 끝) {
        int VALUE = Birem[읽는자리], озынлык_VALUE = команда_озынлык(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_урнаштыру = 읽는자리 + 1;
            while ((BASE_урнаштыру - эшләтү) % 4 != 0) BASE_урнаштыру++;
            if (끝 - BASE_урнаштыру < (VALUE == 170 ? 12 : 8)) return 0;
            int кертү_COUNT = VALUE == 170 ? урнаштыру_бөтен_сан(BASE_урнаштыру + 8) - урнаштыру_бөтен_сан(BASE_урнаштыру + 4) + 1 : урнаштыру_бөтен_сан(BASE_урнаштыру + 4);
            if (кертү_COUNT < 0 || кертү_COUNT > 2048) return 0;
            озынлык_VALUE = BASE_урнаштыру - 읽는자리 + (VALUE == 170 ? 12 + 4 * кертү_COUNT : 8 + 8 * кертү_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_мәгълүмат = Birem[읽는자리 + 1]; озынлык_VALUE = Word_мәгълүмат == 132 ? 6 : (Word_мәгълүмат == 21 || Word_мәгълүмат == 25 || Word_мәгълүмат == 54 || Word_мәгълүмат == 58) ? 4 : 0;
        }
        return озынлык_VALUE > 0 && озынлык_VALUE <= 끝 - 읽는자리 ? озынлык_VALUE : 0;
    }
    static void чек_күчерү_урыны_VALUE(int күчерү_урыны_VALUE, int ФУНКЦИЯ_VALUE) {
        if (күчерү_урыны_VALUE < ысул_Start[ФУНКЦИЯ_VALUE] || күчерү_урыны_VALUE >= ысул_тәмамлау[ФУНКЦИЯ_VALUE] || 경계[күчерү_урыны_VALUE] != ФУНКЦИЯ_VALUE + 1) эштән_туктау_VALUE("invalid branch target");
    }
    static void 클래스읽기(int класс_Билгеләмә) {
        현재읽는종 = класс_Билгеләмә; 읽기위치 = класс_Билгеләмә * 16384; үлчәмен_үзгәртү = 읽기위치 + класс_Билгеләмә_үлчәмен_үзгәртү[класс_Билгеләмә];
        if (бөтен_сан() != 0xcafebabe) { эштән_туктау_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), версия_VALUE = 짧은수();
        if (версия_VALUE < 45 || версия_VALUE > 52 || 부판 != 0) { эштән_туктау_VALUE("supported class versions: 45..52, minor 0"); return; }
        int константа_COUNT = 짧은수(), BASE_урнаштыру = класс_Билгеләмә * 512;
        if (константа_COUNT < 1 || константа_COUNT > 512) { эштән_туктау_VALUE("constant pool limit (511)"); return; }
        for (int кертү_COUNT = 1; кертү_COUNT < константа_COUNT && !Хата; кертү_COUNT++) {
            int 수 = BASE_урнаштыру + кертү_COUNT, 종류 = байт_VALUE(); константа_тәг[수] = 종류;
            if (종류 == 1) { константа_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(константа_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = бөтен_сан();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); константа_SECOND_VALUE[수] = 상번호(); }
            else эштән_туктау_VALUE("unsupported constant type");
        }
        int рөхсәт_VALUE = 짧은수();
        if ((рөхсәт_VALUE & (0x2000 | 0x4000)) != 0) эштән_туктау_VALUE("annotation/enum class unsupported");
        класс_Билгеләмә_исем[класс_Билгеләмә] = класс_исем_СМС(상번호());
        종부모[класс_Билгеләмә] = класс_исем_СМС(상번호());
        int интерфейс_COUNT = 짧은수(); if (интерфейс_COUNT > 16) { эштән_туктау_VALUE("interface count limit"); return; }
        класс_интерфейс_COUNT[класс_Билгеләмә] = интерфейс_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < интерфейс_COUNT; Loop_INDEX++) класс_интерфейс[класс_Билгеләмә * 16 + Loop_INDEX] = класс_исем_СМС(상번호());
        int кыр_COUNT = 짧은수();
        if (кыр_COUNT > 512 - оя_COUNT) { эштән_туктау_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < кыр_COUNT && !Хата; Loop_INDEX++) {
            int файл_INDEX = оя_COUNT++; оя_биләүче[файл_INDEX] = класс_Билгеләмә; оя_хокук_бирү[файл_INDEX] = 짧은수(); оя_исем[файл_INDEX] = 상번호(); оя_TYPE[файл_INDEX] = 상번호();
            чек_константа(оя_исем[файл_INDEX], 1); чек_константа(оя_TYPE[файл_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[оя_TYPE[файл_INDEX]]; int категория_CODE = 서술형(읽기위치 + константа_SECOND_VALUE[оя_TYPE[файл_INDEX]], false); 읽기위치 = 보존값;
            if ((оя_хокук_бирү[файл_INDEX] & 8) == 0) оя_урнаштыру[файл_INDEX] = класс_оя_COUNT[класс_Билгеләмә]++;
            int аергыч_мәгълүмат = 짧은수();
            for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < аергыч_мәгълүмат && !Хата; Эчке_берләштерү_урнаштыру++) {
                int исем_константа = 상번호(), 유효길이 = бөтен_сан();
                if (Word_СМС(исем_константа, "ConstantValue") && 유효길이 == 2) {
                    int мәгълүмат_VALUE = 상번호();
                    if (категория_CODE == 1 && чек_константа(мәгълүмат_VALUE, 3)) оя_мәгълүмат[файл_INDEX] = 상가[мәгълүмат_VALUE];
                    else if (категория_CODE == 2 && чек_константа(мәгълүмат_VALUE, 8)) оя_мәгълүмат[файл_INDEX] = константа_СМС(상가[мәгълүмат_VALUE]);
                } else 건너(유효길이);
            }
        }
        int элемент_COUNT = 짧은수();
        if (элемент_COUNT > 512 - ысул_COUNT) { эштән_туктау_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < элемент_COUNT && !Хата; Loop_INDEX++) {
            int 수 = ысул_COUNT++; ысул_биләүче[수] = класс_Билгеләмә;
            ысул_керү[수] = 짧은수(); ысул_исем_СМС[수] = 상번호(); ысул_TYPE[수] = 상번호();
            чек_константа(ысул_исем_СМС[수], 1); 서술읽기(수);
            if ((ысул_керү[수] & 8) == 0) {
                if (ысул_аргумент_COUNT[수] == 16) { эштән_туктау_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = ысул_аргумент_COUNT[수]; 비교자리 > 0; 비교자리--) ысул_аргумент_TYPE[수 * 16 + 비교자리] = ысул_аргумент_TYPE[수 * 16 + 비교자리 - 1];
                ысул_аргумент_TYPE[수 * 16] = 2; ысул_аргумент_COUNT[수]++;
            }
            if ((ысул_керү[수] & 0x100) != 0) эштән_туктау_VALUE("user native method unsupported");
            if (Word_СМС(ысул_исем_СМС[수], "<clinit>")) инициализацияләү_класс_Билгеләмә[класс_Билгеләмә] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (ысул_биләүче[앞] == класс_Билгеләмә && 같은말(ысул_исем_СМС[앞], ысул_исем_СМС[수]) && 같은말(ысул_TYPE[앞], ысул_TYPE[수])) эштән_туктау_VALUE("duplicate method");
            int аергыч_COUNT = 짧은수();
            for (int аергыч_VALUE_286d43f0 = 0; аергыч_VALUE_286d43f0 < аергыч_COUNT && !Хата; аергыч_VALUE_286d43f0++) {
                int исем = 상번호(), озынлык_VALUE = бөтен_сан(), эшләтү = 읽기위치;
                if (!клип(эшләтү, озынлык_VALUE)) { эштән_туктау_VALUE("truncated method attribute"); break; }
                if (Word_СМС(исем, "Code")) {
                    if (ысул_Start[수] != 0) эштән_туктау_VALUE("duplicate Code attribute");
                    ысул_Стәк[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_озынлык = бөтен_сан();
                    if (ысул_Стәк[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < ысул_аргумент_COUNT[수]
                        || CODE_озынлык < 1 || CODE_озынлык > 8192) эштән_туктау_VALUE("method memory limits exceeded");
                    ысул_Start[수] = 읽기위치; 건너(CODE_озынлык); ысул_тәмамлау[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { эштән_туктау_VALUE("exception table limit"); return; }
                    for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 잡는수; Эчке_берләштерү_урнаштыру++) {
                        int хата_Белешмәлекләр = 잡기수++; 잡기함수[хата_Белешмәлекләр] = 수;
                        잡기시작[хата_Белешмәлекләр] = ысул_Start[수] + 짧은수(); 잡기끝[хата_Белешмәлекләр] = ысул_Start[수] + 짧은수();
                        잡기위치[хата_Белешмәлекләр] = ысул_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[хата_Белешмәлекләр] = 부호값 == 0 ? 0 : класс_исем_СМС(부호값);
                    }
                    속성건너();
                    if (읽기위치 != эшләтү + озынлык_VALUE) эштән_туктау_VALUE("Code attribute size mismatch");
                } else 건너(озынлык_VALUE);
            }
            if ((ысул_керү[수] & 0x400) != 0) continue;
            if (ысул_Start[수] == 0) эштән_туктау_VALUE("missing Code attribute");
            int оя_кертү = ысул_Start[수];
            while (оя_кертү < ысул_тәмамлау[수] && !Хата) {
                int озынлык_VALUE = 길이읽기(оя_кертү, ысул_Start[수], ысул_тәмамлау[수]);
                if (озынлык_VALUE == 0) { эштән_туктау_VALUE("unsupported or truncated bytecode"); break; }
                경계[оя_кертү] = 수 + 1; оя_кертү += озынлык_VALUE;
            }
            оя_кертү = ысул_Start[수];
            while (оя_кертү < ысул_тәмамлау[수] && !Хата) {
                int VALUE = Birem[оя_кертү];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) чек_күчерү_урыны_VALUE(оя_кертү + (short)(Birem[оя_кертү + 1] << 8 | Birem[оя_кертү + 2]), 수);
                if (VALUE == 200) чек_күчерү_урыны_VALUE(оя_кертү + урнаштыру_бөтен_сан(оя_кертү + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = оя_кертү + 1; while ((읽는자리 - ысул_Start[수]) % 4 != 0) 읽는자리++;
                    чек_күчерү_урыны_VALUE(оя_кертү + урнаштыру_бөтен_сан(읽는자리), 수);
                    int кертү_COUNT = VALUE == 170 ? урнаштыру_бөтен_сан(읽는자리 + 8) - урнаштыру_бөтен_сан(읽는자리 + 4) + 1 : урнаштыру_бөтен_сан(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < кертү_COUNT; Эчке_берләштерү_урнаштыру++) чек_күчерү_урыны_VALUE(оя_кертү + урнаштыру_бөтен_сан(읽는자리 + Эчке_берләштерү_урнаштыру * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                оя_кертү += 길이읽기(оя_кертү, ысул_Start[수], ысул_тәмамлау[수]);
            }
            for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 잡기수; Эчке_берләштерү_урнаштыру++) if (잡기함수[Эчке_берләштерү_урнаштыру] == 수) {
                чек_күчерү_урыны_VALUE(잡기시작[Эчке_берләштерү_урнаштыру], 수); чек_күчерү_урыны_VALUE(잡기위치[Эчке_берләштерү_урнаштыру], 수);
                if (잡기끝[Эчке_берләштерү_урнаштыру] != ысул_тәмамлау[수]) чек_күчерү_урыны_VALUE(잡기끝[Эчке_берләштерү_урнаштыру], 수);
                if (잡기시작[Эчке_берләштерү_урнаштыру] >= 잡기끝[Эчке_берләштерү_урнаштыру]) эштән_туктау_VALUE("invalid exception range");
            }
        }
        if (!Хата) 속성건너();
        if (읽기위치 != үлчәмен_үзгәртү) эштән_туктау_VALUE("extra class file data");
    }
    static int атап_бирү_Саклагыч(int 종류, int озынлык_VALUE) { return 새기억(종류, озынлык_VALUE); }
    static boolean объект_VALUE(int Белешмәлекләр, int 종류) {
        if (!객체유효(Белешмәлекләр)) return false;
        if (힙[Белешмәлекләр] != 종류) { эштән_туктау_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int константа_СМС(int INDEX) {
        if (!чек_константа(INDEX, 1)) return 0;
        if (юл_Белешмәлекләр[INDEX] != 0) return юл_Белешмәлекләр[INDEX];
        int Белешмәлекләр = атап_бирү_Саклагыч(1, константа_SECOND_VALUE[INDEX]); if (Хата) return 0;
        int 끝 = 상가[INDEX] + константа_SECOND_VALUE[INDEX], 수 = 상가[INDEX], озынлык_VALUE = 0;
        while (수 < 끝 && !Хата) {
            int VALUE = Birem[수++];
            if (VALUE == 0) эштән_туктау_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Киләсе_элемент = Birem[수++];
                if ((Киләсе_элемент & 192) != 128) эштән_туктау_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Киләсе_элемент & 63;
                if (VALUE != 0 && VALUE < 128) эштән_туктау_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Birem[수++], 나 = Birem[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) эштән_туктау_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) эштән_туктау_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) эштән_туктау_VALUE("invalid modified UTF-8");
            힙[Белешмәлекләр + 2 + озынлык_VALUE++] = VALUE;
        }
        힙[Белешмәлекләр + 1] = озынлык_VALUE; юл_Белешмәлекләр[INDEX] = Белешмәлекләр; return Белешмәлекләр;
    }
    static int хост_символ(String VALUE) {
        int Белешмәлекләр = атап_бирү_Саклагыч(1, VALUE.length()); if (Хата) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Белешмәлекләр + 2 + 수] = VALUE.charAt(수);
        return Белешмәлекләр;
    }
    static void язу_СМС(int Белешмәлекләр) {
        if (Белешмәлекләр == 0) { кулланучы.язу("null"); return; }
        if (!объект_VALUE(Белешмәлекләр, 1)) return;
        for (int 수 = 0; 수 < 힙[Белешмәлекләр + 1]; 수++) кулланучы.язу_символ_VALUE(힙[Белешмәлекләр + 2 + 수]);
    }
    static int сан_символ(int VALUE) {
        int Белешмәлекләр = атап_бирү_Саклагыч(1, 11); if (Хата) return 0;
        int озынлык_VALUE = 0;
        if (VALUE < 0) 힙[Белешмәлекләр + 2 + озынлык_VALUE++] = '-'; else VALUE = -VALUE;
        int урнаштыру_INDEX = 1000000000; boolean эшләтү = false;
        while (урнаштыру_INDEX != 0) {
            int 수 = -(VALUE / урнаштыру_INDEX);
            if (수 != 0 || эшләтү || урнаштыру_INDEX == 1) { 힙[Белешмәлекләр + 2 + озынлык_VALUE++] = '0' + 수; эшләтү = true; }
            VALUE %= урнаштыру_INDEX; урнаштыру_INDEX /= 10;
        }
        힙[Белешмәлекләр + 1] = озынлык_VALUE; return Белешмәлекләр;
    }
    static int 정수해독(int Белешмәлекләр) {
        if (!объект_VALUE(Белешмәлекләр, 1)) return 0;
        int озынлык_VALUE = 힙[Белешмәлекләр + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (озынлык_VALUE > 0 && (힙[Белешмәлекләр + 2] == '-' || 힙[Белешмәлекләр + 2] == '+')) { 음수 = 힙[Белешмәлекләр + 2] == '-'; 수++; }
        if (수 == озынлык_VALUE) эштән_туктау_VALUE("NumberFormatException");
        for (; 수 < озынлык_VALUE && !Хата; 수++) {
            int сан_VALUE = 힙[Белешмәлекләр + 2 + 수] - '0';
            if (сан_VALUE < 0 || сан_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && сан_VALUE > (음수 ? 8 : 7)) эштән_туктау_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - сан_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Хата) return;
        if (кадр_INDEX < 0 || кадр_Стәк[кадр_INDEX] >= ысул_Стәк[кадр_ысул[кадр_INDEX]]) { эштән_туктау_VALUE("operand stack overflow"); return; }
        int оя_кертү = кадр_INDEX * 128 + кадр_Стәк[кадр_INDEX]++; 스택값[оя_кертү] = VALUE; 스택형[оя_кертү] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Хата) return 0;
        if (кадр_INDEX < 0 || кадр_Стәк[кадр_INDEX] < 1) { эштән_туктау_VALUE("operand stack underflow"); return 0; }
        int оя_кертү = кадр_INDEX * 128 + --кадр_Стәк[кадр_INDEX]; кайтару_TYPE = 스택형[оя_кертү];
        if (TYPE_VALUE != 0 && кайтару_TYPE != TYPE_VALUE) эштән_туктау_VALUE("operand type mismatch");
        if (кайтару_TYPE == 2) саклау_VALUE(스택값[оя_кертү]);
        return 스택값[оя_кертү];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[кадр_ысул[кадр_INDEX]] || INDEX < 0 || локаль_TYPE[кадр_INDEX * 128 + INDEX] != TYPE_VALUE) { эштән_туктау_VALUE("invalid or uninitialized local"); return; }
        넣기(локаль_VALUE[кадр_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void язу_локаль(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[кадр_ысул[кадр_INDEX]] || INDEX < 0) { эштән_туктау_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); локаль_VALUE[кадр_INDEX * 128 + INDEX] = VALUE; локаль_TYPE[кадр_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int урнаштыру = кадр_урнаштыру[кадр_INDEX];
        if (урнаштыру < ысул_Start[кадр_ысул[кадр_INDEX]] || урнаштыру >= ысул_тәмамлау[кадр_ысул[кадр_INDEX]]) { эштән_туктау_VALUE("instruction pointer out of range"); return 0; }
        кадр_урнаштыру[кадр_INDEX]++; return Birem[урнаштыру];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void күчерү_VALUE(int урнаштыру) {
        int ФУНКЦИЯ_VALUE = кадр_ысул[кадр_INDEX];
        if (урнаштыру < ысул_Start[ФУНКЦИЯ_VALUE] || урнаштыру >= ысул_тәмамлау[ФУНКЦИЯ_VALUE] || 경계[урнаштыру] != ФУНКЦИЯ_VALUE + 1) эштән_туктау_VALUE("invalid branch target");
        else кадр_урнаштыру[кадр_INDEX] = урнаштыру;
    }
    static void 호출(int ФУНКЦИЯ_VALUE) {
        if (кадр_INDEX % 32 == 31) { эштән_туктау_VALUE("call stack limit (32)"); return; }
        int Киләсе_элемент = кадр_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) локаль_TYPE[Киләсе_элемент * 128 + 수] = 0;
        for (int 수 = ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE] - 1; 수 >= 0; 수--) {
            локаль_VALUE[Киләсе_элемент * 128 + 수] = 빼기(ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수]); локаль_TYPE[Киләсе_элемент * 128 + 수] = ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수];
        }
        if (Хата) return;
        кадр_INDEX = Киләсе_элемент; инициализацияләү_кадр[кадр_INDEX] = 0; кадр_ысул[кадр_INDEX] = ФУНКЦИЯ_VALUE; кадр_урнаштыру[кадр_INDEX] = ысул_Start[ФУНКЦИЯ_VALUE]; кадр_Стәк[кадр_INDEX] = 0;
    }
    static void кайтару_үлчәм(int TYPE_VALUE) {
        if (TYPE_VALUE != ысул_кайтару[кадр_ысул[кадр_INDEX]]) { эштән_туктау_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (инициализацияләү_кадр[кадр_INDEX] != 0) класс_Билгеләмә_халәт[инициализацияләү_кадр[кадр_INDEX] - 1] = 2;
        if (틀잠금[кадр_INDEX] != 0) { 잠금풀기(틀잠금[кадр_INDEX]); 틀잠금[кадр_INDEX] = 0; }
        кадр_INDEX--; if (кадр_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] агым_файл_исем = new int[64];
    static void файл_агым_CALL(int биләүче_VALUE, int исем, int формат_VALUE, int команда) {
        boolean 출력 = Word_СМС(биләүче_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (команда == 183 && Word_СМС(исем, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_СМС(формат_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_СМС(формат_VALUE, "(Ljava/lang/String;)V")) { эштән_туктау_VALUE("unsupported file stream constructor"); return; }
            int файл_кертү_исем = 빼기(2), агым_VALUE = 빼기(2);
            if (!объект_VALUE(файл_кертү_исем, 1) || !объект_VALUE(агым_VALUE, 종류) || Хата) return;
            if (힙[агым_VALUE + 3] != 0) { эштән_туктау_VALUE("file stream already initialized"); return; }
            int озынлык_VALUE = 힙[файл_кертү_исем + 1];
            if (озынлык_VALUE < 1 || озынлык_VALUE > 63) { эштән_туктау_VALUE("invalid file name length"); return; }
            for (int оя_кертү = 0; оя_кертү < озынлык_VALUE; оя_кертү++) {
                int VALUE = 힙[файл_кертү_исем + 2 + оя_кертү];
                if (VALUE < 1) { эштән_туктау_VALUE("invalid file stream path"); return; }
                агым_файл_исем[оя_кертү] = VALUE;
            }
            агым_файл_исем[озынлык_VALUE] = 0;
            int 서술자 = кулланучы.파일서술자열기(агым_файл_исем, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { эштән_туктау_VALUE("FileNotFoundException: file open failed"); return; }
            힙[агым_VALUE + 2] = 서술자; 힙[агым_VALUE + 3] = 1;
            return;
        }
        if (команда != 182) { эштән_туктау_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_СМС(исем, "write") || !출력 && Word_СМС(исем, "read"))
            && (Word_СМС(формат_VALUE, 출력 ? "([B)V" : "([B)I") || Word_СМС(формат_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean клип_VALUE = Word_СМС(формат_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int кертү_COUNT = клип_VALUE ? 빼기(1) : 0, 시작점 = клип_VALUE ? 빼기(1) : 0, мәгълүмат_МАССИВ = 빼기(2), объект_Белешмәлекләр = 빼기(2);
            if (!объект_VALUE(мәгълүмат_МАССИВ, 20) || !объект_VALUE(объект_Белешмәлекләр, 종류)) return;
            if (!клип_VALUE) кертү_COUNT = 힙[мәгълүмат_МАССИВ + 1];
            if (시작점 < 0 || кертү_COUNT < 0 || 시작점 > 힙[мәгълүмат_МАССИВ + 1] - кертү_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[объект_Белешмәлекләр + 3] == 0 || 힙[объект_Белешмәлекләр + 2] < 0) { эштән_туктау_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < кертү_COUNT && !Хата) {
                int 반환값 = 출력 ? кулланучы.파일한바이트쓰기(힙[объект_Белешмәлекләр + 2], 힙[мәгълүмат_МАССИВ + 2 + 시작점 + 완료수]) : кулланучы.파일한바이트읽기(힙[объект_Белешмәлекләр + 2]);
                if (반환값 < 0) { эштән_туктау_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[мәгълүмат_МАССИВ + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(кертү_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_СМС(исем, "flush") && Word_СМС(формат_VALUE, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 종류) && 힙[объект_Белешмәлекләр + 2] < 0) эштән_туктау_VALUE("IOException: stream closed"); return; }
        int Гамәл = -1, VALUE = 0;
        if (Word_СМС(исем, "close") && Word_СМС(формат_VALUE, "()V")) Гамәл = 0;
        if (!출력 && Word_СМС(исем, "read") && Word_СМС(формат_VALUE, "()I")) Гамәл = 1;
        if (출력 && Word_СМС(исем, "write") && Word_СМС(формат_VALUE, "(I)V")) { Гамәл = 2; VALUE = 빼기(1); }
        if (Гамәл < 0) { эштән_туктау_VALUE("unsupported file stream method"); return; }
        int агым_VALUE = 빼기(2);
        if (!объект_VALUE(агым_VALUE, 종류) || Хата) return;
        if (힙[агым_VALUE + 3] == 0) { эштән_туктау_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[агым_VALUE + 2];
        if (Гамәл == 0) {
            if (서술자 >= 0 && кулланучы.파일서술자닫기(서술자) < 0) эштән_туктау_VALUE("IOException: close failed");
            힙[агым_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { эштән_туктау_VALUE("IOException: stream closed"); return; }
        if (Гамәл == 1) {
            int үлчәм = кулланучы.파일한바이트읽기(서술자);
            if (үлчәм < -1) эштән_туктау_VALUE("IOException: read failed"); else 넣기(үлчәм == 256 ? -1 : үлчәм, 1);
        } else if (кулланучы.파일한바이트쓰기(서술자, VALUE) != 1) эштән_туктау_VALUE("IOException: write failed");
    }
    static void CALL_ысул(int INDEX, int команда) {
        if (INDEX <= 0 || INDEX >= константа_тәг.length || (константа_тәг[INDEX] != 10 && константа_тәг[INDEX] != 11)) { эштән_туктау_VALUE("invalid method reference"); return; }
        int биләүче_VALUE = класс_исем_СМС(상가[INDEX]), исем = Белешмәлекләр_исем(константа_SECOND_VALUE[INDEX]), формат_VALUE = Белешмәлекләр_TYPE(константа_SECOND_VALUE[INDEX]);
        if (Хата) return;
        if (기본호출(биләүче_VALUE, исем, формат_VALUE, команда)) return;
        if (Word_СМС(биләүче_VALUE, "java/io/FileInputStream") || Word_СМС(биләүче_VALUE, "java/io/FileOutputStream")) {
            файл_агым_CALL(биләүче_VALUE, исем, формат_VALUE, команда); return;
        }
        if (команда == 184 && Word_СМС(биләүче_VALUE, "java/lang/Integer") && Word_СМС(исем, "parseInt") && Word_СМС(формат_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (команда == 182 && Word_СМС(биләүче_VALUE, "java/io/PrintStream") && (Word_СМС(исем, "println") || Word_СМС(исем, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_СМС(формат_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_СМС(формат_VALUE, "()V") || !Word_СМС(исем, "println")) эштән_туктау_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) эштән_туктау_VALUE("invalid PrintStream receiver");
            if (Хата) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) кулланучы.язу(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) кулланучы.язу_символ_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) язу_СМС(VALUE);
            if (Word_СМС(исем, "println")) кулланучы.язу_символ_VALUE(10);
            return;
        }
        if (команда == 182 && Word_СМС(биләүче_VALUE, "java/lang/String")) {
            if (Word_СМС(исем, "length") && Word_СМС(формат_VALUE, "()I")) {
                int Белешмәлекләр = 빼기(2); if (объект_VALUE(Белешмәлекләр, 1)) 넣기(힙[Белешмәлекләр + 1], 1); return;
            }
            if (Word_СМС(исем, "charAt") && Word_СМС(формат_VALUE, "(I)C")) {
                int аскы_юл_VALUE = 빼기(1), Белешмәлекләр = 빼기(2);
                if (объект_VALUE(Белешмәлекләр, 1)) {
                    if (аскы_юл_VALUE < 0 || аскы_юл_VALUE >= 힙[Белешмәлекләр + 1]) эштән_туктау_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Белешмәлекләр + 2 + аскы_юл_VALUE], 1);
                }
                return;
            }
        }
        if (Word_СМС(биләүче_VALUE, "java/lang/StringBuilder")) {
            if (команда == 183 && Word_СМС(исем, "<init>") && Word_СМС(формат_VALUE, "()V")) { объект_VALUE(빼기(2), 4); return; }
            if (команда == 182 && Word_СМС(исем, "toString") && Word_СМС(формат_VALUE, "()Ljava/lang/String;")) {
                int Белешмәлекләр = 빼기(2); if (объект_VALUE(Белешмәлекләр, 4)) 넣기(힙[Белешмәлекләр + 2] == 0 ? хост_символ("") : 힙[Белешмәлекләр + 2], 2); return;
            }
            if (команда == 182 && Word_СМС(исем, "append")) {
                int Mäten = 0;
                if (Word_СМС(формат_VALUE, "(I)Ljava/lang/StringBuilder;")) Mäten = сан_символ(빼기(1));
                else if (Word_СМС(формат_VALUE, "(Z)Ljava/lang/StringBuilder;")) Mäten = хост_символ(빼기(1) == 0 ? "false" : "true");
                else if (Word_СМС(формат_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Mäten = атап_бирү_Саклагыч(1, 1); if (!Хата) 힙[Mäten + 2] = VALUE & 65535;
                }
                else if (Word_СМС(формат_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Mäten = 빼기(2); if (Mäten == 0) Mäten = хост_символ("null"); }
                else { эштән_туктау_VALUE("unsupported StringBuilder append"); return; }
                int Белешмәлекләр = 빼기(2); if (!объект_VALUE(Белешмәлекләр, 4) || !объект_VALUE(Mäten, 1)) return;
                int 앞 = 힙[Белешмәлекләр + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Артка_VALUE_озынлык = 힙[Mäten + 1];
                int 새글 = атап_бирү_Саклагыч(1, 앞길이 + Артка_VALUE_озынлык); if (Хата) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Артка_VALUE_озынлык; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Mäten + 2 + 수];
                힙[Белешмәлекләр + 2] = 새글; 넣기(Белешмәлекләр, 2); return;
            }
        }
        int класс_Билгеләмә = FIND_класс_Билгеләмә(биләүче_VALUE); if (класс_Билгеләмә < 0 || Хата) return;
        int файл_INDEX = FIND_ысул(класс_Билгеләмә, исем, формат_VALUE);
        if (файл_INDEX < 0) {
            for (int символ_коды = класс_Билгеләмә, кертү_COUNT = 0; символ_коды >= 0 && кертү_COUNT < 16; кертү_COUNT++, символ_коды = 부모종(символ_коды))
                if (Word_СМС(종부모[символ_коды], "java/lang/Thread")) { 가닥호출(исем, формат_VALUE, команда); return; }
            эштән_туктау_VALUE("NoSuchMethodError"); return;
        }
        if (((ысул_керү[файл_INDEX] & 8) != 0) != (команда == 184)) { эштән_туктау_VALUE("method static/instance mismatch"); return; }
        if (команда == 184) { if (!инициализацияләү(ысул_биләүче[файл_INDEX], кадр_инструкция[кадр_INDEX])) return; }
        else {
            int 읽는자리 = кадр_Стәк[кадр_INDEX] - ысул_аргумент_COUNT[файл_INDEX];
            if (읽는자리 < 0 || 스택형[кадр_INDEX * 128 + 읽는자리] != 2) { эштән_туктау_VALUE("invalid method receiver"); return; }
            int объект_Белешмәлекләр = 스택값[кадр_INDEX * 128 + 읽는자리];
            if (!객체유효(объект_Белешмәлекләр)) return;
            if (힙[объект_Белешмәлекләр] < 32 || !종포함(힙[объект_Белешмәлекләр] - 32, биләүче_VALUE)) { эштән_туктау_VALUE("method receiver type mismatch"); return; }
            if (команда != 183) файл_INDEX = FIND_ысул(힙[объект_Белешмәлекләр] - 32, исем, формат_VALUE);
        }
        if (файл_INDEX < 0 || (ысул_керү[файл_INDEX] & 0x400) != 0) { эштән_туктау_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((ысул_керү[файл_INDEX] & 32) != 0) {
            if (команда == 184) { int символ_коды = ысул_биләүче[файл_INDEX]; if (종잠금[символ_коды] == 0) 종잠금[символ_коды] = атап_бирү_Саклагыч(8, 0); 잠금참조 = 종잠금[символ_коды]; }
            else 잠금참조 = 스택값[кадр_INDEX * 128 + кадр_Стәк[кадр_INDEX] - ысул_аргумент_COUNT[файл_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Хата) кадр_урнаштыру[кадр_INDEX] = кадр_инструкция[кадр_INDEX]; return; }
        }
        호출(файл_INDEX); if (!Хата) 틀잠금[кадр_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int МАССИВ_Белешмәлекләр, int мәгълүмат_VALUE) {
        if (мәгълүмат_VALUE == 0 || МАССИВ_элемент[МАССИВ_Белешмәлекләр] == 0) return true;
        boolean 성공여부 = МАССИВ_элемент[МАССИВ_Белешмәлекләр] == -1 ? (мәгълүмат_VALUE > 0 && мәгълүмат_VALUE < 힙끝 && 힙[мәгълүмат_VALUE] == 1) : 맞는객체(мәгълүмат_VALUE, МАССИВ_элемент[МАССИВ_Белешмәлекләр]);
        if (!성공여부 && !Хата) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int МАССИВ_оя(int Белешмәлекләр, int аскы_юл_VALUE, int TYPE_VALUE) {
        if (!объект_VALUE(Белешмәлекләр, TYPE_VALUE)) return 0;
        if (аскы_юл_VALUE < 0 || аскы_юл_VALUE >= 힙[Белешмәлекләр + 1]) { эштән_туктау_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Белешмәлекләр + 2 + аскы_юл_VALUE;
    }
    static void үтәргә_команда() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Хата) { if (던진객체 != 0) 예외처리(); if (Хата || кадр_INDEX < 현재가닥 * 32) break; }
            if (кадр_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_агым()) break; 조각 = 100; }
            if (кадр_INDEX == 0 && класс_Билгеләмә_халәт[кертү_класс_Билгеләмә] != 2 && !инициализацияләү(кертү_класс_Билгеләмә, кадр_урнаштыру[кадр_INDEX])) continue;
            if (кадр_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (ысул_керү[кадр_ысул[кадр_INDEX]] & 32) != 0 && 틀잠금[кадр_INDEX] == 0) {
                int объект_Белешмәлекләр = агым_максат_кыйммәт[현재가닥]; if (!잠금얻기(объект_Белешмәлекләр)) { if (Хата) break; continue; } 틀잠금[кадр_INDEX] = объект_Белешмәлекләр;
            }
            잠시수 = 0;
            if (--남음 == 0) { эштән_туктау_VALUE("instruction limit (500000)"); break; }
            int эшләтү = кадр_урнаштыру[кадр_INDEX]; кадр_инструкция[кадр_INDEX] = эшләтү; int VALUE = 명바();
            if (Хата) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = ысул_биләүче[кадр_ысул[кадр_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= константа_тәг.length) эштән_туктау_VALUE("invalid ldc constant");
                else if (константа_тәг[수] == 3) 넣기(상가[수], 1);
                else if (константа_тәг[수] == 8) 넣기(константа_СМС(상가[수]), 2);
                else эштән_туктау_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { язу_локаль(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { язу_локаль(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { язу_локаль(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int кертү_урнаштыру = 빼기(1), объект_Белешмәлекләр = 빼기(2), категория_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && объект_Белешмәлекләр > 0 && объект_Белешмәлекләр < 힙끝 && 힙[объект_Белешмәлекләр] == 21) категория_CODE = 21;
                int 읽는자리 = МАССИВ_оя(объект_Белешмәлекләр, кертү_урнаштыру, категория_CODE); if (!Хата) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int кертү_Белешмәлекләр = 빼기(VALUE == 83 ? 2 : 1), кертү_урнаштыру = 빼기(1), объект_Белешмәлекләр = 빼기(2), категория_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && объект_Белешмәлекләр > 0 && объект_Белешмәлекләр < 힙끝 && 힙[объект_Белешмәлекләр] == 21) категория_CODE = 21;
                int 읽는자리 = МАССИВ_оя(объект_Белешмәлекләр, кертү_урнаштыру, категория_CODE);
                if (!Хата && категория_CODE == 3 && !배열저장가능(объект_Белешмәлекләр, кертү_Белешмәлекләр)) continue;
                if (!Хата) 힙[읽는자리] = категория_CODE == 20 ? (byte)кертү_Белешмәлекләр : категория_CODE == 21 ? кертү_Белешмәлекләр & 1 : категория_CODE == 22 ? (char)кертү_Белешмәлекләр : категория_CODE == 23 ? (short)кертү_Белешмәлекләр : кертү_Белешмәлекләр;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Стәк_инструкция(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), үлчәм = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { эштән_туктау_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) үлчәм = 가 + 나;
                if (VALUE == 100) үлчәм = 가 - 나;
                if (VALUE == 104) үлчәм = 가 * 나;
                if (VALUE == 108) үлчәм = 가 / 나;
                if (VALUE == 112) үлчәм = 가 % 나;
                if (VALUE == 120) үлчәм = 가 << 나;
                if (VALUE == 122) үлчәм = 가 >> 나;
                if (VALUE == 124) үлчәм = 가 >>> 나;
                if (VALUE == 126) үлчәм = 가 & 나;
                if (VALUE == 128) үлчәм = 가 | 나;
                if (VALUE == 130) үлчәм = 가 ^ 나;
                넣기(үлчәм, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int локаль_даирә = 명바(), 증분 = (byte)명바(); 지역읽기(локаль_даирә, 1); 넣기(빼기(1) + 증분, 1); язу_локаль(локаль_даирә, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int күчерү_урыны_VALUE = эшләтү + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) күчерү_VALUE(күчерү_урыны_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { кайтару_үлчәм(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, эшләтү); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { эштән_туктау_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_ысул(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(класс_исем_СМС(명상수()), эшләтү); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int категория_CODE = 3, компонент = 0;
                if (VALUE == 188) { int 임시값 = 명바(); категория_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else компонент = класс_исем_СМС(명상수());
                if (категория_CODE == 0) { эштән_туктау_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), объект_Белешмәлекләр = атап_бирү_Саклагыч(категория_CODE, 유효길이); if (!Хата) МАССИВ_элемент[объект_Белешмәлекләр] = компонент; 넣기(объект_Белешмәлекләр, 2); continue;
            }
            if (VALUE == 190) {
                int объект_Белешмәлекләр = 빼기(2);
                if (객체유효(объект_Белешмәлекләр)) { int 비교자리 = 힙[объект_Белешмәлекләр]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) эштән_туктау_VALUE("not an array"); else 넣기(힙[объект_Белешмәлекләр + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int объект_Белешмәлекләр = 빼기(2); if (객체유효(объект_Белешмәлекләр)) { if (힙[объект_Белешмәлекләр] != 9) эштән_туктау_VALUE("athrow requires supported Throwable"); else { 던진객체 = объект_Белешмәлекләр; Хата = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int исем_константа = класс_исем_СМС(명상수()), объект_Белешмәлекләр = 빼기(2); boolean MATCH = 맞는객체(объект_Белешмәлекләр, исем_константа);
                if (VALUE == 193) 넣기(объект_Белешмәлекләр != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Хата) эштән_туктау_VALUE("ClassCastException"); 넣기(объект_Белешмәлекләр, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = эшләтү + 1, файл_INDEX = кадр_ысул[кадр_INDEX], ачкыч_Белешмәлекләр = 빼기(1);
                while ((읽는자리 - ысул_Start[файл_INDEX]) % 4 != 0) 읽는자리++;
                int максат_кыйммәт_адрес = урнаштыру_бөтен_сан(읽는자리);
                if (VALUE == 170) { int 낮은값 = урнаштыру_бөтен_сан(읽는자리 + 4), 높은값 = урнаштыру_бөтен_сан(읽는자리 + 8); if (ачкыч_Белешмәлекләр >= 낮은값 && ачкыч_Белешмәлекләр <= 높은값) максат_кыйммәт_адрес = урнаштыру_бөтен_сан(읽는자리 + 12 + (ачкыч_Белешмәлекләр - 낮은값) * 4); }
                else { int 총수 = урнаштыру_бөтен_сан(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (урнаштыру_бөтен_сан(읽는자리 + 8 + Loop_INDEX * 8) == ачкыч_Белешмәлекләр) максат_кыйммәт_адрес = урнаштыру_бөтен_сан(읽는자리 + 12 + Loop_INDEX * 8); }
                күчерү_VALUE(эшләтү + максат_кыйммәт_адрес); continue;
            }
            if (VALUE == 200) { күчерү_VALUE(эшләтү + урнаштыру_бөтен_сан(эшләтү + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int объект_Белешмәлекләр = 빼기(2);
                if (VALUE == 195) 잠금풀기(объект_Белешмәлекләр);
                else if (!잠금얻기(объект_Белешмәлекләр) && !Хата) { 넣기(объект_Белешмәлекләр, 2); кадр_урнаштыру[кадр_INDEX] = эшләтү; }
                continue;
            }
            if (VALUE == 196) {
                int команда_CODE = 명바(), кертү_урнаштыру = 명짧();
                if (команда_CODE == 21 || команда_CODE == 25) 지역읽기(кертү_урнаштыру, команда_CODE == 21 ? 1 : 2);
                else if (команда_CODE == 54 || команда_CODE == 58) язу_локаль(кертү_урнаштыру, команда_CODE == 54 ? 1 : 2);
                else if (команда_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(кертү_урнаштыру, 1); 넣기(빼기(1) + DELTA_VALUE, 1); язу_локаль(кертү_урнаштыру, 1); }
                else эштән_туктау_VALUE("unsupported wide opcode");
                continue;
            }
            эштән_туктау_VALUE("unsupported bytecode");
        }
    }
    static int FIND_класс_Билгеләмә(int исем) {
        for (int Loop_INDEX = 0; Loop_INDEX < класс_Билгеләмә_COUNT; Loop_INDEX++) if (класс_Билгеләмә_исем[Loop_INDEX] != 0 && 같은말(класс_Билгеләмә_исем[Loop_INDEX], исем)) return Loop_INDEX;
        return йөкләү_класс_Билгеләмә(константа_СМС(исем));
    }
    static int йөкләү_класс_Билгеләмә(int исем_юл) {
        if (!объект_VALUE(исем_юл, 1)) return -1;
        int озынлык_VALUE = 힙[исем_юл + 1];
        if (озынлык_VALUE < 1 || озынлык_VALUE > 505 || класс_Билгеләмә_COUNT == 16) { эштән_туктау_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < озынлык_VALUE; Loop_INDEX++) { int символ_коды = 힙[исем_юл + 2 + Loop_INDEX]; файл_исем_СМС[Loop_INDEX] = символ_коды == '/' ? '.' : символ_коды; }
        файл_исем_СМС[озынлык_VALUE] = '.'; файл_исем_СМС[озынлык_VALUE + 1] = 'c'; файл_исем_СМС[озынлык_VALUE + 2] = 'l'; файл_исем_СМС[озынлык_VALUE + 3] = 'a'; файл_исем_СМС[озынлык_VALUE + 4] = 's'; файл_исем_СМС[озынлык_VALUE + 5] = 's'; файл_исем_СМС[озынлык_VALUE + 6] = 0;
        int үлчәмен_үзгәртү = кулланучы.파일읽기(файл_исем_СМС, 임시파일);
        if (үлчәмен_үзгәртү < 0) { эштән_туктау_VALUE("ClassNotFoundException"); return -1; }
        int класс_Билгеләмә = класс_Билгеләмә_COUNT++; класс_Билгеләмә_үлчәмен_үзгәртү[класс_Билгеләмә] = үлчәмен_үзгәртү;
        for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) Birem[класс_Билгеләмә * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(класс_Билгеләмә); if (Хата) return -1;
        int фактик_мәгълүмат = константа_СМС(класс_Билгеләмә_исем[класс_Билгеләмә]);
        if (!글같음(фактик_мәгълүмат, исем_юл, true)) { эштән_туктау_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[класс_Билгеләмә];
        if (부모 != 0 && !Word_СМС(부모, "java/lang/Object") && !Word_СМС(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_класс_Билгеләмә(부모);
            if (Хата || 위 < 0) return -1;
            int 읽는자리 = 위, чор_COUNT = 0;
            while (읽는자리 >= 0 && чор_COUNT++ < 16) {
                if (읽는자리 == класс_Билгеләмә) { эштән_туктау_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = класс_оя_COUNT[위];
            for (int файл_INDEX = 0; файл_INDEX < оя_COUNT; файл_INDEX++) if (оя_биләүче[файл_INDEX] == класс_Билгеләмә && (оя_хокук_бирү[файл_INDEX] & 8) == 0) оя_урнаштыру[файл_INDEX] += 시작변위;
            класс_оя_COUNT[класс_Билгеләмә] += 시작변위;
        }
        return класс_Билгеләмә;
    }
    static int 부모종(int класс_Билгеләмә) {
        int исем = 종부모[класс_Билгеләмә];
        for (int Loop_INDEX = 0; Loop_INDEX < класс_Билгеләмә_COUNT; Loop_INDEX++) if (исем != 0 && класс_Билгеләмә_исем[Loop_INDEX] != 0 && 같은말(класс_Билгеләмә_исем[Loop_INDEX], исем)) return Loop_INDEX;
        return -1;
    }
    static int FIND_ысул(int класс_Билгеләмә, int исем, int формат_VALUE) {
        for (int 깊이 = 0; класс_Билгеләмә >= 0 && 깊이 < 16; 깊이++, класс_Билгеләмә = 부모종(класс_Билгеләмә)) {
            for (int Loop_INDEX = 0; Loop_INDEX < ысул_COUNT; Loop_INDEX++) if (ысул_биләүче[Loop_INDEX] == класс_Билгеләмә && 같은말(ысул_исем_СМС[Loop_INDEX], исем) && 같은말(ысул_TYPE[Loop_INDEX], формат_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int исем_ысул(int класс_Билгеләмә, String исем, String формат_VALUE) {
        for (int 깊이 = 0; класс_Билгеләмә >= 0 && 깊이 < 16; 깊이++, класс_Билгеләмә = 부모종(класс_Билгеләмә))
            for (int Loop_INDEX = 0; Loop_INDEX < ысул_COUNT; Loop_INDEX++) if (ысул_биләүче[Loop_INDEX] == класс_Билгеләмә && Word_СМС(ысул_исем_СМС[Loop_INDEX], исем) && Word_СМС(ысул_TYPE[Loop_INDEX], формат_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int исем) { return Birem[상가[исем]] == 'L' || Birem[상가[исем]] == '[' ? 2 : 1; }
    static boolean инициализацияләү(int класс_Билгеләмә, int команда_Start) {
        if (класс_Билгеләмә < 0 || Хата) return false;
        if (класс_Билгеләмә_халәт[класс_Билгеләмә] == 3) { эштән_туктау_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (класс_Билгеләмә_халәт[класс_Билгеләмә] == 1 && класс_агым[класс_Билгеләмә] != 현재가닥) { кадр_урнаштыру[кадр_INDEX] = команда_Start; 바꿈요청 = true; return false; }
        if (класс_Билгеләмә_халәт[класс_Билгеләмә] != 0) return true;
        int 위 = 부모종(класс_Билгеләмә);
        if (위 >= 0 && !инициализацияләү(위, команда_Start)) return false;
        класс_Билгеләмә_халәт[класс_Билгеләмә] = 1; класс_агым[класс_Билгеләмә] = 현재가닥;
        if (инициализацияләү_класс_Билгеләмә[класс_Билгеләмә] != 0) {
            кадр_урнаштыру[кадр_INDEX] = команда_Start;
            호출(инициализацияләү_класс_Билгеләмә[класс_Билгеләмә] - 1); if (!Хата) инициализацияләү_кадр[кадр_INDEX] = класс_Билгеләмә + 1;
            return false;
        }
        класс_Билгеләмә_халәт[класс_Билгеләмә] = 2; return true;
    }
    static void 필드호출(int INDEX, int команда, int эшләтү) {
        if (!чек_константа(INDEX, 9)) return;
        int биләүче_VALUE = класс_исем_СМС(상가[INDEX]), исем = Белешмәлекләр_исем(константа_SECOND_VALUE[INDEX]), формат_VALUE = Белешмәлекләр_TYPE(константа_SECOND_VALUE[INDEX]);
        if (Word_СМС(биләүче_VALUE, "java/lang/System") && (Word_СМС(исем, "out") || Word_СМС(исем, "err")) && Word_СМС(формат_VALUE, "Ljava/io/PrintStream;") && команда == 178) { 넣기(-1, 2); return; }
        int класс_Билгеләмә = FIND_класс_Билгеләмә(биләүче_VALUE); if (класс_Билгеләмә < 0 || Хата) return;
        int 찾음 = -1;
        for (int 읽는자리 = класс_Билгеләмә, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int файл_INDEX = 0; файл_INDEX < оя_COUNT; файл_INDEX++) if (оя_биләүче[файл_INDEX] == 읽는자리 && 같은말(оя_исем[файл_INDEX], исем) && 같은말(оя_TYPE[файл_INDEX], формат_VALUE)) 찾음 = файл_INDEX;
        if (찾음 < 0) { эштән_туктау_VALUE("NoSuchFieldError"); return; }
        boolean статик_VALUE = команда == 178 || команда == 179;
        if (статик_VALUE != ((оя_хокук_бирү[찾음] & 8) != 0)) { эштән_туктау_VALUE("field static/instance mismatch"); return; }
        if (статик_VALUE && !инициализацияләү(оя_биләүче[찾음], эшләтү)) return;
        int TYPE_VALUE = 형종류(формат_VALUE), VALUE = 0;
        if (команда == 179 || команда == 181) VALUE = 빼기(TYPE_VALUE);
        if (статик_VALUE) { if (команда == 178) 넣기(оя_мәгълүмат[찾음], TYPE_VALUE); else if (!Хата) оя_мәгълүмат[찾음] = VALUE; return; }
        int объект_Белешмәлекләр = 빼기(2);
        if (!객체유효(объект_Белешмәлекләр)) return;
        if (힙[объект_Белешмәлекләр] < 32 || !종포함(힙[объект_Белешмәлекләр] - 32, биләүче_VALUE)) { эштән_туктау_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = объект_Белешмәлекләр + 2 + оя_урнаштыру[찾음];
        if (команда == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Хата) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int класс_Билгеләмә, int исем) {
        for (int 중첩깊이 = 0; класс_Билгеләмә >= 0 && 중첩깊이 < 16; 중첩깊이++, класс_Билгеләмә = 부모종(класс_Билгеләмә)) {
            if (같은말(класс_Билгеләмә_исем[класс_Билгеләмә], исем) || (종부모[класс_Билгеләмә] != 0 && 같은말(종부모[класс_Билгеләмә], исем))) return true;
            for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < класс_интерфейс_COUNT[класс_Билгеләмә]; Эчке_берләштерү_урнаштыру++) if (같은말(класс_интерфейс[класс_Билгеләмә * 16 + Эчке_берләштерү_урнаштыру], исем)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int байт_мәгълүмат, boolean Yul) {
        if (첫값 == байт_мәгълүмат) return true;
        if (첫값 <= 0 || байт_мәгълүмат <= 0 || 힙[첫값] != 1 || 힙[байт_мәгълүмат] != 1 || 힙[첫값 + 1] != 힙[байт_мәгълүмат + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int X_координатасы = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[байт_мәгълүмат + 2 + Loop_INDEX];
            if (Yul) { if (X_координатасы == '.') X_координатасы = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (X_координатасы != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int объект_Белешмәлекләр) {
        if (объект_Белешмәлекләр == 0) { эштән_туктау_VALUE("NullPointerException"); return false; }
        if (объект_Белешмәлекләр < 1 || объект_Белешмәлекләр >= 힙끝 || 힙폭[объект_Белешмәлекләр] < 2 || 힙[объект_Белешмәлекләр] == 0) { эштән_туктау_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void саклау_VALUE(int объект_Белешмәлекләр) {
        if (объект_Белешмәлекләр > 0 && объект_Белешмәлекләр < 힙끝 && 힙폭[объект_Белешмәлекләр] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = объект_Белешмәлекләр;
    }
    static void күрсәтү_VALUE(int объект_Белешмәлекләр) {
        if (объект_Белешмәлекләр > 0 && объект_Белешмәлекләр < 힙끝 && 힙폭[объект_Белешмәлекләр] >= 2 && 힙[объект_Белешмәлекләр] != 0 && 힙표시[объект_Белешмәлекләр] == 0) {
            힙표시[объект_Белешмәлекләр] = 1; 표시대기[дисплей_COUNT++] = объект_Белешмәлекләр;
        }
    }
    static void 수거() {
        дисплей_COUNT = 0; туплама_COUNT++;
        for (int чек_урнаштыру = 1; чек_урнаштыру < 힙끝; чек_урнаштыру += 힙폭[чек_урнаштыру]) 힙표시[чек_урнаштыру] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < юл_Белешмәлекләр.length; Loop_INDEX++) күрсәтү_VALUE(юл_Белешмәлекләр[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < оя_COUNT; Loop_INDEX++) if ((оя_хокук_бирү[Loop_INDEX] & 8) != 0 && 형종류(оя_TYPE[Loop_INDEX]) == 2) күрсәтү_VALUE(оя_мәгълүмат[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < агым_COUNT; 임시값++) {
            күрсәтү_VALUE(агым_объект[임시값]); күрсәтү_VALUE(агым_максат_кыйммәт[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? кадр_INDEX : агым_кадр[임시값];
            for (int файл_INDEX = 임시값 * 32; файл_INDEX <= 꼭대기자리; файл_INDEX++) {
                for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 함수지역[кадр_ысул[файл_INDEX]]; Эчке_берләштерү_урнаштыру++) if (локаль_TYPE[файл_INDEX * 128 + Эчке_берләштерү_урнаштыру] == 2) күрсәтү_VALUE(локаль_VALUE[файл_INDEX * 128 + Эчке_берләштерү_урнаштыру]);
                for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < кадр_Стәк[файл_INDEX]; Эчке_берләштерү_урнаштыру++) if (스택형[файл_INDEX * 128 + Эчке_берләштерү_урнаштыру] == 2) күрсәтү_VALUE(스택값[файл_INDEX * 128 + Эчке_берләштерү_урнаштыру]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) күрсәтү_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) күрсәтү_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_бөтен_сан.length; Loop_INDEX++) күрсәтү_VALUE(Store_бөтен_сан[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < класс_Билгеләмә_COUNT; Loop_INDEX++) күрсәтү_VALUE(종잠금[Loop_INDEX]);
        for (int чек_урнаштыру = 1; чек_урнаштыру < 힙끝; чек_урнаштыру += 힙폭[чек_урнаштыру]) if (잠금깊이[чек_урнаштыру] > 0) күрсәтү_VALUE(чек_урнаштыру);
        күрсәтү_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) күрсәтү_VALUE(잠시참조[Loop_INDEX]);
        while (дисплей_COUNT > 0) {
            int объект_Белешмәлекләр = 표시대기[--дисплей_COUNT], категория_CODE = 힙[объект_Белешмәлекләр];
            for (int Loop_INDEX = объект_Белешмәлекләр + 2; Loop_INDEX < объект_Белешмәлекләр + 힙폭[объект_Белешмәлекләр]; Loop_INDEX++) if (категория_CODE == 3 || категория_CODE == 4 || 힙참조[Loop_INDEX] != 0) күрсәтү_VALUE(힙[Loop_INDEX]);
        }
        for (int чек_урнаштыру = 1; чек_урнаштыру < 힙끝; чек_урнаштыру += 힙폭[чек_урнаштыру]) if (힙표시[чек_урнаштыру] == 0) 힙[чек_урнаштыру] = 0;
        for (int чек_урнаштыру = 1; чек_урнаштыру < 힙끝; чек_урнаштыру += 힙폭[чек_урнаштыру]) if (힙[чек_урнаштыру] == 0) {
            while (чек_урнаштыру + 힙폭[чек_урнаштыру] < 힙끝 && 힙[чек_урнаштыру + 힙폭[чек_урнаштыру]] == 0) { int Киләсе_урнаштыру = чек_урнаштыру + 힙폭[чек_урнаштыру]; 힙폭[чек_урнаштыру] += 힙폭[Киләсе_урнаштыру]; 힙폭[Киләсе_урнаштыру] = 0; }
            if (чек_урнаштыру + 힙폭[чек_урнаштыру] == 힙끝) { 힙끝 = чек_урнаштыру; break; }
        }
    }
    static int 새기억(int 종류, int озынлык_VALUE) {
        if (озынлык_VALUE < 0) { эштән_туктау_VALUE("NegativeArraySizeException"); return 0; }
        if (озынлык_VALUE > 힙.length - 3) { эштән_туктау_VALUE("object heap exhausted"); return 0; }
        int 필요수 = озынлык_VALUE + 2, объект_Белешмәлекләр = 0;
        if (필요수 <= 힙.length - 힙끝) { объект_Белешмәлекләр = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { объект_Белешмәлекләр = 읽는자리; break; }
            if (объект_Белешмәлекләр != 0) {
                int 남은길이 = 힙폭[объект_Белешмәлекләр] - 필요수;
                if (남은길이 >= 2) { 힙폭[объект_Белешмәлекләр + 필요수] = 남은길이; 힙[объект_Белешмәлекләр + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { объект_Белешмәлекләр = 힙끝; 힙끝 += 필요수; }
        }
        if (объект_Белешмәлекләр == 0) { эштән_туктау_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[объект_Белешмәлекләр + Loop_INDEX] = 0; 힙참조[объект_Белешмәлекләр + Loop_INDEX] = 0; 힙폭[объект_Белешмәлекләр + Loop_INDEX] = 0; }
        МАССИВ_элемент[объект_Белешмәлекләр] = 0;
        힙폭[объект_Белешмәлекләр] = 필요수; 힙[объект_Белешмәлекләр] = 종류; 힙[объект_Белешмәлекләр + 1] = озынлык_VALUE; саклау_VALUE(объект_Белешмәлекләр); return объект_Белешмәлекләр;
    }
    static int 예외종(String исем_константа) {
        if (자바도구.같음(исем_константа, "java/lang/Throwable")) return 1;
        if (자바도구.같음(исем_константа, "java/lang/Exception")) return 2;
        if (자바도구.같음(исем_константа, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(исем_константа, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(исем_константа, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(исем_константа, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(исем_константа, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(исем_константа, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(исем_константа, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(исем_константа, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(исем_константа, "java/io/IOException")) return 11;
        if (자바도구.같음(исем_константа, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(исем_константа, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(исем_константа, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(исем_константа, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int исем) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_СМС(исем, 예외이름(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String 예외이름(int тәңгәллек_VALUE) {
        if (тәңгәллек_VALUE == 40) return "java/lang/InterruptedException";
        if (тәңгәллек_VALUE == 41) return "Татарча/자체/대기중단예외";
        if (тәңгәллек_VALUE == 39) return "java/net/SocketException";
        if (тәңгәллек_VALUE == 20) return "Татарча/자체/예외";
        if (тәңгәллек_VALUE == 21) return "Татарча/자체/실행예외";
        if (тәңгәллек_VALUE == 22) return "Татарча/자체/입출력예외";
        if (тәңгәллек_VALUE == 23) return "Татарча/자체/대기시간초과예외";
        if (тәңгәллек_VALUE == 24) return "Татарча/자체/주소확인예외";
        if (тәңгәллек_VALUE == 25) return "Татарча/자체/파일없음예외";
        if (тәңгәллек_VALUE == 26) return "Татарча/자체/통신예외";
        if (тәңгәллек_VALUE == 27) return "Татарча/자체/잘못된인수예외";
        if (тәңгәллек_VALUE == 28) return "Татарча/자체/숫자형식예외";
        if (тәңгәллек_VALUE == 29) return "Татарча/자체/범위예외";
        if (тәңгәллек_VALUE == 30) return "Татарча/자체/배열범위예외";
        if (тәңгәллек_VALUE == 31) return "Татарча/자체/문자열범위예외";
        if (тәңгәллек_VALUE == 32) return "Татарча/자체/빈참조예외";
        if (тәңгәллек_VALUE == 33) return "Татарча/자체/산술예외";
        if (тәңгәллек_VALUE == 34) return "Татарча/자체/상태예외";
        if (тәңгәллек_VALUE == 35) return "Татарча/자체/형변환예외";
        if (тәңгәллек_VALUE == 36) return "Татарча/자체/음수배열크기예외";
        if (тәңгәллек_VALUE == 37) return "Татарча/자체/МАССИВ_Store_эштән_туктау";
        if (тәңгәллек_VALUE == 38) return "Татарча/자체/가닥상태예외";
        if (тәңгәллек_VALUE == 1) return "java/lang/Throwable"; if (тәңгәллек_VALUE == 2) return "java/lang/Exception";
        if (тәңгәллек_VALUE == 3) return "java/lang/RuntimeException"; if (тәңгәллек_VALUE == 4) return "java/lang/ArithmeticException";
        if (тәңгәллек_VALUE == 5) return "java/lang/NullPointerException"; if (тәңгәллек_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (тәңгәллек_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (тәңгәллек_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (тәңгәллек_VALUE == 9) return "java/lang/IllegalArgumentException"; if (тәңгәллек_VALUE == 10) return "java/lang/NumberFormatException";
        if (тәңгәллек_VALUE == 11) return "java/io/IOException"; if (тәңгәллек_VALUE == 12) return "java/io/FileNotFoundException";
        if (тәңгәллек_VALUE == 17) return "java/lang/ArrayStoreException";
        if (тәңгәллек_VALUE == 18) return "java/net/UnknownHostException";
        if (тәңгәллек_VALUE == 19) return "java/net/SocketTimeoutException";
        if (тәңгәллек_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (тәңгәллек_VALUE == 13) return "java/lang/IllegalStateException"; if (тәңгәллек_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int тәңгәллек_VALUE) {
        if (тәңгәллек_VALUE == 40) return 2;
        if (тәңгәллек_VALUE == 41) return 40;
        if (тәңгәллек_VALUE == 39) return 11;
        if (тәңгәллек_VALUE == 1) return 0;
        if (тәңгәллек_VALUE == 2) return 1;
        if (тәңгәллек_VALUE == 3) return 2;
        if (тәңгәллек_VALUE == 4) return 3;
        if (тәңгәллек_VALUE == 5) return 3;
        if (тәңгәллек_VALUE == 6) return 3;
        if (тәңгәллек_VALUE == 7) return 6;
        if (тәңгәллек_VALUE == 8) return 6;
        if (тәңгәллек_VALUE == 9) return 3;
        if (тәңгәллек_VALUE == 10) return 9;
        if (тәңгәллек_VALUE == 11) return 2;
        if (тәңгәллек_VALUE == 12) return 11;
        if (тәңгәллек_VALUE == 13) return 3;
        if (тәңгәллек_VALUE == 14) return 3;
        if (тәңгәллек_VALUE == 15) return 3;
        if (тәңгәллек_VALUE == 16) return 9;
        if (тәңгәллек_VALUE == 17) return 3;
        if (тәңгәллек_VALUE == 18) return 11;
        if (тәңгәллек_VALUE == 19) return 11;
        if (тәңгәллек_VALUE == 20) return 2;
        if (тәңгәллек_VALUE == 21) return 3;
        if (тәңгәллек_VALUE == 22) return 11;
        if (тәңгәллек_VALUE == 23) return 22;
        if (тәңгәллек_VALUE == 24) return 22;
        if (тәңгәллек_VALUE == 25) return 22;
        if (тәңгәллек_VALUE == 26) return 22;
        if (тәңгәллек_VALUE == 27) return 9;
        if (тәңгәллек_VALUE == 28) return 27;
        if (тәңгәллек_VALUE == 29) return 6;
        if (тәңгәллек_VALUE == 30) return 29;
        if (тәңгәллек_VALUE == 31) return 29;
        if (тәңгәллек_VALUE == 32) return 5;
        if (тәңгәллек_VALUE == 33) return 4;
        if (тәңгәллек_VALUE == 34) return 13;
        if (тәңгәллек_VALUE == 35) return 14;
        if (тәңгәллек_VALUE == 36) return 15;
        if (тәңгәллек_VALUE == 37) return 17;
        if (тәңгәллек_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int фактик_VALUE, int 요구값) {
        for (int 깊이 = 0; фактик_VALUE != 0 && 깊이 < 16; 깊이++, фактик_VALUE = 예외부모(фактик_VALUE))
            if (фактик_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int тәңгәллек_VALUE, String Белешмә_файлы_Белешмәлекләр) {
        int объект_Белешмәлекләр = 새기억(9, 2); if (Хата) return;
        힙[объект_Белешмәлекләр + 2] = тәңгәллек_VALUE; 힙[объект_Белешмәлекләр + 3] = хост_символ(Белешмә_файлы_Белешмәлекләр); 힙참조[объект_Белешмәлекләр + 3] = 1;
        던진객체 = объект_Белешмәлекләр; Хата = true;
    }
    static boolean 맞는객체(int объект_Белешмәлекләр, int исем) {
        if (объект_Белешмәлекләр == 0) return true;
        if (!객체유효(объект_Белешмәлекләр)) return false;
        int категория_CODE = 힙[объект_Белешмәлекләр];
        if (Word_СМС(исем, "java/lang/Object")) return true;
        if (категория_CODE >= 32) return 종포함(категория_CODE - 32, исем);
        if (категория_CODE == 9) { int максат_кыйммәт_адрес = 예외상수(исем); return максат_кыйммәт_адрес != 0 && 예외포함(힙[объект_Белешмәлекләр + 2], максат_кыйммәт_адрес); }
        if (категория_CODE == 1) return Word_СМС(исем, "java/lang/String") || Word_СМС(исем, "java/lang/CharSequence");
        if (категория_CODE == 4) return Word_СМС(исем, "java/lang/StringBuilder") || Word_СМС(исем, "java/lang/CharSequence");
        if (категория_CODE == 10) return Word_СМС(исем, "java/util/ArrayList") || Word_СМС(исем, "java/util/List");
        if (категория_CODE == 11) return Word_СМС(исем, "java/util/HashMap") || Word_СМС(исем, "java/util/Map");
        if (категория_CODE == 12) return Word_СМС(исем, "java/lang/Integer") || Word_СМС(исем, "java/lang/Number");
        if (категория_CODE >= 24 && категория_CODE <= 28 && 힙[объект_Белешмәлекләр + 13] != 0) return 한국어화면종(исем) == категория_CODE || Word_СМС(исем, "Татарча/자체/화면구성요소");
        if (категория_CODE >= 24 && категория_CODE <= 28) return (한국어화면종(исем) == 0 && 화면종(исем) == категория_CODE) || Word_СМС(исем, "java/awt/Component") || Word_СМС(исем, "java/awt/Container") || Word_СМС(исем, "javax/swing/JComponent");
        if (категория_CODE == 29) return Word_СМС(исем, 힙[объект_Белешмәлекләр + 3] != 0 ? "Татарча/자체/동작알림" : "java/awt/event/ActionEvent");
        if (категория_CODE == 30) return Word_СМС(исем, "java/awt/FlowLayout") || Word_СМС(исем, "java/awt/LayoutManager");
        if (категория_CODE == 17) return Word_СМС(исем, "java/net/Socket");
        if (категория_CODE == 18) return Word_СМС(исем, "java/net/ServerSocket");
        if (категория_CODE == 19) return Word_СМС(исем, 힙[объект_Белешмәлекләр + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (категория_CODE == 14) return Word_СМС(исем, "java/net/InetAddress");
        if (категория_CODE == 15) return Word_СМС(исем, "java/net/DatagramSocket");
        if (категория_CODE == 16) return Word_СМС(исем, "java/net/DatagramPacket");
        if (категория_CODE == 13) return Word_СМС(исем, 힙[объект_Белешмәлекләр + 3] != 0 ? "Татарча/자체/작업가닥" : "java/lang/Thread");
        if (категория_CODE == 2) return Word_СМС(исем, "[I"); if (категория_CODE == 20) return Word_СМС(исем, "[B"); if (категория_CODE == 21) return Word_СМС(исем, "[Z");
        if (категория_CODE == 22) return Word_СМС(исем, "[C"); if (категория_CODE == 23) return Word_СМС(исем, "[S");
        if (категория_CODE != 3) return false;
        if (Word_СМС(исем, "[Ljava/lang/Object;")) return true;
        int компонент = МАССИВ_элемент[объект_Белешмәлекләр];
        if (компонент == -1) return Word_СМС(исем, "[Ljava/lang/String;") || Word_СМС(исем, "[Ljava/lang/CharSequence;");
        if (компонент == 0) return false;
        if (배열종비교(компонент, исем)) return true;
        if ((Word_СМС(компонент, "java/lang/String") || Word_СМС(компонент, "java/lang/StringBuilder")) && Word_СМС(исем, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < класс_Билгеләмә_COUNT; Loop_INDEX++) if (같은말(класс_Билгеләмә_исем[Loop_INDEX], компонент)) {
            for (int символ_коды = Loop_INDEX, 중첩깊이 = 0; символ_коды >= 0 && 중첩깊이 < 16; 중첩깊이++, символ_коды = 부모종(символ_коды)) {
                if (배열종비교(종부모[символ_коды], исем)) return true;
                for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < класс_интерфейс_COUNT[символ_коды]; Эчке_берләштерү_урнаштыру++) if (배열종비교(класс_интерфейс[символ_коды * 16 + Эчке_берләштерү_урнаштыру], исем)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int исем_константа, int 형식참조) {
        int чек_урнаштыру = 상가[형식참조], кертү_COUNT = константа_SECOND_VALUE[형식참조];
        if (исем_константа == 0 || кертү_COUNT < 4 || Birem[чек_урнаштыру] != '[' || Birem[чек_урнаштыру + 1] != 'L' || Birem[чек_урнаштыру + кертү_COUNT - 1] != ';' || константа_SECOND_VALUE[исем_константа] != кертү_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT - 3; Loop_INDEX++) if (Birem[상가[исем_константа] + Loop_INDEX] != Birem[чек_урнаштыру + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Хата = false;
        while (кадр_INDEX >= 현재가닥 * 32) {
            int файл_INDEX = кадр_ысул[кадр_INDEX], 읽는자리 = кадр_инструкция[кадр_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == файл_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                кадр_урнаштыру[кадр_INDEX] = 잡기위치[Loop_INDEX]; кадр_Стәк[кадр_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (инициализацияләү_кадр[кадр_INDEX] != 0) класс_Билгеләмә_халәт[инициализацияләү_кадр[кадр_INDEX] - 1] = 3;
            if (틀잠금[кадр_INDEX] != 0) { 잠금풀기(틀잠금[кадр_INDEX]); 틀잠금[кадр_INDEX] = 0; }
            кадр_INDEX--;
        }
        кулланучы.язу("Uncaught ");
        if (힙[던진객체] == 9) { кулланучы.язу(예외이름(힙[던진객체 + 2])); кулланучы.язу(": "); язу_СМС(힙[던진객체 + 3]); }
        else кулланучы.язу("user exception");
        кулланучы.язу_символ_VALUE(10); 던진객체 = 0; Хата = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Стәк_инструкция(int команда_CODE) {
        int 첫값 = 빼기(0), 첫형식 = кайтару_TYPE;
        if (команда_CODE == 87) return;
        if (команда_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int байт_мәгълүмат = 빼기(0), SECOND_формат = кайтару_TYPE;
        if (команда_CODE == 88) return;
        if (команда_CODE == 90) { 넣기(첫값, 첫형식); 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (команда_CODE == 92) { 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (команда_CODE == 95) { 넣기(첫값, 첫형식); 넣기(байт_мәгълүмат, SECOND_формат); return; }
        int символ_коды = 빼기(0), 셋째형식 = кайтару_TYPE;
        if (команда_CODE == 91) { 넣기(첫값, 첫형식); 넣기(символ_коды, 셋째형식); 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (команда_CODE == 93) { 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); 넣기(символ_коды, 셋째형식); 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = кайтару_TYPE;
        넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(символ_коды, 셋째형식); 넣기(байт_мәгълүмат, SECOND_формат); 넣기(첫값, 첫형식);
    }
    static void 새객체(int исем_константа, int 시작점) {
        int категория_CODE = 0, 유효길이 = 0, 예외참조 = 예외상수(исем_константа);
        if (Word_СМС(исем_константа, "java/lang/StringBuilder")) { категория_CODE = 4; 유효길이 = 1; }
        if (Word_СМС(исем_константа, "java/io/FileInputStream")) { категория_CODE = 5; 유효길이 = 2; }
        if (Word_СМС(исем_константа, "java/io/FileOutputStream")) { категория_CODE = 6; 유효길이 = 2; }
        if (예외참조 != 0) { категория_CODE = 9; 유효길이 = 2; }
        if (Word_СМС(исем_константа, "java/util/ArrayList")) { категория_CODE = 10; 유효길이 = 2; }
        if (Word_СМС(исем_константа, "java/util/HashMap")) { категория_CODE = 11; 유효길이 = 2; }
        if (Word_СМС(исем_константа, "java/lang/Integer")) { категория_CODE = 12; 유효길이 = 1; }
        if (Word_СМС(исем_константа, "java/net/Socket")) { категория_CODE = 17; 유효길이 = 5; }
        if (Word_СМС(исем_константа, "java/net/ServerSocket")) { категория_CODE = 18; 유효길이 = 5; }
        if (Word_СМС(исем_константа, "java/net/DatagramSocket")) { категория_CODE = 15; 유효길이 = 3; }
        if (Word_СМС(исем_константа, "java/net/DatagramPacket")) { категория_CODE = 16; 유효길이 = 4; }
        if (Word_СМС(исем_константа, "java/lang/Thread") || Word_СМС(исем_константа, "Татарча/자체/작업가닥")) { категория_CODE = 13; 유효길이 = 2; }
        if (Word_СМС(исем_константа, "java/lang/Object")) { категория_CODE = 8; }
        if (категория_CODE == 0 && 화면종(исем_константа) != 0) { категория_CODE = 화면종(исем_константа); 유효길이 = 12; }
        if (категория_CODE == 0) {
            int символ_коды = FIND_класс_Билгеләмә(исем_константа); if (символ_коды < 0 || Хата || !инициализацияләү(символ_коды, 시작점)) return;
            категория_CODE = 32 + символ_коды; 유효길이 = класс_оя_COUNT[символ_коды];
        }
        int объект_Белешмәлекләр = атап_бирү_Саклагыч(категория_CODE, 유효길이); if (Хата) return;
        if (категория_CODE == 13 && Word_СМС(исем_константа, "Татарча/자체/작업가닥")) 힙[объект_Белешмәлекләр + 3] = 1;
        if (категория_CODE >= 24 && категория_CODE <= 28 && 한국어화면종(исем_константа) != 0) 힙[объект_Белешмәлекләр + 13] = 1;
        if (категория_CODE == 5 || категория_CODE == 6 || категория_CODE == 15 || категория_CODE == 17 || категория_CODE == 18) 힙[объект_Белешмәлекләр + 2] = -1;
        if (категория_CODE == 9) 힙[объект_Белешмәлекләр + 2] = 예외참조;
        넣기(объект_Белешмәлекләр, 2);
    }
    static boolean 값같음(int 첫값, int байт_мәгълүмат) {
        if (첫값 == байт_мәгълүмат) return true;
        if (첫값 == 0 || байт_мәгълүмат == 0 || 첫값 < 0 || байт_мәгълүмат < 0 || 첫값 >= 힙끝 || байт_мәгълүмат >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[байт_мәгълүмат] == 1) return 글같음(첫값, байт_мәгълүмат, false);
        return 힙[첫값] == 12 && 힙[байт_мәгълүмат] == 12 && 힙[첫값 + 2] == 힙[байт_мәгълүмат + 2];
    }
    static int 글조각(int объект_Белешмәлекләр, int Start_урнаштыру, int тәмамлау_урнаштыру) {
        if (!объект_VALUE(объект_Белешмәлекләр, 1)) return 0;
        if (Start_урнаштыру < 0 || тәмамлау_урнаштыру < Start_урнаштыру || тәмамлау_урнаштыру > 힙[объект_Белешмәлекләр + 1]) { эштән_туктау_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = атап_бирү_Саклагыч(1, тәмамлау_урнаштыру - Start_урнаштыру); if (Хата) return 0;
        for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < тәмамлау_урнаштыру; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_урнаштыру] = 힙[объект_Белешмәлекләр + 2 + Loop_INDEX];
        return 반환값;
    }
    static int кушылу_СМС(int 첫값, int байт_мәгълүмат) {
        if (!объект_VALUE(첫값, 1) || !объект_VALUE(байт_мәгълүмат, 1)) return 0;
        int кертү_COUNT = 힙[첫값 + 1], ысул_INDEX = 힙[байт_мәгълүмат + 1], 반환값 = атап_бирү_Саклагыч(1, кертү_COUNT + ысул_INDEX); if (Хата) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < ысул_INDEX; Loop_INDEX++) 힙[반환값 + 2 + кертү_COUNT + Loop_INDEX] = 힙[байт_мәгълүмат + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        if (Word_СМС(биләүче, "Татарча/자체/실행인수") && команда_CODE == 184) {
            if (Word_СМС(исем_константа, "элемент_COUNT") && Word_СМС(서술상수, "()I")) { 넣기(кулланучы.인수개수() - 1, 1); return true; }
            if (Word_СМС(исем_константа, "Mäten") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= кулланучы.인수개수() - 1) 예외던짐(29, "үтәргә_команда 인수 범위를 벗어났습니다");
                else 넣기(хост_символ(кулланучы.인수(순번 + 1)), 2);
                return true;
            }
            эштән_туктау_VALUE("지원하지 않는 Татарча үтәргә_команда 인수 호출"); return true;
        }
        if (Word_СМС(биләүче, "Татарча/자체/작업가닥")) { Процесс_агым(исем_константа, 서술상수, команда_CODE, true); return true; }
        if (한국어화면소유(биләүче)) { 한국어화면호출(биләүче, исем_константа, 서술상수, команда_CODE); return true; }
        if (화면소유(биләүче)) { 화면호출(биләүче, исем_константа, 서술상수, команда_CODE); return true; }
        if (Word_СМС(биләүче, "java/net/Socket") || Word_СМС(биләүче, "java/net/ServerSocket") || Word_СМС(биләүче, "java/io/InputStream") || Word_СМС(биләүче, "java/io/OutputStream")) { 흐름호출(биләүче, исем_константа, 서술상수, команда_CODE); return true; }
        if (Word_СМС(биләүче, "Татарча/자체/төш_VALUE") && команда_CODE == 184) {
            if (Word_СМС(исем_константа, "화면너비") && Word_СМС(서술상수, "()I")) { 넣기(кулланучы.화면너비(), 1); return true; }
            if (Word_СМС(исем_константа, "화면높이") && Word_СМС(서술상수, "()I")) { 넣기(кулланучы.화면높이(), 1); return true; }
            if (Word_СМС(исем_константа, "밀리초") && Word_СМС(서술상수, "()I")) { 넣기(кулланучы.밀리초(), 1); return true; }
            if (Word_СМС(исем_константа, "그림대기") && Word_СМС(서술상수, "()I")) { 넣기(кулланучы.그림대기(), 1); return true; }
            if (Word_СМС(исем_константа, "사각형") && Word_СМС(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), X_координатасы = 빼기(1); 넣기(кулланучы.사각형(X_координатасы, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_СМС(биләүче, "java/net/InetAddress") || Word_СМС(биләүче, "java/net/DatagramPacket") || Word_СМС(биләүче, "java/net/DatagramSocket")) { 통신호출(биләүче, исем_константа, 서술상수, команда_CODE); return true; }
        if (Word_СМС(биләүче, "java/lang/Thread")) { 가닥호출(исем_константа, 서술상수, команда_CODE); return true; }
        if (Word_СМС(биләүче, "java/lang/Object")) {
            if (Word_СМС(исем_константа, "<init>") && Word_СМС(서술상수, "()V") && команда_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_СМС(исем_константа, "equals") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) { int байт_мәгълүмат = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == байт_мәгълүмат ? 1 : 0, 1); return true; }
        }
        if (예외상수(биләүче) != 0) {
            if (Word_СМС(исем_константа, "<init>") && команда_CODE == 183 && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, "(Ljava/lang/String;)V"))) {
                int тәкъдим = Word_СМС(서술상수, "()V") ? 0 : 빼기(2), объект_Белешмәлекләр = 빼기(2);
                if (объект_VALUE(объект_Белешмәлекләр, 9)) { 힙[объект_Белешмәлекләр + 3] = тәкъдим; 힙참조[объект_Белешмәлекләр + 3] = 1; } return true;
            }
            if ((Word_СМС(исем_константа, "getMessage") || Word_СМС(исем_константа, "설명")) && Word_СМС(서술상수, "()Ljava/lang/String;")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 9)) 넣기(힙[объект_Белешмәлекләр + 3], 2); return true; }
        }
        if (Word_СМС(биләүче, "java/lang/String")) {
            if (команда_CODE == 182 && Word_СМС(исем_константа, "getBytes") && (Word_СМС(서술상수, "()[B") || Word_СМС(서술상수, "(Ljava/lang/String;)[B"))) {
                int кодлау_исем = Word_СМС(서술상수, "()[B") ? 0 : 빼기(2), объект_Белешмәлекләр = 빼기(2);
                if (!объект_VALUE(объект_Белешмәлекләр, 1)) return true;
                if (кодлау_исем != 0 && !글같음(кодлау_исем, хост_символ("UTF-8"), false) && !글같음(кодлау_исем, хост_символ("UTF8"), false) && !글같음(кодлау_исем, хост_символ("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int кертү_COUNT = 힙[объект_Белешмәлекләр + 1], 반환값 = атап_бирү_Саклагыч(20, кертү_COUNT * 3), 사용수 = 0; if (Хата) return true;
                for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < кертү_COUNT; Эчке_берләштерү_урнаштыру++) {
                    int символ_коды = 힙[объект_Белешмәлекләр + 2 + Эчке_берләштерү_урнаштыру];
                    if (символ_коды >= 0xd800 && символ_коды <= 0xdbff && Эчке_берләштерү_урнаштыру + 1 < кертү_COUNT && 힙[объект_Белешмәлекләр + 3 + Эчке_берләштерү_урнаштыру] >= 0xdc00 && 힙[объект_Белешмәлекләр + 3 + Эчке_берләштерү_урнаштыру] <= 0xdfff) символ_коды = 0x10000 + ((символ_коды - 0xd800) << 10) + 힙[объект_Белешмәлекләр + 2 + ++Эчке_берләштерү_урнаштыру] - 0xdc00;
                    else if (символ_коды >= 0xd800 && символ_коды <= 0xdfff) символ_коды = '?';
                    if (символ_коды < 128) 힙[반환값 + 2 + 사용수++] = символ_коды;
                    else { int байт_COUNT = символ_коды < 2048 ? 2 : символ_коды < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((байт_COUNT == 2 ? 192 : байт_COUNT == 3 ? 224 : 240) | символ_коды >> (6 * (байт_COUNT - 1))); for (int 비교자리 = байт_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | символ_коды >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (команда_CODE == 184 && Word_СМС(исем_константа, "valueOf") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) { 넣기(сан_символ(빼기(1)), 2); return true; }
            if (команда_CODE != 182) return false;
            if (Word_СМС(исем_константа, "equals") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) { int байт_мәгълүмат = 빼기(2), 첫값 = 빼기(2); if (объект_VALUE(첫값, 1)) 넣기(글같음(첫값, байт_мәгълүмат, false) ? 1 : 0, 1); return true; }
            if (Word_СМС(исем_константа, "isEmpty") && Word_СМС(서술상수, "()Z")) { int 첫값 = 빼기(2); if (объект_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_СМС(исем_константа, "substring") && (Word_СМС(서술상수, "(I)Ljava/lang/String;") || Word_СМС(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_СМС(서술상수, "(II)Ljava/lang/String;"); int тәмамлау_урнаштыру = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (объект_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? тәмамлау_урнаштыру : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_СМС(исем_константа, "concat") && Word_СМС(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int байт_мәгълүмат = 빼기(2), 첫값 = 빼기(2); 넣기(кушылу_СМС(첫값, байт_мәгълүмат), 2); return true; }
            if (Word_СМС(исем_константа, "hashCode") && Word_СМС(서술상수, "()I")) { int 첫값 = 빼기(2), Хәш_VALUE = 0; if (объект_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) Хәш_VALUE = Хәш_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(Хәш_VALUE, 1); } return true; }
            if (Word_СМС(исем_константа, "toString") && Word_СМС(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (объект_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_СМС(биләүче, "java/lang/Integer")) {
            if (команда_CODE == 184 && Word_СМС(исем_константа, "valueOf") && Word_СМС(서술상수, "(I)Ljava/lang/Integer;")) { int мәгълүмат_VALUE = 빼기(1), объект_Белешмәлекләр = мәгълүмат_VALUE >= -128 && мәгълүмат_VALUE <= 127 ? Store_бөтен_сан[мәгълүмат_VALUE + 128] : 0; if (объект_Белешмәлекләр == 0) { объект_Белешмәлекләр = атап_бирү_Саклагыч(12, 1); if (!Хата) { 힙[объект_Белешмәлекләр + 2] = мәгълүмат_VALUE; if (мәгълүмат_VALUE >= -128 && мәгълүмат_VALUE <= 127) Store_бөтен_сан[мәгълүмат_VALUE + 128] = объект_Белешмәлекләр; } } 넣기(объект_Белешмәлекләр, 2); return true; }
            if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>") && Word_СМС(서술상수, "(I)V")) { int мәгълүмат_VALUE = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 12)) 힙[объект_Белешмәлекләр + 2] = мәгълүмат_VALUE; return true; }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "intValue") && Word_СМС(서술상수, "()I")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 12)) 넣기(힙[объект_Белешмәлекләр + 2], 1); return true; }
            if (команда_CODE == 184 && Word_СМС(исем_константа, "toString") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) { 넣기(сан_символ(빼기(1)), 2); return true; }
        }
        if (Word_СМС(биләүче, "java/lang/Math") && команда_CODE == 184) {
            if (Word_СМС(исем_константа, "abs") && Word_СМС(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_СМС(исем_константа, "min") || Word_СМС(исем_константа, "max")) && Word_СМС(서술상수, "(II)I")) { int байт_мәгълүмат = 빼기(1), 첫값 = 빼기(1); 넣기(Word_СМС(исем_константа, "min") ? (첫값 < байт_мәгълүмат ? 첫값 : байт_мәгълүмат) : (첫값 > байт_мәгълүмат ? 첫값 : байт_мәгълүмат), 1); return true; }
        }
        if (Word_СМС(биләүче, "java/lang/System") && команда_CODE == 184) {
            if (Word_СМС(исем_константа, "gc") && Word_СМС(서술상수, "()V")) { 수거(); return true; }
            if (Word_СМС(исем_константа, "arraycopy") && Word_СМС(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int кертү_COUNT = 빼기(1), күчерү_урыны_VALUE_INDEX = 빼기(1), байт_мәгълүмат = 빼기(2), Start_урнаштыру = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(байт_мәгълүмат)) {
                    int категория_CODE = 힙[첫값];
                    if (힙[байт_мәгълүмат] != категория_CODE || (категория_CODE != 2 && категория_CODE != 3 && (категория_CODE < 20 || категория_CODE > 23))) эштән_туктау_VALUE("arraycopy type mismatch");
                    else if (кертү_COUNT < 0 || Start_урнаштыру < 0 || күчерү_урыны_VALUE_INDEX < 0 || Start_урнаштыру > 힙[첫값 + 1] - кертү_COUNT || күчерү_урыны_VALUE_INDEX > 힙[байт_мәгълүмат + 1] - кертү_COUNT) эштән_туктау_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == байт_мәгълүмат && күчерү_урыны_VALUE_INDEX > Start_урнаштыру) { for (int Loop_INDEX = кертү_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[байт_мәгълүмат + 2 + күчерү_урыны_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_урнаштыру + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT && !Хата; Loop_INDEX++) { int мәгълүмат_VALUE = 힙[첫값 + 2 + Start_урнаштыру + Loop_INDEX]; if (категория_CODE != 3 || 배열저장가능(байт_мәгълүмат, мәгълүмат_VALUE)) 힙[байт_мәгълүмат + 2 + күчерү_урыны_VALUE_INDEX + Loop_INDEX] = мәгълүмат_VALUE; } }
                }
                return true;
            }
        }
        if (Word_СМС(биләүче, "java/util/ArrayList") || Word_СМС(биләүче, "java/util/List") || Word_СМС(биләүче, "java/util/HashMap") || Word_СМС(биләүче, "java/util/Map")) {
            모음호출(биләүче, исем_константа, 서술상수, команда_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int объект_Белешмәлекләр, int 필요수) {
        int 이전값 = 힙[объект_Белешмәлекләр + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Киләсе_урнаштыру = 용량값 < 8 ? 8 : 용량값 * 2; if (Киләсе_урнаштыру < 필요수) Киләсе_урнаштыру = 필요수;
        int мәгълүмат_МАССИВ = атап_бирү_Саклагыч(3, Киләсе_урнаштыру); if (Хата) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[мәгълүмат_МАССИВ + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[объект_Белешмәлекләр + 2] = мәгълүмат_МАССИВ; 힙참조[объект_Белешмәлекләр + 2] = 1;
    }
    static void 모음호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        boolean 대응참조 = Word_СМС(биләүче, "java/util/HashMap") || Word_СМС(биләүче, "java/util/Map"); int категория_CODE = 대응참조 ? 11 : 10;
        if (Word_СМС(исем_константа, "<init>") && команда_CODE == 183 && Word_СМС(서술상수, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, категория_CODE)) 모음늘리기(объект_Белешмәлекләр, 8); return; }
        if (команда_CODE != 182 && команда_CODE != 185) { эштән_туктау_VALUE("invalid collection invocation"); return; }
        if (Word_СМС(исем_константа, "size") && Word_СМС(서술상수, "()I") || Word_СМС(исем_константа, "isEmpty") && Word_СМС(서술상수, "()Z")) {
            int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, категория_CODE)) 넣기(Word_СМС(исем_константа, "size") ? 힙[объект_Белешмәлекләр + 3] : 힙[объект_Белешмәлекләр + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_СМС(исем_константа, "clear") && Word_СМС(서술상수, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, категория_CODE)) { int мәгълүмат_МАССИВ = 힙[объект_Белешмәлекләр + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[мәгълүмат_МАССИВ + 1]; Loop_INDEX++) 힙[мәгълүмат_МАССИВ + 2 + Loop_INDEX] = 0; 힙[объект_Белешмәлекләр + 3] = 0; } return; }
        if (!대응참조 && Word_СМС(исем_константа, "add") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) {
            int мәгълүмат_VALUE = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 10)) return;
            int кертү_COUNT = 힙[объект_Белешмәлекләр + 3]; 모음늘리기(объект_Белешмәлекләр, кертү_COUNT + 1); if (!Хата) { 힙[힙[объект_Белешмәлекләр + 2] + 2 + кертү_COUNT] = мәгълүмат_VALUE; 힙[объект_Белешмәлекләр + 3] = кертү_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_СМС(исем_константа, "get") || Word_СМС(исем_константа, "remove")) && Word_СМС(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_СМС(исем_константа, "set") && Word_СМС(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_СМС(исем_константа, "set"); int мәгълүмат_VALUE = 지정여부 ? 빼기(2) : 0, кертү_урнаштыру = 빼기(1), объект_Белешмәлекләр = 빼기(2);
            if (!объект_VALUE(объект_Белешмәлекләр, 10)) return;
            int кертү_COUNT = 힙[объект_Белешмәлекләр + 3], мәгълүмат_МАССИВ = 힙[объект_Белешмәлекләр + 2];
            if (кертү_урнаштыру < 0 || кертү_урнаштыру >= кертү_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[мәгълүмат_МАССИВ + 2 + кертү_урнаштыру];
            if (지정여부) 힙[мәгълүмат_МАССИВ + 2 + кертү_урнаштыру] = мәгълүмат_VALUE;
            if (Word_СМС(исем_константа, "remove")) { for (int Loop_INDEX = кертү_урнаштыру + 1; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 힙[мәгълүмат_МАССИВ + 1 + Loop_INDEX] = 힙[мәгълүмат_МАССИВ + 2 + Loop_INDEX]; 힙[мәгълүмат_МАССИВ + 1 + кертү_COUNT] = 0; 힙[объект_Белешмәлекләр + 3] = кертү_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_СМС(исем_константа, "get") || Word_СМС(исем_константа, "remove")) && Word_СМС(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_СМС(исем_константа, "put") && Word_СМС(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_СМС(исем_константа, "containsKey") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_СМС(исем_константа, "put"), бетерү = Word_СМС(исем_константа, "remove");
            int мәгълүмат_VALUE = 넣기여부 ? 빼기(2) : 0, ачкыч_Белешмәлекләр = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 11)) return;
            int кертү_COUNT = 힙[объект_Белешмәлекләр + 3], мәгълүмат_МАССИВ = 힙[объект_Белешмәлекләр + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) if (값같음(ачкыч_Белешмәлекләр, 힙[мәгълүмат_МАССИВ + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[мәгълүмат_МАССИВ + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(объект_Белешмәлекләр, (кертү_COUNT + 1) * 2); мәгълүмат_МАССИВ = 힙[объект_Белешмәлекләр + 2]; 찾은여부 = кертү_COUNT; if (!Хата) 힙[объект_Белешмәлекләр + 3] = кертү_COUNT + 1; }
                if (!Хата) { 힙[мәгълүмат_МАССИВ + 2 + 2 * 찾은여부] = ачкыч_Белешмәлекләр; 힙[мәгълүмат_МАССИВ + 3 + 2 * 찾은여부] = мәгълүмат_VALUE; }
            }
            if (бетерү && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < кертү_COUNT; Loop_INDEX++) { 힙[мәгълүмат_МАССИВ + 2 * Loop_INDEX] = 힙[мәгълүмат_МАССИВ + 2 + 2 * Loop_INDEX]; 힙[мәгълүмат_МАССИВ + 1 + 2 * Loop_INDEX] = 힙[мәгълүмат_МАССИВ + 3 + 2 * Loop_INDEX]; } 힙[мәгълүмат_МАССИВ + 2 * кертү_COUNT] = 0; 힙[мәгълүмат_МАССИВ + 1 + 2 * кертү_COUNT] = 0; 힙[объект_Белешмәлекләр + 3] = кертү_COUNT - 1; }
            if (Word_СМС(исем_константа, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        эштән_туктау_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int объект_Белешмәлекләр) {
        if (!객체유효(объект_Белешмәлекләр)) return false;
        if (잠금깊이[объект_Белешмәлекләр] != 0 && 잠금주인[объект_Белешмәлекләр] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[объект_Белешмәлекләр] = 현재가닥 + 1; 잠금깊이[объект_Белешмәлекләр]++; return true;
    }
    static void 잠금풀기(int объект_Белешмәлекләр) {
        if (!객체유효(объект_Белешмәлекләр)) return;
        if (잠금깊이[объект_Белешмәлекләр] == 0 || 잠금주인[объект_Белешмәлекләр] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[объект_Белешмәлекләр] == 0) 잠금주인[объект_Белешмәлекләр] = 0;
    }
    static boolean SWITCH_агым() {
        агым_кадр[현재가닥] = кадр_INDEX;
        if (кадр_INDEX < 현재가닥 * 32) агым_халәт[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < агым_COUNT; Loop_INDEX++) if (агым_халәт[Loop_INDEX] == 2 && агым_халәт[가닥대기[Loop_INDEX]] == 3) агым_халәт[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= агым_COUNT; Loop_INDEX++) {
            int Киләсе_урнаштыру = (현재가닥 + Loop_INDEX) % агым_COUNT;
            if (агым_халәт[Киләсе_урнаштыру] == 1) { 현재가닥 = Киләсе_урнаштыру; кадр_INDEX = агым_кадр[Киләсе_урнаштыру]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < агым_COUNT; Loop_INDEX++) if (агым_халәт[Loop_INDEX] != 3) { эштән_туктау_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int исем_константа, int 서술상수, int команда_CODE) { Процесс_агым(исем_константа, 서술상수, команда_CODE, false); }
    static void Процесс_агым(int исем_константа, int 서술상수, int команда_CODE, boolean Татарча) {
        if (команда_CODE == 184 && Word_СМС(исем_константа, Татарча ? "YIELD_мәсьәлә" : "yield") && Word_СМС(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (команда_CODE == 184 && Word_СМС(исем_константа, "currentThread") && Word_СМС(서술상수, "()Ljava/lang/Thread;")) { 넣기(агым_объект[현재가닥], 2); return; }
        if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>") && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, Татарча ? "(LТатарча/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int максат_кыйммәт_адрес = Word_СМС(서술상수, "()V") ? 0 : 빼기(2), объект_Белешмәлекләр = 빼기(2);
            if (!객체유효(объект_Белешмәлекләр)) return;
            if (힙[объект_Белешмәлекләр] == 13) { 힙[объект_Белешмәлекләр + 2] = максат_кыйммәт_адрес; 힙참조[объект_Белешмәлекләр + 2] = 1; }
            else if (максат_кыйммәт_адрес != 0) эштән_туктау_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (команда_CODE == 182 && (Word_СМС(исем_константа, Татарча ? "Start_мәсьәлә" : "start") || Word_СМС(исем_константа, Татарча ? "기다리기" : "join")) && Word_СМС(서술상수, "()V") || команда_CODE == 182 && Word_СМС(исем_константа, Татарча ? "살아있는가" : "isAlive") && Word_СМС(서술상수, "()Z")) {
            int объект_Белешмәлекләр = 빼기(2); if (!객체유효(объект_Белешмәлекләр)) return;
            int тәңгәллек_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < агым_COUNT; Loop_INDEX++) if (агым_объект[Loop_INDEX] == объект_Белешмәлекләр) тәңгәллек_VALUE = Loop_INDEX;
            if (Word_СМС(исем_константа, Татарча ? "살아있는가" : "isAlive")) { 넣기(тәңгәллек_VALUE >= 0 && агым_халәт[тәңгәллек_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_СМС(исем_константа, Татарча ? "기다리기" : "join")) { if (тәңгәллек_VALUE >= 0 && агым_халәт[тәңгәллек_VALUE] != 3) { 가닥대기[현재가닥] = тәңгәллек_VALUE; агым_халәт[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (тәңгәллек_VALUE >= 0) { 예외던짐(Татарча ? 38 : 16, "thread already started"); return; }
            if (агым_COUNT == 4) { эштән_туктау_VALUE("thread limit (4 including main)"); return; }
            int максат_кыйммәт_адрес = 힙[объект_Белешмәлекләр] == 13 ? 힙[объект_Белешмәлекләр + 2] : объект_Белешмәлекләр;
            int файл_INDEX = максат_кыйммәт_адрес > 0 && 힙[максат_кыйммәт_адрес] >= 32 ? исем_ысул(힙[максат_кыйммәт_адрес] - 32, Татарча ? "Башкару" : "run", "()V") : -1;
            if (максат_кыйммәт_адрес != 0 && файл_INDEX < 0) { эштән_туктау_VALUE("Runnable.run required"); return; }
            тәңгәллек_VALUE = агым_COUNT++; агым_объект[тәңгәллек_VALUE] = объект_Белешмәлекләр; агым_максат_кыйммәт[тәңгәллек_VALUE] = максат_кыйммәт_адрес;
            int кадр = тәңгәллек_VALUE * 32; агым_кадр[тәңгәллек_VALUE] = файл_INDEX < 0 ? кадр - 1 : кадр; агым_халәт[тәңгәллек_VALUE] = файл_INDEX < 0 ? 3 : 1;
            if (файл_INDEX >= 0) { кадр_ысул[кадр] = файл_INDEX; кадр_урнаштыру[кадр] = ысул_Start[файл_INDEX]; локаль_VALUE[кадр * 128] = максат_кыйммәт_адрес; локаль_TYPE[кадр * 128] = 2; }
            return;
        }
        эштән_туктау_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], адрес_СМС = new int[16];
    static int локаль_адрес() { return адрес_объект(0x7f000001); }
    static int адрес_объект(int VALUE) { int объект_Белешмәлекләр = атап_бирү_Саклагыч(14, 1); if (!Хата) 힙[объект_Белешмәлекләр + 2] = VALUE; return объект_Белешмәлекләр; }
    static int 주소해독(int объект_Белешмәлекләр) {
        if (объект_Белешмәлекләр == 0 || 글같음(объект_Белешмәлекләр, хост_символ("localhost"), false)) return 0x7f000001;
        if (!объект_VALUE(объект_Белешмәлекләр, 1)) return 0;
        int мәгълүмат_VALUE = 0, 총수 = 0, адрес_байт = 0, 자릿수 = 0, кертү_COUNT = 힙[объект_Белешмәлекләр + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= кертү_COUNT; Loop_INDEX++) {
            int символ_коды = Loop_INDEX == кертү_COUNT ? '.' : 힙[объект_Белешмәлекләр + 2 + Loop_INDEX];
            if (символ_коды == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } мәгълүмат_VALUE = мәгълүмат_VALUE << 8 | адрес_байт; 총수++; адрес_байт = 자릿수 = 0; }
            else { if (символ_коды < '0' || символ_коды > '9' || ++자릿수 > 3 || (адрес_байт = адрес_байт * 10 + символ_коды - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return мәгълүмат_VALUE;
    }
    static int адрес_символ(int мәгълүмат_VALUE) {
        int кертү_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int адрес_байт = мәгълүмат_VALUE >>> 이동비트 & 255;
            if (адрес_байт >= 100) адрес_СМС[кертү_COUNT++] = '0' + адрес_байт / 100;
            if (адрес_байт >= 10) адрес_СМС[кертү_COUNT++] = '0' + адрес_байт / 10 % 10;
            адрес_СМС[кертү_COUNT++] = '0' + адрес_байт % 10; if (이동비트 != 0) адрес_СМС[кертү_COUNT++] = '.';
        }
        int объект_Белешмәлекләр = атап_бирү_Саклагыч(1, кертү_COUNT); if (!Хата) for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 힙[объект_Белешмәлекләр + 2 + Loop_INDEX] = адрес_СМС[Loop_INDEX]; return объект_Белешмәлекләр;
    }
    static void 통신호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        if (Word_СМС(биләүче, "java/net/InetAddress")) {
            if (команда_CODE == 184 && Word_СМС(исем_константа, "getLoopbackAddress") && Word_СМС(서술상수, "()Ljava/net/InetAddress;")) { 넣기(локаль_адрес(), 2); return; }
            if (команда_CODE == 184 && Word_СМС(исем_константа, "getByName") && Word_СМС(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int мәгълүмат_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Хата) 넣기(адрес_объект(мәгълүмат_VALUE), 2); return;
            }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "getHostAddress") && Word_СМС(서술상수, "()Ljava/lang/String;")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 14)) 넣기(адрес_символ(힙[объект_Белешмәлекләр + 2]), 2); return; }
        }
        if (Word_СМС(биләүче, "java/net/DatagramPacket")) {
            if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>") && (Word_СМС(서술상수, "([BI)V") || Word_СМС(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean күчерү_урыны_VALUE_Белешмәлекләр = Word_СМС(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = күчерү_урыны_VALUE_Белешмәлекләр ? 빼기(1) : 0, адрес_Белешмәлекләр = күчерү_урыны_VALUE_Белешмәлекләр ? 빼기(2) : 0;
                int кертү_COUNT = 빼기(1), мәгълүмат_МАССИВ = 빼기(2), объект_Белешмәлекләр = 빼기(2);
                if (!объект_VALUE(объект_Белешмәлекләр, 16) || !объект_VALUE(мәгълүмат_МАССИВ, 20)) return;
                if (кертү_COUNT < 0 || кертү_COUNT > 힙[мәгълүмат_МАССИВ + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (адрес_Белешмәлекләр != 0 && !объект_VALUE(адрес_Белешмәлекләр, 14)) return;
                힙[объект_Белешмәлекләр + 2] = мәгълүмат_МАССИВ; 힙참조[объект_Белешмәлекләр + 2] = 1; 힙[объект_Белешмәлекләр + 3] = кертү_COUNT;
                힙[объект_Белешмәлекләр + 4] = адрес_Белешмәлекләр; 힙참조[объект_Белешмәлекләр + 4] = 1; 힙[объект_Белешмәлекләр + 5] = 접속번호; return;
            }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "setLength") && Word_СМС(서술상수, "(I)V")) {
                int кертү_COUNT = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 16)) return;
                if (кертү_COUNT < 0 || кертү_COUNT > 힙[힙[объект_Белешмәлекләр + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[объект_Белешмәлекләр + 3] = кертү_COUNT; return;
            }
            if (команда_CODE == 182 && (Word_СМС(исем_константа, "getData") && Word_СМС(서술상수, "()[B") || Word_СМС(исем_константа, "getLength") && Word_СМС(서술상수, "()I") || Word_СМС(исем_константа, "getAddress") && Word_СМС(서술상수, "()Ljava/net/InetAddress;") || Word_СМС(исем_константа, "getPort") && Word_СМС(서술상수, "()I"))) {
                int объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 16)) return;
                int кертү_урнаштыру = Word_СМС(исем_константа, "getData") ? 2 : Word_СМС(исем_константа, "getLength") ? 3 : Word_СМС(исем_константа, "getAddress") ? 4 : 5;
                넣기(힙[объект_Белешмәлекләр + кертү_урнаштыру], кертү_урнаштыру == 2 || кертү_урнаштыру == 4 ? 2 : 1); return;
            }
        }
        if (Word_СМС(биләүче, "java/net/DatagramSocket")) {
            if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>") && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, "(I)V"))) {
                int 접속번호 = Word_СМС(서술상수, "()V") ? 0 : 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = кулланучы.ачу_Челтәр(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[объект_Белешмәлекләр + 2] = 열린파일번호; return;
            }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "setSoTimeout") && Word_СМС(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[объект_Белешмәлекләр + 3] = 밀리초값; return;
            }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "getLocalPort") && Word_СМС(서술상수, "()I")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 15)) 넣기(힙[объект_Белешмәлекләр + 2] < 0 ? -1 : кулланучы.Челтәр_порт(힙[объект_Белешмәлекләр + 2]), 1); return; }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "isClosed") && Word_СМС(서술상수, "()Z")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 15)) 넣기(힙[объект_Белешмәлекләр + 2] < 0 ? 1 : 0, 1); return; }
            if (команда_CODE == 182 && Word_СМС(исем_константа, "close") && Word_СМС(서술상수, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 15) && 힙[объект_Белешмәлекләр + 2] >= 0) { кулланучы.파일서술자닫기(힙[объект_Белешмәлекләр + 2]); 힙[объект_Белешмәлекләр + 2] = -1; } return; }
            if (команда_CODE == 182 && (Word_СМС(исем_константа, "send") || Word_СМС(исем_константа, "receive")) && Word_СМС(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(전문참조, 16) || !объект_VALUE(объект_Белешмәлекләр, 15)) return;
                int мәгълүмат_МАССИВ = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[объект_Белешмәлекләр + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_СМС(исем_константа, "send")) {
                    if (!объект_VALUE(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[мәгълүмат_МАССИВ + 2 + Loop_INDEX];
                    if (кулланучы.җибәрү_Челтәр(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int кертү_COUNT = кулланучы.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (кертү_COUNT == -11) {
                        int 현재시각 = кулланучы.밀리초();
                        if (힙[объект_Белешмәлекләр + 4] == 0) 힙[объект_Белешмәлекләр + 4] = 현재시각 + 1;
                        if (힙[объект_Белешмәлекләр + 3] > 0 && 현재시각 - (힙[объект_Белешмәлекләр + 4] - 1) >= 힙[объект_Белешмәлекләр + 3]) { 힙[объект_Белешмәлекләр + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(объект_Белешмәлекләр, 2); 넣기(전문참조, 2); кадр_урнаштыру[кадр_INDEX] = кадр_инструкция[кадр_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[объект_Белешмәлекләр + 4] = 0;
                    if (кертү_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 힙[мәгълүмат_МАССИВ + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[전문참조 + 3] = кертү_COUNT; 힙[전문참조 + 4] = адрес_объект(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        эштән_туктау_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int объект_Белешмәлекләр) {
        int 현재시각 = кулланучы.밀리초();
        if (힙[объект_Белешмәлекләр + 5] == 0) 힙[объект_Белешмәлекләр + 5] = 현재시각 + 1;
        if (힙[объект_Белешмәлекләр + 3] > 0 && 현재시각 - (힙[объект_Белешмәлекләр + 5] - 1) >= 힙[объект_Белешмәлекләр + 3]) { 힙[объект_Белешмәлекләр + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        кадр_урнаштыру[кадр_INDEX] = кадр_инструкция[кадр_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        boolean 수신쪽 = Word_СМС(биләүче, "java/net/ServerSocket"), агым = Word_СМС(биләүче, "java/io/InputStream") || Word_СМС(биләүче, "java/io/OutputStream");
        if (!агым && команда_CODE == 183 && Word_СМС(исем_константа, "<init>")) {
            boolean 빈여부 = Word_СМС(서술상수, "()V"), 이름지정여부 = Word_СМС(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_СМС(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_СМС(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { эштән_туктау_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), адрес_Белешмәлекләр = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, объект_Белешмәлекләр = 빼기(2);
            if (!объект_VALUE(объект_Белешмәлекләр, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !объект_VALUE(адрес_Белешмәлекләр, 14)) return;
            int Челтәр_адрес = 이름지정여부 ? 주소해독(адрес_Белешмәлекләр) : 주소지정여부 ? 힙[адрес_Белешмәлекләр + 2] : 0x7f000001;
            if (Хата || 던진객체 != 0) return;
            int 열린파일번호 = кулланучы.агым_идарә(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? кулланучы.агым_идарә(1, 열린파일번호, 접속번호) : кулланучы.ялгау_агым(열린파일번호, Челтәр_адрес, 접속번호);
            if (처리값 < 0) { кулланучы.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[объект_Белешмәлекләр + 2] = 열린파일번호; 힙[объект_Белешмәлекләр + 4] = 접속번호; 힙[объект_Белешмәлекләр + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!агым && Word_СМС(исем_константа, "setSoTimeout") && Word_СМС(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[объект_Белешмәлекләр + 3] = 밀리초값; return; }
        if (!агым && Word_СМС(исем_константа, "close") && Word_СМС(서술상수, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (объект_VALUE(объект_Белешмәлекләр, 수신쪽 ? 18 : 17) && 힙[объект_Белешмәлекләр + 2] >= 0) { кулланучы.파일서술자닫기(힙[объект_Белешмәлекләр + 2]); 힙[объект_Белешмәлекләр + 2] = -1; } return; }
        if (!агым && (Word_СМС(исем_константа, "getLocalPort") || Word_СМС(исем_константа, "getPort") || Word_СМС(исем_константа, "isClosed") || Word_СМС(исем_константа, "isConnected"))) {
            int объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 수신쪽 ? 18 : 17)) return;
            넣기(Word_СМС(исем_константа, "isClosed") ? 힙[объект_Белешмәлекләр + 2] < 0 ? 1 : 0 : Word_СМС(исем_константа, "isConnected") ? 힙[объект_Белешмәлекләр + 6] : Word_СМС(исем_константа, "getPort") ? 힙[объект_Белешмәлекләр + 4] : 힙[объект_Белешмәлекләр + 2] < 0 ? -1 : кулланучы.агым_идарә(4, 힙[объект_Белешмәлекләр + 2], 0), 1); return;
        }
        if (수신쪽 && Word_СМС(исем_константа, "accept") && Word_СМС(서술상수, "()Ljava/net/Socket;")) {
            int объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 18)) return; int 열린파일번호 = кулланучы.агым_идарә(3, 힙[объект_Белешмәлекләр + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(объект_Белешмәлекләр)) 넣기(объект_Белешмәлекләр, 2); return; }
            힙[объект_Белешмәлекләр + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = атап_бирү_Саклагыч(17, 5); if (Хата) { кулланучы.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = кулланучы.агым_идарә(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !агым && ((Word_СМС(исем_константа, "getInputStream") && Word_СМС(서술상수, "()Ljava/io/InputStream;")) || (Word_СМС(исем_константа, "getOutputStream") && Word_СМС(서술상수, "()Ljava/io/OutputStream;")))) {
            int объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 17)) return; if (힙[объект_Белешмәлекләр + 2] < 0 || 힙[объект_Белешмәлекләр + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = атап_бирү_Саклагыч(19, 4); if (Хата) return; 힙[반환값 + 2] = объект_Белешмәлекләр; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_СМС(исем_константа, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (агым) {
            boolean 읽기여부 = Word_СМС(исем_константа, "read"), 쓰기여부 = Word_СМС(исем_константа, "write"), тыю = Word_СМС(서술상수, "([B)I") || Word_СМС(서술상수, "([B)V"), 부분배열여부 = Word_СМС(서술상수, "([BII)I") || Word_СМС(서술상수, "([BII)V");
            int кертү_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, мәгълүмат_МАССИВ = тыю || 부분배열여부 ? 빼기(2) : 0;
            int мәгълүмат_VALUE = 쓰기여부 && Word_СМС(서술상수, "(I)V") ? 빼기(1) : 0, объект_Белешмәлекләр = 빼기(2);
            if (!объект_VALUE(объект_Белешмәлекләр, 19)) return; int 부모참조 = 힙[объект_Белешмәлекләр + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_СМС(исем_константа, "close") && Word_СМС(서술상수, "()V")) { кулланучы.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_СМС(исем_константа, "flush") && Word_СМС(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[объект_Белешмәлекләр + 3] == 0)) { эштән_туктау_VALUE("unsupported stream operation"); return; }
            if (тыю || 부분배열여부) { if (!объект_VALUE(мәгълүмат_МАССИВ, 20)) return; if (тыю) кертү_COUNT = 힙[мәгълүмат_МАССИВ + 1]; if (시작변위 < 0 || кертү_COUNT < 0 || 시작변위 > 힙[мәгълүмат_МАССИВ + 1] - кертү_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else кертү_COUNT = 1;
            if (кертү_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[объект_Белешмәлекләр + 4] : 0, 처리값 = 0;
            while (완료수 < кертү_COUNT) {
                처리값 = 읽기여부 ? кулланучы.파일한바이트읽기(열린파일번호) : кулланучы.파일한바이트쓰기(열린파일번호, тыю || 부분배열여부 ? 힙[мәгълүмат_МАССИВ + 2 + 시작변위 + 완료수] : мәгълүмат_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (тыю || 부분배열여부)) 힙[мәгълүмат_МАССИВ + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(тыю || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[объект_Белешмәлекләр + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(объект_Белешмәлекләр, 2); if (тыю || 부분배열여부) 넣기(мәгълүмат_МАССИВ, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(кертү_COUNT, 1); } if (쓰기여부 && !(тыю || 부분배열여부)) 넣기(мәгълүмат_VALUE, 1); } return;
            }
            힙[объект_Белешмәлекләр + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : тыю || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        эштән_туктау_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int исем_константа) {
        if (Word_СМС(исем_константа, "Татарча/자체/тәрәз")) return 24;
        if (Word_СМС(исем_константа, "Татарча/자체/тамга")) return 26;
        if (Word_СМС(исем_константа, "Татарча/자체/төймә")) return 27;
        if (Word_СМС(исем_константа, "Татарча/자체/текст_кыры")) return 28;
        if (Word_СМС(исем_константа, "Татарча/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int исем_константа) {
        return 한국어화면종(исем_константа) != 0 || Word_СМС(исем_константа, "Татарча/자체/화면구성요소") || Word_СМС(исем_константа, "Татарча/자체/вакыйга_чират");
    }
    static int 화면종(int исем_константа) {
        int 한국어종 = 한국어화면종(исем_константа); if (한국어종 != 0) return 한국어종;
        if (Word_СМС(исем_константа, "javax/swing/JFrame")) return 24;
        if (Word_СМС(исем_константа, "javax/swing/JPanel")) return 25;
        if (Word_СМС(исем_константа, "javax/swing/JLabel")) return 26;
        if (Word_СМС(исем_константа, "javax/swing/JButton")) return 27;
        if (Word_СМС(исем_константа, "javax/swing/JTextField")) return 28;
        if (Word_СМС(исем_константа, "java/awt/event/ActionEvent")) return 29;
        if (Word_СМС(исем_константа, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int исем_константа) {
        return 화면종(исем_константа) != 0 || Word_СМС(исем_константа, "java/awt/Component") || Word_СМС(исем_константа, "java/awt/Container") || Word_СМС(исем_константа, "javax/swing/JComponent") || Word_СМС(исем_константа, "javax/swing/AbstractButton") || Word_СМС(исем_константа, "javax/swing/text/JTextComponent") || Word_СМС(исем_константа, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int объект_Белешмәлекләр) { if (!객체유효(объект_Белешмәлекләр)) return false; if (힙[объект_Белешмәлекләр] < 24 || 힙[объект_Белешмәлекләр] > 28) { эштән_туктау_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int объект_Белешмәлекләр, int СМС_Белешмәлекләр) {
        if (СМС_Белешмәлекләр != 0 && !объект_VALUE(СМС_Белешмәлекләр, 1)) return;
        int кертү_COUNT = СМС_Белешмәлекләр == 0 ? 0 : 힙[СМС_Белешмәлекләр + 1]; if (кертү_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[СМС_Белешмәлекләр + 2 + Loop_INDEX];
        if (кулланучы.화면글(힙[объект_Белешмәлекләр + 2], 화면글임시, кертү_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[объект_Белешмәлекләр + 3] = СМС_Белешмәлекләр; 힙참조[объект_Белешмәлекләр + 3] = 1;
    }
    static int 화면문자읽기(int объект_Белешмәлекләр) {
        int тәңгәллек_VALUE = 힙[объект_Белешмәлекләр + 2], кертү_COUNT = кулланучы.화면연결(8, тәңгәллек_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (кертү_COUNT < 0) { эштән_туктау_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) { int 부호값 = кулланучы.화면연결(9, тәңгәллек_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = атап_бирү_Саклагыч(1, 사용수); if (!Хата) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Татарча 객체를 직접 만들고 төш_VALUE 화면 기능에 연결한다. Swing объект_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        if (Word_СМС(биләүче, "Татарча/자체/вакыйга_чират")) {
            if (команда_CODE == 184 && Word_СМС(исем_константа, "나중에실행") && Word_СМС(서술상수, "(LТатарча/자체/실행할일;)V")) {
                int мәсьәлә_гамәл = 빼기(2); if (!객체유효(мәсьәлә_гамәл)) return;
                if (나중수 == 8) { эштән_туктау_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = мәсьәлә_гамәл; return;
            }
            if (команда_CODE == 184 && Word_СМС(исем_константа, "사건처리중인가") && Word_СМС(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            эштән_туктау_VALUE("지원하지 않는 Татарча 화면 일정 호출"); return;
        }
        if (Word_СМС(биләүче, "Татарча/자체/동작알림")) {
            int 알림 = 빼기(2); if (!объект_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_СМС(исем_константа, "вакыйга_чыганак") && Word_СМС(서술상수, "()LТатарча/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_СМС(исем_константа, "команда_СМС") && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_СМС(исем_константа, "INDEX") && Word_СМС(서술상수, "()I")) 넣기(1001, 1);
            else эштән_туктау_VALUE("지원하지 않는 Татарча Гамәл 알림 호출"); return;
        }
        if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>")) {
            int 종류 = 한국어화면종(биләүче), 받이 = 0, 가로 = 0, Вертикаль_урнаштыру = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_СМС(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (кулланучы.화면너비() - 폭) / 2; Вертикаль_урнаштыру = (кулланучы.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_СМС(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_СМС(서술상수, "(Ljava/lang/String;IIIILТатарча/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Вертикаль_урнаштыру = 빼기(1); 가로 = 빼기(1);
            } else { эштән_туктау_VALUE("지원하지 않는 Татарча 화면 생성자"); return; }
            int Mäten = 빼기(2), элемент_VALUE = 빼기(2); if (!화면객체(элемент_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Вертикаль_урнаштыру < 0 || 폭 > кулланучы.화면너비() - 가로 || 높이 > кулланучы.화면높이() - Вертикаль_урнаштыру) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = кулланучы.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { эштән_туктау_VALUE("화면 элемент_VALUE 자리가 가득 찼습니다"); return; }
            힙[элемент_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = элемент_VALUE;
            힙[элемент_VALUE + 5] = 가로; 힙[элемент_VALUE + 6] = Вертикаль_урнаштыру; 힙[элемент_VALUE + 7] = 폭; 힙[элемент_VALUE + 8] = 높이; 힙[элемент_VALUE + 10] = 2;
            힙[элемент_VALUE + 4] = 받이; 힙참조[элемент_VALUE + 4] = 1; 힙[элемент_VALUE + 12] = 1;
            кулланучы.화면연결(1, INDEX, 가로, Вертикаль_урнаштыру, 폭, 높이);
            if (종류 == 24) кулланучы.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(элемент_VALUE, Mäten); return;
        }
        if (команда_CODE != 182) { эштән_туктау_VALUE("잘못된 Татарча 화면 호출 команда"); return; }
        if (Word_СМС(исем_константа, "язу_СМС") && Word_СМС(서술상수, "(Ljava/lang/String;)V")) {
            int Mäten = 빼기(2), элемент_VALUE = 빼기(2); if (화면객체(элемент_VALUE)) 화면문자설정(элемент_VALUE, Mäten); return;
        }
        if (Word_СМС(исем_константа, "글읽기") && Word_СМС(서술상수, "()Ljava/lang/String;")) {
            int элемент_VALUE = 빼기(2); if (화면객체(элемент_VALUE)) 넣기(화면문자읽기(элемент_VALUE), 2); return;
        }
        if (Word_СМС(исем_константа, "동작맡기기") && Word_СМС(서술상수, "(LТатарча/자체/동작받이;)V")) {
            int 받이 = 빼기(2), элемент_VALUE = 빼기(2);
            if (화면객체(элемент_VALUE)) { 힙[элемент_VALUE + 4] = 받이; 힙참조[элемент_VALUE + 4] = 1; 힙[элемент_VALUE + 12] = 1; } return;
        }
        if (Word_СМС(исем_константа, "өстәү_элемент") && Word_СМС(서술상수, "(LТатарча/자체/화면구성요소;)V")) {
            int бала_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(бала_VALUE) || !화면객체(부모)) return;
            if (кулланучы.화면연결(2, 힙[부모 + 2], 힙[бала_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[бала_VALUE + 11] = 부모; 힙참조[бала_VALUE + 11] = 1; return;
        }
        if (Word_СМС(исем_константа, "자리정하기") && Word_СМС(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Вертикаль_урнаштыру = 빼기(1), 가로 = 빼기(1), элемент_VALUE = 빼기(2); if (!화면객체(элемент_VALUE)) return;
            if (кулланучы.화면연결(1, 힙[элемент_VALUE + 2], 가로, Вертикаль_урнаштыру, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[элемент_VALUE + 5] = 가로; 힙[элемент_VALUE + 6] = Вертикаль_урнаштыру; 힙[элемент_VALUE + 7] = 폭; 힙[элемент_VALUE + 8] = 높이; return;
        }
        if ((Word_СМС(исем_константа, "күрсәтү_тәрәз") || Word_СМС(исем_константа, "Yap")) && Word_СМС(서술상수, "()V")) {
            boolean күренүчәнлек_VALUE = Word_СМС(исем_константа, "күрсәтү_тәрәз"); int элемент_VALUE = 빼기(2); if (!화면객체(элемент_VALUE)) return;
            if (кулланучы.화면연결(күренүчәнлек_VALUE ? 3 : 4, 힙[элемент_VALUE + 2], күренүчәнлек_VALUE ? 1 : 0, 0, 0, 0) < 0) { эштән_туктау_VALUE("화면은 интерактив 명령에서 실행해야 합니다"); return; }
            힙[элемент_VALUE + 9] = күренүчәнлек_VALUE ? 1 : 0; return;
        }
        if (Word_СМС(исем_константа, "보이는가") && Word_СМС(서술상수, "()Z")) { int элемент_VALUE = 빼기(2); if (화면객체(элемент_VALUE)) 넣기(힙[элемент_VALUE + 9], 1); return; }
        эштән_туктау_VALUE("지원하지 않는 Татарча 화면 ысул_VALUE");
    }
    static void 화면호출(int биләүче, int исем_константа, int 서술상수, int команда_CODE) {
        if (Word_СМС(биләүче, "javax/swing/SwingUtilities")) {
            if (команда_CODE == 184 && Word_СМС(исем_константа, "invokeLater") && Word_СМС(서술상수, "(Ljava/lang/Runnable;)V")) { int объект_Белешмәлекләр = 빼기(2); if (!객체유효(объект_Белешмәлекләр)) return; if (나중수 == 8) { эштән_туктау_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = объект_Белешмәлекләр; return; }
            if (команда_CODE == 184 && Word_СМС(исем_константа, "isEventDispatchThread") && Word_СМС(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            эштән_туктау_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_СМС(биләүче, "java/awt/event/ActionEvent")) {
            int объект_Белешмәлекләр = 빼기(2); if (!объект_VALUE(объект_Белешмәлекләр, 29)) return;
            if (Word_СМС(исем_константа, "getSource") && Word_СМС(서술상수, "()Ljava/lang/Object;")) 넣기(힙[объект_Белешмәлекләр + 2], 2);
            else if (Word_СМС(исем_константа, "getActionCommand") && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[объект_Белешмәлекләр + 2]), 2);
            else if (Word_СМС(исем_константа, "getID") && Word_СМС(서술상수, "()I")) 넣기(1001, 1);
            else эштән_туктау_VALUE("unsupported ActionEvent method"); return;
        }
        if (команда_CODE == 183 && Word_СМС(исем_константа, "<init>")) {
            int COLUMNS = 0, СМС_Белешмәлекләр = 0;
            if (Word_СМС(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_СМС(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); СМС_Белешмәлекләр = 빼기(2); }
            else if (Word_СМС(서술상수, "(Ljava/lang/String;)V")) СМС_Белешмәлекләр = 빼기(2);
            else if (Word_СМС(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_СМС(서술상수, "()V")) { эштән_туктау_VALUE("unsupported Swing constructor"); return; }
            int объект_Белешмәлекләр = 빼기(2); if (!객체유효(объект_Белешмәлекләр)) return;
            if (힙[объект_Белешмәлекләр] == 30) { эштән_туктау_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(объект_Белешмәлекләр) || COLUMNS < 0) return;
            int тәңгәллек_VALUE = кулланучы.화면연결(0, 힙[объект_Белешмәлекләр] - 23, 0, 0, 0, 0);
            if (тәңгәллек_VALUE < 1 || тәңгәллек_VALUE > 32) { эштән_туктау_VALUE("GUI widget slots exhausted"); return; }
            힙[объект_Белешмәлекләр + 2] = тәңгәллек_VALUE; 화면참조[тәңгәллек_VALUE - 1] = объект_Белешмәлекләр; 힙[объект_Белешмәлекләр + 5] = 힙[объект_Белешмәлекләр] == 24 ? 130 : 16; 힙[объект_Белешмәлекләр + 6] = 힙[объект_Белешмәлекләр] == 24 ? 110 : 16;
            힙[объект_Белешмәлекләр + 7] = 힙[объект_Белешмәлекләр] == 24 ? 380 : 220; 힙[объект_Белешмәлекләр + 8] = 힙[объект_Белешмәлекләр] == 24 ? 240 : 28; 힙[объект_Белешмәлекләр + 10] = 1;
            화면문자설정(объект_Белешмәлекләр, СМС_Белешмәлекләр); return;
        }
        if (Word_СМС(исем_константа, "setText") || Word_СМС(исем_константа, "setTitle")) { int СМС_Белешмәлекләр = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр) && Word_СМС(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(объект_Белешмәлекләр, СМС_Белешмәлекләр); return; }
        if (Word_СМС(исем_константа, "getText") || Word_СМС(исем_константа, "getTitle")) { int объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр) && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(объект_Белешмәлекләр), 2); return; }
        if (Word_СМС(исем_константа, "addActionListener") && Word_СМС(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) { 힙[объект_Белешмәлекләр + 4] = 수신참조; 힙참조[объект_Белешмәлекләр + 4] = 1; } return; }
        if (Word_СМС(исем_константа, "getContentPane") && Word_СМС(서술상수, "()Ljava/awt/Container;")) { int объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) 넣기(объект_Белешмәлекләр, 2); return; }
        if (Word_СМС(исем_константа, "setLayout") && Word_СМС(서술상수, "(Ljava/awt/LayoutManager;)V")) { int план_Белешмәлекләр = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр) && план_Белешмәлекләр != 0) эштән_туктау_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_СМС(исем_константа, "add") && (Word_СМС(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_СМС(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean план_шарт = Word_СМС(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (план_шарт) 빼기(2);
            int бала_Белешмәлекләр = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (!화면객체(бала_Белешмәлекләр) || !화면객체(объект_Белешмәлекләр)) return;
            if (кулланучы.화면연결(2, 힙[объект_Белешмәлекләр + 2], 힙[бала_Белешмәлекләр + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[бала_Белешмәлекләр + 11] = объект_Белешмәлекләр; 힙참조[бала_Белешмәлекләр + 11] = 1; if (!план_шарт) 넣기(бала_Белешмәлекләр, 2); return;
        }
        if (Word_СМС(исем_константа, "setBounds") && Word_СМС(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), X_координатасы = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!화면객체(объект_Белешмәлекләр)) return;
            if (кулланучы.화면연결(1, 힙[объект_Белешмәлекләр + 2], X_координатасы, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[объект_Белешмәлекләр + 5] = X_координатасы; 힙[объект_Белешмәлекләр + 6] = 세로좌표; 힙[объект_Белешмәлекләр + 7] = 너비; 힙[объект_Белешмәлекләр + 8] = 높이; return;
        }
        if (Word_СМС(исем_константа, "setSize") && Word_СМС(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (!화면객체(объект_Белешмәлекләр)) return;
            if (кулланучы.화면연결(1, 힙[объект_Белешмәлекләр + 2], 힙[объект_Белешмәлекләр + 5], 힙[объект_Белешмәлекләр + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[объект_Белешмәлекләр + 7] = 너비; 힙[объект_Белешмәлекләр + 8] = 높이; } return;
        }
        if (Word_СМС(исем_константа, "setLocationRelativeTo") && Word_СМС(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), объект_Белешмәлекләр = 빼기(2); if (!화면객체(объект_Белешмәлекләр)) return; if (상대배치 != 0) { эштән_туктау_VALUE("only screen centering supported"); return; } 힙[объект_Белешмәлекләр + 5] = (кулланучы.화면너비() - 힙[объект_Белешмәлекләр + 7]) / 2; 힙[объект_Белешмәлекләр + 6] = (кулланучы.화면높이() - 힙[объект_Белешмәлекләр + 8]) / 2; кулланучы.화면연결(1, 힙[объект_Белешмәлекләр + 2], 힙[объект_Белешмәлекләр + 5], 힙[объект_Белешмәлекләр + 6], 힙[объект_Белешмәлекләр + 7], 힙[объект_Белешмәлекләр + 8]); return; }
        if (Word_СМС(исем_константа, "setDefaultCloseOperation") && Word_СМС(서술상수, "(I)V")) { int политика = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) { if (политика < 0 || политика > 3) 예외던짐(9, "close policy"); else { 힙[объект_Белешмәлекләр + 10] = политика; кулланучы.화면연결(7, 힙[объект_Белешмәлекләр + 2], политика, 0, 0, 0); } } return; }
        if (Word_СМС(исем_константа, "setVisible") && Word_СМС(서술상수, "(Z)V")) { int мәгълүмат_VALUE = 빼기(1), объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) { int 처리값 = кулланучы.화면연결(3, 힙[объект_Белешмәлекләр + 2], мәгълүмат_VALUE, 0, 0, 0); if (처리값 < 0) эштән_туктау_VALUE("Swing requires a standalone interactive command"); else 힙[объект_Белешмәлекләр + 9] = мәгълүмат_VALUE; } return; }
        if (Word_СМС(исем_константа, "dispose") && Word_СМС(서술상수, "()V")) { int объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) { кулланучы.화면연결(4, 힙[объект_Белешмәлекләр + 2], 0, 0, 0, 0); 힙[объект_Белешмәлекләр + 9] = 0; } return; }
        if (Word_СМС(исем_константа, "repaint") || Word_СМС(исем_константа, "validate")) { int объект_Белешмәлекләр = 빼기(2); if (!화면객체(объект_Белешмәлекләр) || !Word_СМС(서술상수, "()V")) return; кулланучы.화면연결(1, 힙[объект_Белешмәлекләр + 2], 힙[объект_Белешмәлекләр + 5], 힙[объект_Белешмәлекләр + 6], 힙[объект_Белешмәлекләр + 7], 힙[объект_Белешмәлекләр + 8]); return; }
        if (Word_СМС(исем_константа, "isVisible") && Word_СМС(서술상수, "()Z")) { int объект_Белешмәлекләр = 빼기(2); if (화면객체(объект_Белешмәлекләр)) 넣기(힙[объект_Белешмәлекләр + 9], 1); return; }
        эштән_туктау_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int максат_кыйммәт_адрес, int 사건번호, boolean Татарча) {
        if (максат_кыйммәт_адрес < 1 || 힙[максат_кыйммәт_адрес] < 32) { эштән_туктау_VALUE("Java event listener required"); return; }
        int файл_INDEX = исем_ысул(힙[максат_кыйммәт_адрес] - 32, 사건번호 == 0 ? (Татарча ? "Башкару" : "run") : (Татарча ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Татарча ? "(LТатарча/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (файл_INDEX < 0) { эштән_туктау_VALUE("event callback missing"); return; }
        현재가닥 = 0; агым_COUNT = 1; кадр_INDEX = 0; агым_халәт[0] = 1; кадр_Стәк[0] = 0; 틀잠금[0] = инициализацияләү_кадр[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { локаль_VALUE[Loop_INDEX] = локаль_TYPE[Loop_INDEX] = 0; }
        кадр_ысул[0] = файл_INDEX; кадр_урнаштыру[0] = ысул_Start[файл_INDEX]; локаль_VALUE[0] = максат_кыйммәт_адрес; локаль_TYPE[0] = 2;
        if (사건번호 != 0) { локаль_VALUE[1] = 사건번호; локаль_TYPE[1] = 2; }
        사건중 = true; үтәргә_команда(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Хата) {
            if (나중수 > 0) { int максат_кыйммәт_адрес = 나중실행[0], Татарча = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(максат_кыйммәт_адрес, 0, Татарча != 0); continue; }
            if (кулланучы.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = кулланучы.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { эштән_туктау_VALUE("GUI event I/O failed"); return; }
            int тәңгәллек_VALUE = 사건번호 & 65535; if (тәңгәллек_VALUE < 1 || тәңгәллек_VALUE > 32) continue; int объект_Белешмәлекләр = 화면참조[тәңгәллек_VALUE - 1]; if (объект_Белешмәлекләр == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[объект_Белешмәлекләр + 10] != 0) 힙[объект_Белешмәлекләр + 9] = 0;
                if (힙[объект_Белешмәлекләр + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) кулланучы.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[объект_Белешмәлекләр + 4] != 0) {
                int Белешмә_файлы_Белешмәлекләр = атап_бирү_Саклагыч(29, 2); if (Хата) return; 힙[Белешмә_файлы_Белешмәлекләр + 2] = объект_Белешмәлекләр; 힙[Белешмә_файлы_Белешмәлекләр + 3] = 힙[объект_Белешмәлекләр + 12]; 힙참조[Белешмә_файлы_Белешмәлекләр + 2] = 1; 사건실행(힙[объект_Белешмәлекләр + 4], Белешмә_файлы_Белешмәлекләр, 힙[объект_Белешмәлекләр + 12] != 0);
            }
        }
    }
    public static int эшләтү() {
        if (кулланучы.인수개수() == 1 && 자바도구.같음(кулланучы.인수(0), "-version")) {
            кулланучы.язу("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (кулланучы.인수개수() < 1) { кулланучы.язу("Usage: java CLASS [ARGS]\n"); return 2; }
        кертү_класс_Билгеләмә = йөкләү_класс_Билгеләмә(хост_символ(кулланучы.인수(0))); if (Хата || кертү_класс_Билгеләмә < 0) return 1;
        int кертү_балл_VALUE = исем_ысул(кертү_класс_Билгеләмә, "эшләтү", "()V");
        boolean 한국어진입 = кертү_балл_VALUE >= 0 && (ысул_керү[кертү_балл_VALUE] & 9) == 9;
        if (!한국어진입) кертү_балл_VALUE = исем_ысул(кертү_класс_Билгеләмә, "main", "([Ljava/lang/String;)V");
        if (кертү_балл_VALUE < 0 || (ысул_керү[кертү_балл_VALUE] & 9) != 9) эштән_туктау_VALUE("public static void эшләтү() or main(String[] args) required");
        if (Хата) return 1;
        int 인수 = атап_бирү_Саклагыч(3, кулланучы.인수개수() - 1); МАССИВ_элемент[인수] = -1;
        for (int 수 = 1; 수 < кулланучы.인수개수() && !Хата; 수++) 힙[인수 + 1 + 수] = хост_символ(кулланучы.인수(수));
        кадр_INDEX = 0; кадр_ысул[0] = кертү_балл_VALUE; кадр_урнаштыру[0] = ысул_Start[кертү_балл_VALUE]; локаль_VALUE[0] = 한국어진입 ? 0 : 인수; локаль_TYPE[0] = 한국어진입 ? 0 : 2;
        агым_халәт[0] = 1; агым_объект[0] = атап_бирү_Саклагыч(13, 2);
        үтәргә_команда(); if (!Хата) 화면사건들(); return Хата ? 1 : 0;
    }
}
