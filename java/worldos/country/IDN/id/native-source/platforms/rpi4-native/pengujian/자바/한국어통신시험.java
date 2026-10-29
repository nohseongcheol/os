// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Indonesia.Asli.*;

/** 동일 바이트코드를 OpenJDK와 Asli JVM에서 실행하는 komunikasi 계약 pengujian. */
public class 한국어통신시험 {
    public static void main(String[] argumen) throws I_O_pengecualian {
        terima_port port_VALUE = 연결통신.수신열기(0);
        koneksi tamu_VALUE = 연결통신.Buka("127.0.0.1", port_VALUE.nomor_port());
        koneksi pemilik_pengidentifikasi = port_VALUE.terima();
        tamu_VALUE.TIMEOUT(200); pemilik_pengidentifikasi.TIMEOUT(200);
        검사.참인지(tamu_VALUE.연결됨() && !tamu_VALUE.닫힘(), "Sambung Status_VALUE");
        검사.참인지(pemilik_pengidentifikasi.nomor_port() == tamu_VALUE.lokal_nomor_port(), "serekan_VALUE nomor_port");
        검사.참인지(tamu_VALUE.nomor_port() == pemilik_pengidentifikasi.lokal_nomor_port(), "lokal_Cakupan nomor_port");
        aliran_input 입력 = pemilik_pengidentifikasi.입력(); aliran_output 출력쪽 = tamu_VALUE.keluaranTeks();
        byte[] email = 문자.부호화("한글 Stream_VALUE");
        출력쪽.Tulis(email, 0, email.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[email.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Baca(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 berkas 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekripsikan_data(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Tulis");
        출력쪽.Tulis(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Baca(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Baca");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Baca();
        검사.참인지(두바이트[1] == 18, "나머지 Baca");
        pemilik_pengidentifikasi.keluaranTeks().Tulis(255);
        검사.참인지(tamu_VALUE.입력().Baca() == 255, "pengodean_VALUE 없는 한 byte_VALUE");
        출력쪽.Tutup();
        검사.참인지(tamu_VALUE.닫힘() && 입력.Baca() == -1, "닫기와 berkas 끝");
        입력.Tutup(); 검사.참인지(pemilik_pengidentifikasi.닫힘(), "입력 Stream_VALUE Tutup");
        tamu_VALUE.Tutup(); pemilik_pengidentifikasi.Tutup();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.terima(); } catch (tunggu_TIMEOUT_pengecualian 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "terima_VALUE TIMEOUT");
        port_VALUE.Tutup(); 검사.참인지(port_VALUE.닫힘(), "terima_port Tutup");
        전문통로 받는곳 = 전문통로.Buka(0), 보내는곳 = 전문통로.Buka(0);
        받는곳.TIMEOUT(200);
        보내는곳.kirim("127.0.0.1", 받는곳.nomor_port(), "전문 한글");
        검사.참인지(문자.같음(받는곳.terima(), "전문 한글"), "전문 송수신");
        보내는곳.Tutup(); 받는곳.Tutup();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Tutup");
        keluaranTeks.tulis_baris("Indonesia komunikasi periksa: Sambung 전문 Stream_VALUE 시간제한 Tutup");
    }
}
