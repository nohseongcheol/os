// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.मोबाइल_मूल्य;

/** PIT चे ठोके आणि कार्याधिकार काढून घेण्याची वेळ सांभाळते. */
public final class घड्याळ {
    private final int कालठोके_प्रति_दुसरे;
    private long कालठोका_संख्या;

    public घड्याळ(int कालठोके_प्रति_दुसरे) {
        if (कालठोके_प्रति_दुसरे <= 0) {
            throw new IllegalArgumentException("초당 कालठोका_मूल्य 수가 올바르지 않습니다.");
        }
        this.कालठोके_प्रति_दुसरे = कालठोके_प्रति_दुसरे;
    }

    public long कालठोका_मूल्य() {
        return ++कालठोका_संख्या;
    }

    public long कालठोका_संख्या() {
        return कालठोका_संख्या;
    }

    public long कालावधी_पश्चात_मिलिसेकंद() {
        return कालठोका_संख्या * 1000L / कालठोके_प्रति_दुसरे;
    }
}

