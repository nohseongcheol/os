// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ข้อผิดพลาด 상태도 호출자가 판단할 หมายเลข 있도록 ตอบกลับ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI อีเมล, Duration ขีดจํากัดเวลา)
            throws IOException, InterruptedException {
        HttpClient เชื่อมต่อ = HttpClient.newBuilder().connectTimeout(ขีดจํากัดเวลา).build();
        return เชื่อมต่อ.send(HttpRequest.newBuilder(อีเมล).timeout(ขีดจํากัดเวลา).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket เชื่อมต่อ_ปลายทาง(String อีเมล, int ฮาร์ดแวร์_แปลง, int 제한밀리초) throws IOException {
        Socket เชื่อมต่อ = new Socket();
        try {
            เชื่อมต่อ.connect(new InetSocketAddress(อีเมล, ฮาร์ดแวร์_แปลง), 제한밀리초);
            เชื่อมต่อ.setSoTimeout(제한밀리초);
            return เชื่อมต่อ;
        } catch (IOException ข้อผิดพลาด) { เชื่อมต่อ.close(); throw ข้อผิดพลาด; }
    }
}
