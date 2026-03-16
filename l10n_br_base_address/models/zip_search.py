import re
import logging
from odoo import models

_logger = logging.getLogger(__name__)




class ZipSearchMixin(models.AbstractModel):
    _name = 'zip.search.mixin'
    _description = 'Pesquisa de CEP'

    def search_address_by_zip(self, zip_code):
        zip_code = re.sub('[^0-9]', '', zip_code or '')
        try:
            import requests
            url = f"https://viacep.com.br/ws/{zip_code}/json/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            res = response.json()
            if "erro" in res:
                return {}
        except Exception:
            return {}

        state = self.env['res.country.state'].search(
            [('country_id.code', '=', 'BR'),
             ('code', '=', res.get('uf'))])

        city = self.env['res.city'].search([
            ('name', '=ilike', res.get('localidade')),
            ('state_id', '=', state.id)])

        return {
            'zip': zip_code,
            'street': res.get('logradouro'),
            'l10n_br_district': res.get('bairro'),
            'country_id': state.country_id.id,
            'state_id': state.id,
            'city_id': city.id
        }
