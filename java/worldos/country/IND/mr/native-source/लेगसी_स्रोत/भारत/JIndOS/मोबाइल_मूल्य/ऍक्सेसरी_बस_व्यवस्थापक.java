// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.मोबाइल_मूल्य;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI साधनशोधाचे निष्कर्ष आणि BAR/IRQ मूल्ये सांभाळते. */
public final class ऍक्सेसरी_बस_व्यवस्थापक {
    public static final class मोबाइल_मूल्य {
        private final int पुरवठादार_आयडेंटिफायर;
        private final int मोबाइल_आयडेंटिफायर;
        private final int आदानप्रदान_पाया;
        private final int इंटरप्ट_संख्या;

        public मोबाइल_मूल्य(int पुरवठादार_आयडेंटिफायर, int मोबाइल_आयडेंटिफायर, int आदानप्रदान_पाया, int इंटरप्ट_संख्या) {
            this.पुरवठादार_आयडेंटिफायर = पुरवठादार_आयडेंटिफायर;
            this.मोबाइल_आयडेंटिफायर = मोबाइल_आयडेंटिफायर;
            this.आदानप्रदान_पाया = आदानप्रदान_पाया;
            this.इंटरप्ट_संख्या = इंटरप्ट_संख्या;
        }

        public int पुरवठादार_आयडेंटिफायर() { return पुरवठादार_आयडेंटिफायर; }
        public int मोबाइल_आयडेंटिफायर() { return मोबाइल_आयडेंटिफायर; }
        public int आदानप्रदान_पाया() { return आदानप्रदान_पाया; }
        public int इंटरप्ट_संख्या() { return इंटरप्ट_संख्या; }
    }

    private final List<मोबाइल_मूल्य> उपकरणे_यादी = new ArrayList<मोबाइल_मूल्य>();

    public void शोधलेले_मूल्य(मोबाइल_मूल्य मोबाइल_मूल्य) {
        उपकरणे_यादी.add(मोबाइल_मूल्य);
    }

    public List<मोबाइल_मूल्य> उपकरणे_यादी() {
        return Collections.unmodifiableList(उपकरणे_यादी);
    }

    public मोबाइल_मूल्य प्रविष्टी_शोधा(int पुरवठादार_आयडेंटिफायर, int मोबाइल_आयडेंटिफायर) {
        for (मोबाइल_मूल्य उमेदवार : उपकरणे_यादी) {
            if (उमेदवार.पुरवठादार_आयडेंटिफायर == पुरवठादार_आयडेंटिफायर && उमेदवार.मोबाइल_आयडेंटिफायर == मोबाइल_आयडेंटिफायर) {
                return उमेदवार;
            }
        }
        return null;
    }
}

