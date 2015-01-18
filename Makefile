BUILDDIRS = bww qs bf ook
SUBDIRS = bash python3 bww qs bf ook

all depend clean:
	for i in $(BUILDDIRS); do make -C $$i $@; done

install uninstall:
	for i in $(SUBDIRS); do make -C $$i $@; done
