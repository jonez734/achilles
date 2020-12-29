all:

clean:
	-rm *~

install:
	mkdir -p $(STAGEPROD)tmpl/
	$(installfile) *.tmpl $(STAGEPROD)tmpl/

release:
	mkdir -p $(PROJECTBUILDDIR)skin/tmpl/
	$(installfile) Makefile *.tmpl $(PROJECTBUILDDIR)skin/tmpl/
