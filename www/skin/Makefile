all:

clean:
	-rm *~
	$(MAKE) -C css clean
	$(MAKE) -C tmpl clean
	# $(MAKE) -C art clean

install:
	mkdir -p $(DOCROOT)skin/tmpl/
	mkdir -p $(DOCROOT)skin/css/
	mkdir -p $(DOCROOT)skin/art/
	$(MAKE) -C scss install
	$(MAKE) -C tmpl install
	# $(MAKE) -C art install

release:
	mkdir -p $(PROJECTBUILDDIR)skin/
	$(installfile) Makefile $(PROJECTBUILDDIR)skin/
	$(MAKE) -C tmpl release
	$(MAKE) -C css release
