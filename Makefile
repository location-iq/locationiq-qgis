PLUGINNAME = locationiq-qgis
PLUGINS = "$(HOME)"/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)
PY_FILES = __init__.py bulkDialog.py bulkNominatim.py reverseGeocode.py settings.py
EXTRAS = metadata.txt
UIFILES = bulkNominatim.ui settings.ui reverseGeocode.ui

deploy:
	mkdir -p $(PLUGINS)
	cp -vf $(PY_FILES) $(PLUGINS)
	cp -vf $(EXTRAS) $(PLUGINS)
	cp -vfr images $(PLUGINS)
	cp -vf $(UIFILES) $(PLUGINS)
	cp -vfr doc $(PLUGINS)

