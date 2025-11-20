FONT := block_ascii block_cyrillic block_extended block_punctuation
FONT_JSON := $(patsubst %,%.json,$(FONT))
FONT_PNG := $(patsubst %,%.png,$(FONT))

font.json: $(FONT_JSON) $(FONT_PNG)
	./tool -read $(FONT) --verbose
