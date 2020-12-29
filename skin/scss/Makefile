all:

.scss.css:
	$(SCSS) $< $@

install: 
	$(SCSS) --update --watch .:$(DOCROOT)skin/css/

clean:
	-rm *~ *.css *.css.map

.SUFFIXES: .scss .css
