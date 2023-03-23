export HOST = merlin
export PROJECT = achilles

export PROD = $(HOST):/srv/www/vhosts/$(PROJECT).zoidtechnologies.com/
export STAGEPROD = /srv/staging/$(PROJECT).zoidtechnologies.com/
export STAGEPRODDOCROOT = $(STAGEPROD)html/

export datestamp = $(shell date +%Y%m%d-%H%M)
export archivename = $(PROJECT)-$(datestamp)-$(USER)
export installfile = install --mode=0660

export RSYNC = rsync --delete-after --chmod=Dg=rwxs,Fgu=rw,Fo=r --verbose \
	--archive --update --backup --recursive \
	--human-readable --rsh=ssh \
	--no-owner --no-group --checksum

export PROJECTRELEASEDIR = /srv/repo/$(PROJECT)/
export PROJECTRELEASES = /home/jam/projects/zoidweb2/trunk/$(PROJECT)/releases/
export PROJECTBUILDDIR = $(PROJECTRELEASES)$(archivename)/

export SCSS = sass --sourcemap=none --stop-on-error --trace --style expanded

all:

clean:
	-rm *~
	$(MAKE) -C skin clean
	$(MAKE) -C php clean

prod:	export DOCROOT = $(STAGEPRODDOCROOT)
prod:	export STAGE = $(STAGEPROD)
prod:
	mkdir -p $(DOCROOT)
	mkdir -p $(STAGE)templates_c/

#	$(MAKE) -C .. prod
	$(MAKE) -C php install
	$(MAKE) -C skin install
	-$(MAKE) -C js install
	$(installfile) config-prod.php $(DOCROOT)config.php
	# $(installfile) ../php/zoidweb2.php ../php/bbsengine3.php $(DOCROOT)
	-$(installfile) htaccess-prod $(DOCROOT).htaccess
	$(RSYNC) --delete-after $(STAGE) $(PROD)

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
