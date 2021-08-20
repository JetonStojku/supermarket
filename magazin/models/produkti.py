from odoo import fields, models, api


class Produkti(models.Model):
    _inherit = 'produkti'

    magazinat_ids = fields.One2many(comodel_name='magazin.sasia', inverse_name='produkt_id', string='Magazinat_ids', required=False)
    sasia_ne_gjendje = fields.Float(string='Sasia ne gjendje', compute='gjej_sasine_totale')

    @api.multi
    @api.depends('magazinat_ids')
    def gjej_sasine_totale(self):
        for produkti in self:
            search = self.env['magazin.sasia'].search([('produkt_id', '=', produkti.id)])
            produkti.sasia_ne_gjendje = 0
            for produkt in search:
                produkti.sasia_ne_gjendje += produkt.sasia


class Sasia(models.Model):
    _name = 'magazin.sasia'

    produkt_id = fields.Many2one(comodel_name='produkti', string='Produkti', required=True)
    magazine_id = fields.Many2one(comodel_name='magazin.magazina', string='Magazine ID', required=True)
    vendodhja_ne_mag = fields.Char(string='Vendodhja ne magazine', required=False)
    sasia = fields.Float(string='Sasia', required=True)

    _sql_constraints = [('prod_mag_unique', 'unique (produkt_id, magazine_id)', 'ID e produktit te jet unik per magazine')]
