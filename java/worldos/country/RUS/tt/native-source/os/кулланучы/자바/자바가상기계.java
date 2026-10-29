// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Birem/스택/Белешмәлекләр/тармак 경계를 үтәргә_команда 중 검사한다. */
public final class 자바가상기계 {
    static int[] Birem = new int[16384], файл_исем_СМС = new int[64];
    static int[] константа_тәг = new int[512], 상가 = new int[512], константа_SECOND_VALUE = new int[512], юл_Белешмәлекләр = new int[512];
    static int[] ысул_исем_СМС = new int[32], ысул_TYPE = new int[32], ысул_керү = new int[32];
    static int[] ысул_Start = new int[32], ысул_тәмамлау = new int[32], ысул_Стәк = new int[32], 함수지역 = new int[32];
    static int[] ысул_аргумент_COUNT = new int[32], ысул_аргумент_TYPE = new int[512], ысул_кайтару = new int[32];
    static int[] 경계 = new int[16384];
    static int[] локаль_VALUE = new int[4096], локаль_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] кадр_ысул = new int[32], кадр_урнаштыру = new int[32], кадр_Стәк = new int[32];
    static int[] 힙 = new int[8192];
    static int үлчәмен_үзгәртү, 읽기위치, константа_COUNT, ысул_COUNT, класс_исем, кадр_INDEX = -1, 힙끝 = 1, кайтару_TYPE;
    static boolean Хата;

    static void эштән_туктау_VALUE(String Word_СМС) {
        if (!Хата) { кулланучы.язу("JVM error: "); кулланучы.язу(Word_СМС); кулланучы.язу_символ_VALUE(10); }
        Хата = true;
    }
    static boolean клип(int эшләтү, int озынлык_VALUE) { return эшләтү >= 0 && озынлык_VALUE >= 0 && эшләтү <= үлчәмен_үзгәртү - озынлык_VALUE; }
    static int байт_VALUE() {
        if (!клип(읽기위치, 1)) { эштән_туктау_VALUE("truncated class file"); return 0; }
        return Birem[읽기위치++];
    }
    static int 짧은수() { return байт_VALUE() << 8 | байт_VALUE(); }
    static int бөтен_сан() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int озынлык_VALUE) { if (!клип(읽기위치, озынлык_VALUE)) эштән_туктау_VALUE("invalid attribute size"); else 읽기위치 += озынлык_VALUE; }
    static boolean чек_константа(int 수, int 종류) {
        if (수 <= 0 || 수 >= константа_COUNT || константа_тәг[수] != 종류) { эштән_туктау_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int эшләтү, int озынлык_VALUE, String Word_СМС) {
        if (!клип(эшләтү, озынлык_VALUE) || озынлык_VALUE != Word_СМС.length()) return false;
        for (int 수 = 0; 수 < озынлык_VALUE; 수++) if (Birem[эшләтү + 수] != Word_СМС.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int элемент_COUNT = 짧은수();
        for (int 수 = 0; 수 < элемент_COUNT && !Хата; 수++) { чек_константа(짧은수(), 1); 건너(бөтен_сан()); }
    }
    static int команда_озынлык(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (бөтен_сан() != 0xcafebabe) эштән_туктау_VALUE("not a class file");
        int 부판 = 짧은수(), версия_VALUE = 짧은수();
        if (версия_VALUE < 45 || версия_VALUE > 52 || 부판 != 0) эштән_туктау_VALUE("supported class versions: 45..52, minor 0");
        константа_COUNT = 짧은수();
        if (константа_COUNT < 1 || константа_COUNT > 512) { эштән_туктау_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < константа_COUNT && !Хата; 수++) {
            int 종류 = байт_VALUE(); константа_тәг[수] = 종류;
            if (종류 == 1) { константа_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(константа_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = бөтен_сан();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); константа_SECOND_VALUE[수] = 짧은수(); }
            else эштән_туктау_VALUE("unsupported constant type");
        }
        int рөхсәт_VALUE = 짧은수();
        if ((рөхсәт_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) эштән_туктау_VALUE("unsupported class flags");
        класс_исем = класс_исем_СМС(짧은수());
        if (!Word_СМС(класс_исем_СМС(짧은수()), "java/lang/Object")) эштән_туктау_VALUE("inheritance unsupported");
        if (짧은수() != 0) эштән_туктау_VALUE("interfaces unsupported");
        if (짧은수() != 0) эштән_туктау_VALUE("fields unsupported");
        ысул_COUNT = 짧은수();
        if (ысул_COUNT < 1 || ысул_COUNT > 32) { эштән_туктау_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < ысул_COUNT && !Хата; 수++) {
            ысул_керү[수] = 짧은수(); ысул_исем_СМС[수] = 짧은수(); ысул_TYPE[수] = 짧은수();
            чек_константа(ысул_исем_СМС[수], 1); 서술읽기(수);
            if ((ысул_керү[수] & (0x100 | 0x400 | 0x20)) != 0) эштән_туктау_VALUE("native, abstract and synchronized methods unsupported");
            if ((ысул_керү[수] & 8) == 0 && !Word_СМС(ысул_исем_СМС[수], "<init>")) эштән_туктау_VALUE("instance methods unsupported");
            if (Word_СМС(ысул_исем_СМС[수], "<clinit>")) эштән_туктау_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(ысул_исем_СМС[앞], ысул_исем_СМС[수]) && 같은말(ысул_TYPE[앞], ысул_TYPE[수])) эштән_туктау_VALUE("duplicate method");
            int элемент_COUNT = 짧은수();
            for (int аергыч_VALUE_286d43f0 = 0; аергыч_VALUE_286d43f0 < элемент_COUNT && !Хата; аергыч_VALUE_286d43f0++) {
                int исем = 짧은수(), озынлык_VALUE = бөтен_сан(), эшләтү = 읽기위치;
                if (!клип(эшләтү, озынлык_VALUE)) { эштән_туктау_VALUE("truncated method attribute"); break; }
                if (Word_СМС(исем, "Code")) {
                    if (ысул_Start[수] != 0) эштән_туктау_VALUE("duplicate Code attribute");
                    ысул_Стәк[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_озынлык = бөтен_сан();
                    if (ысул_Стәк[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < ысул_аргумент_COUNT[수]
                        || CODE_озынлык < 1 || CODE_озынлык > 8192) эштән_туктау_VALUE("method memory limits exceeded");
                    ысул_Start[수] = 읽기위치; 건너(CODE_озынлык); ысул_тәмамлау[수] = 읽기위치;
                    if (짧은수() != 0) эштән_туктау_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != эшләтү + озынлык_VALUE) эштән_туктау_VALUE("Code attribute size mismatch");
                } else 건너(озынлык_VALUE);
            }
            if (ысул_Start[수] == 0) эштән_туктау_VALUE("missing Code attribute");
            int оя_кертү = ысул_Start[수];
            while (оя_кертү < ысул_тәмамлау[수] && !Хата) {
                int озынлык_VALUE = команда_озынлык(Birem[оя_кертү]);
                if (озынлык_VALUE == 0 || озынлык_VALUE > ысул_тәмамлау[수] - оя_кертү) { эштән_туктау_VALUE("unsupported or truncated bytecode"); break; }
                경계[оя_кертү] = 수 + 1; оя_кертү += озынлык_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 тармак 목적지를 허용하지 않는다.
            оя_кертү = ысул_Start[수];
            while (оя_кертү < ысул_тәмамлау[수] && !Хата) {
                int VALUE = Birem[оя_кертү];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int күчерү_урыны_VALUE = оя_кертү + (short)(Birem[оя_кертү + 1] << 8 | Birem[оя_кертү + 2]);
                    if (күчерү_урыны_VALUE < ысул_Start[수] || күчерү_урыны_VALUE >= ысул_тәмамлау[수] || 경계[күчерү_урыны_VALUE] != 수 + 1) эштән_туктау_VALUE("invalid branch target");
                }
                оя_кертү += команда_озынлык(VALUE);
            }
        }
        if (!Хата) 속성건너();
        if (읽기위치 != үлчәмен_үзгәртү) эштән_туктау_VALUE("extra class file data");
    }
    static int атап_бирү_Саклагыч(int 종류, int озынлык_VALUE) {
        if (озынлык_VALUE < 0 || озынлык_VALUE > 힙.length - 힙끝 - 2) { эштән_туктау_VALUE("object heap exhausted or negative array size"); return 0; }
        int Белешмәлекләр = 힙끝; 힙끝 += озынлык_VALUE + 2; 힙[Белешмәлекләр] = 종류; 힙[Белешмәлекләр + 1] = озынлык_VALUE;
        return Белешмәлекләр;
    }
    static boolean объект_VALUE(int Белешмәлекләр, int 종류) {
        if (Белешмәлекләр < 1 || Белешмәлекләр >= 힙끝 - 1 || 힙[Белешмәлекләр] != 종류) { эштән_туктау_VALUE("null or invalid object reference"); return false; }
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
        if (кадр_INDEX == 31) { эштән_туктау_VALUE("call stack limit (32)"); return; }
        int Киләсе_элемент = кадр_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) локаль_TYPE[Киләсе_элемент * 128 + 수] = 0;
        for (int 수 = ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE] - 1; 수 >= 0; 수--) {
            локаль_VALUE[Киләсе_элемент * 128 + 수] = 빼기(ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수]); локаль_TYPE[Киләсе_элемент * 128 + 수] = ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수];
        }
        кадр_INDEX = Киләсе_элемент; кадр_ысул[кадр_INDEX] = ФУНКЦИЯ_VALUE; кадр_урнаштыру[кадр_INDEX] = ысул_Start[ФУНКЦИЯ_VALUE]; кадр_Стәк[кадр_INDEX] = 0;
    }
    static void кайтару_үлчәм(int TYPE_VALUE) {
        if (TYPE_VALUE != ысул_кайтару[кадр_ысул[кадр_INDEX]]) { эштән_туктау_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        кадр_INDEX--; if (кадр_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { эштән_туктау_VALUE("file stream paths currently require ASCII"); return; }
                агым_файл_исем[оя_кертү] = VALUE;
            }
            агым_файл_исем[озынлык_VALUE] = 0;
            int 서술자 = кулланучы.파일서술자열기(агым_файл_исем, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { эштән_туктау_VALUE("FileNotFoundException: file open failed"); return; }
            힙[агым_VALUE + 2] = 서술자; 힙[агым_VALUE + 3] = 1;
            return;
        }
        if (команда != 182) { эштән_туктау_VALUE("invalid file stream invocation"); return; }
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
            if (үлчәм < -1) эштән_туктау_VALUE("IOException: read failed"); else 넣기(үлчәм, 1);
        } else if (кулланучы.파일한바이트쓰기(서술자, VALUE) != 1) эштән_туктау_VALUE("IOException: write failed");
    }
    static void CALL_ысул(int INDEX, int команда) {
        if (!чек_константа(INDEX, 10)) return;
        int биләүче_VALUE = класс_исем_СМС(상가[INDEX]), исем = Белешмәлекләр_исем(константа_SECOND_VALUE[INDEX]), формат_VALUE = Белешмәлекләр_TYPE(константа_SECOND_VALUE[INDEX]);
        if (Хата) return;
        if (같은말(биләүче_VALUE, класс_исем)) {
            if (команда != 184) { эштән_туктау_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < ысул_COUNT; 수++) if (같은말(исем, ысул_исем_СМС[수]) && 같은말(формат_VALUE, ысул_TYPE[수])) {
                if ((ысул_керү[수] & 8) == 0) эштән_туктау_VALUE("method is not static"); else 호출(수);
                return;
            }
            эштән_туктау_VALUE("NoSuchMethodError"); return;
        }
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
        эштән_туктау_VALUE("unsupported library method");
    }
    static int МАССИВ_оя(int Белешмәлекләр, int аскы_юл_VALUE, int TYPE_VALUE) {
        if (!объект_VALUE(Белешмәлекләр, TYPE_VALUE)) return 0;
        if (аскы_юл_VALUE < 0 || аскы_юл_VALUE >= 힙[Белешмәлекләр + 1]) { эштән_туктау_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Белешмәлекләр + 2 + аскы_юл_VALUE;
    }
    static void үтәргә_команда() {
        int 남음 = 500000;
        while (кадр_INDEX >= 0 && !Хата) {
            if (--남음 == 0) { эштән_туктау_VALUE("instruction limit (500000)"); break; }
            int эшләтү = кадр_урнаштыру[кадр_INDEX], VALUE = 명바();
            if (Хата) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= константа_COUNT) эштән_туктау_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int аскы_юл_VALUE = 빼기(1), Белешмәлекләр = 빼기(2), оя_кертү = МАССИВ_оя(Белешмәлекләр, аскы_юл_VALUE, VALUE == 46 ? 2 : 3);
                if (!Хата) 넣기(힙[оя_кертү], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int элемент_элемент = 빼기(VALUE == 79 ? 1 : 2), аскы_юл_VALUE = 빼기(1), Белешмәлекләр = 빼기(2), оя_кертү = МАССИВ_оя(Белешмәлекләр, аскы_юл_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && элемент_элемент != 0) объект_VALUE(элемент_элемент, 1);
                if (!Хата) 힙[оя_кертү] = элемент_элемент; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = кайтару_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = кайтару_TYPE, 나 = 빼기(0), 나형 = кайтару_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!чек_константа(수, 9)) continue;
                if (!Word_СМС(класс_исем_СМС(상가[수]), "java/lang/System") || !Word_СМС(Белешмәлекләр_исем(константа_SECOND_VALUE[수]), "out")
                    || !Word_СМС(Белешмәлекләр_TYPE(константа_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) эштән_туктау_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_ысул(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int исем = класс_исем_СМС(명짧());
                if (Word_СМС(исем, "java/lang/StringBuilder")) 넣기(атап_бирү_Саклагыч(4, 1), 2);
                else if (Word_СМС(исем, "java/io/FileInputStream") || Word_СМС(исем, "java/io/FileOutputStream")) {
                    int Белешмәлекләр = атап_бирү_Саклагыч(Word_СМС(исем, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Хата) { 힙[Белешмәлекләр + 2] = -1; 넣기(Белешмәлекләр, 2); }
                } else эштән_туктау_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) эштән_туктау_VALUE("only int[] newarray is supported"); }
                else if (!Word_СМС(класс_исем_СМС(명짧()), "java/lang/String")) эштән_туктау_VALUE("only String[] anewarray is supported");
                int озынлык_VALUE = 빼기(1); 넣기(атап_бирү_Саклагыч(VALUE == 188 ? 2 : 3, озынлык_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Белешмәлекләр = 빼기(2);
                if (Белешмәлекләр < 1 || Белешмәлекләр >= 힙끝 - 1 || (힙[Белешмәлекләр] != 2 && 힙[Белешмәлекләр] != 3)) эштән_туктау_VALUE("null or invalid array");
                else 넣기(힙[Белешмәлекләр + 1], 1); continue;
            }
            if (VALUE == 192) {
                int исем = класс_исем_СМС(명짧()), Белешмәлекләр = 빼기(2);
                if (!Word_СМС(исем, "java/lang/String")) эштән_туктау_VALUE("unsupported checkcast");
                else if (Белешмәлекләр != 0) объект_VALUE(Белешмәлекләр, 1);
                넣기(Белешмәлекләр, 2); continue;
            }
            эштән_туктау_VALUE("unsupported bytecode");
        }
    }
    public static int эшләтү() {
        if (кулланучы.인수개수() == 1 && 자바도구.같음(кулланучы.인수(0), "-version")) {
            кулланучы.язу("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (кулланучы.인수개수() < 1) { кулланучы.язу("Usage: java CLASS [ARGS]\n"); return 2; }
        int озынлык_VALUE = 자바도구.исем(файл_исем_СМС, кулланучы.인수(0));
        if (озынлык_VALUE < 1 || озынлык_VALUE > 57) { кулланучы.язу("java: invalid class name\n"); return 2; }
        файл_исем_СМС[озынлык_VALUE] = '.'; файл_исем_СМС[озынлык_VALUE + 1] = 'c'; файл_исем_СМС[озынлык_VALUE + 2] = 'l'; файл_исем_СМС[озынлык_VALUE + 3] = 'a'; файл_исем_СМС[озынлык_VALUE + 4] = 's'; файл_исем_СМС[озынлык_VALUE + 5] = 's';
        үлчәмен_үзгәртү = кулланучы.파일읽기(файл_исем_СМС, Birem);
        if (үлчәмен_үзгәртү < 0) { кулланучы.язу("java: cannot read class: "); 자바도구.수쓰기(үлчәмен_үзгәртү); кулланучы.язу_символ_VALUE(10); return 1; }
        클래스읽기(); if (Хата) return 1;
        int символ_исем = константа_СМС(класс_исем);
        if (!Хата && 힙[символ_исем + 1] != озынлык_VALUE) эштән_туктау_VALUE("class name does not match file");
        for (int 수 = 0; 수 < озынлык_VALUE && !Хата; 수++) if (힙[символ_исем + 2 + 수] != файл_исем_СМС[수]) эштән_туктау_VALUE("class name does not match file");
        int кертү_балл_VALUE = -1;
        for (int 수 = 0; 수 < ысул_COUNT; 수++) if (Word_СМС(ысул_исем_СМС[수], "main") && Word_СМС(ысул_TYPE[수], "([Ljava/lang/String;)V") && (ысул_керү[수] & 9) == 9) кертү_балл_VALUE = 수;
        if (кертү_балл_VALUE < 0) эштән_туктау_VALUE("public static void main(String[] args) required");
        if (Хата) return 1;
        int 인수 = атап_бирү_Саклагыч(3, кулланучы.인수개수() - 1);
        for (int 수 = 1; 수 < кулланучы.인수개수() && !Хата; 수++) 힙[인수 + 1 + 수] = хост_символ(кулланучы.인수(수));
        кадр_INDEX = 0; кадр_ысул[0] = кертү_балл_VALUE; кадр_урнаштыру[0] = ысул_Start[кертү_балл_VALUE]; локаль_VALUE[0] = 인수; локаль_TYPE[0] = 2;
        үтәргә_команда(); return Хата ? 1 : 0;
    }
}
