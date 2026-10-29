// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 ukoresha mwerekana/길이는 kwinjira_icyinjizwa 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_uburebure(int aderesi) {
        if (!실행관리.kiripu(aderesi, 4)) return -14;
        int uburebure_agaciro = 실행관리.수(aderesi);
        if (uburebure_agaciro < 0 || uburebure_agaciro > (실행관리.ukoresha_kurangiza - aderesi - 4) / 4) return -14;
        return uburebure_agaciro;
    }

    public static int Inzira_agaciro_icyinjizwa(int umugerekashakiro, int 가, int 나, int 다, int 라, int 마) {
        if (umugerekashakiro == 30) return 파일서술자관리.kurema_dosiye(가, 나, 다);
        if (umugerekashakiro == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (umugerekashakiro == 32) return 파일서술자관리.kwandika_dosiye(가, 나, 다);
        if (umugerekashakiro == 33) return 파일서술자관리.gufunga_dosiye(가);
        if (umugerekashakiro == 34) return 파일서술자관리.파일위치옮기기(가, 나, 다);
        if (umugerekashakiro == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (umugerekashakiro == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (umugerekashakiro == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (umugerekashakiro == 38) return 파일서술자관리.gukuramo_dosiye_icyinjizwa_izina(가);
        if (umugerekashakiro == 39) return 파일서술자관리.itsinda_dosiye_uburebure(가, 나);
        if (umugerekashakiro == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (umugerekashakiro == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (umugerekashakiro == 42) return 파일서술자관리.BIND_aderesi(가, 나, 다);
        if (umugerekashakiro == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (umugerekashakiro == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (umugerekashakiro == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (umugerekashakiro == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (umugerekashakiro == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.guhuza();
        }
        if (umugerekashakiro == 1) {
            int uburebure_agaciro = ARRAY_uburebure(가);
            if (uburebure_agaciro < 0) return uburebure_agaciro;
            if (uburebure_agaciro > 4096) return -90;
            for (int inyuguti_agaciro = 0; inyuguti_agaciro < uburebure_agaciro; inyuguti_agaciro++) 문자단말.문자(실행관리.수(가 + 4 + inyuguti_agaciro * 4) & 65535);
            return uburebure_agaciro;
        }
        if (umugerekashakiro == 2) return 실행관리.인수수;
        if (umugerekashakiro == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.ingingo_aderesi[가] : 0;
        if (umugerekashakiro == 10) return Urusobemiyoboro_Ikirundo.Gufungura(가);
        if (umugerekashakiro == 11) {
            int uburebure_agaciro = ARRAY_uburebure(라);
            if (uburebure_agaciro < 0) return uburebure_agaciro;
            if (마 < 0 || 마 > uburebure_agaciro || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Urusobemiyoboro_Ikirundo.kohereza(가, 나, 다, 임시자료, 마);
        }
        if (umugerekashakiro == 12) {
            int uburebure_agaciro = ARRAY_uburebure(나);
            if (uburebure_agaciro < 0) return uburebure_agaciro;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Urusobemiyoboro_Ikirundo.받기(가, 임시자료, uburebure_agaciro < 1024 ? uburebure_agaciro : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (umugerekashakiro == 13) return Urusobemiyoboro_Ikirundo.Gufunga(가);
        if (umugerekashakiro == 14) return Urusobemiyoboro_Ikirundo.내주소;
        if (umugerekashakiro == 15) return Urusobemiyoboro_Ikirundo.Mugenzi_aderesi(가);
        if (umugerekashakiro == 16) return Urusobemiyoboro_Ikirundo.상대접속번호(가);
        if (umugerekashakiro == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (umugerekashakiro == 20 || umugerekashakiro == 21) {
            int izina_ingano = ARRAY_uburebure(가), amakurushingiro_ingano = ARRAY_uburebure(나);
            if (izina_ingano < 0 || amakurushingiro_ingano < 0) return -14;
            if (izina_ingano < 1 || izina_ingano > 64) return -22;
            int uburebure_agaciro = 0;
            while (uburebure_agaciro < izina_ingano && 실행관리.수(가 + 4 + uburebure_agaciro * 4) != 0) {
                ububiko_sisitemu_ya_dosiye.Izina[uburebure_agaciro] = 실행관리.수(가 + 4 + uburebure_agaciro * 4);
                uburebure_agaciro++;
            }
            if (!ububiko_sisitemu_ya_dosiye.sheki_izina(ububiko_sisitemu_ya_dosiye.Izina, uburebure_agaciro)) return -22;
            if (umugerekashakiro == 20) {
                int Idosiye = ububiko_sisitemu_ya_dosiye.gushaka_icyinjizwa(ububiko_sisitemu_ya_dosiye.Izina, uburebure_agaciro);
                if (Idosiye < 0) return Idosiye;
                int Ingano = ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye];
                if (Ingano > amakurushingiro_ingano) return -90;
                int aderesi = igendanwa_agaciro.dosiye_ububiko() + Idosiye * ububiko_sisitemu_ya_dosiye.최대크기;
                for (int 수 = 0; 수 < Ingano; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, igendanwa_agaciro.기억읽기(aderesi + 수));
                return Ingano;
            }
            if (다 < 0 || 다 > amakurushingiro_ingano) return -22;
            if (다 > ububiko_sisitemu_ya_dosiye.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) ububiko_sisitemu_ya_dosiye.guhindura_agaciro[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return ububiko_sisitemu_ya_dosiye.Store_agaciro(ububiko_sisitemu_ya_dosiye.Izina, uburebure_agaciro, ububiko_sisitemu_ya_dosiye.guhindura_agaciro, 다);
        }
        return -38;
    }
}
