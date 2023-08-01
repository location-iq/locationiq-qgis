import os
import urllib.parse

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

NOMURL = 'https://us1.locationiq.com/v1'

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings.ui'))


class SettingsWidget(QDialog, FORM_CLASS):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore)
        self.nominatimURL = NOMURL
        settings = QSettings()
        self.liq_url_textbox.setText(settings.value('/LocationIQ/URL', NOMURL))
        self.api_key = settings.value('/LocationIQ/api_access_token')
        self.api_access_token_textbox.setText(self.api_key)
        self.language = settings.value('/LocationIQ/language')
        self.language_textbox.setText(self.language)
        self.country_codes = settings.value('/LocationIQ/country_codes')
        self.country_codes_textbox.setText(self.country_codes)
        self.zoom = settings.value('/LocationIQ/zoom', '18')
        self.bounded = settings.value('/LocationIQ/bounded')
        self.bounded_checkbox.setChecked(True if self.bounded == '1' else False)
        self.viewbox = settings.value('/LocationIQ/viewbox')
        self.viewbox_textbox.setText(self.viewbox)
        self.source = settings.value('/LocationIQ/source')
        self.source_textbox.setText(self.source)
        self.normalize = settings.value('/LocationIQ/normalize', '1')
        self.normalize_checkbox.setChecked(True if self.normalize == '1' else False)
        self.maxAddress = int(settings.value('/LocationIQ/maxAddress', 100))

    def accept(self):
        '''Accept the settings and save them for next time.'''
        settings = QSettings()
        self.nominatimURL = self.liq_url_textbox.text()
        settings.setValue('/LocationIQ/URL', self.nominatimURL)
        self.api_key = self.api_access_token_textbox.text()
        settings.setValue('/LocationIQ/api_access_token', self.api_key)
        self.zoom = self.zoom_spinBox.text()
        settings.setValue('/LocationIQ/zoom', self.zoom)
        self.language = self.language_textbox.text()
        settings.setValue('/LocationIQ/language', self.language)
        self.country_codes = self.country_codes_textbox.text()
        settings.setValue('/LocationIQ/country_codes', self.country_codes)
        self.viewbox = self.viewbox_textbox.text()
        settings.setValue('/LocationIQ/view_box', self.viewbox)
        self.bounded = '1' if self.bounded_checkbox.isChecked() else '0'
        settings.setValue('/LocationIQ/bounded', self.bounded)
        self.source = self.source_textbox.text()
        settings.setValue('/LocationIQ/source', self.source)
        self.normalize = '1' if self.normalize_checkbox.isChecked() else '0'
        settings.setValue('/LocationIQ/normalize', self.normalize)
        self.maxAddress = self.maxAddress_textbox.text() or '100'
        settings.setValue('/LocationIQ/maxAddress', self.maxAddress)
        self.close()

    def restore(self):
        self.liq_url_textbox.setText(NOMURL)
        self.api_access_token_textbox.clear()
        self.language_textbox.clear()
        self.country_codes_textbox.clear()
        self.viewbox_textbox.clear()
        self.bounded_checkbox.setChecked(False)
        self.source_textbox.clear()
        self.normalize_checkbox.setChecked(True)
        self.zoom_spinBox.setValue(18)
        self.maxAddress_textbox.clear()

    def searchURL(self):
        return self.nominatimURL + '/search'

    def reverseURL(self):
        return self.nominatimURL + '/reverse'

    def url_params_str(self):
        params = {
            "key": self.api_key,
        }
        if self.language:
            params["accept-language"] = self.language
        if self.country_codes:
            params["countrycodes"] = self.country_codes
        if self.zoom:
            params["zoom"] = self.zoom
        if self.bounded != '0':
            params["bounded"] = self.bounded
        if self.viewbox:
            params["viewbox"] = self.viewbox
        if self.source != 'null':
            params["source"] = self.source
        if self.normalize != '0':
            params["normalizeaddress"] = self.normalize
        if self.maxAddress:
            params["limit"] = self.maxAddress
        return urllib.parse.urlencode(params)
