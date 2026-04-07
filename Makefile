export HOST = merlin
export PROJECT = achilles
export VERSION = $(shell date +%Y%m%d%H%M)

export PROD = $(HOST):/srv/www/vhosts/zoidtechnologies.com/html/$(PROJECT)/
export STAGE = /srv/staging/zoidtechnologies.com/html/$(PROJECT)/

export datestamp = $(shell date +%Y%m%d-%H%M)
export archivename = $(PROJECT)-$(datestamp)-$(USER)
export installfile = install --mode=0660

export RSYNC = rsync --delete-after --chmod=Dg=rwxs,Fgu=rw,Fo=r --verbose \
	--archive --update --backup --recursive \
	--human-readable --rsh=ssh --mkpath \
	--no-owner --no-group --checksum

export SCSS = sass --sourcemap=none --stop-on-error --trace --style expanded

all:

version:
	@echo '__version__ = "0.0.1.dev$(VERSION)"' > py/src/achilles/_version.py
	@echo '__datestamp__ = "'`date +%Y%m%d-%H%M`-`whoami`'"' >> py/src/achilles/_version.py

clean:
	-rm *~
#	$(MAKE) -C skin clean
#	$(MAKE) -C php clean
	$(MAKE) -C sql clean
	$(MAKE) -C www clean

www:
	-$(MAKE) -C www stage
	$(RSYNC) $(STAGE) $(PROD)

release:
	echo "-=- making a new release of $(PROJECT) -=-";
	mkdir -p $(PROJECTRELEASEDIR);
	mkdir -p $(PROJECTBUILDDIR)
	$(installfile) Makefile config-prod.php htaccess-prod $(PROJECTBUILDDIR);
	$(MAKE) -C php release;
	$(MAKE) -C skin release;
	$(MAKE) -C sql release;
	pushd $(PROJECTRELEASES);\
	echo -n "pwd=";pwd;\
	echo -n "projectreleases="; echo $(PROJECTRELEASES);\
	echo -n "archivename=";echo $(archivename);\
	tar jcvf $(PROJECTRELEASEDIR)$(archivename).tar.bz2 $(archivename)/*;\
	tar zcvf $(PROJECTRELEASEDIR)$(archivename).tgz $(archivename)/*;\
	zip -r $(PROJECTRELEASEDIR)$(archivename).zip $(archivename)/*;\
	popd;\
	echo "[DONE]"

push:
	git push -u github master

backup:
	rsync --recursive --verbose --exclude=.venv . /run/media/jam/AEAB-CF37/projects/$(PROJECT)/
	
.PHONY: www
