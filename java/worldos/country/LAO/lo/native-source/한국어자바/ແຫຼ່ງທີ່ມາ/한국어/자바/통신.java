// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ຂໍ້ຜິດພາດ 상태도 호출자가 판단할 수 있도록 ຕອບກັບ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ອີເມວ, Duration ຈໍາກັດເວລາ)
            throws IOException, InterruptedException {
        HttpClient ເຊື່ອມຕໍ່ = HttpClient.newBuilder().connectTimeout(ຈໍາກັດເວລາ).build();
        return ເຊື່ອມຕໍ່.send(HttpRequest.newBuilder(ອີເມວ).timeout(ຈໍາກັດເວລາ).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ອີເມວ, int 포트, int 제한밀리초) throws IOException {
        Socket ເຊື່ອມຕໍ່ = new Socket();
        try {
            ເຊື່ອມຕໍ່.connect(new InetSocketAddress(ອີເມວ, 포트), 제한밀리초);
            ເຊື່ອມຕໍ່.setSoTimeout(제한밀리초);
            return ເຊື່ອມຕໍ່;
        } catch (IOException ຂໍ້ຜິດພາດ) { ເຊື່ອມຕໍ່.close(); throw ຂໍ້ຜິດພາດ; }
    }
}
