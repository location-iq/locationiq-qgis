import os
import urllib.parse

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

NOMURL = 'https://us1.locationiq.com/v1'

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'liq_settings.ui'))


class LIQSettingsWidget(QDialog, FORM_CLASS):
    def __init__(self, parent):
        super(LIQSettingsWidget, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore)
        self.nominatimURL = NOMURL
        settings = QSettings()
        self.liq_url_textbox.setText(settings.value('/BulkNominatim/URL', NOMURL))
        self.api_key = settings.value('/BulkNominatim/api_access_token')
        self.api_access_token_textbox.setText(self.api_key)
        self.language = settings.value('/BulkNominatim/language')
        self.language_textbox.setText(self.language)
        self.country_codes = settings.value('/BulkNominatim/country_codes')
        self.country_codes_textbox.setText(self.country_codes)
        self.zoom = settings.value('/BulkNominatim/levelOfDetail', '18')
        self.bounded = settings.value('/BulkNominatim/bounded')
        self.bounded_checkbox.setChecked(True if self.bounded == '1' else False)
        self.viewbox = settings.value('/BulkNominatim/viewbox')
        self.viewbox_textbox.setText(self.viewbox)
        self.source = settings.value('/BulkNominatim/source')
        self.source_textbox.setText(self.source)
        print(settings.value('/BulkNominatim/normalize', '1'))
        self.normalize = settings.value('/BulkNominatim/normalize', '1')
        self.normalize_checkbox.setChecked(True if self.normalize == '1' else False)

    def accept(self):
        '''Accept the settings and save them for next time.'''
        settings = QSettings()
        self.nominatimURL = self.liq_url_textbox.text()
        settings.setValue('/BulkNominatim/URL', self.nominatimURL)
        self.api_key = self.api_access_token_textbox.text()
        settings.setValue('/BulkNominatim/api_access_token', self.api_key)
        self.language = self.language_textbox.text()
        settings.setValue('/BulkNominatim/language', self.language)
        self.country_codes = self.country_codes_textbox.text()
        settings.setValue('/BulkNominatim/country_codes', self.country_codes)
        self.viewbox = self.viewbox_textbox.text()
        settings.setValue('/BulkNominatim/view_box', self.viewbox)
        self.bounded = '1' if self.bounded_checkbox.isChecked() else '0'
        settings.setValue('/BulkNominatim/bounded', self.bounded)
        self.source = self.source_textbox.text()
        settings.setValue('/BulkNominatim/source', self.source)
        self.normalize = '1' if self.normalize_checkbox.isChecked() else '0'
        settings.setValue('/BulkNominatim/normalize', self.normalize)
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
        return urllib.parse.urlencode(params)
