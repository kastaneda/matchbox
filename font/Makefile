FONT := block_ascii block_cyrillic block_extended block_punctuation
FONT_JSON = $(FONT:=.json)
FONT_PNG = $(FONT:=.png)

font.json: $(FONT_JSON) $(FONT_PNG)
	./tool -read $(FONT) --verbose
