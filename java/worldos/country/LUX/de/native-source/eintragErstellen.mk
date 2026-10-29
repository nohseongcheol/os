JavaÜbersetzer ?= javac
javaStarter ?= java
altsystemQuelltextDateien := $(shell find Kernquelltext -type f -name '*.java' | sort)
klasseAusgabeVerzeichnis := ergebnis/klasseWert
fertigstellungMarkierung := $(klasseAusgabeVerzeichnis)/.istFertig

.PHONY: alleErzeugenAbbild Prüfpunkte Wirtssystem hangulPrüfen bereinigenErzeugenAbbild abbildErzeugenAbbild

alleErzeugenAbbild: Prüfpunkte

$(fertigstellungMarkierung): $(altsystemQuelltextDateien)
	mkdir -p $(klasseAusgabeVerzeichnis)
	$(JavaÜbersetzer) -encoding UTF-8 -Xlint:all -Werror -d $(klasseAusgabeVerzeichnis) $(altsystemQuelltextDateien)
	touch $(fertigstellungMarkierung)

hangulPrüfen:
	@sh Werkzeuge/BezeichnerPrüfung.sh

Prüfpunkte: hangulPrüfen $(fertigstellungMarkierung)
	$(javaStarter) -ea -cp $(klasseAusgabeVerzeichnis) Luxemburg.JLuxOS.Prüfungen.allePrüfung

Wirtssystem: Prüfpunkte
	$(javaStarter) -cp $(klasseAusgabeVerzeichnis) Luxemburg.JLuxOS.Wirtssystem.wirtssystemAnlauf

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 Kernquelltext/의 objektWert grundlage 관리 betriebskernWert 전체를 AOT 변환하는 대상은 아니다.
abbildErzeugenAbbild:
	$(MAKE) -C os iso

bereinigenErzeugenAbbild:
	rm -rf ergebnis
