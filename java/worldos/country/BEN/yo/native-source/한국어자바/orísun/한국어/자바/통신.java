// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP àṣìṣe 상태도 호출자가 판단할 수 있도록 Fèsì 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI àdírẹ́ẹ̀sì, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Darapọ̀ = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Darapọ̀.send(HttpRequest.newBuilder(àdírẹ́ẹ̀sì).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String àdírẹ́ẹ̀sì, int ohun_èlò_alárídìmú_ojú, int 제한밀리초) throws IOException {
        Socket Darapọ̀ = new Socket();
        try {
            Darapọ̀.connect(new InetSocketAddress(àdírẹ́ẹ̀sì, ohun_èlò_alárídìmú_ojú), 제한밀리초);
            Darapọ̀.setSoTimeout(제한밀리초);
            return Darapọ̀;
        } catch (IOException àṣìṣe) { Darapọ̀.close(); throw àṣìṣe; }
    }
}
