all:

clean:
	-rm *~

release:
	mkdir -p $(PROJECTRELEASEDIR)php/
	$(RSYNC) Makefile *.php $(PROJECTRELEASEDIR)php/

prod:
	mkdir -p $(STAGE)/html/
	$(RSYNC) *.php $(STAGE)/html/
