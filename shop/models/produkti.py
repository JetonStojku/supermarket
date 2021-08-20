from odoo import fields, models, api


class Produkti (models.Model):
    _name = 'produkti'
    _description = 'Description'

    name = fields.Char(string='Emri', required=True)
    cmimi = fields.Float(string='Cmimi', required=False)
    sasia_ne_gjendje = fields.Float(string='Sasia ne gjendje')
    vendodhja = fields.Char(string='Vendodhja', required=False)
    shporta_ids = fields.One2many(comodel_name='shporta', inverse_name='produkti', string='Shporta_ids')
