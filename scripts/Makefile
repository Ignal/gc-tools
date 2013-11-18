SCRIPTS=arrange_csv.sh bstw.sh gc-kml.sh gc-gpx.sh inv_letters.sh \
        rot.sh setcoords.sh

install:
	cp -i $(SCRIPTS) /usr/local/bin

uninstall:
	for i in $(SCRIPTS); do rm -f /usr/local/bin/$$i; done
