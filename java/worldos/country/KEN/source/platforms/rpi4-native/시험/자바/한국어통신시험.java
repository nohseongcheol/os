// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_T_vighairi {
        수신창구 kituo_thamani = 연결통신.수신열기(0);
        muunganisho mgeni_thamani = 연결통신.unda("127.0.0.1", kituo_thamani.namba_ya_kituo());
        muunganisho mmiliki_kitambulishi = kituo_thamani.받기();
        mgeni_thamani.대기시간(200); mmiliki_kitambulishi.대기시간(200);
        검사.참인지(mgeni_thamani.연결됨() && !mgeni_thamani.닫힘(), "UNGANISHA hali_thamani");
        검사.참인지(mmiliki_kitambulishi.namba_ya_kituo() == mgeni_thamani.jirani_namba_ya_kituo(), "kompyuta_rika_thamani namba_ya_kituo");
        검사.참인지(mgeni_thamani.namba_ya_kituo() == mmiliki_kitambulishi.jirani_namba_ya_kituo(), "jirani_upeo namba_ya_kituo");
        입력흐름 입력 = mmiliki_kitambulishi.입력(); 출력흐름 출력쪽 = mgeni_thamani.출력();
        byte[] ujumbe = 문자.부호화("한글 Stream_thamani");
        출력쪽.andika(ujumbe, 0, ujumbe.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[ujumbe.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 faili 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.simbua_fiche_data(받은글), "한글 Stream_thamani"), "부분 읽기와 andika");
        출력쪽.andika(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_thamani 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        mmiliki_kitambulishi.출력().andika(255);
        검사.참인지(mgeni_thamani.입력().읽기() == 255, "usimbaji_thamani 없는 한 baiti_thamani");
        출력쪽.funga();
        검사.참인지(mgeni_thamani.닫힘() && 입력.읽기() == -1, "닫기와 faili 끝");
        입력.funga(); 검사.참인지(mmiliki_kitambulishi.닫힘(), "입력 Stream_thamani funga");
        mgeni_thamani.funga(); mmiliki_kitambulishi.funga();
        kituo_thamani.대기시간(15);
        boolean 시간제한 = false;
        try { kituo_thamani.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        kituo_thamani.funga(); 검사.참인지(kituo_thamani.닫힘(), "수신창구 funga");
        전문통로 받는곳 = 전문통로.unda(0), 보내는곳 = 전문통로.unda(0);
        받는곳.대기시간(200);
        보내는곳.tuma("127.0.0.1", 받는곳.namba_ya_kituo(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.funga(); 받는곳.funga();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 funga");
        출력.andika_laini("한국어 통신 thibitisha: UNGANISHA 전문 Stream_thamani 시간제한 funga");
    }
}
