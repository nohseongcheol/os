package main

import (
	"bytes"
	"encoding/json"
	"encoding/xml"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

const (
	countriesPath = "/usr/share/iso-codes/json/iso_3166-1.json"
	languagesPath = "/usr/share/iso-codes/json/iso_639-3.json"
	cldrPath      = "/usr/share/liblangtag/common/supplemental/supplementalData.xml"
)

type country struct {
	Alpha2 string `json:"alpha_2"`
	Alpha3 string `json:"alpha_3"`
	Name   string `json:"name"`
}

type countriesFile struct {
	Countries []country `json:"3166-1"`
}

type language struct {
	Alpha2 string `json:"alpha_2"`
	Alpha3 string `json:"alpha_3"`
	Name   string `json:"name"`
}

type languagesFile struct {
	Languages []language `json:"639-3"`
}

type languagePopulation struct {
	Type           string `xml:"type,attr"`
	Population     string `xml:"populationPercent,attr"`
	OfficialStatus string `xml:"officialStatus,attr"`
}

type territory struct {
	Type      string               `xml:"type,attr"`
	Languages []languagePopulation `xml:"languagePopulation"`
}

type supplementalData struct {
	TerritoryInfo struct {
		Territories []territory `xml:"territory"`
	} `xml:"territoryInfo"`
}

type selection struct {
	Code       string
	Population float64
	Status     string
}

func load(path string, target interface{}) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		panic(err)
	}
	switch target.(type) {
	case *supplementalData:
		err = xml.Unmarshal(data, target)
	default:
		err = json.Unmarshal(data, target)
	}
	if err != nil {
		panic(err)
	}
}

func baseLanguage(code string) string {
	if index := strings.Index(code, "_"); index >= 0 {
		return code[:index]
	}
	return code
}

func selectLanguage(item territory) selection {
	bestOfficial := selection{}
	bestAny := selection{}
	for _, candidate := range item.Languages {
		population, _ := strconv.ParseFloat(candidate.Population, 64)
		current := selection{Code: candidate.Type, Population: population, Status: candidate.OfficialStatus}
		if population > bestAny.Population {
			bestAny = current
		}
		if candidate.OfficialStatus == "official" || candidate.OfficialStatus == "de_facto_official" {
			if population > bestOfficial.Population {
				bestOfficial = current
			}
		}
	}
	if bestOfficial.Code != "" {
		return bestOfficial
	}
	return bestAny
}

func nativeLanguageName(localeCode, english string) string {
	command := exec.Command("gettext", "-d", "iso_639-3", english)
	command.Env = append(os.Environ(), "LANGUAGE="+baseLanguage(localeCode), "LC_ALL=C.UTF-8")
	output, err := command.Output()
	if err != nil {
		return english
	}
	value := strings.TrimSpace(string(output))
	if value == "" {
		return english
	}
	return value
}

func glossaryStats(path string) (translated, fallback int) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return 0, 0
	}
	for index, line := range strings.Split(string(data), "\n") {
		if index == 0 || line == "" {
			continue
		}
		fields := strings.Split(line, "\t")
		if len(fields) >= 3 && (fields[2] == "gettext" || fields[2] == "native-English" || fields[2] == "curated-seed") {
			translated++
		} else {
			fallback++
		}
	}
	return translated, fallback
}

func effectiveGlossaryStats(path, language string) (translated, fallback int) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return 0, 0
	}
	english := language == "en" || language == "und" || strings.HasPrefix(language, "en_")
	for index, line := range strings.Split(string(data), "\n") {
		if index == 0 || line == "" {
			continue
		}
		fields := strings.Split(line, "\t")
		if len(fields) >= 2 && (english || fields[0] != fields[1]) {
			translated++
		} else {
			fallback++
		}
	}
	return translated, fallback
}

