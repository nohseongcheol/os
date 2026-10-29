CompilateurJava ?= javac
lanceurJava ?= java
fichiersSourceAncienSystème := $(shell find SourcesFondamentales -type f -name '*.java' | sort)
répertoireSortieClasse := résultat/valeurClasse
marqueurAchèvement := $(répertoireSortieClasse)/.estTerminé

.PHONY: construireTous Contrôles Hôte contrôlerHangul construireNettoyer construireImage

construireTous: Contrôles

$(marqueurAchèvement): $(fichiersSourceAncienSystème)
	mkdir -p $(répertoireSortieClasse)
	$(CompilateurJava) -encoding UTF-8 -Xlint:all -Werror -d $(répertoireSortieClasse) $(fichiersSourceAncienSystème)
	touch $(marqueurAchèvement)

contrôlerHangul:
	@sh Outils/ContrôleIdentifiants.sh

Contrôles: contrôlerHangul $(marqueurAchèvement)
	$(lanceurJava) -ea -cp $(répertoireSortieClasse) Guyane_française.JGufOS.Tests.testTous

Hôte: Contrôles
	$(lanceurJava) -cp $(répertoireSortieClasse) Guyane_française.JGufOS.Hôte.démarrageHôte

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 SourcesFondamentales/의 valeurObjet fondation 관리 valeurNoyau 전체를 AOT 변환하는 대상은 아니다.
construireImage:
	$(MAKE) -C os iso

construireNettoyer:
	rm -rf résultat
