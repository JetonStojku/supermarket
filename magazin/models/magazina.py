from odoo import fields, models, api


class Magazina(models.Model):
    _name = 'magazin.magazina'

    name = fields.Char(string='Emri', required=True)
    adresa = fields.Char(string='Adresa', required=False)
    produkt_ids = fields.One2many(comodel_name='magazin.sasia', inverse_name='magazine_id', string='Produkt_ids', required=False)
