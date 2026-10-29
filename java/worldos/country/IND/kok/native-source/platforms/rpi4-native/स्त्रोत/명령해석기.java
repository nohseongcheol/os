// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 आदेश_रेग. उतारो, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] रेग = new int[4096], टोकन_मोल = new int[4096], 시작점 = new int[32], लांबाय_मोल = new int[32];
    static int[] 편집내용 = new int[16384], संपादन_करचें_नांव = new int[63];
    static int टोकन_COUNT, संपादन_करचें_नांव_लांबाय, मेजप;
    static boolean 앞줄;
    static void 원바이트(int मोल) { बोर्ड.직렬쓰기(मोल); }
    static int 줄읽기() { return रेग_संपादक.읽기(); }
    static boolean 나누기(int आवाठ) {
        int स्थिती = 0, 끝 = 0; टोकन_COUNT = 0;
        while (स्थिती < आवाठ) {
            while (स्थिती < आवाठ && (रेग[स्थिती] == 32 || रेग[स्थिती] == 9)) स्थिती++;
            if (स्थिती == आवाठ) break;
            if (टोकन_COUNT == 16) { 단말.बरोवचें("आदेश व्याकरणी_फोडणिशी_मोल: 인수가 너무 많습니다\n"); return false; }
            시작점[टोकन_COUNT] = 끝; int उतारो_मोल = 0;
            while (स्थिती < आवाठ) {
                int मोल = रेग[स्थिती++];
                if (उतारो_मोल == 0 && (मोल == 32 || मोल == 9)) break;
                if (मोल == उतारो_मोल) { उतारो_मोल = 0; continue; }
                if (उतारो_मोल == 0 && (मोल == 39 || मोल == 34)) { उतारो_मोल = मोल; continue; }
                टोकन_मोल[끝++] = मोल;
            }
            if (उतारो_मोल != 0) { 단말.बरोवचें("आदेश व्याकरणी_फोडणिशी_मोल: 따옴표가 닫히지 않았습니다\n"); return false; }
            लांबाय_मोल[टोकन_COUNT] = 끝 - 시작점[टोकन_COUNT]; टोकन_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= टोकन_COUNT) return false;
        int स्थिती_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int वर्ण_कोड=Word_SMS.charAt(순번);
            if (वर्ण_कोड>=0xd800 && वर्ण_कोड<=0xdbff && 순번+1<Word_SMS.length()) वर्ण_कोड=0x10000+((वर्ण_कोड-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int बायट_COUNT=वर्ण_कोड<128?1:वर्ण_कोड<2048?2:वर्ण_कोड<65536?3:4;
            for (int SEQUENCE_मोल=बायट_COUNT-1; SEQUENCE_मोल>=0; SEQUENCE_मोल--) {
                int मोल=बायट_COUNT==1?वर्ण_कोड:SEQUENCE_मोल==बायट_COUNT-1?(बायट_COUNT==2?0xc0:बायट_COUNT==3?0xe0:0xf0)|(वर्ण_कोड>>(6*SEQUENCE_मोल)):0x80|((वर्ण_कोड>>(6*SEQUENCE_मोल))&63);
                if (स्थिती_INDEX>=लांबाय_मोल[INDEX] || टोकन_मोल[시작점[INDEX]+स्थिती_INDEX++]!=मोल) return false;
            }
        }
        return स्थिती_INDEX==लांबाय_मोल[INDEX];
    }
    static int पाथ(int INDEX) {
        if (INDEX >= टोकन_COUNT) return -22;
        int मेजप = मेमरी_फायली.पाथ_Start(लांबाय_मोल[INDEX]); if (मेजप < 0) return मेजप;
        for (int लूप_INDEX = 0; लूप_INDEX < लांबाय_मोल[INDEX]; लूप_INDEX++) {
            मेजप = मेमरी_फायली.पाथ_बायट(लूप_INDEX, टोकन_मोल[시작점[INDEX] + लूप_INDEX]); if (मेजप < 0) return मेजप;
        }
        return 0;
    }
    static void चूक(int INDEX) { मेजप = 1; 단말.बरोवचें("चूक "); 단말.수(INDEX); 단말.문자(10); }
    static void दृश्य_मोल() {
        if (टोकन_COUNT != 2) { 단말.बरोवचें("사용법: cat फायल\n"); return; }
        int मेजप = पाथ(1); if (मेजप < 0) { चूक(मेजप); return; }
        int फायल = मेमरी_फायली.उगडचें(0); if (फायल < 0) { चूक(फायल); return; }
        while (true) { int मोल = मेमरी_फायली.읽기(फायल); if (मोल == 256) break; if (मोल < 0) { चूक(मोल); break; } 원바이트(मोल); }
        मेमरी_फायली.शेवट(फायल); 단말.문자(10);
    }
    static void संपादन_करचें_मोल() {
        if (टोकन_COUNT != 2) { 단말.बरोवचें("사용법: edit फायल\n"); return; }
        int मेजप = पाथ(1); if (मेजप < 0) { चूक(मेजप); return; }
        संपादन_करचें_नांव_लांबाय = लांबाय_मोल[1];
        for (int लूप_INDEX = 0; लूप_INDEX < संपादन_करचें_नांव_लांबाय; लूप_INDEX++) संपादन_करचें_नांव[लूप_INDEX] = टोकन_मोल[시작점[1] + लूप_INDEX];
        단말.बरोवचें("EDIT: फायल 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int आवाठ = 0;
        while (true) {
            단말.बरोवचें("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.बरोवचें("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && रेग[0] == '.') break;
            if (입력 + 1 > 편집내용.length - आवाठ) { 단말.बरोवचें("EDIT CANCELLED: file too large\n"); return; }
            for (int लूप_INDEX = 0; लूप_INDEX < 입력; लूप_INDEX++) 편집내용[आवाठ++] = रेग[लूप_INDEX];
            편집내용[आवाठ++] = 10;
        }
        मेमरी_फायली.पाथ_Start(संपादन_करचें_नांव_लांबाय);
        for (int लूप_INDEX = 0; लूप_INDEX < संपादन_करचें_नांव_लांबाय; लूप_INDEX++) मेमरी_फायली.पाथ_बायट(लूप_INDEX, संपादन_करचें_नांव[लूप_INDEX]);
        int फायल = मेमरी_फायली.उगडचें(577); if (फायल < 0) { चूक(फायल); return; }
        for (int लूप_INDEX = 0; लूप_INDEX < आवाठ; लूप_INDEX++) मेमरी_फायली.बरोवचें(फायल, 편집내용[लूप_INDEX]);
        मेमरी_फायली.शेवट(फायल); 단말.बरोवचें("SAVED "); 단말.수(आवाठ); 단말.बरोवचें("बायट_मोल(주기억 फायल)\n");
    }
    static int हॅक्स_मोल(int मोल) {
        if (मोल >= '0' && मोल <= '9') return मोल - '0';
        if (मोल >= 'a' && मोल <= 'f') return मोल - 'a' + 10;
        if (मोल >= 'A' && मोल <= 'F') return मोल - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (टोकन_COUNT != 2) { 단말.बरोवचें("사용법: load फायल | hex फायल\n"); return; }
        int मेजप = पाथ(1); if (मेजप < 0) { चूक(मेजप); return; }
        if (!넣기) {
            int फायल = मेमरी_फायली.उगडचें(0); if (फायल < 0) { चूक(फायल); return; }
            단말.बरोवचें("HEX BEGIN "); 단말.수(मेमरी_फायली.आवाठ(फायल)); 단말.문자(10);
            int प्रवेश_COUNT = 0;
            while (true) {
                int मोल = मेमरी_फायली.읽기(फायल); if (मोल < 0 || मोल == 256) break;
                단말.문자("0123456789abcdef".charAt(मोल >> 4)); 단말.문자("0123456789abcdef".charAt(मोल & 15));
                if (++प्रवेश_COUNT % 32 == 0) 단말.문자(10);
            }
            if (प्रवेश_COUNT % 32 != 0) 단말.문자(10);
            मेमरी_फायली.शेवट(फायल); 단말.बरोवचें("HEX END\n"); return;
        }
        संपादन_करचें_नांव_लांबाय = लांबाय_मोल[1];
        for (int लूप_INDEX = 0; लूप_INDEX < संपादन_करचें_नांव_लांबाय; लूप_INDEX++) संपादन_करचें_नांव[लूप_INDEX] = टोकन_मोल[시작점[1] + लूप_INDEX];
        단말.बरोवचें("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int आवाठ = 0;
        while (true) {
            단말.बरोवचें("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.बरोवचें("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && रेग[0] == '.') break;
            int 앞 = -1;
            for (int लूप_INDEX = 0; लूप_INDEX < 입력; लूप_INDEX++) {
                if (रेग[लूप_INDEX] == 32 || रेग[लूप_INDEX] == 9) continue;
                int मोल = हॅक्स_मोल(रेग[लूप_INDEX]);
                if (मोल < 0 || आवाठ >= 편집내용.length) { 단말.बरोवचें("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = मोल; else { 편집내용[आवाठ++] = 앞 * 16 + मोल; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.बरोवचें("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        मेमरी_फायली.पाथ_Start(संपादन_करचें_नांव_लांबाय);
        for (int लूप_INDEX = 0; लूप_INDEX < संपादन_करचें_नांव_लांबाय; लूप_INDEX++) मेमरी_फायली.पाथ_बायट(लूप_INDEX, संपादन_करचें_नांव[लूप_INDEX]);
        int फायल = मेमरी_फायली.उगडचें(577); if (फायल < 0) { चूक(फायल); return; }
        for (int लूप_INDEX = 0; लूप_INDEX < आवाठ; लूप_INDEX++) मेमरी_फायली.बरोवचें(फायल, 편집내용[लूप_INDEX]);
        मेमरी_फायली.शेवट(फायल); 단말.बरोवचें("LOADED "); 단말.수(आवाठ); 단말.बरोवचें("बायट_मोल(주기억 फायल)\n");
    }
    static int साधनां(int INDEX) {
        return साधन_प्रवेश(INDEX, 1);
    }
    static int साधन_प्रवेश(int INDEX, int चलोवप) {
        if (टोकन_COUNT - चलोवप > 8) return -22;
        बोर्ड.인수준비(टोकन_COUNT - चलोवप);
        for (int 첫값 = चलोवप; 첫값 < टोकन_COUNT; 첫값++) {
            if (लांबाय_मोल[첫값] > 255) return -36;
            for (int लूप_INDEX = 0; लूप_INDEX < लांबाय_मोल[첫값]; लूप_INDEX++) बोर्ड.युक्तीवाद_बायट(첫값 - चलोवप, लूप_INDEX, टोकन_मोल[시작점[첫값] + लूप_INDEX]);
        }
        return INDEX == -2 ? बोर्ड.리눅스파일실행() : INDEX < 0 ? बोर्ड.पाळो_दिवचो_उपेगकर्तो_फायल() : बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(INDEX);
    }
    static int PYTHON_रास() {
        if (टोकन_COUNT > 8) return -22;
        बोर्ड.인수준비(टोकन_COUNT);
        String पाथ = "/lib/रास.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int स्थिती_INDEX = 0;
        for (int 순번 = 0; 순번 < पाथ.length(); 순번++) {
            int वर्ण_मोल = पाथ.charAt(순번);
            if (वर्ण_मोल < 128) बोर्ड.युक्तीवाद_बायट(0, स्थिती_INDEX++, वर्ण_मोल);
            else { बोर्ड.युक्तीवाद_बायट(0, स्थिती_INDEX++, 0xe0 | (वर्ण_मोल >> 12)); बोर्ड.युक्तीवाद_बायट(0, स्थिती_INDEX++, 0x80 | ((वर्ण_मोल >> 6) & 63)); बोर्ड.युक्तीवाद_बायट(0, स्थिती_INDEX++, 0x80 | (वर्ण_मोल & 63)); }
        }
        for (int 순번 = 1; 순번 < टोकन_COUNT; 순번++) {
            if (लांबाय_मोल[순번] > 255) return -36;
            for (int वर्ण_मोल = 0; वर्ण_मोल < लांबाय_मोल[순번]; वर्ण_मोल++) बोर्ड.युक्तीवाद_बायट(순번, वर्ण_मोल, टोकन_मोल[시작점[순번] + वर्ण_मोल]);
        }
        return बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(12);
    }
    static int 실행형식() {
        int 처리값 = पाथ(0); if (처리값 < 0) return 처리값;
        int फायल = मेमरी_फायली.उगडचें(0); if (फायल < 0) return फायल;
        int 첫값 = मेमरी_फायली.읽기(फायल), बायट_डेटा = मेमरी_फायली.읽기(फायल), वर्ण_कोड = मेमरी_फायली.읽기(फायल), 뒷값 = मेमरी_फायली.읽기(फायल);
        मेमरी_फायली.शेवट(फायल);
        if (첫값 == 127 && बायट_डेटा == 'E' && वर्ण_कोड == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && बायट_डेटा == 'K' && वर्ण_कोड == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        बोर्ड.인수준비(1);
        for (int लूप_INDEX = 0; लूप_INDEX < 인수.length(); लूप_INDEX++) बोर्ड.युक्तीवाद_बायट(0, लूप_INDEX, 인수.charAt(लूप_INDEX));
        return बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(INDEX);
    }
    static void SMS_बायट(int फायल, int मोल) { मेमरी_फायली.बरोवचें(फायल, मोल); }
    static void थीर_फायल(String नांव, String अनुक्रमणिका_मोल) {
        // रास 파일명은 ASCII. फायल 내용은 UTF-8로 저장한다.
        मेमरी_फायली.पाथ_Start(नांव.length());
        for (int लूप_INDEX = 0; लूप_INDEX < नांव.length(); लूप_INDEX++) मेमरी_फायली.पाथ_बायट(लूप_INDEX, नांव.charAt(लूप_INDEX));
        int फायल = मेमरी_फायली.उगडचें(193); if (फायल < 0) return;
        for (int लूप_INDEX = 0; लूप_INDEX < अनुक्रमणिका_मोल.length(); लूप_INDEX++) {
            int वर्ण_कोड = अनुक्रमणिका_मोल.charAt(लूप_INDEX);
            if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdbff && लूप_INDEX + 1 < अनुक्रमणिका_मोल.length()) वर्ण_कोड = 0x10000 + ((वर्ण_कोड - 0xd800) << 10) + अनुक्रमणिका_मोल.charAt(++लूप_INDEX) - 0xdc00;
            if (वर्ण_कोड < 128) SMS_बायट(फायल, वर्ण_कोड);
            else {
                int 수 = वर्ण_कोड < 2048 ? 2 : वर्ण_कोड < 65536 ? 3 : 4;
                SMS_बायट(फायल, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (वर्ण_कोड >> (6 * (수 - 1))));
                for (int प्रवेश_COUNT = 수 - 1; प्रवेश_COUNT > 0; प्रवेश_COUNT--) SMS_बायट(फायल, 0x80 | ((वर्ण_कोड >> (6 * (प्रवेश_COUNT - 1))) & 63));
            }
        }
        मेमरी_फायली.शेवट(फायल);
    }
    static void 한글도움말() {
        단말.बरोवचें("F9 / Shift+Space: [EN] ↔ [kok]\n");
        단말.बरोवचें("  [KOK] keyboard; [EN] ASCII\n");
        단말.बरोवचें("  a → a\n");
        단말.बरोवचें("  F9: EN ↔ kok | Ctrl+Shift+V: UTF-8\n");
        단말.बरोवचें("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.बरोवचें("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String नांव) {
        int बायट_COUNT = 0;
        for (int लूप_INDEX = 0; लूप_INDEX < नांव.length(); लूप_INDEX++) { int वर्ण_कोड = नांव.charAt(लूप_INDEX); if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdfff) return -22; बायट_COUNT += वर्ण_कोड < 128 ? 1 : वर्ण_कोड < 2048 ? 2 : 3; }
        int 처리값 = मेमरी_फायली.पाथ_Start(बायट_COUNT); if (처리값 < 0) return 처리값;
        int स्थिती_INDEX = 0;
        for (int लूप_INDEX = 0; लूप_INDEX < नांव.length(); लूप_INDEX++) {
            int वर्ण_कोड = नांव.charAt(लूप_INDEX);
            if (वर्ण_कोड < 128) मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, वर्ण_कोड);
            else if (वर्ण_कोड < 2048) { मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, 0xc0 | (वर्ण_कोड >> 6)); मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, 0x80 | (वर्ण_कोड & 63)); }
            else { मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, 0xe0 | (वर्ण_कोड >> 12)); मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, 0x80 | ((वर्ण_कोड >> 6) & 63)); मेमरी_फायली.पाथ_बायट(स्थिती_INDEX++, 0x80 | (वर्ण_कोड & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String नांव) {
        int 처리값 = 예제경로(नांव); if (처리값 < 0) return 처리값;
        처리값 = मेमरी_फायली.निर्माण_करचें_नामावळ(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String नांव, String डेटा) {
        int 처리값 = 예제경로(नांव); if (처리값 < 0) return 처리값;
        int फायल = मेमरी_फायली.उगडचें(193); if (फायल == -17) return 0; if (फायल < 0) return फायल;
        for (int लूप_INDEX = 0; लूप_INDEX < डेटा.length(); लूप_INDEX += 2) {
            처리값 = मेमरी_फायली.बरोवचें(फायल, हॅक्स_मोल(डेटा.charAt(लूप_INDEX)) * 16 + हॅक्स_मोल(डेटा.charAt(लूप_INDEX + 1)));
            if (처리값 < 0) { मेमरी_फायली.शेवट(फायल); return 처리값; }
        }
        return मेमरी_फायली.शेवट(फायल);
    }
    static void शो_आदार() {
        प्रणाली_साधन.शो_आदार();
        단말.बरोवचें("sshd / सुरक्षीत_शॅल start|stop|status: SSH :22 (user, 장치별 पासवर्ड_मोल)\n");
        단말.बरोवचें("vncd / दुर्मीळ_प्रदर्शन start|stop|status: VNC :5900 (장치별 पासवर्ड_मोल)\n");
        단말.बरोवचें("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.बरोवचें("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.बरोवचें("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.बरोवचें("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.बरोवचें("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.बरोवचें("모서리 + 왼쪽 버튼 ओडचें_मोल: टर्मिनल आवाठ बदलचें_मोल; terminal size: स्तंभ_मोल/ROW_मोल\n");
        단말.बरोवचें("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.बरोवचें("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.बरोवचें("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.बरोवचें("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.बरोवचें("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.बरोवचें("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.बरोवचें("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.बरोवचें("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.बरोवचें("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.बरोवचें("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.बरोवचें("pip: MicroPython स्त्रोत_ट्री स्थापणूक_मोल; येजमान --network --pip 필요; /lib는 RAM\n");
        단말.बरोवचें("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.बरोवचें("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.बरोवचें("/example/java /example/c /example/python: examples ready at boot\n");
        단말.बरोवचें("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void टर्मिनल(boolean 전환여부) {
        if (전환여부 && बोर्ड.टर्मिनल(2) != 0) { बोर्ड.टर्मिनल(0); 단말.बरोवचें("TERMINAL CLOSED\n"); }
        else if (बोर्ड.टर्मिनल(1) < 0) चूक(-19);
        else 단말.बरोवचें("TERMINAL READY — kok terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void आदेश() {
        if (टोकन_COUNT == 0) return;
        if (प्रणाली_साधन.पाळो_दिवचो_आदेश()) return;
        if (같음(0,"sshd") || 같음(0,"सुरक्षीत_शॅल") || 같음(0,"vncd") || 같음(0,"दुर्मीळ_प्रदर्शन")) {
            int 종류=같음(0,"vncd")||같음(0,"दुर्मीळ_प्रदर्शन")?1:0;
            int कृती=같음(1,"start")||같음(1,"चलोवप")?1:같음(1,"stop")||같음(1,"थांबचें")?0:2;
            int स्थिती_मोल_e10195a1=बोर्ड.छायांकन(종류,कृती);
            if(स्थिती_मोल_e10195a1<0)चूक(स्थिती_मोल_e10195a1);else 단말.बरोवचें(बोर्ड.छायांकन(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else शो_आदार(); }
        else if (같음(0, "info") || 같음(0, "i")) कर्नेल.msinfo32_exe();
        else if (같음(0, "pwd")) { मेमरी_फायली.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (टोकन_COUNT == 1) { मेमरी_फायली.पाथ_Start(1); 처리값 = मेमरी_फायली.पाथ_बायट(0, '/'); } else 처리값 = टोकन_COUNT == 2 ? पाथ(1) : -22;
            if (처리값 >= 0) 처리값 = मेमरी_फायली.बदलचें_नामावळ(); if (처리값 < 0) चूक(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int युक्तीवाद_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (टोकन_COUNT == युक्तीवाद_INDEX) { मेमरी_फायली.पाथ_Start(1); 처리값 = मेमरी_फायली.पाथ_बायट(0, '.'); } else 처리값 = टोकन_COUNT == युक्तीवाद_INDEX + 1 ? पाथ(युक्तीवाद_INDEX) : -22;
            if (처리값 >= 0) 처리값 = मेमरी_फायली.경로목록(); if (처리값 < 0) चूक(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) शॅल_साधनां.फायल_काम(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) शॅल_साधनां.इन्सटन्स_मोल(같음(0, "mv"));
        else if (같음(0, "cat")) शॅल_साधनां.दृश्य_मोल();
        else if (같음(0, "wc")) शॅल_साधनां.세기();
        else if (같음(0, "grep")) शॅल_साधनां.FIND_प्रवेश();
        else if (같음(0, "head") || 같음(0, "tail")) शॅल_साधनां.머리(같음(0, "tail"));
        else if (같음(0, "tee")) शॅल_साधनां.함께쓰기();
        else if (같음(0, "env")) शॅल_वाक्य_रचणूक.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (टोकन_COUNT == 1) शॅल_वाक्य_रचणूक.환경보기();
            for (int लूप_INDEX = 1; लूप_INDEX < टोकन_COUNT; लूप_INDEX++) { int 처리값 = शॅल_वाक्य_रचणूक.환경설정(लूप_INDEX, 같음(0, "unset")); if (처리값 != 0) { मेजप = 처리값; 단말.बरोवचें("आदेश व्याकरणी_फोडणिशी_मोल: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) शॅल_वाक्य_रचणूक.पाळो_दिवचो_फायल();
        else if (같음(0, "true")) मेजप = 0;
        else if (같음(0, "false")) मेजप = 1;
        else if (같음(0, "history")) रेग_संपादक.शो_LOG();
        else if (같음(0, "exit")) {
            if (शॅल_वाक्य_रचणूक.깊이 > 0) { मेजप = टोकन_COUNT == 1 ? शॅल_वाक्य_रचणूक.स्थिती_मोल_e10195a1 : शॅल_साधनां.अंक_मोल(1); if (मेजप < 0 || मेजप > 255) मेजप = 2; शॅल_वाक्य_रचणूक.स्क्रिप्ट_सोपोवचें = true; }
            else if (बोर्ड.टर्मिनल(2) != 0) टर्मिनल(true);
            else 단말.बरोवचें("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) संपादन_करचें_मोल();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (टोकन_COUNT < 2) { मेजप = 2; 단말.बरोवचें("사용법: rm फायल...\n"); }
            for (int लूप_INDEX = 1; लूप_INDEX < टोकन_COUNT; लूप_INDEX++) { int 처리값 = पाथ(लूप_INDEX); if (처리값 == 0) 처리값 = मेमरी_फायली.지우기(); if (처리값 < 0) चूक(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_स्थिती = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_स्थिती; 첫값 < टोकन_COUNT; 첫값++) { if (첫값 > Start_स्थिती) 단말.문자(32); for (int लूप_INDEX = 0; लूप_INDEX < लांबाय_मोल[첫값]; लूप_INDEX++) बोर्ड.직렬쓰기(टोकन_मोल[시작점[첫값] + लूप_INDEX]); }
            if (Start_स्थिती == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.बरोवचें("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_रास() : साधनां(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); मेजप = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !शॅल_वाक्य_रचणूक.연결중) { 단말.बरोवचें("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = साधनां(13); मेजप = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = साधनां(15); मेजप = 처리값 < 0 ? 126 : 처리값; if (!शॅल_वाक्य_रचणूक.연결중) { 단말.बरोवचें("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = साधनां(16); मेजप = 처리값 < 0 ? 126 : 처리값; if (!शॅल_वाक्य_रचणूक.연결중) { 단말.बरोवचें("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int आवाठ = बोर्ड.टर्मिनल(13); 단말.बरोवचें("TERMINAL SIZE "); 단말.수(आवाठ & 65535); 단말.문자('x'); 단말.수(आवाठ >>> 16); 단말.문자(10); }
            else टर्मिनल(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { बोर्ड.टर्मिनल(9); डॅस्कटॉप.पाळो_दिवचो_आदेश(); }
        else if (같음(0, "c")) कर्नेल.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) कर्नेल.작업시험();
        else if (같음(0, "g")) कर्नेल.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) कर्नेल.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(0); if (처리값 == 0) 단말.बरोवचें("ELF DEMO PASS\n"); else चूक(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? साधन_प्रवेश(-2, 2) : साधनां(-1); मेजप = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !शॅल_वाक्य_रचणूक.연결중) { 단말.बरोवचें("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) कर्नेल.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = बोर्ड.फायल_ट्रान्सफर_सेवा(1); if (처리값 < 0) चूक(처리값); else { 단말.बरोवचें("FTP listening "); प्रणाली_साधन.बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(0,0)); 단말.बरोवचें(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { बोर्ड.फायल_ट्रान्सफर_सेवा(0); 단말.बरोवचें("FTP stopped\n"); }
            else 단말.बरोवचें(बोर्ड.फायल_ट्रान्सफर_सेवा(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { रास.तयार_करचें_9ce364fc(); 단말.बरोवचें("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int भास = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (टोकन_COUNT != 2 || भास < 0) 단말.बरोवचें("example java|c|python: 출력, फायल, 네트워크, 그래픽, Java Swing विंडो 예제\n");
            else { int 처리값 = 예제꾸러미.स्थापणूक_मोल(भास); if (처리값 < 0) { चूक(처리값); if (처리값 == -28) 단말.बरोवचें("RAM full: remove unused files, then retry example\n"); } else 단말.बरोवचें("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int स्वरूप_मोल = 실행형식();
            if (स्वरूप_मोल == 1 || स्वरूप_मोल == 2) {
                int 처리값 = साधन_प्रवेश(स्वरूप_मोल == 1 ? -1 : 14, 0); मेजप = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !शॅल_वाक्य_रचणूक.연결중) { 단말.बरोवचें("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (स्वरूप_मोल == 0) { मेजप = 126; 단말.बरोवचें("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { मेजप = 127; 단말.बरोवचें("Unknown command. help: commands\n"); }
        }
    }
    public static void पाळो_दिवचो_आदेश() {
        रास.तयार_करचें_9ce364fc();
        for (int भास = 0; भास < 3; भास++) { int 처리값 = 예제꾸러미.स्थापणूक_मोल(भास); if (처리값 < 0) चूक(처리값); }
        शो_आदार();
        while (true) {
            विंडो_सत्र.प्रक्रिया_मोल_प्रवेश(); if (विंडो_सत्र.재개()) continue;
            if (!विंडो_सत्र.이어읽기) 단말.बरोवचें("jkoros-native> "); रेग_संपादक.आदेश_रेग = true; बोर्ड.원격대기(1); int आवाठ = 줄읽기(); बोर्ड.원격대기(0); रेग_संपादक.आदेश_रेग = false;
            if (आवाठ == -3) continue;
            if (आवाठ == -2) 단말.बरोवचें("आदेश व्याकरणी_फोडणिशी_मोल: 명령줄이 너무 깁니다\n");
            if (आवाठ >= 0) { शॅल_वाक्य_रचणूक.स्क्रिप्ट_सोपोवचें = false; शॅल_वाक्य_रचणूक.पाळो_दिवचो_आदेश(रेग, 0, आवाठ, 0); } else शॅल_वाक्य_रचणूक.स्थिती_मोल_e10195a1 = 130;
            बोर्ड.सोपोवचें_दुर्मीळ_आदेश(शॅल_वाक्य_रचणूक.स्थिती_मोल_e10195a1);
            रेग_संपादक.आवाठ = रेग_संपादक.कर्सर_मोल = रेग_संपादक.Start_विंडो = 0;
        }
    }
}
