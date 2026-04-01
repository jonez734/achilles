MAIN_FILES = achilles.scss section.scss timeline.scss topbar.scss
CSS_FILES = $(MAIN_FILES:.scss=.css)

all: $(CSS_FILES)

%.css: %.scss
	sass --no-cache --load-path /home/opencode/data/work/zoid6/shared/skin/scss/ \
	     --load-path /home/opencode/data/work/bbsengine6/skin/scss/ \
	     --load-path /home/opencode/data/work/zoid6/scss/ \
	     --load-path $(CURDIR) \
	     --sourcemap=none --stop-on-error --trace --style expanded $< $@

stage: $(CSS_FILES)
	sass --no-cache --load-path /home/opencode/data/work/zoid6/shared/skin/scss/ \
	     --load-path /home/opencode/data/work/bbsengine6/skin/scss/ \
	     --load-path /home/opencode/data/work/zoid6/scss/ \
	     --load-path $(CURDIR) \
	     --sourcemap=none --stop-on-error --trace --style expanded \
	     --update .:$(STAGE)skin/css/

clean:
	-rm *~ *.css *.css.map

.PHONY: all clean stage
