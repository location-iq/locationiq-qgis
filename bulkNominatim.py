# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolButton

import os.path
import webbrowser
from .bulkDialog import BulkNominatimDialog
from .reverseGeocode import ReverseGeocodeTool
from .settings import SettingsWidget

class BulkNominatim(object):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self):
        """Initialize BulkNominatim GUI."""
        # Set up a toolbar
        self.toolbar = self.iface.addToolBar('LocationIQ Toolbar')
        self.toolbar.setObjectName('LocationIQToolbar')
        self.toolbar.setToolTip('LocationIQ Toolbar')

        # Initialize the Dialog Boxes
        self.settingsDialog = SettingsWidget(self.iface.mainWindow())
        self.reverseGeocodeTool = ReverseGeocodeTool(self.iface, self.settingsDialog)
        self.bulkNominatimDialog = BulkNominatimDialog(self.iface, self.iface.mainWindow(), self.settingsDialog)

        self.canvas.mapToolSet.connect(self.unsetTool)

        # Initialize the bulk nominatim dialog box
        icon = QIcon(os.path.dirname(__file__) + "/images/icon.png")
        self.nominatimAction = QAction(icon, u"Bulk GeoCoding", self.iface.mainWindow())
        self.nominatimAction.triggered.connect(self.nominatimTool)
        self.toolbar.addAction(self.nominatimAction)
        self.iface.addPluginToMenu(u"LocationIQ GeoCoding", self.nominatimAction)

        # Add Interface for Reverse GeoCoding
        icon = QIcon(os.path.dirname(__file__) + "/images/reverse.png")
        self.reverseGeocodeAction = QAction(icon, u"Reverse Point GeoCoding", self.iface.mainWindow())
        self.reverseGeocodeAction.triggered.connect(self.setReverseGeocodeTool)
        self.reverseGeocodeAction.setCheckable(True)
        self.toolbar.addAction(self.reverseGeocodeAction)
        self.iface.addPluginToMenu(u"LocationIQ GeoCoding", self.reverseGeocodeAction)


        # Initialize the Settings Menu
        settingsicon = QIcon(os.path.dirname(__file__) + '/images/settings.png')
        self.settingsAction = QAction(settingsicon, u"LocationIQ Settings", self.iface.mainWindow())
        self.settingsAction.triggered.connect(self.settings)
        self.iface.addPluginToMenu(u"LocationIQ GeoCoding", self.settingsAction)

        # Help
        helpicon = QIcon(os.path.dirname(__file__) + '/images/help.png')
        self.helpAction = QAction(helpicon, u"Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.help)
        self.iface.addPluginToMenu(u"LocationIQ GeoCoding", self.helpAction)

    def unsetTool(self, tool):
        '''Uncheck the Reverse Geocoding tool'''
        try:
            if not isinstance(tool, ReverseGeocodeTool):
                self.reverseGeocodeAction.setChecked(False)
                self.reverseGeocodeTool.clearSelection()
        except:
            pass

    def unload(self):
        """Unload BulkNominatim from the QGIS interface."""
        self.canvas.unsetMapTool(self.reverseGeocodeTool)
        self.iface.removePluginMenu(u"LocationIQ GeoCoding", self.nominatimAction)
        self.iface.removePluginMenu(u"LocationIQ GeoCoding", self.reverseGeocodeAction)
        self.iface.removePluginMenu(u"LocationIQ GeoCoding", self.settingsAction)
        self.iface.removePluginMenu(u"LocationIQ GeoCoding", self.helpAction)
        # Remove Toolbar
        del self.toolbar
        self.reverseGeocodeTool.unload()

    def setReverseGeocodeTool(self):
        self.reverseGeocodeAction.setChecked(True)
        self.canvas.setMapTool(self.reverseGeocodeTool)

    def nominatimTool(self):
        """Display the dialog window."""
        self.bulkNominatimDialog.show()

    def settings(self):
        self.settingsDialog.show()

    def help(self):
        '''Display a help page'''
        url = QUrl("https://locationiq.com/docs?ref=qgis").toString()
        webbrowser.open(url, new=2)