func main() {
	rootFlag := flag.String("root", "/home/user/worldos", "WorldOS root")
	sourceFlag := flag.String("source", "/home/user/engos", "engos source")
	localizerFlag := flag.String("localizer", "/home/user/worldos/tools/localize_engos", "compiled localizer")
	glossaryBuilderFlag := flag.String("glossary-builder", "/home/user/worldos/tools/build_semantic_glossary", "compiled semantic glossary builder")
	replaceFlag := flag.Bool("replace", false, "replace generated source directories")
	limitFlag := flag.Int("limit", 0, "generate only this many countries; zero means all")
	countryFlag := flag.String("country", "", "generate one ISO 3166-1 alpha-3 country")
	indexOnlyFlag := flag.Bool("index-only", false, "rebuild only the country/language index from existing glossaries")
	flag.Parse()
	// Named source trees contain audited local work. Regeneration is a separate
	// operation, and must not silently recreate a second Korean-named tree or
	// erase the localized one (even with the old -replace flag).
	if !*indexOnlyFlag {
		layouts, err := filepath.Glob(filepath.Join(*rootFlag, "나라", "*", "layout.json"))
		if err != nil {
			panic(err)
		}
		for _, layout := range layouts {
			if *countryFlag == "" || filepath.Base(filepath.Dir(layout)) == strings.ToUpper(*countryFlag) {
				panic("refusing donor regeneration of a localized source tree; edit the existing source, or use -index-only: " + layout)
			}
		}
	}
	management := func(root, name string) string {
		data, err := ioutil.ReadFile(filepath.Join(root, "layout.json"))
		if os.IsNotExist(err) {
			return filepath.Join(root, name)
		}
		var layout struct {
			Version int               `json:"version"`
			Paths   map[string]string `json:"paths"`
		}
		if err != nil || json.Unmarshal(data, &layout) != nil || layout.Version != 1 {
			panic("invalid management layout: " + root)
		}
		if mapped, ok := layout.Paths[name]; ok {
			name = mapped
		}
		if filepath.IsAbs(name) || name == ".." || strings.HasPrefix(filepath.Clean(name), "../") {
			panic("unsafe management path")
		}
		return filepath.Join(root, name)
	}

	var countries countriesFile
	var languages languagesFile
	var cldr supplementalData
	load(countriesPath, &countries)
	load(languagesPath, &languages)
	load(cldrPath, &cldr)

	territories := map[string]territory{}
	for _, item := range cldr.TerritoryInfo.Territories {
		territories[item.Type] = item
	}
	languageNames := map[string]string{}
	for _, item := range languages.Languages {
		languageNames[item.Alpha3] = item.Name
		if item.Alpha2 != "" {
			languageNames[item.Alpha2] = item.Name
		}
	}
	sort.Slice(countries.Countries, func(i, j int) bool { return countries.Countries[i].Alpha3 < countries.Countries[j].Alpha3 })

	var index io.Writer = &bytes.Buffer{}
	if *countryFlag == "" {
		indexPath := filepath.Join(*rootFlag, "나라-소스-언어선택.tsv")
		indexFile, err := os.Create(indexPath)
		if err != nil {
			panic(err)
		}
		defer indexFile.Close()
		index = indexFile
		fmt.Fprintln(index, "country_alpha3\tcountry_alpha2\tcountry_name\tlanguage\tpopulation_percent\tstatus\tnative_name\ttranslated_terms\tfallback_terms\tnaming")
	}

	generated := 0
	builtGlossaries := map[string]bool{}
	for _, item := range countries.Countries {
		if *countryFlag != "" && item.Alpha3 != strings.ToUpper(*countryFlag) {
			continue
		}
		if *limitFlag > 0 && generated >= *limitFlag {
			break
		}
		selected := selectLanguage(territories[item.Alpha2])
		if selected.Code == "" {
			selected = selection{Code: "en", Status: "fallback"}
		}
		base := baseLanguage(selected.Code)
		englishName := languageNames[base]
		if englishName == "" {
			englishName = base
		}
		nativeName := nativeLanguageName(base, englishName)
		glossaryCode := selected.Code
		if glossaryCode == "und" {
			glossaryCode = "en"
		}
		glossaryPath := filepath.Join(*rootFlag, "용어사전", strings.Replace(glossaryCode, "@", "_", -1)+".tsv")
		if !builtGlossaries[glossaryCode] {
			_, glossaryErr := os.Stat(glossaryPath)
			if !*indexOnlyFlag || glossaryErr != nil {
				command := exec.Command(*glossaryBuilderFlag, "-language", glossaryCode, "-vocabulary", filepath.Join(*rootFlag, "식별자-영어-어휘.tsv"), "-output", glossaryPath)
				command.Stdout = os.Stdout
				command.Stderr = os.Stderr
				if err := command.Run(); err != nil {
					panic(fmt.Sprintf("glossary %s: %v", glossaryCode, err))
				}
			}
			builtGlossaries[glossaryCode] = true
		}
		translated, fallback := glossaryStats(glossaryPath)
		destination := management(filepath.Join(*rootFlag, "나라", item.Alpha3), "소스")
		if *indexOnlyFlag {
			if effectiveTranslated, effectiveFallback := effectiveGlossaryStats(management(destination, "용어사전.tsv"), selected.Code); effectiveTranslated+effectiveFallback != 0 {
				translated, fallback = effectiveTranslated, effectiveFallback
			}
			fmt.Fprintf(index, "%s\t%s\t%s\t%s\t%.6g\t%s\t%s\t%d\t%d\tsemantic-word-translation\n", item.Alpha3, item.Alpha2, item.Name, selected.Code, selected.Population, selected.Status, nativeName, translated, fallback)
			generated++
			continue
		}
		if _, err := os.Stat(destination); err == nil {
			if !*replaceFlag {
				fmt.Fprintf(os.Stderr, "%s exists; use -replace to regenerate\n", destination)
				os.Exit(2)
			}
			if _, err := os.Stat(filepath.Join(destination, "이름대응표.tsv")); err != nil {
				fmt.Fprintf(os.Stderr, "refusing to replace non-generated directory: %s\n", destination)
				os.Exit(2)
			}
			if err := os.RemoveAll(destination); err != nil {
				panic(err)
			}
		}
		command := exec.Command(*localizerFlag, "country", *sourceFlag, destination, item.Alpha3, selected.Code, glossaryPath)
		command.Stdout = os.Stdout
		command.Stderr = os.Stderr
		if err := command.Run(); err != nil {
			panic(fmt.Sprintf("%s/%s: %v", item.Alpha3, selected.Code, err))
		}
		translated, fallback = effectiveGlossaryStats(filepath.Join(destination, "용어사전.tsv"), selected.Code)
		countryRoot := filepath.Dir(destination)
		makefile := fmt.Sprintf("COUNTRY_ALPHA3 := %s\nCOUNTRY_ALPHA2 := %s\n\n.PHONY: all kernel iso clean info source source-iso\n\nall: iso\ninfo:\n\t@sed -n '1,8p' country.conf\nkernel source:\n\t$(MAKE) -C 소스 kernel\niso source-iso:\n\t$(MAKE) -C 소스 iso\nclean:\n\t$(MAKE) -C 소스 clean\n", item.Alpha3, item.Alpha2)
		// Preserve independently installed launchers and all local parent targets.
		if _, err := os.Lstat(filepath.Join(countryRoot, "vbox-entry.json")); os.IsNotExist(err) {
			if err := ioutil.WriteFile(filepath.Join(countryRoot, "Makefile"), []byte(makefile), 0644); err != nil {
				panic(err)
			}
		} else if err != nil {
			panic(err)
		}
		configurationPath := filepath.Join(countryRoot, "country.conf")
		if configuration, err := ioutil.ReadFile(configurationPath); err == nil {
			lines := strings.Split(string(configuration), "\n")
			for index, line := range lines {
				if strings.HasPrefix(line, "DEFAULT_LANGUAGE=") {
					lines[index] = "DEFAULT_LANGUAGE=" + selected.Code
				}
			}
			if err := ioutil.WriteFile(configurationPath, []byte(strings.Join(lines, "\n")), 0644); err != nil {
				panic(err)
			}
		}
		details := fmt.Sprintf("# %s (%s) source language\n\n- country: %s (%s)\n- selected language: %s\n- CLDR population: %.6g%%\n- official status: %s\n- native language name: %s\n- target-language vocabulary: %d\n- unresolved source-glossary vocabulary: %d\n- naming mode: semantic word translation\n\nIdentifiers and source paths are composed from reviewed translated meanings. Language-name prefixes, hashes and invented letter-by-letter readings are prohibited. A technical loanword is accepted only when an installed gettext catalog or an explicit reviewed seed establishes common usage. `용어근거.tsv` records unresolved source-glossary fallbacks. ABI entry points, toolchain syntax, CPU registers and international standard abbreviations retain compatibility names. This directory contains its own kernel, assembly, build scripts, diagnostics and POSIX userland wrapper sources.\n", item.Name, item.Alpha3, item.Name, item.Alpha2, selected.Code, selected.Population, selected.Status, nativeName, translated, fallback)
		if err := ioutil.WriteFile(filepath.Join(destination, "나라언어.md"), []byte(details), 0644); err != nil {
			panic(err)
		}
		// Apply the same whole-concept policy used to migrate existing trees.
		// This changes names only, after the standalone implementation is copied.
		refine := exec.Command("python3", filepath.Join(*rootFlag, "tools", "refine_country_names.py"), "--root", *rootFlag, "--country", item.Alpha3, "--apply")
		refine.Stdout, refine.Stderr = os.Stdout, os.Stderr
		if err := refine.Run(); err != nil {
			panic(fmt.Sprintf("%s naming refinement: %v", item.Alpha3, err))
		}
		fmt.Fprintf(index, "%s\t%s\t%s\t%s\t%.6g\t%s\t%s\t%d\t%d\tsemantic-word-translation\n", item.Alpha3, item.Alpha2, item.Name, selected.Code, selected.Population, selected.Status, nativeName, translated, fallback)
		generated++
		if generated%10 == 0 || generated == len(countries.Countries) {
			fmt.Printf("generated country sources: %d/%d\n", generated, len(countries.Countries))
		}
	}
	if *countryFlag == "" && !*indexOnlyFlag && *limitFlag == 0 {
		check := exec.Command("python3", filepath.Join(*rootFlag, "tools", "refine_country_names.py"), "--root", *rootFlag, "--check")
		check.Stdout, check.Stderr = os.Stdout, os.Stderr
		if err := check.Run(); err != nil {
			panic(err)
		}
	}
}
